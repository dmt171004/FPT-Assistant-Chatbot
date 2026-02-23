import fitz  # PyMuPDF
import base64
import os
from app.core.config import RAG_DATA_DIR

def get_page_image(file_name: str, page_number: int):
    """Trích xuất trang PDF từ thư mục RAG_DATA_DIR thành ảnh Base64"""
    try:
        # Tạo đường dẫn đầy đủ đến file PDF trong thư mục data
        pdf_path = os.path.join(RAG_DATA_DIR, file_name)
        
        if not os.path.exists(pdf_path):
            print(f"Lỗi: Không tìm thấy file {pdf_path}")
            return None

        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        if page_number < 1 or page_number > total_pages:
            print(f"Lỗi: Số trang {page_number} nằm ngoài phạm vi (1-{total_pages}) của file {file_name}")
            return None

        page = doc.load_page(page_number - 1) 
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        doc.close() 
        
        return base64.b64encode(img_data).decode("utf-8")
    except Exception as e:
        print(f"Error extracting PDF page: {e}")
        return None