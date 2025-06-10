# TaskNinja Backend

TaskNinja is an AI-powered task management system built with Django and Django REST Framework.
[Link to Frontend Repo](https://github.com/Viserion-7/Task_Ninja_Frontend)
## Features

- User Authentication
- Task Management (CRUD operations)
- Categories and Tags
- Due Dates and Reminders
- Email Notifications
- Profile Management
- AI-Powered Task Suggestions

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd SE_backend_dj
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- POST `/api/register/`: Register new user
- POST `/api/login/`: Login user

### Tasks
- GET `/api/tasks/`: List all tasks
- POST `/api/tasks/`: Create new task
- GET `/api/tasks/{id}/`: Get task details
- PUT `/api/tasks/{id}/`: Update task
- DELETE `/api/tasks/{id}/`: Delete task
- POST `/api/tasks/{id}/complete/`: Mark task as complete

### Categories
- GET `/api/categories/`: List categories
- POST `/api/categories/`: Create category

### Profile
- GET `/api/profile/`: Get user profile
- PUT `/api/profile/update/`: Update profile

### Reminders
- GET `/api/tasks/{id}/reminders/`: List task reminders
- POST `/api/tasks/{id}/reminders/`: Create reminder

## Environment Variables

```
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Testing

Run tests with:
```bash
python manage.py test
```

## Email Notifications

1. Enable Gmail 2FA
2. Generate App Password
3. Update EMAIL settings in .env

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License.
