import tempfile
import os
from openai import OpenAI
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def speech_to_text(audio_bytes: bytes, filename: str) -> str:
    tmp_path = None
    try:
        # Sử dụng hậu tố .webm hoặc .wav tùy theo thực tế browser gửi
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language="vi" # Ép tiếng Việt
            )
        
        # In ra để xem thực tế Whisper trả về cái gì
        print(f"--- WHISPER RESULT: '{transcript.text}' ---")
        return transcript.text

    except Exception as e:
        print(f"STT Error: {e}")
        return ""
    finally:
        # Xóa file tạm sau khi xong để tránh đầy bộ nhớ
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)