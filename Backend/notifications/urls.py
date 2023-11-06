from django.urls import path
from .views import NotificationListView, MarkNotificationAsReadView, create_notification, mark_notification_as_read

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/mark-as-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('notifications/create-notification/', create_notification, name='create-notification'),
    path('notifications/mark-notification-as-read/<int:pk>/', mark_notification_as_read,
         name='mark-notification-as-read'),
]
