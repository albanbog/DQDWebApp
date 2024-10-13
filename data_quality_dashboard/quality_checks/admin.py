from django.contrib import admin
from .models import *  # Import your models

# Register your models here
admin.site.register(ParticipantOverview)
admin.site.register(FitbitLightlyActiveMinutes)
admin.site.register(FitbitModeratelyActiveMinutes)
admin.site.register(FitbitRestingHeartRate)
admin.site.register(FitbitSedentaryMinutes)
admin.site.register(FitbitTimeInHeartRateZones)
admin.site.register(FitbitVeryActiveMinutes)
admin.site.register(FitbitSteps)
admin.site.register(FitbitDistance)
# Inline admin for ActivityLevel
class ActivityLevelInline(admin.TabularInline):
    model = ActivityLevel
    extra = 1  # This allows adding an additional row by default
    readonly_fields = ['name', 'minutes']  # If you want these fields to be read-only

# Inline admin for HeartRateZone
class HeartRateZoneInline(admin.TabularInline):
    model = HeartRateZone
    extra = 1
    readonly_fields = ['name', 'min', 'max', 'minutes']

# Inline admin for ExerciseSource
class ExerciseSourceInline(admin.StackedInline):  # You could also use TabularInline if you prefer
    model = ExerciseSource
    extra = 1
    readonly_fields = ['type', 'name', 'tracker_id', 'url', 'tracker_features']

# Admin for FitbitExercise
class FitbitExerciseAdmin(admin.ModelAdmin):
    list_display = ('participant', 'activityName', 'logId', 'startTime', 'duration')
    inlines = [ActivityLevelInline, HeartRateZoneInline, ExerciseSourceInline]  # Attach inlines to the main admin

# Register the main and related models
admin.site.register(FitbitExercise, FitbitExerciseAdmin)
admin.site.register(ActivityLevel)
admin.site.register(HeartRateZone)
admin.site.register(ExerciseSource)
admin.site.register(FitbitCalories)
admin.site.register(FitbitHeartRate)
admin.site.register(SleepLog)
admin.site.register(SleepLevelSummary)
admin.site.register(SleepLevelData)
admin.site.register(SleepShortData)
admin.site.register(FitbitSleepScore)
admin.site.register(Injury)



class SRPEAdmin(admin.ModelAdmin):
   list_display = ('participant', 'end_date_time', 'perceived_exertion', 'duration_min', 'display_activity_names')

   def display_activity_names(self, obj):
        return ', '.join(obj.activity_names) if obj.activity_names else "No activities"
   display_activity_names.short_description = 'Activity Names'

admin.site.register(SRPE, SRPEAdmin)  

class WellnessAdmin(admin.ModelAdmin):
    list_display = ('participant', 'effective_time_frame', 'fatigue', 'mood', 'readiness', 'sleep_duration_h', 'sleep_quality', 'soreness', 'stress')
    search_fields = ('participant__participant_id', 'effective_time_frame')
    list_filter = ('participant', 'effective_time_frame')

admin.site.register(Wellness, WellnessAdmin)

admin.site.register(Reporting)


@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'expected_records')
    search_fields = ('file_name',)