# **Cloud-Native Modular Portfolio Showcase**
This project has been prepared for the purposes of understanding real-world development and deployment on cloud servers using various tools.

A high-performance, modular web application engineered to batch convert PDF documents into image archives. This project demonstrates a production-grade full-stack architecture, featuring a decoupled frontend, high-speed Python processing, and a complete CI/CD pipeline deployed on AWS infrastructure.

**This project is primarily designed as a modular showcase platform.** It provides a scalable and simple foundation to easily integrate and display future Python and C++ projects within a unified, professional web interface.

## **Key Features**

* **Modular Portfolio Architecture:** Designed specifically to serve as an extensible showcase website. The code structure allows for the seamless addition of new modules (projects) with minimal configuration, making it the perfect home for future Python and C++(incorporated as python modules) applications.  
* **High-Performance Processing:** Leverages **PyMuPDF (Fitz)** for rapid PDF operations.  
* **Decoupled Frontend:** Delivers a "Single Page Application" (SPA) feel using static HTML5/CSS3 served directly by Flask, communicating via REST-like endpoints.  
* **Production Infrastructure:** Hosted on **AWS EC2** (Ubuntu), utilizing **Nginx** as a reverse proxy and **Gunicorn** as the WSGI application server.  
* **Automated DevOps:** Features a robust CI/CD pipeline using **GitHub Actions** for automated testing and zero-downtime deployment to the live environment.

## **Tech Stack**

### **Backend & Logic**

* **Python 3.12**: Core application language.  
* **Flask**: Micro-framework acting as both the API Gateway and Static File Server.  
* **PyMuPDF (Fitz)**: High-performance engine for PDF parsing and rendering.  
* **Standard Libs**: io, zipfile, tempfile used for efficient stream handling.

### **Frontend**

* **HTML5**: Semantic, static markup served by Flask.  
* **CSS3**: Custom modern styling with CSS variables and responsive Grid/Flexbox layouts.

### **Infrastructure & DevOps ("The Ops Stack")**

* **Cloud Provider**: AWS EC2 (Ubuntu Linux).  
* **Web Server**: Nginx (Reverse Proxy handling HTTP traffic and security headers).  
* **App Server**: Gunicorn (WSGI server managing worker processes).  
* **Process Management**: Systemd (Ensures high availability and service recovery).  
* **DNS**: DuckDNS (Dynamic DNS resolution).  
* **CI/CD**: GitHub Actions (Automated deployment workflow).

## **Installation & Local Development**
To run this project locally on your machine:

1. **Clone the repository:**  
   git clone https://github.com/isinare/FOSSProjectSem2.git \
   cd FOSSProjectSem2  

2. **Create a Virtual Environment:**  
   python3 \-m venv venv  
   source venv/bin/activate  \# On Windows use \`venv\\Scripts\\activate\`  

3. **Install Dependencies:**  
   pip install \-r requirements.txt  
   
4. **Run the Development Server:**  
   python app.py  
   Access the application at http://localhost:5000.

## **Deployment (AWS EC2)**

The live production environment is deployed using the following configuration:

1. Systemd Service (flaskportfolio.service):  
   Manages the Gunicorn process, ensuring it starts on boot and restarts on failure.  
2. Nginx Configuration:  
   Routes incoming traffic to the Gunicorn socket.  
3. CI/CD Pipeline:  
   Any push to the main branch triggers the GitHub Actions workflow, which:  
   * Connects to the EC2 instance via SSH.  
   * Pulls the latest code.  
   * Updates dependencies.  
   * Restarts the Systemd service to apply changes instantly.

## **License**
This project is licensed under the MIT License

**Author:** Ishan Sinare

**Project:** FOSS Recruitment Showcase Project
