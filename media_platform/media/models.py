import mimetypes
from django.db import models
# from django.db.models import Avg
# from django_postgres_extensions.models.fields import ArrayField
from django.forms import ValidationError
from django.core.validators import FileExtensionValidator

import os
from typing import Dict, List, Optional

# Create your models here.
ext_validator = FileExtensionValidator(['MOV', 'avi', 'mp4', 'webm', 'mkv', 'pdf', 'doc', 'docx', 'txt'])

class Content(models.Model):
    title = models.CharField(max_length=255)
    metadata = models.JSONField()
    rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    class Meta:
       db_table = 'contents'

    def clean(self):
        """
        Ensure that rating value is between 0 and 10.
        """
        if not (0 <= self.rating <= 10):
            raise ValidationError('Rating value must be between 0 and 10.')
    
    def __str__(self):
        return self.title
    
class File(models.Model):
    content = models.ForeignKey(Content, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='content_files/', validators=[ext_validator])

    class Meta:
       db_table = 'files'

    def clean(self):
        # Ensure the file extension is valid
        super().clean()

    def file_type(self) -> Optional[str]:
        """
        Detection of the file type based on the file extension.
        """
        file_type, _ = mimetypes.guess_type(self.file.path)
        return file_type if file_type else 'Unknown file type'
    
    def __str__(self):
        return f'{self.file_type()} - {self.content.title}'
    
# class Metadata(models.Model):
#     description = models.TextField()
#     authors = ArrayField(models.CharField(max_length=100), null=True, blank=True)
#     content = models.ForeignKey(Content, related_name='metadata', on_delete=models.CASCADE)

class Group(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
       db_table = 'groups'

    def __str__(self):
        return self.name
    
class Channel(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='channel_pictures/')
    subchannels = models.ManyToManyField('self', blank=True, symmetrical=False)
    contents = models.ManyToManyField(Content, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    class Meta:
       db_table = 'channels'

    def __str__(self):
        return self.title

    def clean(self):
        """
        Ensure that a Channel either contains contents or subchannels, but not both.
        """
        if self.contents.exists() and self.subchannels.exists():
            raise ValidationError('A channel cannot have both contents and subchannels.')
        if not self.contents.exists() and not self.subchannels.exists():
            raise ValidationError('A channel must have at least one content or one subchannel.')

    def avg_rating(self):
        """
        Compute the rating of the channel based on subchannels or contents.
        """
        ratings = None
        if self.subchannels.exists():
            ratings = [subchannel.avg_rating() for subchannel in self.subchannels.all() if subchannel.avg_rating() is not None]
        elif self.contents.exists():
            ratings = [content.rating for content in self.contents.all() if content.rating is not None]
        return sum(ratings) / len(ratings) if ratings else None
    
    
