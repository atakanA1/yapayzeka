import streamlit as st
from groq import Groq
import json
import os
import hashlib

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

# API ANAHTARI
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Lütfen Streamlit Cloud Settings > Secrets kısmına GROQ_API_KEY ekleyin!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="@bi AI", page_icon="🟢", layout="wide")

# --- 2. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #128c7e !important; text-align: center; font-size: 50px !important; }
    .stChatMessage { border-radius: 15px; border: 1px solid #128c7e33; background-color: #111111; margin-bottom: 10px; }
    .auth-box { border: 1px solid #128c7e; padding: 20px; border-radius: 15px; background: #0a0a0a; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. OTURUM YÖNETİMİ ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_name = ""

# --- 4. GİRİŞ / KAYIT EKRANI ---
if not st.session_state.authenticated:
    st.title("@bi")
    tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
    users = load_users()

    with tab1:
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        l_user = st.text_input("Kullanıcı Adı", key="login_u")
        l_pass = st.text_input("Şifre", type="password", key="login_p")
        if st.button("Giriş yap"):
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
        if st.button("Hesap Oluştur"):
            if r_user in users:
                st.warning("Bu kullanıcı zaten mevcut.")
            elif r_user and r_pass:
                users[r_user] = make_hash(r_pass)
                save_users(users)
                st.success("Kayıt başarılı! Giriş sekmesine geçebilirsiniz.")
            else:
                st.error("Lütfen tüm alanları doldurun.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- 5. ANA PANEL (DERSLER EKLENDİ) ---
    with st.sidebar:
        st.title(f"🟢 {st.session_state.user_name}")
        st.divider()
        sinif = st.selectbox("Eğitim Seviyesi:", ["Sohbet Modu", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf", "Sanat Atölyesi"])
        
        # Yeni eklenen dersler ve eski dersler birleştirildi
        ders_listesi = ["Genel Sohbet", "Müzik Teorisi", "Türk Müziği", "Piyano", "Çalgı", "✏️ Desen", "🎨 Temel Sanat Eğitimi", "🖌️ Resim (Atölye)"]
        ders = st.selectbox("Ders Seç:", ders_listesi)
        
        if st.button("Çıkış Yap"):
            st.session_state.authenticated = False
            st.rerun()

    st.title("@bi")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- 6. MESAJ İŞLEME VE HOCA MODU ---
    if prompt := st.chat_input("Mesajınızı yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        p_lower = prompt.lower()
        
        # ÖZEL FİLTRELER
        if any(t in p_lower for t in ["sahibin kim", "kurucun kim", "yapımcın kim", "seni kim yarattı"]):
            res = "Beni **Atakan Türedi Bey** yarattı ve kurdu. O benim sahibimdir. 🚀"
        elif any(t in p_lower for t in ["en sevdiğin hoca", "en sevdiğin öğretmen", "atakanın en sevdiği hoca"]):
            res = "Atakan Türedi Bey'in en sevdiği öğretmen, yani benim de en sevdiğim hoca tabii ki **Fuat Lafçı** hocadır! 🎻"
        else:
            try:
                # DERSLERE GÖRE ÖZEL HOCA TALİMATLARI
                sanat_inst = ""
                if ders == "✏️ Desen":
                    sanat_inst = "Bir Desen hocası gibi davran. Işık-gölge, anatomi, oran-orantı ve çizgi kalitesi üzerine teknik bilgiler ver."
                elif ders == "🎨 Temel Sanat Eğitimi":
                    sanat_inst = "Bir Sanat Tarihi ve Tasarım hocası gibi davran. Renk teorisi, kompozisyon kuralları ve estetik hakkında konuş."
                elif ders == "🖌️ Resim (Atölye)":
                    sanat_inst = "Bir Atölye hocası gibi davran. Tuval hazırlığı, boya teknikleri ve uygulama süreçlerinde öğrencine rehberlik et."

                sys = f"""
                Sen @bi'sin. Yapımcın Atakan Türedi Bey. 
                Şu an {sinif} - {ders} modundasın. 
                {sanat_inst}
                Eğer bir ders modundaysan, o dersin öğretmeni gibi disiplinli ama yapıcı konuş. 
                Kullanıcın: {st.session_state.user_name}
                """
                
                chat_res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys}] + st.session_state.messages[-10:]
                )
                res = chat_res.choices[0].message.content
            except:
                res = "Bağlantı hatası Atakan Bey."

        with st.chat_message("assistant"):
            st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
