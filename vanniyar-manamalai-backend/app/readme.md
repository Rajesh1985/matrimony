## Vanniyar Manamalai Backend

### About this application
This is the backend service for the Vanniyar Manamalai matrimony platform. It is built with Python and FastAPI, providing RESTful APIs for user management, profile handling, and other core features required for a matrimony application.

### How to setup environment
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd vanniyar-manamalai-backend/app
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Linux/Mac
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Create a `.env` file in the `app` directory and add your configuration (DB connection, secrets, etc).

### How to run the application
1. **Activate the virtual environment:**
   ```sh
   venv\Scripts\activate  # On Windows
   ```
2. **Start the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

### Steps to deploy in the server
1. **Upload the project files to your server.**
2. **Set up Python and virtual environment on the server.**
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables and database.**
5. **Run the application with a production server (e.g., Gunicorn/Uvicorn):**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
6. **(Optional) Use a process manager like systemd or supervisor to keep the app running.**
7. **(Optional) Set up a reverse proxy (e.g., Nginx) for HTTPS and domain routing.**
