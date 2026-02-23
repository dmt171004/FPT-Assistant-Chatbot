from fastapi import APIRouter
import re
from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.rag_service import retrieve_context
from app.services.llm_service import generate_answer
from app.prompts.exam_support import SYSTEM_PROMPT
from app.rag.retriever import get_page_image 

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest): # Thêm async nếu cần xử lý đồng bộ
    image_description = ""
    query_text = req.message if req.message else ""
    
    # BƯỚC 1: Xử lý hình ảnh (Giữ nguyên logic của bạn)
    if req.image:
        vision_extraction_prompt = (
            "Chỉ trích xuất mã lỗi hoặc thông báo lỗi ngắn gọn xuất hiện trong ảnh. "
            "Nếu không thấy chữ rõ ràng, hãy trả về 'None'."
        )
        image_description = generate_answer(vision_extraction_prompt, image_base64=req.image)
        if image_description.lower() != "none":
            query_text = f"{query_text} {image_description}".strip()

    # BƯỚC 2: Truy xuất tài liệu (RAG)
    if not query_text:
        return ChatResponse(answer="Vui lòng nhập câu hỏi hoặc gửi ảnh lỗi để tôi hỗ trợ.", page_images=[])

    # Nhận thêm source_documents từ hàm mới
    context, source_docs = retrieve_context(query_text)

    # BƯỚC 3: Xử lý khi không có dữ liệu
    if not context:
        return ChatResponse(answer="Tài liệu không có thông tin về vấn đề này. Bạn vui lòng liên hệ giám thị.", page_images=[])

    # BƯỚC 4: Xây dựng Final Prompt (Cập nhật để LLM trả về đúng định dạng đa file)
    final_prompt = f"""
{SYSTEM_PROMPT}

[DỮ LIỆU ĐẦU VÀO]
- Mô tả lỗi từ ảnh (OCR): {image_description if image_description else "Không có"}
- Câu hỏi của sinh viên: {req.message if req.message else "Sinh viên gửi ảnh lỗi."}

[TÀI LIỆU HƯỚNG DẪN LIÊN QUAN]
{context}

[YÊU CẦU QUAN TRỌNG VỀ TRÍCH DẪN]
Khi hướng dẫn, bạn PHẢI trích dẫn nguồn bằng định dạng chính xác sau ở cuối câu trả lời nếu có thông tin liên quan:
[SOURCE: tên_file_pdf, PAGE: số_trang]
Ví dụ: [SOURCE: HDSD HT E360_31.12.25.pdf, PAGE: 5]
"""

    # BƯỚC 5: Gọi LLM tạo câu trả lời
    answer = generate_answer(final_prompt, image_base64=req.image)

    # BƯỚC 6: Trích xuất ảnh từ NHIỀU file PDF dựa trên tag mới
    page_images_data = []
    seen_references = set() 
    
    # Regex mới để bắt cả tên file và số trang: [SOURCE: ..., PAGE: ...]
    pattern = r"\[SOURCE:\s*(.*?),\s*PAGE:\s*(\d+)\]"
    matches = re.findall(pattern, answer, re.IGNORECASE)

    for file_name, page_num in matches:
        file_name = file_name.strip()
        page_num = int(page_num.strip())
        ref_key = f"{file_name}_{page_num}"

        if ref_key not in seen_references:
            # Gọi hàm retriever với file_name linh hoạt (không còn hardcode path)
            img_b64 = get_page_image(file_name, page_num)
            if img_b64:
                page_images_data.append({
                    "page": page_num,
                    "file_name": file_name, # Có thể thêm field này vào schema nếu muốn
                    "base64": img_b64
                })
                seen_references.add(ref_key)

    # Xóa tất cả tag trích dẫn khỏi câu trả lời để giao diện sạch
    clean_answer = re.sub(pattern, "", answer, flags=re.IGNORECASE).strip()

    return ChatResponse(
        answer=clean_answer,
        page_images=page_images_data
    )