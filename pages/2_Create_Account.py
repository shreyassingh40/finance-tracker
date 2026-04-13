import streamlit as st
import bcrypt
import yaml

st.title("🆕 Create Account")
st.write("Fill in the details below to register.")

username = st.text_input("Choose a Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm = st.text_input("Confirm Password", type="password")

if st.button("Create Account"):
    if password != confirm:
        st.error("Passwords do not match.")
    elif not username or not password:
        st.warning("Please fill out all fields.")
    else:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Append new user to YAML
        with open("auth_config.yaml") as file:
            config = yaml.safe_load(file)

        if username in config["credentials"]["usernames"]:
            st.error("Username already exists.")
        else:
            config["credentials"]["usernames"][username] = {
                "email": email,
                "name": username.title(),
                "password": hashed_pw
            }

            with open("auth_config.yaml", "w") as file:
                yaml.dump(config, file)

            st.success("Account created successfully! Please log in.")
            st.switch_page("1_Login.py")
