from django.contrib.auth.backends import UserModel
from django.core.validators import FileExtensionValidator
from django.db import models


class Token(models.Model):
    token = models.CharField(max_length=100, primary_key=True)
    user_id = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="auth"
    )


class New(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewImage(models.Model):
    item = models.ForeignKey(New, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")


HELPS_TYPES = {
    'MG': ('MG', 'Marriage aid'),
    'B': ('B', 'Building aid'),
    'D': ('D', 'Pay off debts'),
    'O': ('O', 'Other'),
    'MD': ('MD', 'Medical aid'),
    'R': ('R', 'Reduction of pays'),
    'P': ('P', 'Paying the rent'),
    'F': ('F', 'Feed and clothe')
}
HELPS_SOURCE = {
    'I': ('I', 'Imam hussain holy shrain'),
    'S': ('S', 'Sharia rights')
}


class Help(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    type = models.CharField(
        max_length=2,
        choices=HELPS_TYPES.values(),
        default="O",
    )
    source = models.CharField(
        max_length=1,
        choices=HELPS_SOURCE.values(),
        default="I",
    )
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HelpImage(models.Model):
    item = models.ForeignKey(Help, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    video = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LectureVideo(models.Model):
    item = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="files"
    )
    image = models.ImageField(upload_to="videos")


class FridaySermon(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    title_1 = models.CharField(max_length=100)
    title_2 = models.CharField(max_length=100)
    desc_1 = models.CharField(max_length=1000000)
    desc_2 = models.CharField(max_length=1000000)
    video_1 = models.URLField(max_length=500)
    video_2 = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FridaySermonVideo(models.Model):
    item = models.ForeignKey(FridaySermon, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="videos")


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Status(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StatusImage(models.Model):
    item = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookPDF(models.Model):
    item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="files")
    image = models.ImageField(upload_to="images")
    pdf = models.FileField(upload_to="pdfs", validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])])


class Live(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)


class Views(models.Model):
    type = models.CharField(max_length=200)
    model_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Stat(models.Model):
    label = models.CharField(max_length=255)
    value = models.FloatField()
    count = models.IntegerField()
    year = models.IntegerField()
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.year) + " - " + self.label + " - " + str(self.value) + " - " + str(self.count)
