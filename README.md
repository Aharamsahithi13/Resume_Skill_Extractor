# 📄 Resume Skill Extractor

A full-stack web application that automates the extraction of relevant information from PDF resumes using natural language processing. Built with **Flask** and **PyMuPDF**, this tool allows users to upload resumes and instantly view extracted details like name, email, phone number, skills, and experience. The project is containerized using **Docker**, and deployed directly on **Render using Docker images**.

---

## 🚀 Features

- 📤 Upload PDF resumes through a web interface
- 📌 Extracts:
  - Full Name
  - Email Address
  - Phone Number
  - Skills
  - Work Experience
- 🧠 Uses PyMuPDF + Regex for smart and flexible text extraction
- 💾 Stores output in:
  - Individual JSON files (one per resume)
  - A central JSON database (`resumes_data.json`)
  - CSV format (`resumes_data.csv`) for analysis
- 🔎 Filter resumes on `/results` page using keyword search
- 🌐 Deployed using Docker and hosted on Render
- 🐳 No GitHub integration — deployed directly using Docker image

---

## 🛠️ Tech Stack

| Layer        | Tools/Libraries         |
|--------------|--------------------------|
| Backend      | Flask, Python            |
| PDF Parsing  | PyMuPDF (fitz), Regex   |
| Frontend     | HTML, Bootstrap          |
| Deployment   | Docker, Render           |
| Storage      | JSON, CSV                |

---

## 📁 Project Structure

Resume_data_extractor_1/
├── pycache/ # Python cache files
├── app/ # (Unused or reserved for expansion)
├── results/ # JSON/CSV output files
├── resumes/ # Uploaded PDF files
├── templates/ # Frontend HTML templates
│ ├── index.html # Upload form + result display
│ └── results.html # Searchable results viewer
├── app.py # Main Flask application
├── Dockerfile # Docker setup instructions
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── resume_info.py # PDF parsing and data handling logic
└──.gitattributes #github attributes

## 💻 Run Locally (Without Docker locally)

python app.py

🐳 Docker Deployment
Step 1: Build the Docker Image
bash
Copy
Edit
docker build -t resume_extractor .
Step 2: Test Locally
bash
Copy
Edit
docker run -p 5000:5000 resume_extractor
Access your app at: http://localhost:5000

☁️ Deployment on Render
I deployed this project on Render using a Docker image directly. Here's how:

Build and test the Docker image locally:

bash
Copy
Edit
docker build -t resume_extractor .
Tag and push the image to a container registry (Docker Hub):

bash
Copy
Edit
docker tag resume_extractor aharam13/resume_skill_extractor
docker push aharam13/resume_skill_extractor
Go to https://render.com → New Web Service → Deploy an existing Docker image

Enter the image name (e.g., aharam13/resume_skill_extractor)

Render will deploy and give you a live public URL like https://resume-skill-extractor-latest.onrender.com/
