import streamlit as st
from text_processing import summarize_text

def main():
    st.title("Peringkas Teks")
    st.markdown("---")  # Garis pemisah

    # Input teks pengguna dengan latar belakang berwarna
    input_text = st.text_area("Masukkan teks untuk diringkas", height=200, 
                              max_chars=10000, background="#f0f0f0", 
                              help="Anda dapat mengetik teks di sini")

    # Tombol untuk memproses teks dengan latar belakang dan teks warna yang berbeda
    if st.button("Ringkaskan", 
                 help="Klik tombol ini untuk memproses teks dan melihat ringkasannya", 
                 key="summarize_button"):
        if input_text:
            summary = summarize_text(input_text)
            st.subheader("Ringkasan:")
            st.write(summary)
        else:
            st.warning("Masukkan teks terlebih dahulu")

if __name__ == "__main__":
    main()
