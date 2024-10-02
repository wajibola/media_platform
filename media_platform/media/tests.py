from django.test import TestCase
from .models import Channel, Content
from rest_framework.test import APIClient

from .write_to_db import *

class MediaPlatformTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Write record into DB
        write_contents()
        write_groups()
        write_channels()

        # Populate relationships
        populate_channel_content_relationships()
        populate_content_file_relationship()
        populate_channel_group_relationships()
        populate_channel_subchannel_relationships()

    def setUp(self):
        self.client = APIClient()

    @classmethod
    def tearDownClass(cls):
        # Clean any existing data first
        clean_data()
        
    def test_get_contents(self):
        """
        Test Get contents
        """
        response = self.client.get('/api/contents/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_groups(self):
        """
        Test Get gropus
        """
        response = self.client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_channels(self):
        """
        Test Get channels
        """
        response = self.client.get('/api/channels/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_filter_channels_by_group(self):
        """
        Test filtering channels by group
        """
        response = self.client.get('/api/channels/?groups__name=Group%201')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Channel 1')

    
    def test_channel_rating(self):
        """
        Test the correct calculation of the channel rating
        """
        # Get related channels
        channel1 = Channel.objects.get(title='Channel 1')
        channel2 = Channel.objects.get(title='Channel 2')
        channel3 = Channel.objects.get(title='Channel 3')

        self.assertEqual(channel1.avg_rating(), 8.0)
        self.assertEqual(channel2.avg_rating(), 8.5)
        self.assertIsNone(channel3.avg_rating())

    def test_get_channel_subchannel(self):
        """ 
        Test subchannels
        """
        response = self.client.get('/api/channels/')
        self.assertEqual(response.status_code, 200)

        # Check the response for Channel 3
        channel3_data = next(channel for channel in response.data if channel['title'] == 'Channel 3')
        self.assertEqual(len(channel3_data['subchannels']), 1)
        self.assertEqual(channel3_data['subchannels'][0]['title'], 'Subchannel 1')

    def test_valid_rating(self):
        """
        Test valid content rating
        """
        content = Content(title='Content 4', metadata={'description': 'description content 4'}, rating=8.5)
        # Call clean() method
        content.full_clean()
        content.save()
        self.assertEqual(content.rating, 8.5)

    def test_invalid_rating_below_zero(self):
        """
        Test exception raised when content rating value is below 0
        """
        content = Content(title='Invalid Content', metadata={'description': 'invalid content description'}, rating=-1.0)
        with self.assertRaises(ValidationError):
            content.full_clean()

    def test_invalid_rating_above_ten(self):
        """
        Test exception raised when content rating value is above 10
        """
        content = Content(title='Invalid Content', metadata={'description': 'invalid content description'}, rating=11.0)
        with self.assertRaises(ValidationError):
            content.full_clean()

    def test_valid_file_extension(self):
        """
        Test file extension is valid
        """
        # Get content
        content2 = Content.objects.get(title='Content 2')

        valid_file = SimpleUploadedFile('attachment.pdf', b'file_content', content_type='application/pdf')
        file_instance = File.objects.create(content=content2, file=valid_file)

        self.assertEqual(file_instance.file.name.split('.')[-1], 'pdf')

    def test_invalid_file_extension(self):
        """
        Test file extension is invalid
        """
        # Get content
        content2 = Content.objects.get(title='Content 2')

        invalid_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type='image/jpeg')
        file_instance = File.objects.create(content=content2, file=invalid_file)
        with self.assertRaises(ValidationError):
            file_instance.full_clean()
