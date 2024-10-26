## Instructions for setting up and running the application.

1. Clone the repository `git clone git@github.com:bharat-dangi/rhombus-ai.git`

### Backend Setup (Django)
1. Go to Backend Folder `cd django-be`
2. Create and Activate Virtual Environment
Note: You should use Python 3
```
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

3. Install the required Python packages:
`pip install -r requirements.txt`
4. Create an `.env` file inside the `django-be` directory.
5. Copy and paste the following content into the `.env` file:
`DJANGO_PORT=8000`

6. Run the server to start the backend:
`python manage.py runserver`


### Frontend Setup (React)
1. Go to Frontend folder `cd react-fe`
2. Install the required npm packages:
Note: Use Node version 16
`npm install`
3. Create an `.env` file inside the `react-fe` directory.
4. Copy and paste the following content into the `.env` file:
`REACT_APP_BE_URL=http://127.0.0.1:8000/api/  # Update if backend URL is different`
5. Run the following command to start the frontend:
`npm start`


### Additional Notes and Comments
#### Project Structure
- The project is split into two main parts:

    `Backend (Django)`: Found in the django-be directory. Handles data processing, API endpoints, and core business logic.

    `Frontend (React)`: Located in the react-fe directory. Provides the user interface for interacting with the backend.

- Folder Structure Overview

    `django-be/config`: Contains Django's core configuration files like settings, URLs, and WSGI.

    `django-be/data_processor`: Holds the main application logic for data processing, including the data type inference service.

    `django-be/env`: Virtual environment directory (should be added to .gitignore to avoid committing to version control).

    `react-fe`: Houses the React frontend files for the project.

- Environment Configuration

    `Environment Variables`: This project relies on environment variables for sensitive information (e.g., SECRET_KEY, ALLOWED_HOSTS). Make sure to create a .env file in the django-be directory as per the setup instructions.

    `CORS Configuration`: The backend currently allows requests from all origins. In production, restrict CORS_ALLOW_ALL_ORIGINS to trusted sources for better security.

    `Data Inference Logic` :The backend includes a custom service for processing uploaded files, inferring data types, and handling large datasets in chunks. This chunked processing is optimized for files with millions of rows, ensuring efficient handling.
    Parallel processing and chunk-based type inference have been implemented, although additional optimizations may be added based on specific usage and performance requirements.
- Error Handling

    Basic error handling is implemented for file upload and data type inference. We can add further validations or specific error messages depending on expected data formats and business logic.

- Dependencies

    `Backend`: All Python dependencies are listed in the `requirements.txt` file. Use `pip install -r requirements.txt` in the django-be directory.

    `Frontend`: JavaScript dependencies are managed via `package.json` in the react-fe directory. Use `npm install` in the react-fe directory to install them.
