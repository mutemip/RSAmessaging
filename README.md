# RSAcrypto

RSAcrypto is a web application that uses the RSA encryption algorithm to encrypt and decrypt messages. Users are given control of their keys, with the public key used to encrypt messages and the private key used to decrypt the ciphertext.

## Features

- **User Registration**: Users can register by providing their details and generating their RSA keys.
- **Message Encryption**: Users can compose messages and encrypt them using the recipient's public key.
- **Message Decryption**: Users can decrypt received messages using their private key.
- **Inbox**: Users can view and decrypt messages sent to them.
- **Admin Panel**: Admins can manage users and messages through the Django admin interface.

## Installation

To install the application on your local machine, follow these steps:

1. Clone the repository:
    ```sh
    git clone <https://github.com/mutemip/RSAmessaging>
    ```
2. Navigate to the project directory:
    ```sh
    cd RSAcrypto
    ```
3. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Apply the migrations:
    ```sh
    python manage.py migrate
    ```
6. Create a superuser to access the admin panel:
    ```sh
    python manage.py createsuperuser
    ```
7. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

1. **Register**: Go to the registration page and fill in your details. Generate your RSA keys and keep your private key safe.
2. **Login**: Log in to the system using your credentials.
3. **Compose Message**: Navigate to the compose message page, select a recipient, and write your message. The message will be encrypted using the recipient's public key.
4. **View Inbox**: Go to the inbox page to view received messages. Use your private key to decrypt the messages.
5. **Admin Panel**: Access the admin panel at `/admin` to manage users and messages.

