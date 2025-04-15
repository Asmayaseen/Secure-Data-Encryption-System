import streamlit as st # type: ignore
from cryptography.fernet import Fernet
from dotenv import load_dotenv # type: ignore
import os
import json

# Load environment variables
load_dotenv()
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY")

# Validate the secret key
if not SECRET_KEY or len(SECRET_KEY.encode()) != 44:
    st.error("❌ Invalid SECRET_KEY! Please provide a valid 32-byte base64-encoded Fernet key.")
    st.stop()

cipher = Fernet(SECRET_KEY)

# File paths
DATA_FILE = "encrypted_data.json"
USERS_FILE = "users.json"

# ----------------- Utility Functions ----------------- #

# Encryption/Decryption
def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(token):
    try:
        return cipher.decrypt(token.encode()).decode()
    except Exception:
        return "❌ Invalid encrypted text!"

# Save encrypted data
def save_data(entry):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Load saved data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save user
def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Load users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# ----------------- Streamlit UI ----------------- #

st.set_page_config(page_title="🔐 Secure Encryption App", page_icon="🔒")
st.title("🔐 Secure Encryption App")

# Session state setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Home", "Register", "Login", "Encrypt Text", "Decrypt Text", "Saved Data", "Logout"])

# Home Page
if menu == "Home":
    st.header("🏠 Welcome")
    st.write("Use this app to encrypt/decrypt and store your text securely.")
    st.info("Use the sidebar to navigate.")

# Register Page
elif menu == "Register":
    st.header("📝 Register")
    with st.form("register_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        register = st.form_submit_button("Register")

        if register:
            if new_username and new_password:
                users = load_users()
                if new_username in users:
                    st.error("❌ Username already exists.")
                else:
                    save_user(new_username, new_password)
                    st.success("✅ Registered successfully.")
            else:
                st.warning("⚠️ Fill all fields.")

# Login Page
elif menu == "Login":
    st.header("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            users = load_users()
            if users.get(username) == password or password == MASTER_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome, {username}!")
                st.balloons()
            else:
                st.error("❌ Invalid credentials.")

# Encrypt Page
elif menu == "Encrypt Text":
    if st.session_state.logged_in:
        st.header("🔒 Encrypt Text")
        with st.form("encrypt_form"):
            plain = st.text_area("Enter text to encrypt:")
            encrypt = st.form_submit_button("Encrypt")

            if encrypt and plain:
                encrypted = encrypt_text(plain)
                st.success("✅ Encrypted:")
                st.code(encrypted)

                save_data({"user": st.session_state.username, "encrypted": encrypted})
    else:
        st.warning("⚠️ Login first to encrypt.")

# Decrypt Page
elif menu == "Decrypt Text":
    if st.session_state.logged_in:
        st.header("🔓 Decrypt Text")
        with st.form("decrypt_form"):
            token = st.text_area("Enter encrypted text:")
            decrypt = st.form_submit_button("Decrypt")

            if decrypt and token:
                decrypted = decrypt_text(token)
                st.success("✅ Decrypted:")
                st.code(decrypted)
    else:
        st.warning("⚠️ Login first to decrypt.")

# Saved Data
elif menu == "Saved Data":
    if st.session_state.logged_in:
        st.header("🗃️ Your Encrypted Data")
        data = load_data()
        user_data = [item["encrypted"] for item in data if item.get("user") == st.session_state.username]

        if user_data:
            for i, val in enumerate(user_data, 1):
                st.markdown(f"**{i}.** `{val}`")
        else:
            st.info("ℹ️ No data found.")
    else:
        st.warning("⚠️ Login first.")

# Logout
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("✅ Logged out.")

