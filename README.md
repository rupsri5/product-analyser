# Excel Analyzer - Product Data Analysis Tool

A Django-based web application for analyzing Excel files with user roles and dynamic filtering capabilities.

## Features

- **User Authentication**
  - Admin and regular user roles
  - Secure login system
  - User activity tracking

- **Admin Features**
  - Create and manage users
  - Upload, disable, and remove Excel files
  - Configure sheet and column visibility
  - Set filter and result columns
  - View user activity logs

- **User Features**
  - Dynamic product selection (Excel file selection)
  - Automatic sheet selection if multiple sheets exist
  - Dynamic filters based on admin configuration
  - Results display with configurable columns

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rupsri5/product-analyser.git
   cd product-analyser
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Admin Setup**
   - Log in with admin credentials
   - Create users through the admin panel
   - Upload Excel files
   - Configure file settings:
     - Enable/disable sheets
     - Set filter columns (for dropdowns)
     - Configure result columns (always includes 'total')

2. **User Access**
   - Log in with provided credentials
   - Select a product (Excel file) from dropdown
   - If multiple sheets exist, select the sheet type
   - Use dynamic filters based on admin configuration
   - Click search to view results

## Project Structure

```
product-analyser/
├── apps/
│   └── excel_processor/       # Main application
│       ├── migrations/        # Database migrations
│       ├── templates/         # HTML templates
│       ├── admin.py          # Admin interface configuration
│       ├── forms.py          # Form definitions
│       ├── models.py         # Database models
│       ├── urls.py           # URL routing
│       └── views.py          # View logic
├── excel_analyzer/           # Project settings
├── media/                    # Uploaded files
│   └── excel_files/         # Excel file storage
├── templates/               # Global templates
├── manage.py               # Django management script
└── requirements.txt        # Project dependencies
```

## Security Considerations

- The project uses Django's built-in authentication system
- File uploads are validated for type and size
- CSRF protection is enabled
- User permissions are strictly enforced
- Database credentials should be kept secure
- Debug mode should be disabled in production

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your License Here]

## Support

For support, please open an issue in the repository or contact [your contact information].
