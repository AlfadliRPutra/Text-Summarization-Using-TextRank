import streamlit as st
import hydralit_components as hc
from text_processing import summarize_text

def main():
    # Navbar
    menu_data = [
        {'icon': "fas fa-home", 'label': "Beranda"},
        {'icon': "fas fa-file-alt", 'label': "Summary"},
        {'icon': "fas fa-book", 'label': "Tentang"},
        {'icon': "fas fa-envelope", 'label': "Kontak"}
    ]
    menu_id = hc.nav_bar(menu_definition=menu_data, sticky_nav=True, sticky_mode='pinned')
    
    st.markdown("""<style>
    .stTextInput>div:first-child {
        background-color: #f0f0f0;
        padding: 10px;
    }
    .stTextInput>div:first-child>textarea {
        background-color: transparent !important;
    }
    .stButton>button {
        background-color: #008080;
        color: white;
        width: 200px;  /* Lebar tombol */
        height: 50px;  /* Tinggi tombol */
        font-size: 16px;  /* Ukuran font */
    }
    .welcome-text {
        font-size: 24px;
        font-weight: bold;
    }
    </style>""", unsafe_allow_html=True)
    st.markdown("---")  # Garis pemisah
    
    # Navigasi ke menu yang dipilih
    if menu_id == "Beranda":
        navigate_to_home()
    elif menu_id == "Summary":
        navigate_to_summary()
    elif menu_id == "Tentang":
        navigate_to_about()
    elif menu_id == "Kontak":
        navigate_to_contact()

def navigate_to_home():
    col1, col2, col3 = st.columns([1, 2, 1])  # Menentukan lebar kolom
    col2.markdown("<div class='welcome-text'>Selamat datang di Aplikasi NLP!</div>", unsafe_allow_html=True)
    with col2:
        st.write("")  # Spasi kosong untuk memberi ruang antara teks dan tombol
        if st.button("Navigate to Summary"):
            navigate_to_summary()

def navigate_to_summary():
    # Input teks pengguna
    input_text = st.text_area("Masukkan teks untuk diringkas", height=200, 
                              max_chars=10000, 
                              help="Anda dapat mengetik teks di sini")

    # Tombol untuk memproses teks
    if st.button("Ringkaskan", 
                 help="Klik tombol ini untuk memproses teks dan melihat ringkasannya", 
                 key="summarize_button"):
        if input_text:
            summary = summarize_text(input_text)
            st.subheader("Ringkasan:")
            st.write(summary)
        else:
            st.warning("Masukkan teks terlebih dahulu")

def navigate_to_about():
    st.write("Ini adalah halaman Tentang")
    st.write("Tambahkan konten Tentang di sini")

def navigate_to_contact():
    st.write("Ini adalah halaman Kontak")
    st.write("Tambahkan konten Kontak di sini")

if __name__ == "__main__":
    st.set_page_config(layout='wide')  # Set layout ke 'wide' untuk full screen
    main()
