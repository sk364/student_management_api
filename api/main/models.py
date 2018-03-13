from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=20)
    users = models.ManyToManyField(User, related_name='user_courses')

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)
