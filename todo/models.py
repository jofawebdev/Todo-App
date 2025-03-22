from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Choices for task priority
PRIORITY_CHOICES = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
)

class Task(models.Model):
    title = models.CharField(max_length=200)  # Task title
    description = models.TextField(blank=True)  # Optional detailed description
    due_date = models.DateField()  # When the task is due
    completed = models.BooleanField(default=False)  # Task completion status
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )  # Task priority level

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    ) # Link the task to its creator

    def __str__(self):
        return self.title  # Useful when printing the object
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs):
        # call the original save() method with all parameters.
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)