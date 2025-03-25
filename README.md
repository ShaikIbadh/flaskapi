# Building a RESTful API with Flask

## Introduction

This project is a RESTful API developed using Flask. It implements key functionalities including:

- User Authentication (JWT)
- CRUD Operations
- File Upload with Validation
- Public Route for Accessible Data
- Error Handling for Common Issues

---

## Technologies Used

- **Flask** (Web Framework)
- **MySQL** (Database)
- **JWT (JSON Web Token)** (Authentication)
- **Postman** (API Testing)

---

## Setup Instructions

### Step 1: Install MySQL

To install MySQL on Mac:

```
brew install mysql
brew services start mysql
```

Set the MySQL root password:

```
mysql_secure_installation  # Default root password is 'new_password'
```

### Step 2: Create a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

### Step 4: Project Structure

```
/flaskapi
│
├── /app
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   ├── config.py
│   ├── utils.py
│   ├── routes.py
│
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── /uploads
```

### Step 5: Configure `.env` File

Create a `.env` file in the root directory with the following content:

```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=new_password
MYSQL_DB=flask_api
```

### Step 6: Run the Flask Application

```
python run.py
```

The application should run at `http://127.0.0.1:5000`

---

## API Endpoints

### 1 **User Registration**

- **Method:** `POST`
- **URL:** `/register`
- **Body (JSON):**

```json
{
    "username": "testuser",
    "password": "pass123"
}
```

- **Success Response:**

```json
{
    "message": "User registered successfully"
}
```

---

### 2 **User Login**

- **Method:** `POST`
- **URL:** `/login`
- **Body (JSON):**

```json
{
    "username": "testuser",
    "password": "pass123"
}
```

- **Success Response:**

```json
{
    "access_token": "<YOUR_JWT_TOKEN>"
}
```

---

### 3 **Create Item**

- **Method:** `POST`
- **URL:** `/items`
- **Headers:**
  - `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- **Body (JSON):**

```json
{
    "name": "Sample Item",
    "description": "This is a sample item created via the API"
}
```

- **Success Response:**

```json
{
    "message": "Item created successfully"
}
```

---

### 4 **Read All Items**

- **Method:** `GET`
- **URL:** `/items`
- **Headers:**
  - `Authorization`: `Bearer <YOUR_JWT_TOKEN>`

---

### 5 **Read Item by ID**

- **Method:** `GET`
- **URL:** `/items/<id>`
- **Headers:**
  - `Authorization`: `Bearer <YOUR_JWT_TOKEN>`

---

### 6 **Update Item**

- **Method:** `PUT`
- **URL:** `/items/<id>`
- **Headers:**
  - `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- **Body (JSON):**

```json
{
    "name": "Updated Item",
    "description": "Updated the item 1."
}
```

- **Success Response:**

```json
{
    "message": "Item updated successfully"
}
```

---

### 7 **Delete Item**

- **Method:** `DELETE`
- **URL:** `/items/<id>`
- **Headers:**
  - `Authorization`: `Bearer <YOUR_JWT_TOKEN>`

---

### 8 **File Upload**

- **Method:** `POST`
- **URL:** `/upload`
- **Headers:**
  - `Authorization`: `Bearer <YOUR_JWT_TOKEN>`
- **Body:**
  - Key: `file` (Select file via `form-data` in Postman)
- **Success Response:**

```json
{
    "message": "File uploaded successfully",
    "filename": "Mid_project.pdf"
}
```

---

### 9 **Public Route (No Token Required)**

- **Method:** `GET`
- **URL:** `/public`

---

## Error Handling

The API handles errors effectively, ensuring meaningful responses for:

- `400`: Missing fields or invalid data.
- `401`: Unauthorized access or missing token.
- `404`: Resource not found.
- `500`: Internal server errors.

---

## Contributor

- **Safdar Ibadh Shaik** (Individual Project)
- **CWID: 875437477**
  ## SCREENSHOT OF POSTMAN ![Image 3-25-25 at 1 08 AM](https://github.com/user-attachments/assets/a47c4ef1-eb77-4ce7-95e4-bacccec8ed6a)


