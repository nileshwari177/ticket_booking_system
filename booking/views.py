from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Show, Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Show List View
class ShowListView(ListView):
    model = Show
    template_name = 'show_list.html'
    context_object_name = 'shows'

# Booking Create View
class BookingCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'book_ticket.html'

    def post(self, request):
        show_id = request.POST.get('show_id')
        seats = int(request.POST.get('seats'))
        show = Show.objects.get(id=show_id)
        if show.available_seats >= seats:
            show.available_seats -= seats
            show.save()
            Booking.objects.create(user=request.user, show=show, seats_booked=seats)
            return redirect('booking-history')
        return render(request, self.template_name, {'error': 'Not enough seats'})

# Booking History View
class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_history.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# Register View
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('show-list')

# Login View
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('show-list')
        return render(request, self.template_name, {'error': 'Invalid credentials'})

# Logout View
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect after logout
