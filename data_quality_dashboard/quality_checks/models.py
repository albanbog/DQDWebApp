from django.db import models
from django.db.models import JSONField
 # If using PostgreSQL for dynamic fields


class ParticipantOverview(models.Model):
    participant_id = models.CharField(max_length=10, unique=True)  # Participant code like "p01", "p02"
    age = models.CharField(max_length=10, null=True, blank=True)  # Age of the participant
    height = models.CharField(max_length=10, null=True, blank=True)  # Height in cm
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)  # Gender
    ab_person = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')], null=True, blank=True)  # A or B person type    max_heart_rate = models.IntegerField(null=True, blank=True)  # Maximum heart rate
    max_heart_rate = models.CharField(max_length=10, null=True, blank=True)

    # 1st 5km run details
    run_5km_date = models.CharField(max_length=20, null=True, blank=True)  # Date of the first 5km run as a string
    run_5km_minutes = models.CharField(max_length=10, null=True, blank=True)  # Minutes for the 5km run
    run_5km_seconds = models.CharField(max_length=10, null=True, blank=True)  # Seconds for the 5km run
    
    # Stride length from Fitbit
    stride_walk = models.CharField(max_length=10, null=True, blank=True)  # Stride length for walking (cm), allow null values
    stride_run = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return f"Participant {self.participant_id}"




### Fitbit Models ###

class FitbitLightlyActiveMinutes(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # Date and time of the data
    value = models.IntegerField()  # Value representing the lightly active minutes
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} lightly active minutes"


class FitbitModeratelyActiveMinutes(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # Date and time of the data
    value = models.IntegerField()  # Value representing the moderately active minutes
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} moderately active minutes"


class FitbitRestingHeartRate(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # The datetime of the record
    value_date = models.DateField()  # Date of the heart rate record
    value = models.FloatField()  # The resting heart rate value
    error = models.FloatField(null=True, blank=True)  # The error in measurement
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} bpm (error: {self.error})"


class FitbitSedentaryMinutes(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # The datetime of the record
    value = models.IntegerField()  # The number of sedentary minutes
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} sedentary minutes"


class FitbitTimeInHeartRateZones(models.Model):
    participant = models.ForeignKey(ParticipantOverview, on_delete=models.CASCADE)
    dateTime = models.DateTimeField()
    below_default_zone_1 = models.FloatField()
    in_default_zone_1 = models.FloatField()
    in_default_zone_2 = models.FloatField()
    in_default_zone_3 = models.FloatField()

    def __str__(self):
        return f'{self.participant.participant_id} - {self.dateTime}'



class FitbitVeryActiveMinutes(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # The datetime of the record
    value = models.IntegerField()  # The number of very active minutes
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} very active minutes"


class FitbitSteps(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE, db_index=True)
    dateTime = models.DateTimeField(db_index=True)
    value = models.IntegerField()
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} steps"


class FitbitDistance(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # The datetime of the record
    value = models.FloatField()  # The distance value, likely in centimeters or meters
    
    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.value} distance"



### Start of the Fitbit/exercise.json data model.(Several models as it has nested structure) ###

# Represents the activity level (e.g., sedentary, lightly active, etc.)
class ActivityLevel(models.Model):
    name = models.CharField(max_length=20)  # Name of the activity level (sedentary, lightly, etc.)
    minutes = models.IntegerField()  # Number of minutes spent in this activity level
    exercise = models.ForeignKey('FitbitExercise', on_delete=models.CASCADE, related_name='activity_levels')
    
    def __str__(self):
        return f"{self.exercise.participant} - {self.name}: {self.minutes} minutes"


# Represents the heart rate zones (e.g., Out of Range, Fat Burn, etc.)
class HeartRateZone(models.Model):
    name = models.CharField(max_length=50)  # Name of the heart rate zone (e.g., Out of Range, Fat Burn)
    min = models.FloatField()  # Minimum heart rate for the zone
    max = models.FloatField()  # Maximum heart rate for the zone
    minutes = models.IntegerField()  # Minutes spent in this heart rate zone
    exercise = models.ForeignKey('FitbitExercise', on_delete=models.CASCADE, related_name='heart_rate_zones')
    
    def __str__(self):
        return f"{self.exercise.participant} - {self.name}: {self.minutes} minutes"


# Represents the source object (tracker information)
class ExerciseSource(models.Model):
    type = models.CharField(max_length=50)  # Type of source (e.g., tracker)
    name = models.CharField(max_length=50)  # Name of the tracker (e.g., Versa 2)
    tracker_id = models.CharField(max_length=50)  # Unique identifier for the tracker
    url = models.URLField()  # URL to the tracker webpage
    tracker_features = models.JSONField()  # List of features supported by the tracker
    exercise = models.ForeignKey('FitbitExercise', on_delete=models.CASCADE, related_name='source')
    
    def __str__(self):
        return f"{self.exercise.participant} - {self.name} ({self.type})"



# Define the default value function
def default_manual_values():
    return {"calories": False, "distance": False, "steps": False}

