# KaryaNet – Full Stack Service Platform

KaryaNet is a full-stack web application that connects customers with workers/service providers.  
It allows users to register, log in, and access role-based dashboards (customer and worker).

The project is built using FastAPI for the backend, PostgreSQL for the database, and HTML/CSS/JavaScript for the frontend.

---

## 🚀 Features

- User Registration & Login
- Worker Registration
- Customer Dashboard
- Worker Dashboard
- Service Listing Pages
- FastAPI REST Backend
- PostgreSQL Database Integration
- Responsive Frontend using HTML, CSS, JavaScript

---

## 🛠 Tech Stack

### Frontend
- HTML  
- CSS  
- JavaScript  

### Backend
- Python
- FastAPI

### Database
- PostgreSQL (local)

### Tools
- Git & GitHub

---

## 📁 Project Structure

KaryaNet-project/
│
├── frontend/
│ ├── icons/
│ ├── images/
│ ├── pages/
│ ├── scripts/
│ ├── styles/
│ └── index.html
│
├── main.py
├── models.py
├── database.py
├── database_models.py
├── cgi.py
├── .gitignore
└── README.md
---

## ⚙️ How to Run Locally

### 1. Clone Repository
git clone https://github.com/VGayathrireddy/KaryaNet-project.git
cd KaryaNet-project

### 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
pip install fastapi uvicorn psycopg2 sqlalchemy

### 4. Setup PostgreSQL
Create a PostgreSQL database
Update database credentials inside database.py

### 5. Run Backend
uvicorn main:app --reload

Backend runs at:
http://127.0.0.1:8000

### 6. Run Frontend
Open:
frontend/index.html
in browser.

### 🎯 Future Improvements
Authentication using JWT
Password hashing
Cloud deployment
Admin dashboard
Better UI/UX
Role-based authorization


### 👩‍💻 Author
GAYATHRI REDDY
Full Stack Developer | Python & FastAPI Enthusiast
GitHub: https://github.com/VGayathrireddy

⭐ If you like this project, feel free to star the repository!