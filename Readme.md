# Event Management API

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd EventManagement

2. Use Docker to run the app.
   ```bash
   docker-compose up --build

3. Enter docker console to create a superuser:
   ```bash
   docker ps -a # look at the container id with web
   docker exec -it <container_id> bash
   python manage.py createsuperuser
   ...
   exit
   
3. Get token for Authorization
POST: `/api/token/` with JSON:
   ```bash
   {
      "username": "your_username", 
      "password": "your_password"
   }
You can also refresh your token with POST `/api/token/refresh`

Use it in the `Authorization` header like so:

`Authorization: Bearer <your_token>`

API Docs:

1. GET `/api/events/`: List all events.
2. POST `/api/events/`: Create a new event (authenticated users only).
Example data:
   ```bash
   {
     "title": "Tech Conference 2025",
     "description": "A conference for tech enthusiasts to explore the latest trends in AI, Machine Learning, and Blockchain.",
     "date": "2025-12-15T09:00:00Z", 
     "location": "Tech Arena, Silicon Valley, CA",
     "organizer": 1  # user_id
   }

3. GET `/api/events/{id}/`: Retrieve details of a specific event.
4. PUT `/api/events/{id}/`: Update an existing event.
5. DELETE `/api/events/{id}/`: Delete an event.
6. GET `/api/registrations/`: List all event registrations.

7. POST `api/registrations/<event_id>/register/`: Register a user for an event.
   ```bash
   {
     "user": 1,  # user_id
   }
8. GET `/api/registrations/<registration_id>`: Check registration info by id.
