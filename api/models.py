from django.db import models

# Create your models here.


class Weekly(models.Model):
    contest_id = models.IntegerField(db_index=True)
    username = models.CharField(max_length=30)
    lang = models.CharField(max_length=30)
    page = models.IntegerField(db_index=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "contest_id",
                    "page",
                ]
            ),
        ]


class BiWeekly(models.Model):
    contest_id = models.IntegerField(db_index=True)
    username = models.CharField(max_length=30)
    lang = models.CharField(max_length=30)
    page = models.IntegerField(db_index=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "contest_id",
                    "page",
                ]
            ),
        ]
