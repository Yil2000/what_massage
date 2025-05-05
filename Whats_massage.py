import streamlit as st

st.set_page_config(page_title="שליחת WhatsApp", page_icon="✉️")
st.title("שליחת הודעות WhatsApp")

group_count = st.number_input("כמה קבוצות הודעות תרצו להכין?", min_value=1, max_value=10, value=1)

# נשתמש ב־session_state כדי לזכור אילו קישורים נלחצו
if "clicked_links" not in st.session_state:
    st.session_state.clicked_links = set()

for i in range(group_count):
    st.header(f"קבוצה {i + 1} ")

    msg = st.text_area(f"הודעה לקבוצה {i + 1}", key=f"msg{i}")
    raw_numbers = st.text_area(f"מספרטי טלפון (בפורמט 0500000000, 0500000000 {i + 1}", key=f"nums{i}")

    if st.button(f"🚀 צור קישורים לשליחה", key=f"btn{i}"):
        numbers = [num.strip().replace("-", "") for num in raw_numbers.split(",")]
        links = []
        for number in numbers:
            if number.startswith("0"):
                number = "972" + number[1:]
            url = f"https://wa.me/{number}?text={msg.replace(' ', '%20')}"
            links.append(url)

        st.subheader(f"קישורים לקבוצה {i + 1} ✉️:")

        for idx, link in enumerate(links):
            col1, col2 = st.columns([8, 2])
            with col1:
                # נבדוק אם נלחץ כבר
                if link in st.session_state.clicked_links:
                    st.markdown(f"✅ [{lשink}]({link})", unsafe_allow_html=True)
                else:
                    st.markdown(f"🔗 [{link}]({link})", unsafe_allow_html=True)
            with col2:
                if st.button("נלחץ", key=f"click_{i}_{idx}"):
                    st.session_state.clicked_links.add(link)
                    st.experimental_rerun()  # מרענן את הדף כדי להציג את הסימון
