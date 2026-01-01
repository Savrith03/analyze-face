import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# ១. ការកំណត់ទំព័រកម្មវិធីឱ្យទៅជា "Poster Analyzing"
st.set_page_config(page_title="Poster Analyzing", layout="wide")

# ២. បង្កើតមុខងារ Caching ដើម្បីរក្សាទុក Model AI (ជួយកុំឱ្យ App គាំង RAM)
@st.cache_resource
def load_reader():
    # កំណត់ gpu=False ព្រោះ Server ប្រើតែ CPU
    # ប្រើ 'km' សម្រាប់អក្សរខ្មែរ និង 'en' សម្រាប់អង់គ្លេស
    return easyocr.Reader(['km', 'en'], gpu=False)

# ហៅ Model មកប្រើប្រាស់
try:
    reader = load_reader()
except Exception as e:
    st.error(f"មិនអាចបញ្ចូល Model AI បានទេ: {e}")

# ៣. ចំណងជើងកម្មវិធី (លក្ខណៈទូទៅ)
st.title("🚗 Poster Analyzing Tool")
st.write("ឧបករណ៍ឆ្លាតវៃសម្រាប់វិភាគកម្រិតដង់ស៊ីតេព័ត៌មាន និងអានអក្សរលើរូបភាព Poster")

uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាព Poster (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        # ប្រើ use_container_width ដើម្បីបំបាត់ Error ក្នុង Log
        st.image(image, caption='រូបភាពដែលបានជ្រើសរើស', use_container_width=True)
        
        if st.button('ចាប់ផ្ដើមការវិភាគ'):
            with st.spinner('⏳ កំពុងគណនាទិន្នន័យ (សូមរង់ចាំ)...'):
                # បម្លែងរូបភាពសម្រាប់ OpenCV
                img_array = np.array(image)
                
                # ៤. វិភាគដង់ស៊ីតេព័ត៌មាន (Edge Detection)
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                density = (np.sum(edges > 0) / edges.size) * 100
                
                # ៥. អានអក្សរដោយប្រើ AI (EasyOCR)
                result = reader.readtext(img_array)
                
                # ៦. បង្ហាញរបាយការណ៍លទ្ធផល
                st.subheader("📊 របាយការណ៍វិភាគ")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("កម្រិតដង់ស៊ីតេ (Density)", f"{density:.2f}%")
                    if density > 15:
                        st.warning("⚠️ ព្រមាន៖ Poster នេះមានព័ត៌មានច្រើនពេក អាចនឹងបាត់បង់ Reach!")
                    else:
                        # សារជោគជ័យថ្មីដែលមិនមានបញ្ជាក់តម្លៃទឹកប្រាក់
                        st.success("✅ តុល្យភាពល្អ ស័ក្តិសមសម្រាប់ការផ្សព្វផ្សាយ (Boost Ads)!")
                
                with col2:
                    st.write(f"📝 **រកឃើញប្លុកអក្សរចំនួន:** {len(result)}")
                    for (bbox, text, prob) in result:
                        st.write(f"- {text} (ភាពច្បាស់: {prob:.2f})")
                        
    except Exception as e:
        st.error(f"មានបញ្ហាបច្ចេកទេសក្នុងការវិភាគរូបភាព: {e}")

st.sidebar.markdown("---")
st.sidebar.info("បច្ចេកវិទ្យា Poster Analyzing សម្រាប់ពង្រឹងប្រសិទ្ធភាព Digital Marketing")
