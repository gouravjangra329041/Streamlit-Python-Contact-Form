#streamlit run web.py
import streamlit as st

st.title("Welcome to Our Website")
st.header("A Python Website")
st.subheader("My New Project of building a website using Python Language")
st.markdown("I Love Python")
st.code("""for i in range(1,5,1):
            print("Hello")
        """)
import streamlit as st
import pandas as pd

name = st.text_input("Enter Your Name: ")
email = st.text_input("Enter Your Email Id: ")
address = st.text_area("Enter Your Text: ")
classdata = st.selectbox("Enter Your Class: ",(1,2,3,4,5,6))

button = st.button("Submit")
if button :
    st.markdown(f"""
    Name : {name}
    Email : {email}
    Address : {address}
    class : {classdata}""")
