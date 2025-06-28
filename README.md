SHOPKART

Requirements:
1.Python 3.10 and above
2.Keycloak installed locally
3.Mailhog installed locally

Project Setup
1.To start server
    1.go to the environment location, Scripts\activate
    2.come back to the project directory
    3.python manage.py runserver
2.Start Keycloak
  1.From a command prompt, open the "keycloak-26.2.4\keycloak-26.2.4" directory. (open location accordingly in your machine)
  2.Enter the following command:   "bin\kc.bat start-dev"
  3.keycloak admin url : http://localhost:8080/realms/master/protocol/openid-connect/auth?client_id=security-admin-console&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fadmin%2Fmaster%2Fconsole%2F%23%2Fshopkart%2Frealms&state=2624edda-ae31-40fc-8631-69d4f2110859&response_mode=query&response_type=code&scope=openid&nonce=a67c632c-def3-4d57-a4fc-bb087d260d55&code_challenge=xEZZYA1LO6RXziQDPXIOOtmbjAF31FODdrXPsBBpgk8&code_challenge_method=S256
  (login with username and password) (create a realm and change url accordingly)

3.open mailhog application
  mailhog : http://localhost:8025/
