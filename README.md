# 📦 SHOPKART

# 📑 Requirements

    1.Python 3.10 and above

    2.Keycloak installed locally

    3.Mailhog installed locally

# ⚙️ Project Setup

1️⃣ Start Django Server

# Activate virtual environment
cd {environment-directory}

Scripts\activate

# Go back to project directory and run server
cd {project-directory}

python manage.py runserver

# 2️⃣ Start Keycloak

# Open your Keycloak directory
cd keycloak-26.2.4\keycloak-26.2.4

# Start Keycloak in dev mode
bin\kc.bat start-dev

Keycloak Admin Console:
http://localhost:8080/admin/master/console

Realm Setup:

Log in with your admin username and password.

Create a new realm (name it as you like, e.g. shopkart).

Update URLs accordingly for your realm.

Example Realm URL (adjust shopkart part to your realm name):

http://localhost:8080/realms/shopkart/protocol/openid-connect/auth

# 3️⃣ Open Mailhog

Mailhog URL:
http://localhost:8025/



📌 Notes
Always activate your environment before starting the server.

Create your realm in Keycloak and adjust URLs accordingly in your project settings.

