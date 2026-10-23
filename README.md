# CodeAlpha Task 3 — SocialHub Social Media Platform

Beginner-friendly Django + SQLite social media app: registration/login, profiles and bios, posts, likes, comments, user profile pages, delete-own-post, and Django admin.

## Windows setup
1. Extract the ZIP and open its folder in VS Code.
2. In Terminal run:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
If PowerShell activation is blocked, use Command Prompt and run `.venv\Scripts\activate.bat`.
3. Open http://127.0.0.1:8000/ and create an account.

Optional admin account: `python manage.py createsuperuser`, then visit http://127.0.0.1:8000/admin/.

This is a learning/demo project. Test and understand the code before submitting. DEBUG is enabled for local development; do not deploy these settings publicly. No image uploads or private messaging are included.
