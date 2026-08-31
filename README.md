Qassim Digital Auction

Integrated Digital Platform for Date Auctions, E-Commerce, Sales Analytics, and AI

Qassim Digital Auction is a Django-based digital platform designed to support date auctions and related commercial activities. The project combines an online auction system, seller management, digital shops, sales analytics dashboards, and an AI-based image classification component into one integrated platform.

Project Overview

The platform was developed as a graduation project with the goal of providing a digital environment for managing date auctions and analyzing sales data.

Main Components

• Digital Auction System — Create, publish, manage, and participate in auctions.
• Bidding System — Buyers can place bids while the platform tracks auction prices and bid history.
• Seller Dashboard — Sellers can manage their auctions and related activities.
• Digital Shops — Shop owners can create stores, manage products, inventory, and customer carts.
• Sales Analysis — Interactive dashboards for exploring sales data and generating business insights.
• Qassim Dashboard — Centralized dashboard for presenting project information and analytics.
• User Accounts — Registration, profiles, roles, and account management.
• Staff Panel — Management interface for staff-related operations.
• AI Component — Image-classification functionality using a trained Keras/TensorFlow model.
• Media Management — Support for auction, shop, product, and platform images.

Key Features

Auction Management

• Create and publish auctions.
• Set starting prices and minimum bid increments.
• Configure auction start and end times.
• Upload multiple auction images.
• Place and track bids.
• Suspend auctions when required.
• Display auction details and bidding activity.

Digital Shops

• Create and manage a shop profile.
• Add and manage products.
• Manage product prices and stock.
• Upload product images.
• Enable or disable products.
• Customer shopping cart functionality.
• Shop profile, logo, and banner management.

Sales Analytics

The sales_analysis module provides a dashboard for exploring sales data and presenting business metrics.

The project includes sample sales data and a project database that can be used for analysis and visualization.

The analytics component can be extended to support:

• Total sales
• Sales volume
• Product performance
• Geographic analysis
• Monthly sales trends
• Order/status analysis
• Transaction-size analysis
• Business performance indicators

AI Component

The malaria module contains an AI image-classification component using a trained .h5 model.

It includes preprocessing and model-related scripts for working with image data.

> **Note:** This component is included as part of the integrated project and is intended for software/AI demonstration purposes, not medical diagnosis.

Technology Stack

|Technology        |Purpose                           |
|------------------|----------------------------------|
|Python            |Main programming language         |
|Django            |Web application framework         |
|SQLite            |Local database                    |
|HTML / CSS        |User interface                    |
|JavaScript        |Client-side interactions          |
|Pandas            |Data analysis                     |
|NumPy             |Numerical processing              |
|Plotly            |Interactive data visualization    |
|Matplotlib        |Data visualization                |
|OpenCV            |Image processing                  |
|TensorFlow / Keras|AI model development and inference|
|Pillow            |Image handling                    |

Project Structure

```text
QassimDigitalAuction/
│
├── accounts/                 # User accounts and profiles
├── auctions/                 # Auctions, bids, and auction images
├── seller/                   # Seller functionality
├── shops/                    # Digital shops, products, and carts
├── sales_analysis/           # Sales analysis and dashboard
├── qassim_dashboard/         # Main analytics dashboard
├── staffpanel/               # Staff management
├── portal/                   # Main portal
├── malaria/                  # AI image-classification component
├── media/                    # Uploaded media
├── config/                   # Django project configuration
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── cmds.md                   # Development commands
```

Installation

1. Clone the repository

```bash
git clone https://github.com/1ios7/-Qassim-Date-Auction-Sales-Analysis.git
cd -Qassim-Date-Auction-Sales-Analysis
```

2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Apply migrations

```bash
python manage.py migrate
```

5. Create an administrator account

```bash
python manage.py createsuperuser
```

6. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Configuration

For local development, Django settings are located in:

```text
config/settings.py
```

Before deploying the application to a production environment, configure environment variables for sensitive settings such as the Django SECRET_KEY, disable debug mode, and configure allowed hosts and a production database.

Data

The project contains sample/project data used by the sales-analysis component.

The repository may also contain local SQLite and media files for demonstration purposes. In a production deployment, databases and user-uploaded media should normally be handled separately from source code.

Development Notes

The project is organized as a modular Django application, with separate apps for the major platform features. This structure makes it easier to maintain, extend, and develop each component independently.

Future Improvements

Potential improvements include:

• Deployment to a production cloud environment.
• PostgreSQL or another production-grade database.
• Secure environment-variable configuration.
• Real-time bidding using WebSockets.
• Payment gateway integration.
• Advanced sales forecasting.
• More comprehensive automated testing.
• Role-based permissions and access control.
• CI/CD automation.
• Improved AI model evaluation and monitoring.

Academic Project

Project: Qassim Digital Auction and Sales Analysis

The project demonstrates practical skills in:

• Web application development
• Database design
• Django development
• Data analysis
• Data visualization
• Image processing
• AI integration
• Modular software design

License

This project is provided for educational and portfolio purposes.
