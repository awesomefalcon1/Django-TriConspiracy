from django.contrib import admin
from .models import Event, Question, Prize, Placement


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'starts_at', 'location', 'created_at')
    search_fields = ('title', 'location')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('event', 'text', 'correct_choice', 'created_at')
    search_fields = ('text',)
    list_filter = ('event',)


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('event', 'rank', 'name', 'value')
    list_filter = ('event',)


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('event', 'rank', 'participant_name', 'score')
    list_filter = ('event',)

# Register your models here.
