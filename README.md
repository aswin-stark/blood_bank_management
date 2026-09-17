<div align="center">

# 🩸 Blood Bank Management System (BBMS)

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.0-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Responsive](https://img.shields.io/badge/Design-Fully%20Responsive-brightgreen?style=for-the-badge&logo=css3&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](#)

<p align="center">
  <strong>A modern, responsive, full-featured Blood Bank Management web application built with Django & Bootstrap.</strong><br>
  Streamlines blood donations, emergency patient blood requests, real-time inventory tracking, and administrative decision queues with automated notifications.
</p>

[Key Features](#-key-features) • [Tech Stack](#-tech-stack) • [Installation Guide](#-quick-start--installation) • [Project Structure](#-project-structure) • [Workflows](#-system-workflows)

---

</div>

## 🌟 Overview

The **Blood Bank Management System** bridges the critical gap between blood donors, emergency patients, and blood bank administrators. Built with security, speed, and responsiveness in mind, it provides an intuitive platform for tracking blood inventory levels across all 8 major blood groups, reviewing donor contributions, approving urgent patient requests, and maintaining a complete audit trail.

---

## 🚀 Key Features

### 👑 1. Admin Control Center
- **📊 Real-time Dashboard**: Live summary of total donors, patients, pending blood requests, approved donations, and total units in reserve.
- **🩸 Live Blood Inventory**: Real-time stock status across **A+, A-, B+, B-, O+, O-, AB+, AB-** with restock alerts and stock adjustment forms.
- **💉 Dedicated Donation Workflow**:
  - **Donation Requests Queue**: Review and verify donor contributions with one-click **Approve** and **Reject** actions.
  - **Donation History**: Complete log of all past donations with date, health remarks, and verified stock addition impact.
- **📋 Dedicated Blood Requests Workflow**:
  - **Blood Requests Queue**: Review urgent requests with live available stock checks to prevent out-of-stock approvals.
  - **Request History Archive**: Comprehensive log of fulfilled and rejected requests with stock deduction details.
- **👥 Donor & Patient Directory**: Manage donor/patient accounts, toggle active status, view full activity profiles and donation timelines.
- **📜 Giving Details & Source Tracking**: Record contributions from hospitals, mobile blood camps, and individual walk-ins.
- **📧 Automated Email Alerts**: Automated confirmation and notification emails upon approval or rejection.

---

### 🩸 2. Donor Portal
- **🔐 Secure Authentication**: Custom donor sign-up, login, and password reset.
- **💉 Donate Blood**: Submit donation intentions with health information, age, and disease disclosures.
- **📜 Donation History**: Track personal donation logs, approval statuses, and contributions over time.
- **🆘 Emergency Request**: Donors can also request blood for themselves or family members when in need.
- **📊 Donor Dashboard**: Quick overview of donation counts, approvals, and pending requests.

---

### 🏥 3. Patient Portal
- **📝 Patient Registration**: Easy signup with medical history, doctor remarks, and emergency contact details.
- **🩸 Submit Blood Request**: Request specific blood groups and units with medical reasons and hospital requirements.
- **📑 Request History & Status**: Real-time tracking of request progress (**Pending**, **Approved**, or **Rejected**).
- **📈 Patient Dashboard**: Live stats on approved requests and total units received.

---

### 🎨 4. Modern UI & Responsive Design
- **📱 Fully Responsive**: Seamless experience on Mobile (<600px), Tablet (768px), Laptop, and Desktop displays.
- **🧭 Smart Sub-Navigation**: On-page pill bars to switch between **Requests** and **History** instantly.
- **✨ Polished Aesthetics**: Clean gradients, floating ambient animations, accessible typography, and smooth interactive hover states.

---

## 🛠 Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.7+, Django 3.0+, SQLite3 (Production ready for PostgreSQL / MySQL) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 4, FontAwesome 5 |
| **Styling & Fonts** | Custom Glassmorphism CSS, Space Grotesk, DM Sans, Josefin Sans |
| **Libraries** | `django-widget-tweaks`, `asgiref`, `sqlparse`, `pytz` |

---

## 📋 System Workflows

```
                               ┌─────────────────────────┐
                               │   Blood Bank System     │
                               └────────────┬────────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               ▼                            ▼                            ▼
      ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
      │   Donor Portal  │          │   Admin Portal  │          │  Patient Portal │
      ├─────────────────┤          ├─────────────────┤          ├─────────────────┤
      │ • Register/Login│          │ • Live Stock    │          │ • Register/Login│
      │ • Donate Blood  │──────┐   │ • Approve/Reject│   ┌──────│ • Request Blood │
      │ • View History  │      │   │ • Auto Stock +/-│   │      │ • View Status   │
      │ • Request Blood │      └──►│ • Auto Emails   │◄──┘      │ • Dashboard     │
      └─────────────────┘          └─────────────────┘          └─────────────────┘
```

---

## 💻 Quick Start & Installation

### Prerequisites
- Python 3.7 or higher installed on your machine.
- `pip` package manager.
- Git (optional, for cloning).

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/blood-bank-management.git
cd blood-bank-management
```

### Step 2: Create and Activate a Virtual Environment
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux / macOS
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```
*Follow the on-screen prompts to enter your admin username, email, and password.*

### Step 6: Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Application Home**: [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)
- **Admin Login**: [`http://127.0.0.1:8000/adminlogin`](http://127.0.0.1:8000/adminlogin)
- **Django Standard Admin**: [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)

---

## 📁 Project Structure

```
Blood_Bank_Source_Code/
│
├── blood/                      # Core blood app (stock, requests, giving details)
│   ├── models.py               # Stock, BloodRequest, BloodGiving models
│   ├── views.py                # Admin views, request/donation approval handlers
│   ├── context_processors.py   # Global pending donation/request count badges
│   └── forms.py                # Blood request & stock forms
│
├── donor/                      # Donor management app
│   ├── models.py               # Donor profile & BloodDonate models
│   ├── views.py                # Donor dashboard, donation submission & history
│   └── forms.py                # Donor signup & donation forms
│
├── patient/                    # Patient management app
│   ├── models.py               # Patient profile model
│   ├── views.py                # Patient dashboard & request views
│   └── forms.py                # Patient signup forms
│
├── bloodbankmanagement/        # Django project settings & main routing
│   ├── settings.py             # Global configurations & context processors
│   ├── urls.py                 # Primary URL routing
│   └── wsgi.py                 # WSGI entrypoint
│
├── static/                     # CSS, images, and visual assets
│   ├── css/                    # Custom stylesheets (main, dashboard, role)
│   └── image/                  # Blood bank graphics and illustrations
│
├── templates/                  # HTML templates
│   ├── blood/                  # Admin templates & landing pages
│   ├── donor/                  # Donor dashboard & action templates
│   └── patient/                # Patient dashboard & action templates
│
├── db.sqlite3                  # Default database
├── manage.py                   # Django CLI management script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🔒 Security & Best Practices

- **Role-based Access Control**: Views are protected with `@login_required` and `@user_passes_test` decorators to enforce strict separation between donors, patients, and admins.
- **Atomic Transactions**: Stock additions and subtractions use Django `transaction.atomic()` and `select_for_update()` to prevent race conditions during simultaneous approvals.
- **CSRF Protection**: All POST forms include Django's `{% csrf_token %}` tokens.
- **Media Uploads**: Donor and patient profile photos are securely routed through Django's `MEDIA_ROOT`.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - feel free to use it for personal, academic, or commercial projects.

---

<div align="center">
  <sub>Built with ❤️ for saving lives through efficient blood management.</sub>
</div>

