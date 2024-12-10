from .models import User

def get_user_by_email(email):
       return User.objects.filter(email=email).first()

def update_user_role(user_id, new_role):
       try:
              user = User.objects.get(id=user_id)
              user.role = new_role
              user.onboarding=1
              user.save()
              return user
       except User.DoesNotExist:
              return None
