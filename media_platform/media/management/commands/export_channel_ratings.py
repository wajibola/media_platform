import csv

from django.core.management.base import BaseCommand
from media.models import Channel

class Command(BaseCommand):
    help = 'Calculate the ratings of every channel and export them in a csv file sorted by rating (i.e. the highest rated channels on top)'

    def handle(self, *args, **kwargs):
        channel_data = []
        channels = Channel.objects.all()
        for channel in channels:
            # Append a tuple of (channel title, average rating) to the list
            channel_data.append((channel.title, channel.avg_rating()))

        # Sort the channel data by average rating in descending order
        sorted_channel_data = sorted(
            [item for item in channel_data if item[1] is not None], 
            key=lambda x: x[1], 
            reverse=True
        )

        with open('channel_ratings.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['channel_title', 'average_rating'])
            for channel in sorted_channel_data:
                writer.writerow(channel)

        self.stdout.write(self.style.SUCCESS('Successfully calculated and exported channel ratings to channel_ratings.csv'))
