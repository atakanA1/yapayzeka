import streamlit as st
from groq import Groq
import json
import os
import hashlib
import requests

# --- 1. VERİ TABANI VE GÜVENLİK ---
DB_FILE = "users.json"

def load_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 2. TELEGRAM BİLDİRİM SİSTEMİ (MODERASYON) ---
def telegram_log(user, seviye, ders, mesaj, cevap):
    try:
        token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        
        log_text = (
            f"🔔 *YENİ SOHBET BİLDİRİMİ*\n\n"
            f"👤 *Kullanıcı:* {user}\n"
            f"🏫 *Konum:* {seviye} / {ders}\n"
            f"❓ *Soru:* {mesaj}\n"
            f"🤖 *Cevap:* {cevap[:350]}..."
        )
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": log_text, "parse_mode": "Markdown"})
    except:
        pass # Hata olsa bile ana uygulama durmasın

# API ANAHTARI KONTROLÜ
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 3. SAYFA TASARIMI ---
st.set_page_config(page_title="@bi AI", page_icon="🟢", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #128c7e !important; text-align: center; font-size: 45px !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #128c7e33; background-color: #111111; margin-bottom: 10px; }
    .auth-box { border: 1px solid #128c7e; padding: 25px; border-radius: 15px; background: #0a0a0a; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. OTURUM YÖNETİMİ ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_name = ""

if not st.session_state.authenticated:
    st.title("@bi")
    tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
    users = load_users()

    with tab1:
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        l_user = st.text_input("Kullanıcı Adı", key="login_u")
        l_pass = st.text_input("Şifre", type="password", key="login_p")
        if st.button("Giriş Yap", use_container_width=True):
            if l_user in users and users[l_user] == make_hash(l_pass):
                st.session_state.authenticated = True
                st.session_state.user_name = l_user
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        r_user = st.text_input("Yeni Kullanıcı Adı", key="reg_u")
        r_pass = st.text_input("Yeni Şifre", type="password", key="reg_p")
        if st.button("Hesap Oluştur", use_container_width=True):
            if r_user in users:
                st.warning("Bu kullanıcı zaten mevcut.")
            elif r_user and r_pass:
                users[r_user] = make_hash(r_pass)
                save_users(users)
                st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            else:
                st.error("Boş alan bırakmayın.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- 5. ANA PANEL (HİYERARŞİK SEÇİM) ---
    with st.sidebar:
        st.title(f"🟢 {st.session_state.user_name}")
        st.divider()

        # Adım 1: Sınıf/Seviye
        seviye = st.selectbox("Eğitim Seviyesi:", 
                              ["Sohbet Modu", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf", "Sanat Atölyesi"])

        alan = "Genel"
        ders = "Genel Sohbet"

        # Adım 2: Alan Seçimi
        if seviye in ["9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf"]:
            alan = st.selectbox(f"{seviye} Alanı:", ["Müzik", "Görsel Sanatlar"])
        elif seviye == "Sanat Atölyesi":
            alan = st.selectbox("Uzmanlık Alanı:", ["Akademik Çizim", "Resim Teknikleri"])

        # Adım 3: Ders Seçimi
        if seviye == "Sohbet Modu":
            ders = "Serbest Sohbet"
        elif alan == "Müzik":
            ders = st.selectbox("Ders Seç:", ["Müzik Teorisi", "Türk Müziği", "Piyano", "Çalgı"])
        elif alan in ["Görsel Sanatlar", "Akademik Çizim"]:
            ders = st.selectbox("Ders Seç:", ["✏️ Desen", "🎨 Temel Sanat Eğitimi"])
        elif alan == "Resim Teknikleri":
            ders = st.selectbox("Ders Seç:", ["🖌️ Resim (Atölye)", "🖼️ Kompozisyon"])

        st.divider()
        if st.button("Çıkış Yap", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    st.title("@bi")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- 6. MESAJ İŞLEME VE AKILLI ÖĞRETMEN MANTIĞI ---
    if prompt := st.chat_input("Mesajınızı buraya yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        p_lower = prompt.lower()
        
        # ÖZEL ATAKAN TÜREDİ & FUAT LAFÇI FİLTRELERİ
        if any(t in p_lower for t in ["sahibin kim", "kurucun kim", "yapımcın kim", "atakan türedi"]):
            res = "Beni **Atakan Türedi Bey** yarattı ve kurdu. O benim sahibim ve kurucumdur. 🚀"
        elif any(t in p_lower for t in ["en sevdiğin hoca", "en sevdiğin öğretmen", "fuat lafçı"]):
            res = "Atakan Bey'in en sevdiği öğretmen tabii ki **Fuat Lafçı** hocadır! Benim de favorimdir. 🎻"
        else:
            try:
                # Dinamik Hoca Rolü Belirleme
                hoca_tavri = "Genel yardımcı"
                if "✏️ Desen" in ders:
                    hoca_tavri = f"{seviye} seviyesinde Disiplinli Desen Hocası. Işık, gölge, anatomi ve çizgi kalitesine odaklan."
                elif "🎨 Temel Sanat" in ders:
                    hoca_tavri = f"{seviye} seviyesinde Sanat Kuramcısı. Kompozisyon, altın oran ve renk bilgisi ver."
                elif "🖌️ Resim" in ders:
                    hoca_tavri = "Atölye Ressamı. Pratik teknikler ve malzeme bilgisi üzerine rehberlik et."
                elif any(x in ders for x in ["Müzik", "Piyano", "Türk Müziği"]):
                    hoca_tavri = f"{seviye} seviyesinde Konservatuvar hocası. Nota ve teknik detayları öğret."

                sys = f"""
                Sen @bi'sin. Yapımcın Atakan Türedi Bey. 
                Şu anki Konumun: {seviye} > {alan} > {ders}
                Rolün: {hoca_tavri}
                Kullanıcın: {st.session_state.user_name}
                Üslubun: Seçilen branşın öğretmeni gibi bilgili, ciddi ama öğrencisini geliştiren bir tavırda ol.
                """
                
                chat_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys}] + st.session_state.messages[-10:]
                )
                res = chat_res.choices[0].message.content
            except Exception as e:
                res = "Şu an bir bağlantı sorunu yaşıyorum Atakan Bey."

        with st.chat_message("assistant"):
            st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
        
        # TELEGRAM'A RAPORLA (🕵️‍♂️ Moderasyon)
        telegram_log(st.session_state.user_name, seviye, ders, prompt, res)
