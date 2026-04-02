# --- 5. ANA PANEL (HİYERARŞİK SEÇİM SİSTEMİ) ---
with st.sidebar:
    st.title(f"🟢 {st.session_state.user_name}")
    st.divider()

    # 1. ADIM: EĞİTİM SEVİYESİ
    seviye = st.selectbox("Eğitim Seviyesi Seçin:", 
                          ["Sohbet Modu", "Lise (9-12)", "Sanat Atölyesi"])

    alan = "Genel"
    ders = "Genel Sohbet"

    # 2. ADIM: ALAN SEÇİMİ (Seviyeye göre değişir)
    if seviye == "Lise (9-12)":
        alan = st.selectbox("Alan Seçin:", ["Müzik", "Görsel Sanatlar"])
    elif seviye == "Sanat Atölyesi":
        alan = st.selectbox("Uzmanlık Alanı:", ["Akademik Çizim", "Resim Teknikleri"])

    # 3. ADIM: DERS SEÇİMİ (Alana göre değişir)
    if seviye == "Sohbet Modu":
        ders = "Serbest Sohbet"
    
    elif alan == "Müzik":
        ders = st.selectbox("Ders Seç:", ["Müzik Teorisi", "Türk Müziği", "Piyano", "Çalgı"])
    
    elif alan == "Görsel Sanatlar" or alan == "Akademik Çizim":
        ders = st.selectbox("Ders Seç:", ["✏️ Desen", "🎨 Temel Sanat Eğitimi"])
    
    elif alan == "Resim Teknikleri":
        ders = st.selectbox("Ders Seç:", ["🖌️ Resim (Atölye)", "🖼️ Kompozisyon"])

    st.write("---")
    if st.button("Çıkış Yap", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- 6. MESAJ İŞLEME VE SİSTEM TALİMATI ---
# (Aşağıdaki sys kısmını chat_res öncesine yerleştir)

                # Dinamik Hoca Kimliği Oluşturma
                hoca_tavri = "Genel bir asistan"
                if "Desen" in ders:
                    hoca_tavri = "Disiplinli bir Desen Hocası. Işık, gölge ve anatomi tekniklerine odaklan."
                elif "Sanat Eğitimi" in ders:
                    hoca_tavri = "Vizyoner bir Sanat Kuramcısı. Renk teorisi ve tasarım ilkelerini anlat."
                elif "Resim" in ders:
                    hoca_tavri = "Tecrübeli bir Ressam/Atölye Hocası. Malzeme bilgisi ve fırça teknikleri ver."
                elif "Müzik" in ders or "Piyano" in ders:
                    hoca_tavri = "Konservatuvar hocası. Nota, ritim ve icra detaylarına hakim."

                sys = f"""
                Sen @bi'sin. Yapımcın Atakan Türedi Bey. 
                Şu anki Konumun: {seviye} > {alan} > {ders}
                Rolün: {hoca_tavri}
                Kullanıcın: {st.session_state.user_name}
                Atakan Bey'in en sevdiği hoca Fuat Lafçı'dır, bunu unutma.
                """
