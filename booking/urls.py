from django.urls import path
from .views import ShowListView, BookingCreateView, BookingHistoryView, RegisterView, LoginView, CustomLogoutView

urlpatterns = [
    path('show-list/', ShowListView.as_view(), name='show-list'),
    path('book-ticket/', BookingCreateView.as_view(), name='book-ticket'),
    path('booking-history/', BookingHistoryView.as_view(), name='booking-history'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
