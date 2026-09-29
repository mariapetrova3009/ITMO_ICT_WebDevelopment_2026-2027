from django.shortcuts import get_object_or_404, redirect, render
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation, Review, Room, Stay
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, ReviewForm


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:

        form = UserCreationForm()

    return render(
        request,
        'project_first_app/register.html',
        {'form': form}

    )

def room_list(request):
    rooms = Room.objects.all()

    return render(
        request,
        'project_first_app/room_list.html',
        {'rooms': rooms}
    )


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    return render(
        request,
        'project_first_app/room_detail.html',
        {'room': room}
    )

@login_required
def create_reservation(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)

            reservation.user = request.user
            reservation.room = room

            reservation.save()

            return redirect('my_reservations')

    else:
        form = ReservationForm()

    return render(
        request,
        'project_first_app/reservation_form.html',
        {
            'form': form,
            'room': room
        }
    )
@login_required
def my_reservations(request):
    reservations = request.user.reservations.all()

    return render(
        request,
        'project_first_app/my_reservations.html',
        {'reservations': reservations}
    )

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    if request.method == 'POST':
        form = ReservationForm(
            request.POST,
            instance=reservation
        )

        if form.is_valid():
            form.save()
            return redirect('my_reservations')

    else:
        form = ReservationForm(instance=reservation)

    return render(
        request,
        'project_first_app/reservation_form.html',
        {
            'form': form,
            'room': reservation.room,
            'is_edit': True,
        }
    )


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')

    return render(
        request,
        'project_first_app/reservation_confirm_delete.html',
        {'reservation': reservation}
    )

@login_required
def create_review(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)

            review.user = request.user
            review.room = room

            review.save()

            return redirect('room_detail', room_id=room.id)

    else:
        form = ReviewForm()

    return render(
        request,
        'project_first_app/review_form.html',
        {
            'form': form,
            'room': room,
        }
    )

@login_required
def recent_guests(request):
    if not request.user.is_staff:
        return redirect('room_list')

    month_ago = timezone.now() - timedelta(days=30)

    stays = Stay.objects.filter(
        check_in__gte=month_ago
    ).select_related(
        'user',
        'room',
        'room__hotel'
    ).order_by('-check_in')

    return render(
        request,
        'project_first_app/recent_guests.html',
        {'stays': stays}
    )