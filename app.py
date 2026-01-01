import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

st.set_page_config(page_title="RV99 Poster Analyzer", layout="wide")

st.title("🚗 RV99 Auto Car - Poster Reach Analyzer")
st.write("សូម Upload រូបភាព Poster ឡាន Prius របស់អ្នក ដើម្បីវិភាគរកកម្រិត Reach")

uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាព...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # បង្ហាញរូបភាពដែលបាន Upload
    image = Image.open(uploaded_file)
    st.image(image, caption='Poster ដែលអ្នកបានជ្រើសរើស', use_column_width=True)
    
    # បំប្លែងរូបភាពសម្រាប់ OpenCV
    img_array = np.array(image)
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    if st.button('ចាប់ផ្ដើមវិភាគ'):
        with st.spinner('កំពុងគណនាទិន្នន័យ...'):
            # ១. វិភាគដង់ស៊ីតេព័ត៌មាន
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            density = (np.sum(edges > 0) / edges.size) * 100
            
            # ២. ពិនិត្យអក្សរជាមួយ EasyOCR
            reader = easyocr.Reader(['ku', 'en'])
            result = reader.readtext(img_array)
            
            # បង្ហាញលទ្ធផល
            st.subheader("📊 លទ្ធផលនៃការវិភាគ")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("ដង់ស៊ីតេព័ត៌មាន (Density)", f"{density:.2f}%")
                if density > 15:
                    st.error("⚠️ ព័ត៌មានច្រើនពេក អាចនឹងបាត់ Reach!")
                else:
                    st.success("✅ តុល្យភាពល្អណាស់!")
            
            with col2:
                st.metric("ចំនួនប្លុកអក្សរ", len(result))
                st.write("**ពាក្យដែលរកឃើញ៖**")
                for (bbox, text, prob) in result:
                    st.write(f"- {text} (ភាពច្បាស់: {prob:.2f})")

st.sidebar.info("បង្កើតឡើងសម្រាប់ RV99 Auto Car ដើម្បីពង្រឹងការលក់")
