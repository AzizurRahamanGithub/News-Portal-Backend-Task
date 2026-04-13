import requests
from django.contrib.auth import get_user_model
from .models import Notification
from django.conf import settings
from django.db import router
from apps.auths.models import CustomUser

User = get_user_model()

def send_push_notification(device_token, title, message):
    """Send push notification using Firebase Cloud Messaging (FCM)."""
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        'Authorization': f"key={settings.FCM_SERVER_KEY}",
        'Content-Type': 'application/json',
    }
    data = {
        "to": device_token,
        "notification": {
            "title": title,
            "body": message,
            "sound": "default",
        },
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
        if response.status_code == 200:
            print(f"Push notification sent to {device_token}")
        else:
            print(f"Failed to send push notification: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending push notification to {device_token}: {e}")

def notify_users(title, message, user_ids=None, notify_via_push=False):
    """Create notifications for users and send push notifications if required."""
    if user_ids:
        users = User.objects.filter(id__in=user_ids)
    else:
        users = User.objects.filter(is3_active=True)
    
    for user in users:
        # Create notification record
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message
        )

        # If push notification is enabled and user has a push_token, send it
        if notify_via_push:
            profile = user.profile  # Assuming the user has a profile model with a push_token field
            if profile.push_token:  # Ensure user has a push token
                send_push_notification(profile.push_token, title, message)

        # Log or print the notification creation for debugging
        print(f"Notification sent to {user.username}: {message}")

def notify_admins(title, message):
    """Create a notification for all admins."""
    admin_users = User.objects.filter(role=CustomUser.role, is_active=True)
    for admin in admin_users:
        Notification.objects.create(
            user=admin,
            title=title,
            message=message
        )
    print(f"Notification sent to admins: {title} - {message}")

def notify_user(title, message, user):
    """Create a notification for a single user."""
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    print(f"Notification sent to {user.username}: {message}")
