# SecureWebExtension - Web Content Filtering System

A comprehensive web content filtering and parental control solution built with Django and Chrome extension to protect children from accessing inappropriate websites.

## 🌟 Features

- **Real-time URL Filtering**: Block access to restricted websites and domains
- **Keyword-based Filtering**: Prevent access to content containing restricted keywords
- **Chrome Extension Integration**: Seamless browser-based protection
- **Administrative Dashboard**: Manage restricted URLs and keywords
- **Analytics & Reporting**: Track blocked/allowed access attempts
- **User Authentication**: Secure login system for administrators

## 📁 Project Structure

```
SecureWebExtension/
├── chrome_web_security_project/    # Django project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL configuration
│   └── ...
├── content_filtering/            # Django app (renamed from 'protect')
│   ├── models.py                 # Database models
│   ├── views.py                  # Application views
│   ├── urls.py                   # App URL configuration
│   ├── middleware.py             # Custom middleware
│   ├── templates/                # HTML templates
│   └── ...
├── chrome_content_filtering_extension/  # Chrome extension
│   ├── manifest.json             # Extension manifest
│   ├── background.js             # Background service worker
│   ├── content.js                # Content script
│   ├── popup.html/js             # Extension popup
│   └── ...
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Chrome browser
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tarxemo/SecureWebExtension.git
   cd SecureWebExtension
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser account**
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create admin credentials
   ```

6. **Run the Django development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 🌐 Chrome Extension Setup

### Load the Extension

1. **Open Chrome Extension Management**
   - Open Chrome browser
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right corner)

2. **Load the Extension**
   - Click "Load unpacked" button
   - Select the `chrome_content_filtering_extension` folder from the project
   - The extension will appear in your extensions list

3. **Configure Extension**
   - Click the extension icon in your browser toolbar
   - The extension will automatically communicate with your Django backend

### Extension Configuration

The extension is configured to communicate with the Django backend at `http://127.0.0.1:8000/api/check-url/`. Make sure your Django server is running for the extension to work properly.

## 🔄 Running Django as a Service (Continuous Protection)

### Using Systemd (Linux)

1. **Create a systemd service file**
   ```bash
   sudo nano /etc/systemd/system/SecureWebExtension.service
   ```

2. **Add the following configuration**:
   ```ini
   [Unit]
   Description=SecureWebExtension Django Web Service
   After=network.target
   
   [Service]
   User=your-username
   Group=www-data
   WorkingDirectory=/path/to/SecureWebExtension
   ExecStart=/path/to/SecureWebExtension/venv/bin/python /path/to/SecureWebExtension/manage.py runserver 0.0.0.0:8000
   Restart=always
   RestartSec=10
   Environment="PATH=/path/to/SecureWebExtension/venv/bin"
   Environment="DJANGO_SETTINGS_MODULE=chrome_web_security_project.settings"
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable SecureWebExtension
   sudo systemctl start SecureWebExtension
   sudo systemctl status SecureWebExtension
   ```

### Using Gunicorn with Nginx (Production)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn service file**
   ```bash
   sudo nano /etc/systemd/system/SecureWebExtension-gunicorn.service
   ```

3. **Add Gunicorn configuration**:
   ```ini
   [Unit]
   Description=SecureWebExtension Gunicorn Service
   After=network.target
   
   [Service]
   User=your-username
   Group=www-data
   WorkingDirectory=/path/to/SecureWebExtension
   ExecStart=/path/to/SecureWebExtension/venv/bin/gunicorn --workers 3 --bind unix:/run/SecureWebExtension.sock chrome_web_security_project.wsgi:application
   Restart=always
   RestartSec=10
   Environment="PATH=/path/to/SecureWebExtension/venv/bin"
   Environment="DJANGO_SETTINGS_MODULE=chrome_web_security_project.settings"
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/SecureWebExtension
   ```

5. **Add Nginx configuration**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /path/to/SecureWebExtension;
       }
       
       location / {
           include proxy_params;
           proxy_pass http://unix:/run/SecureWebExtension.sock;
       }
   }
   ```

6. **Enable the site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/SecureWebExtension /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl enable SecureWebExtension-gunicorn
   sudo systemctl start SecureWebExtension-gunicorn
   ```

### Using Screen (Simple Method)

1. **Create a screen session**
   ```bash
   screen -S SecureWebExtension
   ```

2. **Start Django server**
   ```bash
   cd /path/to/SecureWebExtension
   source venv/bin/activate
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Detach from screen**
   - Press `Ctrl+A`, then `D`
   - To reattach: `screen -r SecureWebExtension`

## 📊 Usage Guide

### Managing Restricted URLs

1. **Log in to the admin panel** (`http://127.0.0.1:8000/admin`)
2. **Navigate to "Content filtering" section**
3. **Add restricted URLs**:
   - Go to "Restricted URLs"
   - Click "Add restricted URL"
   - Enter the URL to block (e.g., `https://facebook.com`)
   - Save

4. **Add restricted keywords**:
   - Go to "Restricted keywords"
   - Click "Add restricted keyword"
   - Enter keywords to block (e.g., `gambling`, `adult`)
   - Save

### Viewing Analytics

1. **Access the dashboard** (`http://127.0.0.1:8000`)
2. **View statistics**:
   - Total clicks/requests
   - Recent URL access attempts
   - Daily request trends
   - Blocked vs allowed URLs

## 🔧 Configuration

### Django Settings

Edit `chrome_web_security_project/settings.py` to modify:
- Database configuration
- Security settings
- CORS settings
- Debug mode
- Static files

### Extension Configuration

Edit `chrome_content_filtering_extension/background.js` to modify:
- Backend API URL
- Request timeout
- Error handling

## 🛡️ Security Considerations

- **Production Deployment**: Always set `DEBUG = False` in production
- **Secret Key**: Change the default `SECRET_KEY` in settings.py
- **Database**: Use PostgreSQL/MySQL instead of SQLite for production
- **HTTPS**: Enable SSL/TLS for production deployments
- **CORS**: Restrict CORS origins to your extension only
- **Authentication**: Implement proper user authentication and authorization

## 🐛 Troubleshooting

### Common Issues

1. **Extension not working**:
   - Ensure Django server is running
   - Check CORS settings in Django
   - Verify extension permissions

2. **Database errors**:
   - Run `python manage.py migrate`
   - Check database file permissions

3. **Service not starting**:
   - Check service logs: `sudo journalctl -u SecureWebExtension`
   - Verify file paths and permissions
   - Check Python virtual environment path

### Logs

- **Django logs**: Check console output or configure logging in settings.py
- **Systemd logs**: `sudo journalctl -u SecureWebExtension -f`
- **Extension logs**: Chrome Developer Tools → Extensions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django framework for robust web development
- Chrome Extension API for browser integration
- Django REST Framework for API development
- Django CORS Headers for cross-origin requests

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the project documentation

---

**SecureWebExtension** - Keeping children safe online through intelligent web filtering.
# SecureWebExtension
