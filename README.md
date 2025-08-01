# 🚀 Form Data Management API

A fully Dockerized backend system built using **FastAPI** and **PostgreSQL**, designed to manage structured form-based data such as **Wheel Specifications** and **Bogie Checksheet** records. Ideal for inspection, maintenance, and tracking use cases.

---

## 🛠️ Tech Stack

- ⚙️ FastAPI (Python)
- 🐘 PostgreSQL
- 🐳 Docker & Docker Compose
- 🔐 Pydantic + SQLAlchemy
- 🧪 Swagger UI for API docs

---

## 📦 Features

- Submit & view Wheel Specification forms
- Create, retrieve, and update Bogie Checksheet records
- RESTful APIs
- PostgreSQL integration with SQLAlchemy
- Containerized with Docker for consistent dev environment

---

## 🔧 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Mr-aj33t/Form-Data-Management-API.git
cd Form-Data-Management-API
```
### 2. Set up environment variables

  - Create a .env file (or use .env.example):

    - POSTGRES_DB=your_project_name
    - POSTGRES_USER=your_user_name
    - POSTGRES_PASSWORD=your_password
    - DATABASE_URL=postgresql://your_user_name:your_password@Yourhost/your_project_name
 

### 3. Run with Docker
```bash
docker compose up --build
```
### 4. Test API
Visit:
[Test API Documentation] (http://localhost:8000/docs)http://localhost:8000/docs


###📬 Sample API Payloads
Wheel Specification – POST /api/forms/wheel-specifications/
```json
{
  "formNumber": "WS-001",
  "submittedBy": "Ajeet Kumar",
  "submittedDate": "2025-08-01",
  "fields": {
    "treadDiameterNew": "915 mm",
    "lastShopIssueSize": "910 mm",
    "condemningDia": "845 mm",
    "wheelGauge": "1676 mm",
    "variationSameAxle": "0.2 mm",
    "variationSameBogie": "0.5 mm",
    "variationSameCoach": "1.0 mm",
    "wheelProfile": "OK",
    "intermediateWWP": "Standard WWP",
    "bearingSeatDiameter": "140.5 mm",
    "rollerBearingOuterDia": "200.0 mm",
    "rollerBearingBoreDia": "100.0 mm",
    "rollerBearingWidth": "50.0 mm",
    "axleBoxHousingBoreDia": "250.08 mm",
    "wheelDiscWidth": "160.5 mm",
    "additionalProp1": {
      "inspectedBy": "Inspector AJ",
      "remarks": "All dimensions within tolerance"
    }
  }
}
```

### Bogie Checksheet – POST /api/forms/bogie-checksheet/
```json
{
  "formNumber": "BCS-001",
  "submittedBy": "Supervisor Ajeet Sir",
  "submittedDate": "2025-07-25",
  "fields": {
    "bogieType": "EMU-TypeA",
    "lastCheckDate": "2025-01-15",
    "defectFound": "Minor crack on left side frame near axle",
    "repairedBy": "Team B (Mechanical Dept)",
    "nextCheckDueDate": "2026-01-15",
    "brakeSystemStatus": "OK - Functioning Normally",
    "suspensionCondition": "Good - Rubber springs replaced",
    "additionalNotes": "Follow-up recommended after 3 months for crack inspection.",
    "additionalProp1": {
      "inspectedBy": "Senior Engineer Ajeet Kumar",
      "remarks": "Cleared for service with minor observation"
    }
  }
}
```
### 📁 Project Structure
```
📦 Form-Data-Management-API/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── crud.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```
### Author
  - Ajeet Kumar
🔗 GitHub: [Mr-aj33t](https://github.com/Mr-aj33)
