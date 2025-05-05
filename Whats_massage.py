import streamlit as st
import urllib.parse

st.set_page_config(page_title="שליחת וואטסאפ מותאמת", page_icon="📱")
st.title("📤 שליחת הודעות וואטסאפ מותאמות אישית")

st.markdown("""
הכנס כל מספר טלפון והודעה בשורה נפרדת, כך:  
""")

# טקסט הקלט מהמשתמש
input_text = st.text_area("📋 מספרים והודעות", height=200, placeholder="+972501234567, שלום יוסי!")

# זיכרון לקישורים שנלחצו
if "sent_links" not in st.session_state:
    st.session_state.sent_links = set()

# כפתור יצירת קישורים
if st.button("🚀 צור קישורים לשליחה"):
    if not input_text.strip():
        st.warning("אנא הזן מספרים והודעות.")
    else:
        lines = input_text.strip().split("\n")
        st.subheader("קישורים לשליחה:")

        for idx, line in enumerate(lines):
            try:
                number, message = line.strip().split(",", 1)
                number = number.strip()
                message = message.strip()
                msg_encoded = urllib.parse.quote(message)
                wa_url = f"https://wa.me/{number}?text={msg_encoded}"
                link_id = f"{number}_{idx}"

                col1, col2 = st.columns([3, 2])

                if link_id in st.session_state.sent_links:
                    col1.success(f"✔️ כבר נשלח ל־{number}")
                else:
                    if col2.button(f"שלח ל־{number}", key=link_id):
                        st.session_state.sent_links.add(link_id)
                        st.success(f"💬 שלח ל־{number} — [לחץ כאן לשליחה >>]({wa_url})", icon="📱")
            except Exception as e:
                st.error(f"שורה לא תקינה: {line}")
