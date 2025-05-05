import streamlit as st
import re

st.set_page_config(page_title="שליחת WhatsApp", page_icon="✉️")
st.title("שליחת הודעות WhatsApp")

group_count = st.number_input("כמה קבוצות הודעות תרצה להכין?", min_value=1, max_value=10, value=1)

# נאתחל את מצב הקישורים שנלחצו
if "clicked_links" not in st.session_state:
    st.session_state.clicked_links = set()

# הגדרת CSS לצבעים שונים ולשינויים במצב
st.markdown("""
    <style>
        .clicked-link {
            color: green;
            font-weight: bold;
        }
        .not-clicked-link {
            color: red;
        }
    </style>
""", unsafe_allow_html=True)

# פונקציה לבדוק אם המספר תקין
def is_valid_number(number):
    return bool(re.match(r"^05\d{8}$", number))  # תואם ל-10 ספרות שמתחילות ב-05

for i in range(group_count):
    st.header(f"קבוצה {i + 1}")

    msg = st.text_area(f"הודעה לקבוצה {i + 1}", key=f"msg{i}")
    raw_numbers = st.text_area(f"מספרים לקבוצה {i + 1} (הכנס כל מספר בשורה נפרדת)", key=f"nums{i}")

    if st.button(f"🚀 צור קישורים לשליחה", key=f"btn{i}"):
        # מחלקים את הקלט לשורות ומנקים רווחים
        numbers = [num.strip().replace("-", "") for num in raw_numbers.splitlines() if num.strip()]

        # בדיקת האם המספרים מופרדים בשורות שונות
        if len(numbers) == 0:
            st.error("יש להכניס מספרים בשורות שונות.")
            continue

        # אם יש טקסט שהוא לא מספר, יוצג הודעה
        if any(not num.isdigit() for num in numbers):
            st.error("אנא הכנס מספר תקין.")
            continue

        # בדיקה אם כל המספרים תקינים
        invalid_numbers = [num for num in numbers if not is_valid_number(num)]
        if invalid_numbers:
            st.error(f"המספרים לא תקינים: {', '.join(invalid_numbers)}. אנא הכנס מספרים תקינים בפורמט 05xxxxxxxx.")
            continue

        # יצירת הקישורים
        links = []
        for number in numbers:
            if number.startswith("0"):
                number = "972" + number[1:]
            url = f"https://wa.me/{number}?text={msg.replace(' ', '%20')}"
            links.append(url)

        st.subheader(f"קישורים לקבוצה {i + 1}:")

        for idx, link in enumerate(links):
            col1, col2 = st.columns([8, 2])
            with col1:
                if link in st.session_state.clicked_links:
                    st.markdown(f"<span class='clicked-link'>{link}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='not-clicked-link'>{link}</span>", unsafe_allow_html=True)
            with col2:
                if link in st.session_state.clicked_links:
                    # הצגת טקסט "נשלח" בצבע ירוק
                    st.markdown("<span class='clicked-link'>✔️ נשלח</span>", unsafe_allow_html=True)
                else:
                    # הצגת טקסט "לא נלחץ" בצבע אדום
                    if st.session_state.get(f"clicked_{i}_{idx}", False):
                        st.session_state.clicked_links.add(link)
                        st.session_state[f"clicked_{i}_{idx}"] = True
                        st.experimental_rerun()  # כדי שהתצוגה תתעדכן
                    st.markdown("<span class='not-clicked-link'>לא לא נשלח</span>", unsafe_allow_html=True)
