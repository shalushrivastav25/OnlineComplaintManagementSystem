# Online Complaint Management System

## 📋 Project Description

The Online Complaint Management System is a web-based application developed using Python and Streamlit. It allows users to submit complaints, track complaint status, and enables administrators to manage and resolve complaints efficiently.

## ✨ Features

- Submit complaints online
- Automatically generate complaint IDs
- Track complaints using complaint IDs
- Administrator login
- Admin dashboard to view all complaints
- Search complaints by name, email, or title
- Filter complaints by status
- Update complaint status
- Download complaint reports as CSV
- Store complaint records using SQLite

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas

## 📁 Project Files

- `app.py` — Main application
- `requirements.txt` — Required Python libraries
- `complaints.db` — SQLite database created automatically when the application runs

## 🔑 Demo Administrator Login

- **Username:** `admin`
- **Password:** `admin123`

## 🚀 How to Run the Project

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Start the application

```bash
python -m streamlit run app.py
```

### 3. Open the application

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## ⚠️ Disclaimer

This is an educational project prototype. The demo administrator credentials are not suitable for production use. Real deployments require secure authentication, authorization, and protection of personal complaint information.
