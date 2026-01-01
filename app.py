import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# ១. កំណត់ឈ្មោះទំព័រជា "Poster Analyzing" តាមសំណើរបស់អ្នក
st.set_page_config(page_title="Poster Analyzing", layout="wide")

# ២. មុខងារ Caching ដើម្បីរក្សាទុក Model ក្នុង RAM (ជួយឱ្យ App ដំណើរការលឿន)
@st.cache_resource
def load_reader():
    # កែពី 'ku' (Kurdish) ទៅជា 'km' (Khmer) ដើម្បីអានអក្សរខ្មែរឱ្យបានត្រឹមត្រូវ
    return easyocr.Reader(['km', 'en'])

# ហៅ Model មកប្រើប្រាស់
reader = load_reader()

# ៣. ផ្លាស់ប្តូរចំណងជើងកម្មវិធីមកជា "Poster Analyzing"
st.title("🚗 Poster Analyzing")
st.write("ឧបករណ៍វិភាគកម្រិត Reach សម្រាប់អាជីវកម្ម RV99 Auto Car")

uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាព Poster...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # ប្រើ use_container_width តាមការណែនាំក្នុង Log ដើម្បីបំបាត់ Error
    st.image(image, caption='រូបភាពសម្រាប់វិភាគ', use_container_width=True)
    
    img_array = np.array(image)
    
    if st.button('ចាប់ផ្ដើមវិភាគឥឡូវនេះ'):
        with st.spinner('⏳ កំពុងគណនាដង់ស៊ីតេ និងអានអក្សរ (សូមរង់ចាំ)...'):
            # ៤. វិភាគដង់ស៊ីតេព័ត៌មាន (Reach Density)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            density = (np.sum(edges > 0) / edges.size) * 100
            
            # ៥. ប្រើ Reader ដែលបាន Load ទុកជាមុន (EasyOCR)
            result = reader.readtext(img_array)
            
            # បង្ហាញលទ្ធផល
            st.subheader("📊 របាយការណ៍វិភាគ")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("ដង់ស៊ីតេព័ត៌មាន (Density)", f"{density:.2f}%")
                if density > 15:
                    st.error("⚠️ ព្រមាន៖ Poster នេះមានព័ត៌មានច្រើនពេក អាចនឹងបាត់បង់ Reach!")
                else:
                    st.success("✅ ល្អណាស់៖ Poster នេះមានតុល្យភាពល្អ ស័ក្តិសមសម្រាប់បាញ់ Ads!")
            
            with col2:
                st.write(f"📝 **រកឃើញប្លុកអក្សរចំនួន:** {len(result)}")
                for (bbox, text, prob) in result:
                    st.write(f"- {text} (ភាពច្បាស់: {prob:.2f})")

st.sidebar.markdown("---")
# ប្ដូរឈ្មោះក្នុង Sidebar ផងដែរ
st.sidebar.info("បច្ចេកវិទ្យា AI សម្រាប់កម្មវិធី Poster Analyzing")
