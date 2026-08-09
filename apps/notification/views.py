from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from ..core.response import success_response, failure_response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..core.pagination import CustomPagination
from rest_framework.response import Response
from django.template.context_processors import request
from django.contrib.auth.models import User


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination 

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Stats
        total_count = queryset.count()
        unread_count = queryset.filter(is_read=False).count()
        read_count = queryset.filter(is_read=True).count()

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            paginated_data = {"results": serializer.data}

        # Add stats to the paginated response
        paginated_data.update({
            "total_count": total_count,
            "unread_count": unread_count,
            "read_count": read_count
        })

        return Response(paginated_data)

    
class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        updated_count = Notification.objects.filter(
            user=user, is_read=False).update(is_read=True)
        return success_response(
            'Notifications marked as read successfully',
            {'updated_count': updated_count},
            status.HTTP_200_OK
        )
        

class DeleteNotificationView(APIView):
    def delete(self, request, pk):
        try:
            # Get the notification by primary key (pk)
            notification = Notification.objects.get(id=pk)

            # Check if the notification belongs to the logged-in user
            if notification.user == request.user:
                # Delete the notification
                notification.delete()
                return success_response("Notification deleted successfully", {}, 200)
            else:
                # Unauthorized user trying to delete the notification
                return failure_response("You are not authorized to delete this notification", {}, 403)

        except Notification.DoesNotExist:
            # Notification does not exist
            return failure_response("Notification not found", {}, 404)
        
        except Exception as e:
            # Catch any other exception and return a generic error
            return failure_response("Something went wrong", str(e), 500)
    
    

