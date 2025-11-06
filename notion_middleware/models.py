from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    choice_a = models.CharField(max_length=200)
    choice_b = models.CharField(max_length=200)
    choice_c = models.CharField(max_length=200, blank=True)
    choice_d = models.CharField(max_length=200, blank=True)
    correct_choice = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        default='A',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.event.title} - {self.text[:40]}"


class Prize(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='prizes')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rank = models.PositiveIntegerField(help_text='1 for first place, 2 for second, etc.')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['rank']

    def __str__(self) -> str:
        return f"{self.event.title} - {self.rank}: {self.name}"


class Placement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='placements')
    participant_name = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    rank = models.PositiveIntegerField(help_text='Final standing for the participant')

    class Meta:
        ordering = ['rank']
        unique_together = ('event', 'rank')

    def __str__(self) -> str:
        return f"{self.event.title} - #{self.rank} {self.participant_name} ({self.score})"

# Create your models here.
