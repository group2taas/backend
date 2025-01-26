from django.db import models


class UserProfile(models.Model):
    # TODO: replace with models.UUIDField?
    uid = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
