# Farmer Support Platform (Agri360)

A full-stack Django application design to empower smallholder farmers with access to finance, markets, and expert knowledge.

## Features
*   **Role-Based Access**: Specialized dashboards for Farmers, Extension Officers, and Admins.
*   **Agri-Finance**: Micro-loan requests and crop insurance applications with real-time calculators.
*   **Marketplace**: Direct farmer-to-buyer produce listings.
*   **Knowledge Hub**: Policy documents, GPS service locator, and financial literacy tips.
*   **AI Agri-Advisor**: A chatbot for instant agricultural advice.
*   **Analytics**: Downloadable yield and financial reports.


## Getting Started

### Prerequisites
*   Python 3.8+
*   Django 4.x

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/rick868/cfs-farmers-application.git
    cd cfs-farmers-application
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run migrations:
    ```bash
    python manage.py migrate
    ```
4.  Run the server:
    ```bash
    python manage.py runserver
    ```
5.  Access the app at `http://127.0.0.1:8000/`

## Test Users
| Role | Username | Password |
| :--- | :--- | :--- |
| **Farmer** | `felix_farmer` | `Farming123!` |
| **Officer** | `sarah_officer` | `Officer123!` |
| **Admin** | `admin` | `Admin123!` |

## License
MIT
