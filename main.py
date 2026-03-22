import streamlit as st
import pandas as pd

col1, col2 = st.columns([1, 5])
with col1:
    st.image("CrazyStream_Logo.jpg", width=120)

with col2:
    st.page_link("main.py", label="Home", icon="🥷")
    st.page_link("pages/cars.py", label="Cars", icon="📚")
    st.page_link("pages/dashboard.py", label="Dashboard", icon="📚")
    st.page_link("pages/chatbot.py", label="Chatbot", icon="💬")
    st.page_link("pages/login.py", label="Login", icon="🔐")

st.write("# WELCOME TO CRAZYSTREAM")

x = st.text_input("What is Your Favourite Movie?")
st.write(f"Your Favourite Movie is: {x}")

st.markdown("<style>div[role='colorpicker']{cursor:pointer;}</style>", unsafe_allow_html=True)
color = st.color_picker("Pick A Color", "#f900cf")
st.write("The current color is", color)

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("faces")