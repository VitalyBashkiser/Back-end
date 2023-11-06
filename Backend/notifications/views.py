from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class MarkNotificationAsReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_update(self, serializer):
        serializer.instance.mark_as_read()


@api_view(['POST'])
def create_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mark_notification_as_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification does not exist'}, status=status.HTTP_404_NOT_FOUND)

    notification.mark_as_read()
    return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)