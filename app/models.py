from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

UserModel = get_user_model()

class Token(models.Model):
    token = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="auth"
    )

class New(models.Model):
    title = models.CharField(max_length=100, default='default title')
    desc = models.CharField(max_length=10000, default='default description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NewImage(models.Model):
    item = models.ForeignKey(New, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")

HELPS_TYPES = [
    ('MG', 'Marriage aid'),
    ('B', 'Building aid'),
    ('D', 'Pay off debts'),
    ('O', 'Other'),
    ('MD', 'Medical aid'),
    ('R', 'Reduction of pays'),
    ('P', 'Paying the rent'),
    ('F', 'Feed and clothe')
]
HELPS_SOURCE = [
    ('I', 'Imam hussain holy shrain'),
    ('S', 'Sharia rights')
]

class Help(models.Model):
    title = models.CharField(max_length=100, default='default title')
    desc = models.CharField(max_length=1000, default='default description')
    type = models.CharField(
        max_length=2,
        choices=HELPS_TYPES,
        default="O",
    )
    source = models.CharField(
        max_length=1,
        choices=HELPS_SOURCE,
        default="I",
    )
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class HelpImage(models.Model):
    item = models.ForeignKey(Help, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")

class Lecture(models.Model):
    title = models.CharField(max_length=100, default='default title')
    desc = models.CharField(max_length=1000, default='default description')
    video = models.URLField(max_length=500, default='http://default.video.url')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class LectureVideo(models.Model):
    item = models.OneToOneField(
        Lecture,
        on_delete=models.CASCADE,
        related_name="files"
    )
    image = models.ImageField(upload_to="videos")

class FridaySermon(models.Model):
    title = models.CharField(max_length=100, default='default title')
    desc = models.CharField(max_length=100, default='default description')
    title_1 = models.CharField(max_length=100, default='default title 1')
    title_2 = models.CharField(max_length=100, default='default title 2')
    desc_1 = models.CharField(max_length=1000000, default='default description for desc_1')
    desc_2 = models.CharField(max_length=1000000, default='default description for desc_2')
    video_1 = models.URLField(max_length=500, default='http://default.video.url')
    video_2 = models.URLField(max_length=500, default='http://default.video.url')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class FridaySermonVideo(models.Model):
    item = models.ForeignKey(FridaySermon, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="videos")

class Image(models.Model):
    title = models.CharField(max_length=100, default='default title')
    image = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Status(models.Model):
    title = models.CharField(max_length=100, default='default title')
    desc = models.CharField(max_length=200, default='default description')
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class StatusImage(models.Model):
    item = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")

class Book(models.Model):
    title = models.CharField(max_length=100, default='default title')
    author = models.CharField(max_length=100, default='default author')
    desc = models.CharField(max_length=200, default='default description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class BookPDF(models.Model):
    item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")
    pdf = models.FileField(upload_to="pdfs", validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])])

class Live(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200, default='default title')
    desc = models.CharField(max_length=200, default='default description')

class Views(models.Model):
    type = models.CharField(max_length=200)
    model_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Stat(models.Model):
    label = models.CharField(max_length=255, default='default label')
    value = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    year = models.IntegerField(default=2023)
    source = models.CharField(max_length=100, default='default source')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} - {self.label} - {self.value} - {self.count}"
