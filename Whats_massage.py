import streamlit as st
import urllib.parse

st.title("שליחת הודעת וואטסאפ")

number = st.text_input("הכנס מספר טלפון (לדוג' 972501234567):")
message = st.text_area("הודעה לשליחה:")

if st.button("צור קישור ושלח"):
    if number and message:
        msg_encoded = urllib.parse.quote(message)
        wa_url = f"https://wa.me/{number}?text={msg_encoded}"
        st.success("לחץ על הקישור כדי לשלוח:")
        st.markdown(f"[לחץ כאן לשליחה >>]({wa_url})", unsafe_allow_html=True)
    else:
        st.warning("אנא מלא גם מספר וגם הודעה")
