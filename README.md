# Saeed Ismail - Professional Portfolio Website

A modern, responsive personal portfolio website built with Python, Flask, and Bootstrap 5. This application showcases my academic milestones, software projects, certifications, and provides a contact form that automatically logs visitor messages to a local SQLite/PostgreSQL database and forwards email notifications via Gmail SMTP.

## 🚀 Features

*   **About Me (Home):** An elegant split-screen introduction featuring technical skills, biography, and quick links.
*   **Interactive Resume:** A structured overview of professional experience, education, categorized technical skills, and language competencies.
*   **Project Gallery:** Highlights key projects (like Movie Collection App, Neon Nexus, etc.) with description cards and direct links to GitHub repositories.
*   **Certificates Showcase:** Displays relevant certifications (e.g., Udemy Bootcamps, academic progress) with credential verification links.
*   **Secure Contact System:** 
    *   Saves incoming messages in a database using **SQLAlchemy** declarative models.
    *   Dispatches real-time email notifications to the owner using **Gmail SMTP** and **smtplib**.
*   **Developer Friendly:** Configured with `FLASK_DEBUG` toggles, dotenv integration, and automatic database creation.

---

## 🛠️ Technology Stack

*   **Backend:** Python 3.x, Flask
*   **Database:** SQLite (local development), PostgreSQL (production-ready configuration)
*   **ORM:** SQLAlchemy (Declarative mapping)
*   **Frontend:** Bootstrap 5 (via Bootstrap-Flask), CSS3, Jinja2 Templating
*   **APIs & SMTP:** smtplib, MIME multipart messaging

---

## 💻 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/saeedismail602-creator/my-website.git
    cd my-website
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    # Activate on Windows:
    .venv\Scripts\activate
    # Activate on macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a file named `.env` in the root directory and add the following keys:
    ```ini
    SECRET_KEY_PASS='your-secure-flask-secret-key'
    MAIL_EMAIL='your-smtp-email@gmail.com'
    MAIL_PASSWORD='your-gmail-app-password'
    FLASK_DEBUG=True # Set to False in production
    ```
    > [!IMPORTANT]
    > For the email notification feature, you must use a Google App Password (not your standard account password).

5.  **Run the Server:**
    ```bash
    python main.py
    ```
    The application will start at **http://127.0.0.1:5000**.

---

## 🔒 Security Best Practices Implemented

*   **Ignored Sensitive Data:** Configured `.gitignore` to prevent committing `.env`, `.venv`, IDE configurations, and local databases (`*.db`, `instance/`) to GitHub.
*   **Credential Decoupling:** Database URLs, Flask secret keys, and SMTP credentials are fully loaded dynamically from environment variables using `python-dotenv`.
*   **Production Safety:** Throws warnings and raises errors if critical security configurations are missing when deployed to production.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
