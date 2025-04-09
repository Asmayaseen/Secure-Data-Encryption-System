import streamlit as st
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

# Check if SECRET_KEY is correct
if not SECRET_KEY or len(SECRET_KEY.encode()) != 44:
    st.error("❌ Invalid SECRET_KEY! Please generate a valid Fernet key.")
    st.stop()

# Create cipher
cipher = Fernet(SECRET_KEY)

# File to store encrypted data
DATA_FILE = "encrypted_data.json"

# Function to encrypt text
def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt text
def decrypt_text(token):
    return cipher.decrypt(token.encode()).decode()

# Function to save encrypted data
def save_data(entry):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Function to load encrypted data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Streamlit App
st.set_page_config(page_title="🔐 Secure Data Encryption App", page_icon="🔒")
st.title("🔐 Secure Data Encryption App")

# Login system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login_form"):
        password = st.text_input("Enter Master Password:", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if password == MASTER_PASSWORD:
                st.success("✅ Login Successful!")
                st.session_state.logged_in = True
                st.balloons()
            else:
                st.error("❌ Incorrect password!")

if st.session_state.logged_in:
    st.header("🔏 Encrypt / Decrypt Text")

    option = st.selectbox("Choose an option:", ["Encrypt", "Decrypt", "View Saved Data"])

    if option == "Encrypt":
        text = st.text_area("Enter text to encrypt:")
        if st.button("Encrypt"):
            if text:
                encrypted_text = encrypt_text(text)
                save_data({"type": "encrypted", "text": encrypted_text})
                st.success("✅ Text Encrypted Successfully!")
                st.code(encrypted_text)
                st.balloons()
            else:
                st.warning("⚠️ Please enter some text to encrypt.")

    elif option == "Decrypt":
        encrypted_text = st.text_area("Enter encrypted text:")
        if st.button("Decrypt"):
            if encrypted_text:
                try:
                    decrypted_text = decrypt_text(encrypted_text)
                    save_data({"type": "decrypted", "text": decrypted_text})
                    st.success("✅ Text Decrypted Successfully!")
                    st.code(decrypted_text)
                except Exception as e:
                    st.error(f"❌ Decryption failed: {str(e)}")
            else:
                st.warning("⚠️ Please enter encrypted text to decrypt.")

    elif option == "View Saved Data":
        st.subheader("📂 Saved Data")
        data = load_data()
        if data:
            for i, item in enumerate(data):
                st.write(f"**{i+1}. {item['type'].capitalize()} Text:**")
                st.code(item['text'])
        else:
            st.info("No data saved yet.")
