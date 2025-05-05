import streamlit as st
import urllib.parse

st.set_page_config(page_title="שליחת הודעות וואטסאפ", page_icon="📱")
st.title("📤 שליחת הודעות וואטסאפ מותאמות לקבוצות מספרים")

# הסבר למשתמש
st.markdown("""
**איך זה עובד:**  
לכל קבוצת מספרים, תכניס:
- הודעה אחת
- כמה מספרים מופרדים בפסיקים

ניתן להזין מספרים גם בפורמט ישראלי רגיל, כמו `0585665032` – והקוד יהפוך את זה אוטומטית ל־`+972585665032`.
""")


# פונקציה להמרת מספר לפורמט בינלאומי
def normalize_phone_number(num):
    num = num.strip().replace("-", "").replace(" ", "")
    if num.startswith("0") and len(num) == 10:
        return "+972" + num[1:]
    elif num.startswith("+") and len(num) > 8:
        return num
    else:
        return None  # לא תקין


# קלט: כמה קבוצות?
num_groups = st.number_input("🔢 כמה קבוצות הודעות תרצה להכניס?", min_value=1, max_value=20, value=1)

# עדכון בטוח של רשימת הקבוצות בזיכרון
if "messages_data" not in st.session_state:
    st.session_state.messages_data = [{"message": "", "numbers": ""} for _ in range(num_groups)]
elif len(st.session_state.messages_data) != num_groups:
    st.session_state.messages_data = [{"message": "", "numbers": ""} for _ in range(num_groups)]

if "sent_links" not in st.session_state:
    st.session_state.sent_links = set()

# טפסים לכל קבוצה
for i in range(num_groups):
    st.markdown(f"### ✉️ קבוצה {i + 1}")
    msg = st.text_area(f"הודעה לקבוצה {i + 1}", key=f"msg_{i}", value=st.session_state.messages_data[i]["message"])
    numbers = st.text_area(f"מספרים לקבוצה {i + 1} (מופרדים בפסיקים)", key=f"nums_{i}",
                           value=st.session_state.messages_data[i]["numbers"])
    st.session_state.messages_data[i] = {"message": msg, "numbers": numbers}

st.markdown("---")

# יצירת קישורים לשליחה
if st.button("🚀 צור קישורים לשליחה"):
    for i, data in enumerate(st.session_state.messages_data):
        message = data["message"].strip()
        raw_numbers = data["numbers"].strip()

        if not message or not raw_numbers:
            st.warning(f"⛔ קבוצה {i + 1} לא מלאה – דלג.")
            continue

        numbers_list = [num.strip() for num in raw_numbers.split(",") if num.strip()]
        st.subheader(f"📨 קישורים לקבוצה {i + 1}:")

        for number in numbers_list:
            normalized = normalize_phone_number(number)
            if not normalized:
                st.error(f"❌ מספר לא תקין: {number}")
                continue

            msg_encoded = urllib.parse.quote(message)
            wa_url = f"https://wa.me/{normalized}?text={msg_encoded}"
