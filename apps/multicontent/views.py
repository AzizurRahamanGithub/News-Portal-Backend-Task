from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache

from apps.core.response import success_response, failure_response
from .models import MultimediaAsset, NewsArticle, Content
from .serializers import (
    MultimediaListSerializer,
    MultimediaDetailSerializer,
    NewsArticleSerializer,
    ContentSerializer,
)

CACHE_TTL = 60 * 30  # 30m


class MultimediaListView(APIView):

    def get(self, request):
        cached = cache.get("multimedia_list")
        if cached:
            return success_response(
                message="Multimedia list fetched successfully",
                data=cached,
            )

        assets = list(MultimediaAsset.objects.only("id", "title", "content_type", "created_at"))

        if not assets:
            return failure_response(
                message="No multimedia found",
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MultimediaListSerializer(assets, many=True)
        cache.set("multimedia_list", serializer.data, timeout=CACHE_TTL)

        return success_response(
            message="Multimedia list fetched successfully",
            data=serializer.data,
        )


class MultimediaDetailView(APIView):

    def get(self, request, pk):
        cache_key = f"multimedia_detail_{pk}"
        cached = cache.get(cache_key)
        if cached:
            return success_response(
                message="Multimedia fetched successfully",
                data=cached,
            )

        try:
            asset = MultimediaAsset.objects.only(
                "id", "title", "content_type", "file", "created_at"
            ).get(pk=pk)
        except MultimediaAsset.DoesNotExist:
            return failure_response(
                message="Multimedia not found",
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MultimediaDetailSerializer(asset)
        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)

        return success_response(
            message="Multimedia fetched successfully",
            data=serializer.data,
        )
        

class NewsArticleListView(APIView):

    def get(self, request):
        cached = cache.get("article_list")
        if cached:
            return success_response(
                message="Articles fetched successfully",
                data=cached,
            )

        articles = list(NewsArticle.objects.filter(status="published").only(
            "id", "title", "body", "created_at"
        ))

        if not articles:
            return failure_response(
                message="No articles found",
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = NewsArticleSerializer(articles, many=True)
        cache.set("article_list", serializer.data, timeout=CACHE_TTL)

        return success_response(
            message="Articles fetched successfully",
            data=serializer.data,
        )


class ContentListView(APIView):

    def get(self, request):
        cached = cache.get("content_list")
        if cached:
            return success_response(
                message="Content fetched successfully",
                data=cached,
            )

        contents = list(Content.objects.only(
            "id", "title", "body", "created_at"
        ))

        if not contents:
            return failure_response(
                message="No content found",
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ContentSerializer(contents, many=True)
        cache.set("content_list", serializer.data, timeout=CACHE_TTL)

        return success_response(
            message="Content fetched successfully",
            data=serializer.data,
        )