# Main FitbitExercise model
class FitbitExercise(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    logId = models.BigIntegerField(unique=True)  # Unique log ID for the exercise
    activityName = models.CharField(max_length=100)  # Name of the activity (Walk, Run, etc.)
    activityTypeId = models.IntegerField()  # ID of the activity type
    averageHeartRate = models.IntegerField()  # Average heart rate during the activity
    calories = models.IntegerField()  # Total calories burned during the activity
    duration = models.BigIntegerField()  # Duration of the activity in milliseconds
    activeDuration = models.BigIntegerField()  # Active duration of the activity in milliseconds
    steps = models.IntegerField(null=True, blank=True)  # Number of steps during the activity (if applicable)
    logType = models.CharField(max_length=50)  # Log type (e.g., tracker, auto_detected)
    lastModified = models.DateTimeField()  # Timestamp of the last modification
    startTime = models.DateTimeField()  # Start time of the activity
    originalStartTime = models.DateTimeField()  # Original start time of the activity
    originalDuration = models.BigIntegerField()  # Original duration of the activity in milliseconds
    elevationGain = models.FloatField(null=True, blank=True)  # Elevation gained during the activity (meters)
    hasGps = models.BooleanField(default=False)  # Whether GPS was used during the activity
    shouldFetchDetails = models.BooleanField(default=False)  # Whether more details should be fetched
    distance = models.FloatField(null=True, blank=True)  # Distance covered during the activity
    distanceUnit = models.CharField(max_length=10, null=True, blank=True)  # Unit for distance (e.g., km, miles)
    speed = models.FloatField(null=True, blank=True)  # Speed during the activity (for running, treadmill)
    pace = models.FloatField(null=True, blank=True)  # Pace during the activity (for running)
    swimLengths = models.IntegerField(null=True, blank=True)  # Number of swim lengths (for swimming)
    poolLength = models.FloatField(null=True, blank=True)  # Pool length used during the activity (for swimming)
    poolLengthUnit = models.CharField(max_length=10, null=True, blank=True)  # Unit for pool length (e.g., meters)
    manualValuesSpecified = models.JSONField(default=default_manual_values)  # Use function for default
    tcxLink = models.URLField(null=True, blank=True)  # TCX link for exercise data
    vo2Max = models.FloatField(null=True, blank=True)  # VO2 Max value

    def __str__(self):
        return f"{self.participant} - {self.activityName} ({self.logId})"
# End of Fitbit/exercise.json data model    

class FitbitCalories(models.Model):
        participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
        dateTime = models.DateTimeField()  # The datetime of the record
        value = models.FloatField()  # The value representing the calories burned

        def __str__(self):
            return f"{self.participant} - {self.dateTime}: {self.value} calories"    



class FitbitHeartRate(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    dateTime = models.DateTimeField()  # The datetime of the heart rate record
    bpm = models.IntegerField()  # Beats per minute
    confidence = models.IntegerField()  # Confidence level of the heart rate reading

    def __str__(self):
        return f"{self.participant} - {self.dateTime}: {self.bpm} bpm (confidence: {self.confidence})"


### Start of the  fitbit/sleep.json data models ### 


class SleepLog(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant   
    logId = models.BigIntegerField(unique=True, db_index=True)  # Unique ID for the sleep log
    dateOfSleep = models.DateField()  # The date of the sleep
    startTime = models.DateTimeField()  # Sleep start time
    endTime = models.DateTimeField()  # Sleep end time
    duration = models.BigIntegerField()  # Total duration of the sleep in milliseconds
    minutesToFallAsleep = models.IntegerField()  # Minutes to fall asleep
    minutesAsleep = models.IntegerField()  # Total minutes asleep
    minutesAwake = models.IntegerField()  # Total minutes awake
    minutesAfterWakeup = models.IntegerField()  # Minutes after waking up
    timeInBed = models.IntegerField()  # Total time spent in bed
    efficiency = models.IntegerField()  # Sleep efficiency percentage
    sleep_type = models.CharField(max_length=10, choices=[('stages', 'Stages'), ('classic', 'Classic')])  # Type of sleep
    infoCode = models.IntegerField()  # Additional information code
    mainSleep = models.BooleanField()  # Indicates if this is the main sleep

    def __str__(self):
        return f"{self.participant.participant_id} - Sleep log {self.logId} for {self.dateOfSleep}"


class SleepLevelSummary(models.Model):
    sleep_log = models.OneToOneField(SleepLog, on_delete=models.CASCADE, related_name="summary")  # Link to SleepLog

    deep_count = models.IntegerField()  # Number of deep sleep periods
    deep_minutes = models.IntegerField()  # Total minutes spent in deep sleep
    deep_thirty_day_avg_minutes = models.IntegerField()  # 30-day average of deep sleep minutes

    wake_count = models.IntegerField()  # Number of wake periods
    wake_minutes = models.IntegerField()  # Total minutes spent awake
    wake_thirty_day_avg_minutes = models.IntegerField()  # 30-day average of wake minutes

    light_count = models.IntegerField()  # Number of light sleep periods
    light_minutes = models.IntegerField()  # Total minutes spent in light sleep
    light_thirty_day_avg_minutes = models.IntegerField()  # 30-day average of light sleep minutes

    rem_count = models.IntegerField()  # Number of REM sleep periods
    rem_minutes = models.IntegerField()  # Total minutes spent in REM sleep
    rem_thirty_day_avg_minutes = models.IntegerField()  # 30-day average of REM sleep minutes

    def __str__(self):
        return f"Participant {self.sleep_log.participant.participant_id} - Summary for Sleep Log ID {self.sleep_log.logId}"


class SleepLevelData(models.Model):
    sleep_log = models.ForeignKey(SleepLog, on_delete=models.CASCADE, related_name="levels_data")  # Link to SleepLog
    dateTime = models.DateTimeField()  # Timestamp of the sleep level
    level = models.CharField(max_length=10)  # Sleep level (e.g., wake, light, deep, rem)
    seconds = models.IntegerField()  # Duration in seconds for this level

    def __str__(self):
        return f"Participant {self.sleep_log.participant.participant_id} - Level {self.level} for Sleep Log ID {self.sleep_log.logId}"

class SleepShortData(models.Model):
    sleep_log = models.ForeignKey(SleepLog, on_delete=models.CASCADE, related_name="short_data")  # Link to SleepLog
    dateTime = models.DateTimeField()  # Timestamp of the sleep level
    level = models.CharField(max_length=10)  # Sleep level (e.g., wake, light, deep, rem)
    seconds = models.IntegerField()  # Duration in seconds for this short level

    def __str__(self):
        return f"Participant {self.sleep_log.participant.participant_id} - Short data {self.level} for Sleep Log ID {self.sleep_log.logId} at {self.dateTime}"


### End of fitbit/sleep.json data models ###


class FitbitSleepScore(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    timestamp = models.DateTimeField()  # The timestamp of the sleep score
    sleep_log_entry_id = models.BigIntegerField()  # Unique ID for the sleep log entry
    overall_score = models.IntegerField()  # The overall sleep score
    composition_score = models.IntegerField()  # Score for sleep composition
    revitalization_score = models.IntegerField()  # Score for revitalization
    duration_score = models.IntegerField()  # Score for the sleep duration
    deep_sleep_in_minutes = models.IntegerField()  # Duration of deep sleep in minutes
    resting_heart_rate = models.FloatField()  # Resting heart rate during sleep
    restlessness = models.FloatField()  # Measure of restlessness during sleep
    
    def __str__(self):
        return f"{self.participant} - {self.timestamp}: Overall Score {self.overall_score}"


### Pmsys Models ### 

class Injury(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    effective_time_frame = models.DateTimeField()  # The effective time frame of the injury
    injuries = models.JSONField()  # Stores injuries in JSON format
    
    def __str__(self):
        return f"Injury on {self.effective_time_frame} - {self.injuries}"
    

    
class SRPE(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    end_date_time = models.DateTimeField()  # The end time of the recorded activity
    activity_names = models.JSONField()  # List of activity names, stored as JSON
    perceived_exertion = models.IntegerField()  # Perceived exertion score
    duration_min = models.IntegerField()  # Duration in minutes of the activity
    
    def __str__(self):
        return f"SRPE for {self.participant.participant_id} on {self.end_date_time}"


class Wellness(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    effective_time_frame = models.DateTimeField()  # Timestamp for the wellness data
    fatigue = models.IntegerField()  # Fatigue level
    mood = models.IntegerField()  # Mood level
    readiness = models.IntegerField()  # Readiness level
    sleep_duration_h = models.FloatField()  # Sleep duration in hours
    sleep_quality = models.IntegerField()  # Sleep quality level
    soreness = models.IntegerField()  # Soreness level
    soreness_area = models.JSONField()  # Soreness areas (stored as a list of numeric codes)
    stress = models.IntegerField()  # Stress level

    def __str__(self):
        return f"Wellness data for {self.participant} on {self.effective_time_frame}"
    



class Reporting(models.Model):
    participant = models.ForeignKey('ParticipantOverview', on_delete=models.CASCADE)  # Link to participant
    date = models.CharField(max_length=255)  # Treat date as string for now
    timestamp = models.CharField(max_length=255)  # Treat timestamp as string for now
    meals = models.CharField(max_length=255)  # List of meals consumed (e.g., Breakfast, Dinner)
    weight = models.FloatField(null=True, blank=True)  # Participant's weight (kg)
    glasses_of_fluid = models.IntegerField()  # Number of glasses of fluid consumed
    alcohol_consumed = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])  # Whether alcohol was consumed

    def __str__(self):
        return f"Reporting for {self.participant} on {self.date}"


class FileMetadata(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    expected_records = models.IntegerField()
    expected_variables = models.JSONField()  # Stores the expected variables and their details
    constraints = models.JSONField(null=True, blank=True)  # Optional constraints like uniform_time_format

    def __str__(self):
        return self.file_name