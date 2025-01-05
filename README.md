# FastAPI Authentication Service

A FastAPI-based authentication service with support for JWT tokens and social authentication (Google, Facebook).

## Features

- JWT Authentication
- Google OAuth Integration
- postgres Database (configurable)
- Environment-based configuration

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository
```bash
git clone 
cd auth-fastapi
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the virtual environment

On Windows:
```bash
.\venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Setup

1. Create a `.env` file in the `auth` directory
2. Add the following environment variables:

```env
# Application secrets
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Google OAuth credentials
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URL=yoururl

DB_USER =your-db-name
DB_PASSWORD =your-db-name
DB_HOST =your-db-name
DB_PORT =your-db-name
DB_NAME =your-db-name
```

Replace the placeholder values with your actual:
- Google OAuth credentials (from Google Cloud Console)
- A secure secret key for JWT encryption

## Running the Application

1. Ensure your virtual environment is activated
2. Run the application:
```bash
python -m uvicorn main:app --reload
```
