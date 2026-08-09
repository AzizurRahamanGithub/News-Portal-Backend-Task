from django.urls import path
from .views import NotificationListView, MarkAllNotificationsReadView, DeleteNotificationView

urlpatterns = [
    path("list/", NotificationListView.as_view(), name="notifications"),
    path("mark-all-read/", MarkAllNotificationsReadView.as_view(), name="mark-all-read"),
    path('delete_notification/<int:pk>/', DeleteNotificationView.as_view(), name='delete_notification'),
]
