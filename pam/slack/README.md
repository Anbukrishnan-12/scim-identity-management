# PAM Slack SCIM Client

SCIM API client that calls the Django SCIM server running on port 8000.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Django SCIM server is running on port 8000:
```bash
cd ../..
python manage.py runserver
```

3. Run the Flask client on port 9000:
```bash
python app.py
```

## API Endpoints (Port 9000)

- `GET /` - Home page
- `GET /users` - Get all users
- `GET /users/{id}` - Get specific user
- `POST /users` - Create new user
- `PUT /users/{id}` - Update user
- `PATCH /users/{id}` - Partial update user
- `DELETE /users/{id}` - Delete user
- `GET /test` - Test connection to SCIM server

## SCIM Server Endpoints (Port 8000)

- `GET/POST http://127.0.0.1:8000/scim/v2/Users/`
- `GET/PUT/PATCH/DELETE http://127.0.0.1:8000/scim/v2/Users/{id}/`

## Usage

```python
from scim_client import SCIMClient

client = SCIMClient()
users = client.get_users()
```