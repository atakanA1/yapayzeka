import streamlit as st
import time

# Sayfa ayarı
st.set_page_config(page_title="Abi'yi Kaybettik", layout="centered")

# Arka plan stili
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }

    .title {
        font-size: 48px;
        text-align: center;
        color: #e0e0e0;
        animation: fade 3s ease-in-out;
    }

    .subtitle {
        text-align: center;
        color: #aaaaaa;
        font-size: 18px;
        margin-top: 20px;
        opacity: 0.8;
    }

    @keyframes fade {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    </style>
""", unsafe_allow_html=True)

# Sis efekti (basit)
st.markdown("""
<div style="
position: fixed;
top:0;
left:0;
width:100%;
height:100%;
background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
animation: move 20s linear infinite;
z-index:-1;
"></div>

<style>
@keyframes move {
    from {transform: translate(0,0);}
    to {transform: translate(-10%, -10%);}
}
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("<div class='title'>Abi'yi Kaybettik</div>", unsafe_allow_html=True)

# Animasyonlu yazı
placeholder = st.empty()

text = "Sesin hâlâ burada gibi... ama artık cevap yok."

for i in range(len(text)+1):
    placeholder.markdown(f"<div class='subtitle'>{text[:i]}</div>", unsafe_allow_html=True)
    time.sleep(0.05)

# küçük boşluk
st.write("")
st.write("")
