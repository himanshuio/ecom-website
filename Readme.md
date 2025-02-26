# ShopHouse Ecom Website

## Overview
ShopHouse is a comic-style e-commerce website built using Flask. It features product display, an interactive shopping cart, and an authentication system with login and signup. The UI is designed to be fun and engaging, inspired by comic book aesthetics.

## Features
- **User Authentication**: Signup and login system.
- **Comic-Style UI**: Unique design for product listings and cart.
- **Cart Functionality**: Add/remove items, adjust quantities dynamically.
- **Flask Backend**: Handles user sessions, authentication, and database operations.
- **PostgreSQL Database (Configured in DBeaver)**.
- **Secure Configuration**: Environment variables used to hide sensitive data like `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`.

## Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/himanshuio/ecom-website.git
cd ecom-website
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a `.env` file in the root directory and add:
```sh
SECRET_KEY='your_secret_key_here'
SQLALCHEMY_DATABASE_URI='your_database_url_here'
```

### 4️⃣ Run the Application
```sh
flask run
```
The website will be available at **http://127.0.0.1:5000/**.

## How to Modify Database and Environment Variables
### 🔒 **Modifying Environment Variables**
- Open the `.env` file and change `SECRET_KEY` or `SQLALCHEMY_DATABASE_URI` as needed.
- Restart the Flask server to apply changes.

### 📂 **Viewing the Database**
- If using **SQLite**, you can view the database using **[DB Browser for SQLite](https://sqlitebrowser.org/)**.
- If using **PostgreSQL**, this project is configured in **DBeaver**.

## Live Demo
This project can be viewed here: **[ShopHouse on Render](https://shophouse-xh8n.onrender.com/)**.

## Screenshots
### 🔑 Login Page
![Login Page](D:\webapp2\h.png)

### 🏠 Home Page
![Home Page](D:\webapp2\hdetails.png)

### 🛒 Product Detail Page
![Product Detail](D:\webapp2\hdetails.png)

## License
This project is licensed under the MIT License.

