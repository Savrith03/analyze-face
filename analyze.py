import cv2
import numpy as np
import easyocr

def detail_analysis(image_path):
    print(f"\n--- កំពុងចាប់ផ្ដើមវិភាគរូបភាព: {image_path} ---")
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ រកមិនឃើញ File រូបភាព '{image_path}' ទេ! សូមពិនិត្យឈ្មោះ File ឡើងវិញ។")
        return

    # ១. វាស់ដង់ស៊ីតេព័ត៌មាន (Canny Edge Detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    density = (np.sum(edges > 0) / edges.size) * 100

    # ២. អានអក្សរខ្មែរ និងអង់គ្លេសដោយប្រើ EasyOCR
    print("⏳ កំពុងពិនិត្យអក្សរលើរូបភាព (សូមរង់ចាំបន្តិច)...")
    reader = easyocr.Reader(['ku', 'en']) # 'ku' គឺសម្រាប់ភាសាខ្មែរ
    result = reader.readtext(image_path)

    print(f"\n--- លទ្ធផលវិភាគសម្រាប់ RV99 Auto Car ---")
    print(f"📊 ដង់ស៊ីតេព័ត៌មានសរុប: {density:.2f}%")
    print(f"📝 ចំនួនប្លុកអក្សរដែលរកឃើញ: {len(result)}")
    
    for (bbox, text, prob) in result:
        print(f"   👉 រកឃើញពាក្យ: {text} (ភាពច្បាស់: {prob:.2f})")

    # ៣. វាយតម្លៃ Reach
    if density > 15 or len(result) > 10:
        print("\n⚠️ លទ្ធផល: Poster នេះមានព័ត៌មានច្រើនពេក អាចនឹងបាត់បង់ Reach!")
    else:
        print("\n✅ លទ្ធផល: Poster នេះមានតុល្យភាពល្អ ស័ក្តិសមសម្រាប់បាញ់ Ads!")

# សាកល្បងជាមួយរូបភាពរបស់អ្នក
detail_analysis('1000000661.jpg')
