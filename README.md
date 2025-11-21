# Service Membership System API

A FastAPI-based backend system for managing memberships in service-oriented businesses like gyms, coaching centers, or salons.

## Features

- Member management (create, list with filters)
- Membership plans with flexible durations
- Subscription management with automatic end-date calculation
- Attendance tracking with active subscription validation
- **Database trigger** that automatically tracks total check-ins per member

## Tech Stack

- **Python 3.9+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** (preferred) / SQLite (fallback)
- **Pydantic** - Data validation

## Project Structure


🚀 Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/arupanandaparida/Service-Membership-System.git
cd membership-system

⚙️ 2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows
venv\Scripts\activate

Mac / Linux
source venv/bin/activate

📦 3️⃣ Install Dependencies
pip install -r requirements.txt

🗃️ 4️⃣ Apply Database Migrations (if using SQLite or Postgres)
Create the database tables

Run the project once — SQLAlchemy will auto-create the tables:

uvicorn app.main:app --reload


After the first run, you will have the database file (SQLite) or tables ready (Postgres).

🧨 5️⃣ Apply the Database Trigger
SQLite


Make sure the path matches your actual DB file.

PostgreSQL

If using PostgreSQL:

psql -d your_database -f database/triggers.sql

▶️ 6️⃣ Run the FastAPI Server
uvicorn app.main:app --reload


Open your API docs:

http://127.0.0.1:8000/docs