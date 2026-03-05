import streamlit as st
import google.generativeai as genai
import json

# Lấy mã API Key từ hệ thống bảo mật của Streamlit Cloud
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("⚠️ Lỗi: Chưa cấu hình GEMINI_API_KEY trong cài đặt của Streamlit.")

def tao_content_social(url, chu_de):
    model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
    
    prompt = f"""
    Tôi có link bài viết: {url}
    Chủ đề chính: {chu_de}
    
    Hãy đóng vai chuyên gia SEO, viết nội dung chia sẻ link này lên 3 mạng xã hội. 
    Trả về đúng định dạng JSON:
    {{
        "facebook": "Nội dung Facebook (chuyên nghiệp, có emoji, 3-5 hashtag, call-to-action).",
        "reddit_title": "Tiêu đề Reddit (thảo luận/chia sẻ giá trị, không quảng cáo).",
        "reddit_body": "Nội dung Reddit (tóm tắt giá trị, chèn link tự nhiên).",
        "pinterest": "Mô tả Pinterest (dưới 400 ký tự, có từ khóa và hashtag)."
    }}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Lỗi AI: {e}")
        return None

# --- GIAO DIỆN APP ---
st.set_page_config(page_title="Công cụ Auto Entity SEO", page_icon="🚀", layout="wide")
st.title("🚀 Cỗ Máy Tự Động Phủ Sóng Social")

col1, col2 = st.columns(2)
with col1:
    url_input = st.text_input("🔗 Nhập Link bài viết cần SEO:")
with col2:
    chu_de_input = st.text_input("💡 Chủ đề chính:")

if st.button("Tạo Content Tự Động", type="primary"):
    if url_input and chu_de_input:
        with st.spinner("AI đang xử lý..."):
            ket_qua = tao_content_social(url_input, chu_de_input)
            
            if ket_qua:
                st.success("✅ Đã tạo xong nội dung!")
                
                st.subheader("🔵 Facebook")
                st.text_area("Copy đoạn này đăng Facebook:", ket_qua["facebook"], height=150)
                
                st.markdown("---")
                st.subheader("🟠 Reddit")
                st.text_input("Tiêu đề:", ket_qua["reddit_title"])
                st.text_area("Nội dung:", ket_qua["reddit_body"], height=150)
                
                st.markdown("---")
                st.subheader("🔴 Pinterest")
                st.text_area("Mô tả:", ket_qua["pinterest"], height=100)
    else:
        st.warning("Vui lòng nhập Link và Chủ đề!")
