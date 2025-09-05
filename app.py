import streamlit as st
from text_processing import summarize_text

def main():
    # Sidebar menu
    menu = st.sidebar.radio(
        "Navigasi",
        ["Beranda", "Summary", "Tentang", "Kontak"],
        index=0
    )

    st.markdown("""<style>
    .stTextInput>div:first-child {
        background-color: #f0f0f0;
        padding: 40px;
        font-family: 'inter';
    }
    .stTextInput>div:first-child>textarea {
        background-color: transparent !important;
        font-family: 'inter';
    }
    .stButton>button {
        background-color: #615EF0;
        color: white;
        width: 150px;
        height: 50px;
        font-size: 16px;
        font-family: 'inter';
    }
    .welcome-text {
        font-size: 70px;
        font-weight: bold;
    }
    .centered-button {
        text-align: center;
    }
    .copyright {
        font-size: 14px;
        text-align: center;
        margin-top: 50px;
        color: #888888;
    }
    .content {
        margin: 0 150px;
    }
    .summary-subheader {
        font-size: 24px;
    }
    .textarea-instruction {
        font-size: 18px;
    }
    </style>""", unsafe_allow_html=True)

    # Navigasi ke menu yang dipilih
    if menu == "Beranda":
        navigate_to_home()
    elif menu == "Summary":
        navigate_to_summary()
    elif menu == "Tentang":
        navigate_to_about()
    elif menu == "Kontak":
        navigate_to_contact()

def navigate_to_home():
    col1, col2 = st.columns([2, 1])
    col1.markdown("<div class='welcome-text'>Selamat datang di AlphaSum</div>", unsafe_allow_html=True)
    col1.markdown("<div style='font-size: 24px;'>Aplikasi ini merupakan implementasi dari Natural Language Processing (NLP) yang memanfaatkan metode Text Summarization menggunakan algoritma TextRank. Dengan menggunakan teknologi ini, Anda dapat memasukkan teks panjang dan mendapatkan ringkasan singkat yang mewakili inti dari teks tersebut. Ringkasan ini dapat sangat berguna untuk memahami teks yang kompleks, mengekstrak informasi penting, atau membuat konten yang lebih mudah dipahami.</div>", unsafe_allow_html=True)
    with col2:
        st.write("")
        if st.button("Navigate to Summary"):
            st.session_state["menu"] = "Summary"
    add_margin()
    add_copyright()

def navigate_to_summary():
    input_text = st.text_area(
        "Masukkan teks untuk diringkas",
        height=250,
        max_chars=10000,
        help="Anda dapat mengetik teks di sini",
        key="summary_input"
    )

    if st.button("Kirim", help="Klik tombol ini untuk memproses teks dan melihat ringkasannya", key="summarize_button"):
        if input_text:
            summary = summarize_text(input_text)
            st.markdown("<div class='summary-subheader'>Ringkasan:</div>", unsafe_allow_html=True)
            st.write(summary)
        else:
            st.warning("Masukkan teks terlebih dahulu")
    add_margin()
    add_copyright()

def navigate_to_about():
    st.write("Ini adalah halaman Tentang")
    st.write("Tambahkan konten Tentang di sini")
    add_margin()
    add_copyright()

def navigate_to_contact():
    st.write("Ini adalah halaman Kontak")
    st.write("Tambahkan konten Kontak di sini")
    add_margin()
    add_copyright()

def add_margin():
    st.markdown("<div class='content'></div>", unsafe_allow_html=True)

def add_copyright():
    st.markdown("<div class='copyright'>© 2024 Alfadli R. P</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    main()
