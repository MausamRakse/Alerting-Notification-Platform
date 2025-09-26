# Alerting & Notification Platform

A comprehensive alerting and notification system built with Flask that enables admins to create alerts with configurable visibility and ensures users receive timely notifications with snooze functionality and recurring reminders.

## 🚀 Features

### Admin Capabilities
- **Alert Management**: Create, update, and archive alerts with rich metadata
- **Flexible Visibility**: Target alerts to entire organization, specific teams, or individual users
- **Severity Levels**: Support for Info, Warning, and Critical alert levels
- **Scheduling**: Set start and expiry times for alerts
- **Reminder Control**: Configure reminder frequency and enable/disable reminders
- **Analytics Dashboard**: Comprehensive metrics on alert performance and user engagement

### User Experience
- **Smart Notifications**: Receive alerts based on visibility rules (org/team/user level)
- **Snooze Functionality**: Snooze alerts for the day with automatic reset next day
- **Read/Unread Management**: Track and manage alert status
- **Dashboard**: Personal dashboard with alert summary and statistics
- **Recurring Reminders**: Automatic reminders every 2 hours until snoozed or expired

### System Features
- **Extensible Architecture**: Strategy pattern for notification channels (In-App, Email, SMS)
- **Robust Scheduling**: Background scheduler for automated reminder processing
- **Comprehensive Analytics**: System-wide metrics, trends, and performance data
- **Clean OOP Design**: Proper separation of concerns with SOLID principles
- **Database Logging**: Complete audit trail of all notifications and interactions

## 🏗️ Architecture

### Design Patterns Used
- **Strategy Pattern**: Notification channels (In-App, Email, SMS)
- **Observer Pattern**: User subscription to alerts
- **State Pattern**: Alert status management (read/unread/snoozed)
- **Factory Pattern**: User preference creation

### Key Components
- **Models**: User, Team, Alert, NotificationDelivery, UserAlertPreference
- **Services**: NotificationService, ReminderService
- **Channels**: BaseNotificationChannel, InAppChannel, EmailChannel, SMSChannel
- **Routes**: Admin APIs, User APIs, Analytics APIs

## 📦 Installation

### Prerequisites
- Python 3.8+
- SQLite (default) or PostgreSQL/MySQL (production)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Mousam
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional)**
   ```bash
   export FLASK_ENV=development
   export DATABASE_URL=sqlite:///alerting_platform.db
   export SECRET_KEY=your-secret-key
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

The application will start on `http://127.0.0.1:5000` with seed data automatically loaded.

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Application environment (development/production)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Flask secret key for sessions
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 5000)

### Database Setup
The application uses SQLite by default. For production, configure a PostgreSQL or MySQL database:

```bash
export DATABASE_URL=postgresql://user:password@localhost/alerting_platform
```

## 📚 API Documentation

### Admin APIs (`/api/admin/`)

#### Alert Management
- `POST /api/admin/alerts` - Create new alert
- `GET /api/admin/alerts` - List alerts with filtering
- `GET /api/admin/alerts/{id}` - Get specific alert
- `PUT /api/admin/alerts/{id}` - Update alert
- `POST /api/admin/alerts/{id}/archive` - Archive alert
- `POST /api/admin/alerts/{id}/send-reminder` - Trigger manual reminder

#### System Management
- `GET /api/admin/teams` - List all teams
- `GET /api/admin/users` - List all users
- `GET /api/admin/stats/system` - System-wide statistics

### User APIs (`/api/user/`)

#### Alert Interaction
- `GET /api/user/alerts?user_id={id}` - Get user's alerts
- `POST /api/user/alerts/{id}/read` - Mark alert as read
- `POST /api/user/alerts/{id}/unread` - Mark alert as unread
- `POST /api/user/alerts/{id}/snooze` - Snooze alert for the day
- `GET /api/user/alerts/snoozed?user_id={id}` - Get snoozed alerts

#### Dashboard & History
- `GET /api/user/dashboard?user_id={id}` - User dashboard data
- `POST /api/user/alerts/{id}/view` - Record alert view
- `GET /api/user/notifications/history?user_id={id}` - Notification history

### Analytics APIs (`/api/analytics/`)

