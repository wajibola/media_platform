import inspect
import os
import sys
import pathlib


sys.path.append(os.path.normpath(os.getcwd() + os.sep + os.pardir + '/media_platform'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile

def write_contents():
    Content.objects.create(
        title='Content 1', 
        metadata={'description': 'Content 1 description', 'authors': ['Waz'], 'genre': 'Comedy'}, 
        rating=8.5
    )
    
    Content.objects.create(
        title='Content 2', 
        metadata={'description': 'Content 2 description', 'authors': ['John Doe'], 'genre': 'Drama'}, 
        rating=7.5
    )
    
    Content.objects.create(
        title='Content 3', 
        metadata={'description': 'Content 3 description', 'authors': ['James'], 'genre': 'Thriller'}, 
        rating=9.0,
    )

    print('Contents created...')

def write_groups():
   Group.objects.create(name='Group 1')
   Group.objects.create(name='Group 2')

   print('Groups created...')

def write_channels():
    Channel.objects.create(title='Channel 1', language='EN')
    Channel.objects.create(title='Channel 2', language='EN')
    Channel.objects.create(title='Channel 3', language='EN')

    print('Channels created...')

def populate_channel_group_relationships():
    # Get related channels
    channel1 = Channel.objects.get(title='Channel 1')
    channel2 = Channel.objects.get(title='Channel 2')
    
    # Get related groups
    group1 = Group.objects.get(name='Group 1')
    group2 = Group.objects.get(name='Group 2')

    # Add group to channels
    channel1.groups.add(group1)
    channel2.groups.add(group2)

    print('Channel-group relationships saved... ')

def populate_channel_content_relationships():
    # Get related channels
    channel1 = Channel.objects.get(title='Channel 1')
    channel2 = Channel.objects.get(title='Channel 2')

    # Get related contents
    content1 = Content.objects.get(title='Content 1')
    content2 = Content.objects.get(title='Content 2')

    # Add group to channels
    channel1.contents.set([content1, content2])
    channel2.contents.set([content1])

    print('Channel-content relationships saved...')

def populate_channel_subchannel_relationships():
    # Get related channels
    channel3 = Channel.objects.get(title='Channel 3')

    # Create subchannel
    subchannel1 = Channel.objects.create(title='Subchannel 1', language='EN')
    
    # Add subchannel to channels
    channel3.subchannels.add(subchannel1)

    print('Channel-subchannel relationships saved...')

def populate_content_file_relationship():
    # Get content
    content1 = Content.objects.get(title='Content 1')

    # Create subchannel
    valid_file = SimpleUploadedFile('file.mp4', b'file_content', content_type='video/mp4')
    File.objects.create(content=content1, file=valid_file)

    print('Files created...')

def clean_data():
    # Delete all data to start from fresh
    Content.objects.all().delete()
    File.objects.all().delete()
    Group.objects.all().delete()
    Channel.objects.all().delete()

    print('DB data deleted...')


# # Clean any existing data first
# clean_data()

# # Write record into DB
# write_contents()
# write_groups()
# write_channels()

# # Populate relationships
# populate_channel_content_relationships()
# populate_content_file_relationship()
# populate_channel_group_relationships()
# populate_channel_subchannel_relationships()