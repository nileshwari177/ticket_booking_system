from django.urls import path
from .views import ShowListView, BookingCreateView, BookingHistoryView, register_view, login_view, logout_view

urlpatterns = [
    path('', ShowListView.as_view(), name='show-list'),
    path('book/', BookingCreateView.as_view(), name='book-ticket'),
    path('history/', BookingHistoryView.as_view(), name='booking-history'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
