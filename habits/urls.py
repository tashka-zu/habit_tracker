from django.urls import path
from .views import (
    HabitListCreateView,
    HabitRetrieveUpdateDestroyView,
    PublicHabitListView,
)

urlpatterns = [
    path("habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    path(
        "habits/<int:pk>/",
        HabitRetrieveUpdateDestroyView.as_view(),
        name="habit-retrieve-update-destroy",
    ),
    path("public/", PublicHabitListView.as_view(), name="public-habits"),
    path("", HabitListCreateView.as_view(), name="habit-list"),
]
