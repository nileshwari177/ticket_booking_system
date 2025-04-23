from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Show, Booking
from django.contrib.auth.mixins import LoginRequiredMixin

class ShowListView(ListView):
    model = Show
    template_name = 'show_list.html'
    context_object_name = 'shows'

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

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_history.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

def register_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return redirect('show-list')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('show-list')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
