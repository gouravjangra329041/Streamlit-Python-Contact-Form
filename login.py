import streamlit as st

st.page_link("main.py", label="Back", icon="🏠")

st.title("🔐 Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "admin":
        st.success("Login successful!")
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
    else:
        st.error("Invalid username or password")