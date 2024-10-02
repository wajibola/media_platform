
from rest_framework import serializers
from .models import Channel, Content, File, Group

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'files', 'metadata', 'rating']

    def create(self, validated_data):
        # files_data = validated_data.get('files', [])
        files_data = validated_data.pop('files', [])
        content = Content.objects.create(**validated_data)

        for file_data in files_data:
            # File.objects.create(content=content, **file_data)
            content.files.add(file_data)
        return content
    
    def update(self, instance, validated_data):
        files_data = validated_data.pop('files', [])
        
        # Update content instance
        instance.title = validated_data.get('title', instance.title)
        instance.metadata = validated_data.get('metadata', instance.metadata)
        instance.save()

        # Update files
        for file_data in files_data:
            File.objects.update_or_create(content=instance, **file_data)

class ChannelSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, required=False)
    subchannels = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'title', 'language', 'picture', 'contents', 'subchannels', 'groups']

    # def create(self, validated_data):
    #     pass

    # def update(self, instance, validated_data):
    #     pass

    def get_subchannels(self, obj):
        subchannels = obj.subchannels.all()
        return ChannelSerializer(subchannels, many=True).data
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']