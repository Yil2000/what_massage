import streamlit as st

st.title("שליחת הודעות WhatsApp")

group_count = st.number_input("כמה קבוצות הודעות תרצה להכין?", min_value=1, max_value=10, value=1)

links_per_group = []

for i in range(group_count):
    st.header(f"קבוצה {i + 1} ✉️")

    msg = st.text_area(f"הודעה לקבוצה {i + 1}", key=f"msg{i}")
    raw_numbers = st.text_area(f"מספרים לקבוצה {i + 1} (מופרדים בפסיקים)", key=f"nums{i}")

    if st.button(f"🚀 צור קישורים לשליחה", key=f"btn{i}"):
        numbers = [num.strip().replace("-", "") for num in raw_numbers.split(",")]
        links = []
        for number in numbers:
            if number.startswith("0"):
                number = "972" + number[1:]
            url = f"https://wa.me/{number}?text={msg.replace(' ', '%20')}"
            links.append(url)
        links_per_group.append(links)

# הצגת הקישורים
for idx, links in enumerate(links_per_group):
    st.subheader(f"קישורים לקבוצה {idx + 1} ✉️:")
    for link in links:
        st.markdown(f"[{link}]({link})", unsafe_allow_html=True)
