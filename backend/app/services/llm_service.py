# app/services/llm_service.py
from openai import OpenAI
import os
from app.prompts.exam_support import SYSTEM_PROMPT # Import từ file prompt riêng của bạn

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(prompt: str, image_base64: str = None):
    """
    Hàm hỗ trợ cả text và image. 
    Sử dụng gpt-4o-mini để tối ưu chi phí và tốc độ xử lý Vision.
    """
    
    # 1. Cập nhật System Message với hướng dẫn về số trang
    messages = [
        {
            "role": "system", 
            "content": SYSTEM_PROMPT
        }
    ]
    
    # 2. Cấu trúc nội dung cho User
    user_content = [{"type": "text", "text": prompt}]
    
    # 3. Nếu có ảnh từ sinh viên gửi lên, thêm vào để AI đối chiếu
    if image_base64:
        # Đảm bảo loại bỏ header 'data:image/...' nếu đã có để tránh trùng lặp
        clean_base64 = image_base64.split(",")[-1] if "," in image_base64 else image_base64
        
        user_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{clean_base64}"
            }
        })
    
    messages.append({"role": "user", "content": user_content})

    # 4. Gọi API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1 # Để thấp để câu trả lời chính xác và ổn định định dạng [PAGE: n]
    )

    return response.choices[0].message.content.strip()