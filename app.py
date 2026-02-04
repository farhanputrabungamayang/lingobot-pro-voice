import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import json

# ==========================================
# 1. KONFIGURASI HALAMAN & CSS PREMIUM
# ==========================================
st.set_page_config(page_title="LingoBot Pro", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
    /* Import Font Modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Judul Utama */
    .main-title {
        text-align: center;
        font-weight: 800;
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #1A2980, #26D0CE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* Subjudul */
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 40px;
    }

    /* Container Chat User */
    .user-box {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 15px 15px 0 15px;
        border-left: 5px solid #2196F3;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Container Koreksi (Penting!) */
    .correction-box {
        background-color: #FFF3E0;
        padding: 15px;
        border-radius: 10px;
        border: 1px dashed #FF9800;
        margin-top: 10px;
        font-size: 0.95rem;
    }

    /* Container AI Response */
    .ai-box {
        background-color: #F3E5F5;
        padding: 20px;
        border-radius: 15px 15px 15px 0;
        border-left: 5px solid #9C27B0;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Styling tombol mic recorder (agak tricky karena bawaan library) */
    div[data-testid="stVerticalBlock"] > div > button {
        border-radius: 50%;
        height: 60px;
        width: 60px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SETUP API KEY
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ API Key belum disetting di secrets.toml")
    st.stop()

# ==========================================
# 3. FUNGSI LOGIKA
# ==========================================
def text_to_speech(text):
    """Convert teks ke audio MP3"""
    try:
        tts = gTTS(text=text, lang='en', tld='com') # tld='com' biar aksen US standard
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        return audio_fp
    except: return None

def process_audio_input(audio_bytes):
    """Kirim audio ke Gemini"""
    prompt = """
    Role: Professional English Language Coach.
    
    Task:
    1. Listen to the user's audio.
    2. Transcribe exactly what they said.
    3. Check for grammar/pronunciation context errors.
    4. Respond naturally to continue the conversation.
    
    Output Format (JSON):
    {
        "transcript": "User's exact words",
        "correction": "Corrected sentence (or 'Perfect!' if no error)",
        "explanation": "Brief explanation of the error (optional)",
        "response": "Your natural reply"
    }
    """
    try:
        response = model.generate_content([
            prompt,
            {"mime_type": "audio/wav", "data": audio_bytes}
        ])
        return response.text
    except Exception as e:
        return None

# ==========================================
# 4. TAMPILAN UTAMA
# ==========================================
st.markdown('<h1 class="main-title">LingoBot Pro 🇬🇧</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Native Speaker Partner & Grammar Coach</p>', unsafe_allow_html=True)

# Layout 3 Kolom biar tombol rekam di tengah
col_l, col_center, col_r = st.columns([1, 2, 1])

with col_center:
    st.write("👇 **Tap icon untuk bicara**")
    # Perekam Suara
    audio = mic_recorder(
        start_prompt="🔴 REC",
        stop_prompt="⏹️ STOP",
        key='recorder',
        format="wav",
        use_container_width=True
    )

st.divider()

# ==========================================
# 5. PROSES & HASIL
# ==========================================
if audio:
    # Menggunakan st.status untuk UX loading yang modern
    with st.status("🎧 Menganalisa suara...", expanded=True) as status:
        st.write("📤 Mengirim audio ke server...")
        audio_bytes = audio['bytes']
        
        st.write("🧠 Gemini sedang mencerna grammar...")
        raw_response = process_audio_input(audio_bytes)
        
        if raw_response:
            try:
                # Bersihkan JSON
                clean_json = raw_response.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
                
                status.update(label="✅ Selesai!", state="complete", expanded=False)
                
                # --- LAYOUT HASIL (2 KOLOM) ---
                col_user, col_ai = st.columns(2)
                
                # KOLOM KIRI: USER
                with col_user:
                    st.markdown("### 👤 You Said")
                    st.markdown(f"""
                    <div class="user-box">
                        <h3>"{data['transcript']}"</h3>
                        <div class="correction-box">
                            <b>📝 Correction:</b><br>
                            {data['correction']}
                            <br><i><small>{data.get('explanation', '')}</small></i>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # KOLOM KANAN: AI
                with col_ai:
                    st.markdown("### 🤖 LingoBot Replies")
                    st.markdown(f"""
                    <div class="ai-box">
                        <h3>"{data['response']}"</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Audio Player
                    suara = text_to_speech(data['response'])
                    if suara:
                        st.audio(suara, format='audio/mp3', autoplay=True)
                        
            except Exception as e:
                status.update(label="❌ Error Parsing", state="error")
                st.error("AI bingung. Coba ngomong lebih jelas lagi ya!")
        else:
            status.update(label="❌ Koneksi Gagal", state="error")