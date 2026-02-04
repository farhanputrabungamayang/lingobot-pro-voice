# 🎙️ LingoBot Pro: AI English Speaking Partner

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![Gemini 1.5 Flash](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange)

Aplikasi latihan bahasa Inggris interaktif berbasis suara (Voice-to-Voice).
Lupakan mengetik! Cukup bicara, dan AI akan mendengarkan, mengoreksi grammar, dan menjawab layaknya *Native Speaker*.

**Project Portofolio: Audio Processing & Multimodal AI.**

## 🌟 Fitur Unggulan

* **🗣️ Voice Conversation:** Berbicara langsung menggunakan microphone (Browser/HP).
* **📝 Real-time Grammar Check:** AI mendeteksi kesalahan grammar dan memberikan koreksi instan.
* **🤖 Native Audio Response:** AI menjawab menggunakan suara (Text-to-Speech) agar pengguna terbiasa mendengar aksen bahasa Inggris.
* **🧠 Powered by Gemini 1.5 Flash:** Menggunakan model AI terbaru yang memiliki kemampuan *Audio Understanding* super cepat.

## 🛠️ Teknologi

* **Frontend:** Streamlit & `streamlit-mic-recorder`
* **AI Engine:** Google Gemini 1.5 Flash
* **Audio Engine:** gTTS (Google Text-to-Speech)

## 🚀 Cara Mencoba (Local)

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/USERNAME/lingobot-pro-voice.git](https://github.com/USERNAME/lingobot-pro-voice.git)
    ```
2.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Setup API Key:**
    Isi `.streamlit/secrets.toml` dengan `GOOGLE_API_KEY`.
4.  **Jalankan:**
    ```bash
    streamlit run app.py
    ```

---
Dibuat dengan ❤️ oleh [Nama Masbro]