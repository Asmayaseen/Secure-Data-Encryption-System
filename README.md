
# Secure Data Encryption System

A simple Streamlit app that allows users to securely encrypt and decrypt their text using the **Fernet encryption** system. This app uses a master password and supports user registration and login functionality.

## Features

- **Registration & Login**: Secure user authentication.
- **Text Encryption**: Encrypt any text using the Fernet encryption method.
- **Text Decryption**: Decrypt any previously encrypted text.
- **Data Storage**: Store encrypted text securely and retrieve it later.
- **Master Password**: Option to use a master password for login.

## Requirements

- Python 3.7+
- Streamlit
- Cryptography
- Python-dotenv

## Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/your-repository/secure-encryption-system.git
cd secure-encryption-system
Step 2: Create a virtual environment (optional but recommended)
bash

python -m venv venv
Activate the virtual environment:

On Windows:

bash

venv\Scripts\activate
On macOS/Linux:

bash

source venv/bin/activate
Step 3: Install dependencies
bash

pip install -r requirements.txt
Step 4: Set environment variables
Create a .env file in the root directory and add the following:

ini

SECRET_KEY=your_base64_fernet_key_here
MASTER_PASSWORD=your_master_password_here
Replace your_base64_fernet_key_here with the key generated using the Fernet.generate_key().decode() command.

Replace your_master_password_here with your desired master password (e.g., admin123).

Step 5: Run the app
bash

streamlit run app.py
Step 6: Access the app
Once the app is running, open the provided local URL in your browser to use the app.

Usage
Register: Create a new account by providing a username and password.

Login: Log in using your credentials or the master password.

Encrypt Text: Enter the text you want to encrypt and see the encrypted output.

Decrypt Text: Enter the encrypted text to decrypt and view the original text.

Saved Data: View the encrypted data saved under your username.

File Structure
pgsql

├── app.py               # Main Streamlit app
├── .env                 # Environment variables (SECRET_KEY, MASTER_PASSWORD)
├── encrypted_data.json  # Store encrypted data
├── users.json           # Store user credentials
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
Contributing
Feel free to fork and contribute to this project. Create issues for any bugs or feature requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

vbnet


### Key Points:
- **SECRET_KEY**: Generate this key using `Fernet.generate_key().decode()` and add it to the `.env` file.
- **MASTER_PASSWORD**: Set a strong password (like `admin123`), or use your custom master password.








