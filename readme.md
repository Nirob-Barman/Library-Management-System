# Library Management System

This Django-based library management system allows users to register, log in, borrow and return books, view their transaction history, and update their profile information.

## Features

- User Registration and Authentication
- Book Borrowing and Returning
- Transaction Tracking
- User Profile Management
- Email Notifications for Transactions and Book Events

## Technologies Used

- Django
- Python
- HTML/CSS
- Bootstrap
- SQLite (or your preferred database)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/library-management-system.git
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    cd library-management-system
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

4. Create a superuser account for admin access:

    ```bash
    python manage.py createsuperuser
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

6. Visit [http://localhost:8000/admin/](http://localhost:8000/admin/) to log in with the superuser account.

## Usage

1. Access the application at [http://localhost:8000/](http://localhost:8000/).
2. Register a new user account or log in.
3. Borrow and return books, view transaction history, and update your profile.

## Email Configuration

Ensure that your email settings are configured in the `settings.py` file for email notifications to work.

```python
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
