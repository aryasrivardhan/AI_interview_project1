# AI-Based Interview Question Generator

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple.svg)
![jQuery](https://img.shields.io/badge/jQuery-3.x-blue.svg)

A comprehensive and interactive web application designed to help users prepare for technical interviews. The platform allows users to select a topic, difficulty level, and the desired number of questions to generate tailored interview questions. Each generated question is accompanied by key points and short answers to facilitate rapid learning and self-assessment.

---

## Features

- **Topic Selection**: Choose from core technical topics including `Data Structures`, `Python`, `DBMS`, and `Operating Systems`.
- **Difficulty Levels**: Filter questions by `Easy`, `Medium`, or `Hard` to match your preparation stage.
- **Dynamic Question Count**: Request any number of customizable questions (up to 10) per session.
- **Toggle Answers**: Instantly reveal or hide answers using smooth interactive elements.
- **Responsive UI**: Clean, mobile-friendly, and modern design built with Bootstrap 5 and custom CSS.
- **Loading State**: Visual feedback with a loading spinner during question generation.

---

## Technologies Used

### Frontend
- HTML5
- CSS3 (Custom Styling & Animations)
- Bootstrap 5
- JavaScript (ES6)
- jQuery

### Backend
- Python 3
- Flask (Web Framework)
- Jinja2 (Templating Engine)
- SQLite (Local Database for Question Bank)

---

## Setup Instructions

To run this project locally, follow these simple steps:

### 1. Clone the Repository
Open your terminal and clone the repository:
```bash
git clone https://github.com/aryasrivardhan/AI_interview_project1.git
cd AI_interview_project1
```

### 2. Set up Virtual Environment (Recommended)
Create and activate a virtual environment to manage dependencies:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 5. Access the Web App
Open your web browser and navigate to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Project Structure

```text
ai-interview-generator/
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles and animations
│   └── js/
│       └── script.js      # Frontend interactivity and API calls
├── templates/
│   ├── index.html         # Main landing and form page
│   └── result.html        # Question display page
├── app.py                 # Core Flask application and routing
├── interview_prep.db      # SQLite database for questions
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Contributing
Contributions, issues, and feature requests are welcome! 
Feel free to fork the project, add integrations to actual LLM APIs (like OpenAI), and make pull requests.
