import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Secure secret key config
secret_key = os.getenv("SECRET_KEY_PASS")
if not secret_key and os.getenv("FLASK_ENV") == "production":
    raise ValueError("SECRET_KEY_PASS environment variable must be set in production!")
app.config['SECRET_KEY'] = secret_key or "default_secret_key"

Bootstrap5(app)

# Database Configuration using SQLAlchemy 3.x declarative style
class Base(DeclarativeBase):
    pass

# Dynamic database URL configuration (supports PostgreSQL out-of-the-box for production hosting)
db_url = os.getenv("DATABASE_URL", "sqlite:///messages.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Message model definition
class Message(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

# Create database tables automatically
with app.app_context():
    db.create_all()

# Helper function to send email notification
def send_email_notification(name, sender_user_email, subject, message):
    smtp_email = os.getenv("MAIL_EMAIL")
    smtp_password = os.getenv("MAIL_PASSWORD")
    recipient_email = "saeedismail602@gmail.com"  # Recipient email address
    
    if not smtp_email or not smtp_password:
        print("SMTP credentials are not configured in the .env file. Email sending skipped.")
        return False
        
    try:
        # Create MIME multipart message container
        msg = MIMEMultipart()
        msg['From'] = f"Website Contact <{smtp_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"New Message: {subject}"
        
        # Email body structure
        body = f"You received a new message from your portfolio contact form:\n\n" \
               f"Name: {name}\n" \
               f"Email: {sender_user_email}\n" \
               f"Subject: {subject}\n\n" \
               f"Message:\n{message}"
               
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP (defaults to smtp.gmail.com over TLS)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP sending failed: {e}")
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/certificates")
def certificates():
    return render_template("certificates.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message_content = request.form.get("message")
        
        try:
            # Create a new message database entry
            new_message = Message(
                name=name,
                email=email,
                subject=subject,
                message=message_content
            )
            db.session.add(new_message)
            db.session.commit()
            
            # Send email notification to user
            email_sent = send_email_notification(name, email, subject, message_content)
            if not email_sent:
                print("Warning: Contact message saved to database, but email notification failed.")
            
            # Always show a clean, professional confirmation to the visitor
            flash("Thank you! Your message has been successfully received. I will review it and get back to you as soon as possible.", "success")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error saving/sending message: {e}")
            flash("An error occurred while sending your message. Please try again.", "danger")
            
        return redirect(url_for('contact'))
        
    return render_template("contact.html")

@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "online",
        "service": "Flask Portfolio Backend",
        "database": "SQLAlchemy ORM Active",
        "email_smtp": "Active (SMTP Gateway Ready)"
    })

@app.route("/robots.txt")
def robots_txt():
    content = "User-agent: *\nAllow: /\nSitemap: " + request.url_root.rstrip('/') + "/sitemap.xml"
    return Response(content, mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        url_for('home', _external=True),
        url_for('resume', _external=True),
        url_for('projects', _external=True),
        url_for('certificates', _external=True),
        url_for('contact', _external=True)
    ]
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for p in pages:
        xml.append(f'  <url><loc>{p}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype="application/xml")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    # Determine debug mode from environment variable (default: False for production-safety)
    is_debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    # Also support FLASK_ENV for backwards compatibility
    if os.getenv("FLASK_ENV") == "development":
        is_debug = True
    app.run(debug=is_debug)
