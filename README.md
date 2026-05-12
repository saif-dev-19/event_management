# EventHook - Event Management System

EventHook is a role-based event management web application built with Django. It helps organizers create and manage events, users discover and RSVP to events, and admins control users, roles, categories, and event data from dedicated dashboards.

The project is suitable for university clubs, programming communities, seminar teams, workshop organizers, and local event groups that need a simple platform for publishing events and tracking attendees.

## Key Features

### Authentication and User Management

- User registration and login
- Logout support
- Password change and password reset flow
- Custom user model with profile image and phone number
- Profile view and profile update
- Role-based access using Django groups

### Role-Based Dashboards

The system supports three main roles:

- **Admin**: manages users, roles, groups, events, and system data
- **Organizer**: creates, updates, deletes, and monitors events
- **User**: browses events and RSVP registration status

### Event Management

- Create events with name, description, date, time, location, category, image, and seat capacity
- Update existing events
- Delete events
- View event details
- Upload and display event images
- Categorize events
- Track upcoming, past, and total events

### RSVP and Capacity Management

- Users can RSVP to upcoming events
- Duplicate RSVP is prevented per user
- RSVP status is shown only for the logged-in user
- Event capacity/seat limit is enforced
- RSVP is blocked when an event is full
- Seat booking count is displayed, for example: `12 / 50 seats booked`
- RSVP confirmation email is sent after successful registration

### Organizer and Admin Participant Tracking

- Organizer dashboard shows RSVP participants for each event
- Admin event management view shows RSVP participants for each event
- Event detail page shows RSVP participant list to admins and organizers
- Participant name and email are displayed when available

### Search and Filtering

- Search events by name
- Search/filter by location in dashboard logic
- View all, upcoming, and past events
- Dashboard cards display useful event and participant counts

### Media Support

- Event image uploads through `ImageField`
- Profile image uploads through `ImageField`
- Local media files are served through `/media/`
- Default profile image support

## Tech Stack

- **Backend**: Django 5.2.3
- **Language**: Python
- **Database**: SQLite by default, PostgreSQL-ready through `dj-database-url` and `psycopg2-binary`
- **Frontend**: Django Templates
- **Styling**: Tailwind CSS, custom CSS, Font Awesome icons
- **Authentication**: Django Authentication System
- **Email**: SMTP email backend
- **Media Handling**: Pillow + Django media files
- **Debugging**: Django Debug Toolbar

## Project Structure

```text
event_management/
├── core/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home_page.html
│   │   ├── logged_nav.html
│   │   └── non_logged_nav.html
│   └── views.py
├── event/
│   ├── migrations/
│   ├── templates/
│   │   ├── dashboard/
│   │   │   ├── dashboard.html
│   │   │   ├── event_dashboard.html
│   │   │   └── organizer_dashboard.html
│   │   ├── category_form.html
│   │   ├── event_details.html
│   │   └── event_form.html
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── templates/
│   │   ├── accounts/
│   │   ├── admin/
│   │   └── registration/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── event_management/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── media/
├── static/
│   └── css/
├── manage.py
├── requirements.txt
├── package.json
└── README.md
```

## Main Models

### Event

Stores event information.

Important fields:

- `name`
- `description`
- `date`
- `time`
- `location`
- `capacity`
- `asset`
- `category`
- `rspv`

The `rspv` field is a many-to-many relationship with users. This allows the project to track RSVP status per user instead of globally marking an event as RSVPed.

### Category

Stores event category information.

Important fields:

- `name`
- `description`

### CustomUser

Extends Django's `AbstractUser`.

Extra fields:

- `profile_image`
- `number`

## Main URLs

### Public Pages

| URL | Purpose |
| --- | --- |
| `/` | Home page with featured events |
| `/event/about/` | About page |
| `/event/contact/` | Contact page |
| `/event/event/<id>/details/` | Event details |

### User URLs

| URL | Purpose |
| --- | --- |
| `/users/sign-up/` | Register |
| `/users/sign-in/` | Login |
| `/users/logout/` | Logout |
| `/users/profile/` | Profile |
| `/users/edit-profile/` | Update profile |
| `/users/password-change/` | Change password |
| `/users/password-reset/` | Reset password |

