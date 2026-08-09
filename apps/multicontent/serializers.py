from rest_framework import serializers
from .models import MultimediaAsset, NewsArticle, Content


class MultimediaListSerializer(serializers.ModelSerializer):

    content_type_display = serializers.CharField(
        source="get_content_type_display", read_only=True
    )

    class Meta:
        model = MultimediaAsset
        fields = ["id", "title", "content_type", "content_type_display", "created_at"]


class MultimediaDetailSerializer(serializers.ModelSerializer):

    content_type_display = serializers.CharField(
        source="get_content_type_display", read_only=True
    )

    class Meta:
        model = MultimediaAsset
        fields = ["id", "title", "content_type", "content_type_display", "file", "created_at"]


class NewsArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsArticle
        fields = ["id", "title", "body", "created_at"]


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ["id", "title", "body", "created_at"]