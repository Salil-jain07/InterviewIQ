import streamlit as st
from utils.database import register_user

st.title("📝 Register")

name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):

    if name and email and password:

        success = register_user(
            name,
            email,
            password
        )

        if success:
            st.success("Registration Successful!")
        else:
            st.error("Email already exists!")

    else:
        st.warning("Please fill all fields")