### Dashboard URLs

| URL | Purpose |
| --- | --- |
| `/event/dashboard/` | Redirects user to the correct dashboard |
| `/event/event-dashboard/` | Normal user dashboard |
| `/event/organizer-dashboard/` | Organizer dashboard |
| `/users/admin-dashboard` | Admin dashboard |

### Event Management URLs

| URL | Purpose |
| --- | --- |
| `/event/create-event/` | Create event |
| `/event/update-event/<id>/` | Update event |
| `/event/delete-event/<id>/` | Delete event |
| `/event/create-category/` | Create category |
| `/event/event/<id>/rspv-event/` | RSVP to event |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/saif-dev-19/event_management.git
cd event_management
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
npm install
```

### 5. Create `.env` File

Create a `.env` file in the project root.

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Optional PostgreSQL-style variables are already supported in the code comments:

```env
DB_NAME=event_management
USER=postgres
PASSWORD=your-password
HOST=localhost
PORT=5432
```

By default, the project uses SQLite.

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Build Tailwind CSS

```bash
npm run build:tailwind
```

For development watch mode:

```bash
npm run watch:tailwind
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Role Setup

This project uses Django groups for role-based access.

Create these groups from the admin panel or the app's group management page:

- `Admin`
- `Organizer`
- `User`

Then assign users to the correct group.

Important:

- Admin dashboard requires the `Admin` group.
- Organizer dashboard requires the `Organizer` group.
- User event dashboard requires the `User` group.

## RSVP Flow

1. User logs in.
2. User opens the event dashboard or home page.
3. User clicks RSVP on an event.
4. The system checks:
   - Has this user already RSVPed?
   - Is the event full?
5. If valid, the user is added to the event RSVP list.
6. A confirmation email is sent.
7. The button changes to `Already RSVP` for that specific user only.

## Seat Capacity Flow

Each event has a `capacity` field.

Example:

```text
Capacity: 50
RSVP count: 50
Status: Full
```

When RSVP count reaches capacity:

- New RSVP is blocked
- Button shows `Full`
- Seat count still appears on event cards

## Useful Commands

Run Django checks:

```bash
python manage.py check
```

Run migrations:

```bash
python manage.py migrate
```

Create migrations:

```bash
python manage.py makemigrations
```

Run tests:

```bash
python manage.py test
```

Build Tailwind:

```bash
npm run build:tailwind
```

## Current Test Status

The project currently has test files, but no meaningful automated tests are implemented yet. Recommended future tests:

- RSVP duplicate prevention
- RSVP capacity limit
- Admin dashboard access
- Organizer dashboard access
- Event create/update/delete permissions
- Media upload behavior
- Profile update behavior

## Deployment Notes

For production deployment:

- Set `DEBUG=False` or `DEBUG=production`
- Use a secure `SECRET_KEY`
- Configure a production database such as PostgreSQL
- Configure email SMTP credentials
- Serve static files properly
- Serve media files through a production-ready storage solution or web server
- Do not commit `.env`, database files, or uploaded media containing private data

The project already includes dependencies for PostgreSQL support:

- `dj-database-url`
- `psycopg2-binary`

## Recommended Future Improvements

- Add automated tests
- Remove development `print()` debugging statements
- Improve organizer ownership so organizers only manage their own events
- Add ticket/payment support
- Add event capacity editing rules after RSVP starts
- Add exportable RSVP participant list
- Add event reminder emails
- Add calendar integration
- Add REST API endpoints
- Improve deployment configuration for Render or another hosting platform

## Project Summary

EventHook is a practical event management system with real-world features:

- Authentication
- Role-based authorization
- Admin, organizer, and user dashboards
- Event CRUD
- Category management
- RSVP management
- Seat capacity control
- Email confirmation
- Image upload
- Participant tracking

It is more than a basic CRUD project because it includes access control, event attendance logic, capacity validation, media handling, and dashboard-based workflows.

## Author

**Mahfuz / saif-dev-19**

Repository:

```text
https://github.com/saif-dev-19/event_management
```
