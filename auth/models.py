from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """manger for user profiles"""

    def create_user(self, username,email ,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)

        return user
