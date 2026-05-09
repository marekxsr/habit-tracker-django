from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils import timezone

from .forms import RegisterForm, HabitForm
from .models import Habit, HabitCompletion


def home(request):
    if request.user.is_authenticated:
        habits = Habit.objects.filter(user=request.user)
    else:
        habits = Habit.objects.none()

    today = timezone.localdate()

    start_of_week = today - timedelta(days=today.weekday())

    week_days = []

    for i in range(7):
        day = start_of_week + timedelta(days=i)

        week_days.append({
            "date": day,
            "name": day.strftime("%a"),
            "is_today": day == today
        })

    total_habits = habits.count()
    total_week_tasks = total_habits * 7

    if request.user.is_authenticated:
        completed_week = HabitCompletion.objects.filter(
            habit__user=request.user,
            date__gte=start_of_week,
            date__lte=start_of_week + timedelta(days=6)
        ).count()
    else:
        completed_week = 0

    best_streak = 0

    for habit in habits:
        if habit.streak > best_streak:
            best_streak = habit.streak

    if total_week_tasks > 0:
        completion_rate = round((completed_week / total_week_tasks) * 100)
    else:
        completion_rate = 0

    activity_days = []

    for i in range(31):
        try:
            day = today.replace(day=i + 1)
        except ValueError:
            break

        if request.user.is_authenticated:
            is_completed = HabitCompletion.objects.filter(
                habit__user=request.user,
                date=day
            ).exists()
        else:
            is_completed = False

        activity_days.append({
            "date": day,
            "day_number": i + 1,
            "completed": is_completed,
            "is_today": day == today,
        })

    form = HabitForm()

    return render(request, "index.html", {
        "habits": habits,
        "form": form,
        "week_days": week_days,
        "activity_days": activity_days,
        "total_habits": total_habits,
        "completed_today": completed_week,
        "best_streak": best_streak,
        "completion_rate": completion_rate,
        "total_week_tasks": total_week_tasks,
    })


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })


def add_habit(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = HabitForm(request.POST)

        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()

    return redirect("home")


def delete_habit(request, habit_id):
    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user
    )

    if request.method == "POST":
        habit.delete()

    return redirect("home")


def toggle_habit(request, habit_id, date):
    habit = get_object_or_404(
        Habit,
        id=habit_id,
        user=request.user
    )

    selected_date = timezone.datetime.strptime(date, "%Y-%m-%d").date()

    completion = HabitCompletion.objects.filter(
        habit=habit,
        date=selected_date
    ).first()

    if completion:
        completion.delete()

        if habit.streak > 0:
            habit.streak -= 1

        if selected_date == timezone.localdate():
            habit.completed_today = False

    else:
        HabitCompletion.objects.create(
            habit=habit,
            date=selected_date
        )

        habit.streak += 1

        if selected_date == timezone.localdate():
            habit.completed_today = True
            habit.last_completed_date = selected_date

    habit.save()

    return redirect("home")