#### System Analytics
- `GET /api/analytics/overview` - Comprehensive system overview
- `GET /api/analytics/alerts/performance` - Alert performance metrics
- `GET /api/analytics/trends/daily` - Daily trend analysis
- `GET /api/analytics/users/engagement` - User engagement statistics
- `GET /api/analytics/system/health` - System health status

## 🎯 Usage Examples

### Creating an Alert (Admin)

```bash
curl -X POST http://localhost:5000/api/admin/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "System Maintenance",
    "message": "Scheduled maintenance tonight from 2-4 AM",
    "severity": "warning",
    "visibility_type": "organization",
    "created_by": 1,
    "expiry_time": "2023-12-31T23:59:59Z"
  }'
```

### Getting User Alerts

```bash
curl "http://localhost:5000/api/user/alerts?user_id=3&status=unread"
```

### Snoozing an Alert

```bash
curl -X POST http://localhost:5000/api/user/alerts/1/snooze \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3}'
```

### Getting Analytics Overview

```bash
curl "http://localhost:5000/api/analytics/overview?days=30"
```

## 🗃️ Database Schema

### Core Models
- **User**: User accounts with admin flags and team associations
- **Team**: Organization teams for alert targeting
- **Alert**: Alert definitions with visibility and timing rules
- **NotificationDelivery**: Log of notification attempts and status
- **UserAlertPreference**: User-specific alert states and interactions

### Relationships
- Users belong to Teams (many-to-one)
- Alerts target Users, Teams, or Organization (flexible visibility)
- NotificationDeliveries track delivery attempts per user per alert
- UserAlertPreferences track user interactions per alert

## 🔄 Reminder System

### How It Works
1. **Scheduler**: Runs every 2 hours checking for active alerts
2. **Filtering**: Only sends reminders to users who haven't read or snoozed alerts
3. **Snooze Logic**: Respects daily snooze periods (resets at midnight)
4. **Sequence Tracking**: Tracks reminder sequence numbers for analytics

### Snooze Behavior
- Snoozing an alert prevents reminders until the next day
- Snooze period: Until midnight of the current day
- Next day: Snooze automatically expires, reminders resume
- Read alerts: No further reminders sent

## 📊 Sample Data

The application comes with comprehensive seed data including:
- **5 Teams**: Engineering, Marketing, Sales, Operations, HR
- **16 Users**: Including 2 admins and team members
- **10 Sample Alerts**: Various severities and visibility types
- **Sample Interactions**: Pre-configured user interactions for demo

### Sample Admin Accounts
- `admin@example.com` - General admin user
- `sysadmin@example.com` - Operations team admin

## 🧪 Testing

### Manual Testing
1. Start the application: `python run.py`
2. Use the sample admin accounts to create alerts
3. Test user interactions via API endpoints
4. Monitor reminder system in logs

### API Testing with cURL
See the usage examples above for common API operations.

## 🚀 Production Deployment

### Recommended Setup
1. **Database**: PostgreSQL or MySQL
2. **Web Server**: Gunicorn + Nginx
3. **Process Manager**: Supervisor or systemd
4. **Environment**: Set `FLASK_ENV=production`

### Production Configuration
```bash
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:password@localhost/alerting_platform
export SECRET_KEY=your-secure-secret-key
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🎨 Architecture Highlights

### Object-Oriented Design
- **Encapsulation**: Models encapsulate business logic and data validation
- **Inheritance**: Notification channels inherit from base abstract class
- **Polymorphism**: Different channels handle notifications differently
- **Abstraction**: Service layer abstracts complex operations

### Extensibility Features
- **New Channels**: Easy to add Email, SMS, or custom notification channels
- **Custom Schedulers**: Reminder frequency can be customized per alert
- **Visibility Types**: New visibility types can be added without code changes
- **Analytics**: Metrics system designed for easy extension

### Code Quality
- **Single Responsibility**: Each class has a focused purpose
- **DRY Principle**: Common functionality extracted to base classes
- **Clean APIs**: RESTful design with consistent response formats
- **Error Handling**: Comprehensive error handling with proper HTTP status codes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing code style
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the API documentation above
2. Review the sample data and examples
3. Check application logs for debugging information
4. Create an issue in the repository

---

**Built with ❤️ using Flask, SQLAlchemy, and modern Python practices** 