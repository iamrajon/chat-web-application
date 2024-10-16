# Real-time Chat Application

A **real-time chat application** developed using Python, Django, Django Channels, Redis, HTMX, Tailwind CSS, and PostgreSQL. This application allows users to communicate instantly in both group chats and private messages with real-time updates and secure authentication. The project demonstrates how to integrate WebSockets for real-time communication, build a responsive UI using Tailwind CSS, and manage data efficiently with Redis and Postgres.

## Features

- **Authentication**: User registration, login, and logout functionality with Django's `django-allauth` package.
- **Profile Management**: Users can update and maintain their profile information.
- **Group Chat**: Users can create or join chat groups and communicate in real time.
- **Private Messaging**: One-on-one private chat feature.
- **Real-time Updates**: Real-time messaging powered by Django Channels and WebSockets.
- **Responsive UI**: Clean, modern UI built with Tailwind CSS.
- **Database**: PostgreSQL as the primary database and Redis for real-time data transfer and message storage.
- **Security**: Password hashing, secure authentication, and private chat encryption.

## Tech Stack

- **Backend**: Python, Django, Django Channels, Redis, WebSockets
- **Frontend**: HTML, HTMX, Tailwind CSS
- **Database**: PostgreSQL
- **Caching and Real-time Data**: Redis
- **Authentication**: `django-allauth`

## Screenshots

![Group Chat](./screenshots/group_chat.png)
![Private Chat](./screenshots/private_chat.png)
![Profile Management](./screenshots/profile_management.png)

## Installation

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- PostgreSQL
- Redis
- Node.js (for Tailwind CSS)
- Django and required Python packages (listed in `requirements.txt`)

### Step-by-Step Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/realtime-chat-app.git
    cd realtime-chat-app
    ```

2. Set up a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    ```sql
    CREATE DATABASE chatapp;
    CREATE USER chatuser WITH PASSWORD 'yourpassword';
    ALTER ROLE chatuser SET client_encoding TO 'utf8';
    ALTER ROLE chatuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE chatuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE chatapp TO chatuser;
    ```

5. Migrate the database:
    ```bash
    python manage.py migrate
    ```

6. Set up Redis (ensure Redis is running on your system):
    ```bash
    redis-server
    ```

7. Create a `.env` file in the project root to store environment variables (example):
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_NAME=chatapp
    DATABASE_USER=chatuser
    DATABASE_PASSWORD=yourpassword
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    REDIS_HOST=localhost
    REDIS_PORT=6379
    ```

8. Run the development server:
    ```bash
    python manage.py runserver
    ```

9. Run the WebSocket consumer (if needed):
    ```bash
    daphne -u /run/daphne.sock realtime_chat_app.asgi:application
    ```

10. Compile Tailwind CSS (ensure Node.js is installed):
    ```bash
    npm install
    npx tailwindcss -i ./static/src/tailwind.css -o ./static/css/tailwind.css --watch
    ```

11. Open your browser and navigate to `http://127.0.0.1:8000/` to see the application in action.

## Usage

- **Sign Up**: Create a new account by registering on the platform.
- **Group Chats**: Join or create a group chat to communicate with multiple users.
- **Private Chats**: Send direct messages to individual users in real-time.
- **Profile**: Update your profile details.

## Deployment

To deploy the application in a production environment, follow these steps:

1. Set `DEBUG=False` in your `.env` file.
2. Set up a production database and Redis server.
3. Use `gunicorn` or `daphne` for serving the application.
4. Configure Nginx or Apache to serve static files and proxy requests to the application.

## Contributing

If you'd like to contribute to this project, feel free to open an issue or submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or feedback, feel free to reach out:

- LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/in/rajanc1209/)
- GitHub: [Your GitHub Profile](https://github.com/iamrajon)

