# Di skrip utama Streamlit Anda
import streamlit as st
from text_processing import summarize_text

def main():
    st.title("Peringkas Teks")

    # Input teks pengguna
    input_text = st.text_area("Masukkan teks untuk diringkas")

    # Tombol untuk memproses teks dan menampilkan ringkasan
    if st.button("Ringkaskan"):
        if input_text:
            summary = summarize_text(input_text)
            st.subheader("Ringkasan:")
            st.write(summary)
        else:
            st.warning("Masukkan teks terlebih dahulu")

if __name__ == "__main__":
    main()
