# 📦 ERP Dashboard — Python + Streamlit + PostgreSQL

A lightweight, modern ERP Dashboard Web Application built using:

Python

Streamlit (frontend UI)

PostgreSQL (Google Cloud SQL)

Azure Web App (hosting)

This project provides a clean ERP-style dashboard for internal team operations, analytics, and data management.

## 🚀 Features

✓ Interactive, responsive ERP dashboard
✓ Real-time database connectivity (PostgreSQL)
✓ Modular and scalable project structure
✓ Cloud-ready (Azure Web App compatible)
✓ Secure external DB connection using connection string
✓ Easy to deploy & maintain
✓ Fully open-source

## 🗂 Project Structure

/erp-dashboard
│
├── Dashboard.py        # Main Streamlit UI
├── db.py               # Database connection handler
├── requirements.txt    # Python dependencies
├── Dockerfile          # (Optional) for container deployment
└── README.md           # Project documentation

## 🛠 Installation (Local Development)

1️⃣ Clone the repo

git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set your database environment variable
DB_URL=postgresql://postgres:<PASSWORD>@<PUBLIC_IP>:5432/erpdb

5️⃣ Run the app
streamlit run Dashboard.py

## 🔗 Database — Google Cloud SQL (PostgreSQL)

This project uses Google Cloud SQL as the database backend.

Connection String Format:
postgresql://postgres:<PASSWORD>@<PUBLIC_IP>:5432/erpdb

Enable external access (for Azure):

Google Cloud → SQL → Connections

Add Authorized Network

0.0.0.0/0


Create database:

Name: erpdb

Copy your Public IP and apply it to DB_URL.

## ☁️ Deploy to Azure Web App

1️⃣ Create an Azure Web App (Python 3.10 or 3.11)

2️⃣ Add the environment variable:
Name	Value
DB_URL	postgresql://postgres:<PASSWORD>@<PUBLIC_IP>:5432/erpdb

Location in portal:

Azure Portal → Web App → Configuration → Application Settings

3️⃣ Deploy using GitHub Actions or Zip Deploy

After deploying, restart the Web App.


## 🔧 Environment Variables

Variable	Description
DB_URL	PostgreSQL full connection string (Google Cloud SQL)

## 🧩 Technologies Used

Layer	Technology
Backend	==> Python
Frontend ==> Streamlit
Database	==> PostgreSQL (Google Cloud SQL)
Hosting	==> Azure Web App
DevOps	==> GitHub, Docker

## 📄 License

MIT License — free to use, modify, and distribute.

## 🙌 Acknowledgements

Thanks to the open-source community, Streamlit team, and cloud platforms (Azure + Google Cloud).



