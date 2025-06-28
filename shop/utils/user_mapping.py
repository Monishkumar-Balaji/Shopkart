# # shop/utils/user_mapping.py
# from django.contrib.auth.models import User


# def get_or_create_local_user(keycloak_user): #from local database using keycloak credentials
#     username = keycloak_user.get('preferred_username')
#     email = keycloak_user.get('email')

#     user, _ = User.objects.get_or_create( 
#         username=username,
#         defaults={'email': email}
#     )
#     return user
