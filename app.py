import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# ១. ការកំណត់ទំព័រ
st.set_page_config(page_title="Poster Analyzing", layout="wide")

# បង្កើតអថេរ reader ជាតម្លៃទទេជាមុន ដើម្បីការពារ Error "not defined"
reader = None

@st.cache_resource
def load_reader():
    try:
        # ប្រើប្រាស់ List [] ឱ្យបានត្រឹមត្រូវ និងកំណត់ gpu=False សម្រាប់ Cloud
        return easyocr.Reader(['kh', 'en'], gpu=False)
    except Exception as e:
        st.error(f"មិនអាចបញ្ចូល Model AI ភាសាខ្មែរបានទេ: {e}")
        # ប្រសិនបើភាសាខ្មែរមានបញ្ហា វានឹងប្រើតែភាសាអង់គ្លេសជាបណ្ដោះអាសន្ន
        return easyocr.Reader(['en'], gpu=False)

# ព្យាយាមបញ្ចូល Model
reader = load_reader()

st.title("🚗 Poster Analyzing Tool")
st.write("ឧបករណ៍វិភាគដង់ស៊ីតេព័ត៌មាន និងអានអក្សរ (Version 1.3)")

uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាព Poster...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='រូបភាពសម្រាប់វិភាគ', use_container_width=True)
    
    if st.button('ចាប់ផ្ដើមការវិភាគ'):
        # ពិនិត្យថា តើ reader ត្រូវបានបង្កើតជោគជ័យឬនៅ
        if reader is not None:
            with st.spinner('⏳ កំពុងគណនា...'):
                img_array = np.array(image)
                
                # វិភាគដង់ស៊ីតេ
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                density = (np.sum(edges > 0) / edges.size) * 100
                
                # អានអក្សរ
                result = reader.readtext(img_array)
                
                st.subheader("📊 របាយការណ៍លទ្ធផល")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("កម្រិតដង់ស៊ីតេ (Density)", f"{density:.2f}%")
                    if density > 15:
                        st.warning("⚠️ ព្រមាន៖ Poster នេះមានព័ត៌មានច្រើនពេក!")
                    else:
                        st.success("✅ តុល្យភាពល្អ ស័ក្តិសមសម្រាប់ការផ្សព្វផ្សាយ!")
                
                with col2:
                    st.write(f"📝 រកឃើញប្លុកអក្សរចំនួន: {len(result)}")
                    for (bbox, text, prob) in result:
                        st.write(f"- {text}")
        else:
            st.error("ប្រព័ន្ធ AI មិនទាន់រួចរាល់ឡើយ។ សូមព្យាយាម Refresh ទំព័រនេះម្ដងទៀត។")
