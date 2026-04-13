from django.urls import path
from .views import (
    MultimediaListView,
    MultimediaDetailView,
    NewsArticleListView,
    ContentListView,
)

urlpatterns = [
    path("multimedia/", MultimediaListView.as_view(), name="multimedia-list"),
    path("multimedia/<int:pk>/", MultimediaDetailView.as_view(), name="multimedia-detail"),
    path("articles/", NewsArticleListView.as_view(), name="article-list"),
    path("content/", ContentListView.as_view(), name="content-list"),
]