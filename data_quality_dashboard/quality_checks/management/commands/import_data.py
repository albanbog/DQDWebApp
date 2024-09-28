from django.core.management.base import BaseCommand
from django.contrib import admin
import csv
import os
import json
from datetime import datetime
from django.db import transaction
from tqdm import tqdm 
from concurrent.futures import ProcessPoolExecutor
from django.utils import timezone
from django.utils.dateparse import parse_datetime 
from django.db import connection

from quality_checks.models import *  # Import the correct model



class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):
        # Path to the CSV file
        csv_file_path = 'C:/Users/bogda/OneDrive/Desktop/DQDWebApp/pmdata/participant-overview.csv'

        # Open and read the CSV file
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Import all data as strings
                    participant, created = ParticipantOverview.objects.get_or_create(
                        participant_id=row['participant_id'],
                        defaults={
                            'age': row['age'] if row['age'] != '' else None,
                            'height': row['height'] if row['height'] != '' else None,
                            'gender': row['gender'],
                            'ab_person': row['ab_person'],
                            'max_heart_rate': row['max_heart_rate'] if row['max_heart_rate'] != '' else None,
                            'run_5km_date': row['run_5km_date'] if row['run_5km_date'] != '' else None,
                            'run_5km_minutes': row['run_5km_minutes'] if row['run_5km_minutes'] != '' else None,
                            'run_5km_seconds': row['run_5km_seconds'] if row['run_5km_seconds'] != '' else None,
                            'stride_walk': row['stride_walk'] if row['stride_walk'] != '' else None,
                            'stride_run': row['stride_run'] if row['stride_run'] != '' else None,
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Participant {participant.participant_id} created'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Participant {participant.participant_id} already exists'))

                except Exception as e:
                    self.stderr.write(f"Error processing row for participant {row['participant_id']}: {e}")  
    


class Command(BaseCommand):
    help = 'Load Fitbit data for all participants'

    def handle(self, *args, **kwargs):
        # Define the base directory where the participant folders are located
        BASE_DIR = 'C:/Users/bogda/OneDrive/Desktop/DQDWebApp/pmdata'

        # Loop through each participant folder (p01 to p16)
        for participant in range(1, 17):
            # Construct participant ID like 'p01', 'p02', etc.
            participant_id = f'p{str(participant).zfill(2)}'
            participant_folder = os.path.join(BASE_DIR, participant_id)

            # Check if participant exists in the database
            try:
                # Fetch the participant object from the database
                participant_obj = ParticipantOverview.objects.get(participant_id=participant_id)
                self.stdout.write(self.style.SUCCESS(f'Processing data for {participant_id}'))
            except ParticipantOverview.DoesNotExist:
                # If the participant does not exist, print an error and skip this participant
                self.stdout.write(self.style.ERROR(f'Participant {participant_id} does not exist in the database. Skipping.'))
                continue  # Skip to the next participant if not found

            # Call the function to process lightly_active_minutes.json for the current participant
            self.import_lightly_active_minutes(participant_obj, participant_folder)
            
            # Import moderately_active_minutes.json
            self.import_moderately_active_minutes(participant_obj, participant_folder)

            # Import resting_heart_rate.json
            self.import_resting_heart_rate(participant_obj, participant_folder)

            # Import sedentary_minutes.json
            self.import_sedentary_minutes(participant_obj, participant_folder)

            # Import time_in_heart_rates_zone.json
            self.import_time_in_heart_rate_zones(participant_obj, participant_folder)

            # Import very_active_minutes.json
            self.import_very_active_minutes(participant_obj, participant_folder)

            # Import steps.json
            self.import_steps(participant_obj, participant_folder)

            # Import distance.json
            self.import_distance(participant_obj, participant_folder)

            # Import exercise.json
            self.import_exercise(participant_obj, participant_folder)

            # Import calories.json
            self.import_calories(participant_obj, participant_folder)

            # Import heart_rate.json
            self.import_heart_rate(participant_obj, participant_folder)

            # Import sleep.json
            self.import_sleep(participant_obj, participant_folder)

            # Import sleep score CSV file
            self.import_sleep_score(participant_obj, participant_folder)

            # Import injury.csv
            self.import_injury(participant_obj, participant_folder)

            # Import srpe.csv
            self.import_srpe(participant_obj, participant_folder)

            # Import wellness.csv
            self.import_wellness(participant_obj, participant_folder)

            # Import reporting.csv
            self.import_reporting(participant_obj, participant_folder)


            



    def import_lightly_active_minutes(self, participant_obj, participant_folder):
        
        file_path = os.path.join(participant_folder, 'Fitbit', 'lightly_active_minutes.json')

        if os.path.exists(file_path):
            # Open and load the JSON data
            with open(file_path) as json_file:
                data = json.load(json_file)  # Load the data from the JSON file
                
                # Iterate over each record in the JSON data
                for record in data:
                    # Create and save a new FitbitLightlyActiveMinutes object for each record
                    FitbitLightlyActiveMinutes.objects.create(
                        participant=participant_obj,  # Link to the participant object
                        dateTime=record['dateTime'],  # Use the 'dateTime' field from the JSON
                        value=record['value']  # Use the 'value' field for lightly active minutes
                    )
            
            # Success message after importing the file for the participant
            self.stdout.write(self.style.SUCCESS(f'Imported lightly active minutes for {participant_obj.participant_id}'))
        else:
            # If the file does not exist, print a warning and skip the file
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
    
    
    def import_moderately_active_minutes(self, participant_obj, participant_folder):
        # Path to moderately_active_minutes.json file
        file_path = os.path.join(participant_folder, 'Fitbit', 'moderately_active_minutes.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Iterate through the data and create FitbitModeratelyActiveMinutes instances
        for entry in data:
            FitbitModeratelyActiveMinutes.objects.create(
                participant=participant_obj,
                dateTime=entry['dateTime'],
                value=int(entry['value'])
            )

        self.stdout.write(self.style.SUCCESS(f'Imported moderately active minutes for {participant_obj.participant_id}'))


    def import_resting_heart_rate(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'resting_heart_rate.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as f:
            data = json.load(f)
            for entry in data:
                try:
                    value = entry['value']
                    heart_rate_value = value.get('value')  # Extract the heart rate value
                    error_value = value.get('error')  # Extract the error

                    # Create the FitbitRestingHeartRate record
                    FitbitRestingHeartRate.objects.create(
                        participant=participant_obj,
                        dateTime=entry['dateTime'],
                        value_date=entry['dateTime'][:10],  # Extract the date part
                        value=float(heart_rate_value),  # Use the heart rate value
                        error=float(error_value) if error_value is not None else None  # Use the error if present
                    )

                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Missing key {e} in entry: {entry}'))

        # Log one message per participant
        self.stdout.write(self.style.SUCCESS(f'Imported all resting heart rate data for {participant_obj.participant_id}'))


    def import_sedentary_minutes(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'sedentary_minutes.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as f:
            data = json.load(f)
            for entry in data:
                try:
                    # Create the FitbitSedentaryMinutes record
                    FitbitSedentaryMinutes.objects.create(
                        participant=participant_obj,
                        dateTime=entry['dateTime'],
                        value=int(entry['value'])  # Sedentary minutes should be an integer
                    )
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f'Missing key {e} in entry: {entry}'))

        # Log one message per participant
        self.stdout.write(self.style.SUCCESS(f'Imported sedentary minutes for {participant_obj.participant_id}'))



    def import_time_in_heart_rate_zones(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'time_in_heart_rate_zones.json')
        self.stdout.write(self.style.SUCCESS(f'Starting to import data from {file_path}'))

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        for entry in data:
            try:
                dateTime = entry['dateTime']
                FitbitTimeInHeartRateZones.objects.create(
                    participant=participant_obj,
                    dateTime=dateTime,
                    below_default_zone_1=entry['value']['valuesInZones'].get('BELOW_DEFAULT_ZONE_1', 0.0),
                    in_default_zone_1=entry['value']['valuesInZones'].get('IN_DEFAULT_ZONE_1', 0.0),
                    in_default_zone_2=entry['value']['valuesInZones'].get('IN_DEFAULT_ZONE_2', 0.0),
                    in_default_zone_3=entry['value']['valuesInZones'].get('IN_DEFAULT_ZONE_3', 0.0)
                )
                

            except ParticipantOverview.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Participant with ID {participant_id} does not exist'))
                continue
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing entry for {participant_id} on {dateTime}: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Imported time in heart rate zones for {participant_obj.participant_id}'))


    def import_very_active_minutes(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'very_active_minutes.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        very_active_minutes_records = []
        batch_size = 1000  # Define a batch size for bulk insertion

        # Wrap the bulk insert in a transaction
        with transaction.atomic():
            for entry in data:
                dateTime = entry['dateTime']
                value = int(entry['value'])

                very_active_minutes_records.append(
                    FitbitVeryActiveMinutes(
                        participant=participant_obj,
                        dateTime=dateTime,
                        value=value
                    )
                )

                if len(very_active_minutes_records) >= batch_size:
                    FitbitVeryActiveMinutes.objects.bulk_create(very_active_minutes_records)
                    very_active_minutes_records = []  # Clear the batch after insert

            if very_active_minutes_records:
                FitbitVeryActiveMinutes.objects.bulk_create(very_active_minutes_records)

        # Display a success message when all data for the participant is imported
        self.stdout.write(self.style.SUCCESS(f"Finished importing very active minutes for {participant_obj.participant_id}"))



    
    def import_steps(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'steps.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and load the JSON data
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        steps_entries = []  # List to store steps data for raw SQL
        BATCH_SIZE = 5000  # Adjust batch size depending on your system's resources

        for entry in data:
            try:
                # Prepare raw data to insert using SQL directly
                date_time = entry['dateTime']
                value = int(entry['value'])

                # Append the entry as a raw SQL string
                steps_entries.append(f"({participant_obj.id}, '{date_time}', {value})")

                # If batch size is reached, bulk insert the data
                if len(steps_entries) >= BATCH_SIZE:
                    self.bulk_insert_steps(steps_entries)
                    steps_entries = []  # Clear the list after batch insertion

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing entry for {participant_obj.participant_id}: {e}"))

        # Insert any remaining entries
        if steps_entries:
            self.bulk_insert_steps(steps_entries)

        # Log a message when all steps data for a participant has been imported
        self.stdout.write(self.style.SUCCESS(f'Imported steps data for {participant_obj.participant_id}'))


    def bulk_insert_steps(self, steps_entries):
        """
        This helper function inserts steps data using raw SQL for faster performance.
        """
        if steps_entries:
            # Formulate the raw SQL insert statement
            insert_statement = """
            INSERT INTO quality_checks_fitbitsteps (participant_id, dateTime, value)
            VALUES {}
            """.format(",".join(steps_entries))

            # Execute the SQL statement
            with connection.cursor() as cursor:
                cursor.execute(insert_statement)



    def import_distance(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'distance.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and load the JSON data
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        distance_entries = []  # List to store distance data for raw SQL
        BATCH_SIZE = 5000  # Adjust the batch size depending on your system's resources

        for entry in data:
            try:
                # Prepare raw data to insert using SQL directly
                date_time = entry['dateTime']
                value = float(entry['value'])

                # Append the entry as a raw SQL string
                distance_entries.append(f"({participant_obj.id}, '{date_time}', {value})")

                # If batch size is reached, bulk insert the data
                if len(distance_entries) >= BATCH_SIZE:
                    self.bulk_insert_distance(distance_entries)
                    distance_entries = []  # Clear the list after batch insertion

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing entry for {participant_obj.participant_id}: {e}"))

        # Insert any remaining entries
        if distance_entries:
            self.bulk_insert_distance(distance_entries)

        # Log a message when all distance data for a participant has been imported
        self.stdout.write(self.style.SUCCESS(f'Imported distance data for {participant_obj.participant_id}'))


    def bulk_insert_distance(self, distance_entries):
        """
        This helper function inserts distance data using raw SQL for faster performance.
        """
        if distance_entries:
            # Formulate the raw SQL insert statement
            insert_statement = """
            INSERT INTO quality_checks_fitbitdistance (participant_id, dateTime, value)
            VALUES {}
            """.format(",".join(distance_entries))

            # Execute the SQL statement
            with connection.cursor() as cursor:
                cursor.execute(insert_statement)




    
    
    def import_exercise(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'exercise.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Loop through the data and insert records
        for entry in data:
            try:
                # Check if an exercise with this logId already exists for the participant
                if not FitbitExercise.objects.filter(logId=entry['logId']).exists():
                    # Create the FitbitExercise object if it doesn't exist
                    exercise = FitbitExercise.objects.create(
                        participant=participant_obj,
                        logId=entry['logId'],
                        activityName=entry['activityName'],
                        activityTypeId=entry['activityTypeId'],
                        averageHeartRate=entry['averageHeartRate'],
                        calories=entry['calories'],
                        duration=entry['duration'],
                        activeDuration=entry['activeDuration'],
                        steps=entry.get('steps', None),
                        logType=entry['logType'],
                        lastModified=parse_datetime(entry['lastModified']),
                        startTime=parse_datetime(entry['startTime']),
                        originalStartTime=parse_datetime(entry['originalStartTime']),
                        originalDuration=entry['originalDuration'],
                        elevationGain=entry.get('elevationGain', None),
                        hasGps=entry['hasGps'],
                        shouldFetchDetails=entry['shouldFetchDetails'],
                        distance=entry.get('distance', None),
                        distanceUnit=entry.get('distanceUnit', None),
                        speed=entry.get('speed', None),
                        pace=entry.get('pace', None),
                        swimLengths=entry.get('swimLengths', None),
                        poolLength=entry.get('poolLength', None),
                        poolLengthUnit=entry.get('poolLengthUnit', None)
                    )

                    # Now create related ActivityLevel and HeartRateZone objects
                    for level in entry['activityLevel']:
                        ActivityLevel.objects.create(
                            name=level['name'],
                            minutes=level['minutes'],
                            exercise=exercise
                        )

                    for zone in entry['heartRateZones']:
                        HeartRateZone.objects.create(
                            name=zone['name'],
                            min=zone['min'],
                            max=zone['max'],
                            minutes=zone['minutes'],
                            exercise=exercise
                        )

                    # Create the source object
                    source = entry['source']
                    ExerciseSource.objects.create(
                        type=source['type'],
                        name=source['name'],
                        tracker_id=source['id'],
                        url=source['url'],
                        tracker_features=source['trackerFeatures'],
                        exercise=exercise
                    )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing entry for {participant_obj.participant_id}: {e}"))

        # Log success message after the participant's exercise data has been imported
        self.stdout.write(self.style.SUCCESS(f'Imported exercise data for {participant_obj.participant_id}'))



    def import_calories(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'calories.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and load the JSON data
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        calories_entries = []  # List to store calorie data for raw SQL
        BATCH_SIZE = 5000  # Adjust the batch size depending on system resources

        for entry in data:
            try:
                # Prepare raw data to insert using SQL directly
                date_time = entry['dateTime']
                value = float(entry['value'])

                # Append the entry as a raw SQL string
                calories_entries.append(f"({participant_obj.id}, '{date_time}', {value})")

                # If batch size is reached, bulk insert the data
                if len(calories_entries) >= BATCH_SIZE:
                    self.bulk_insert_calories(calories_entries)
                    calories_entries = []  # Clear the list after batch insertion

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing entry for {participant_obj.participant_id}: {e}"))

        # Insert any remaining entries
        if calories_entries:
            self.bulk_insert_calories(calories_entries)

        # Log a message when all calories data for a participant has been imported
        self.stdout.write(self.style.SUCCESS(f'Imported calories data for {participant_obj.participant_id}'))


    def bulk_insert_calories(self, calories_entries):
        """
        This helper function inserts calorie data using raw SQL for faster performance.
        """
        if calories_entries:
            # Formulate the raw SQL insert statement
            insert_statement = """
            INSERT INTO quality_checks_fitbitcalories (participant_id, dateTime, value)
            VALUES {}
            """.format(",".join(calories_entries))

            # Execute the SQL statement
            with connection.cursor() as cursor:
                cursor.execute(insert_statement)
    


    def import_heart_rate(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'heart_rate.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        heart_rate_entries = []  # List to store FitbitHeartRate data for raw SQL
        BATCH_SIZE = 5000  # Adjust batch size depending on your machine resources

        for entry in data:
            try:
                # No need to parse the dateTime if it's already in a format Django can handle
                date_time = entry['dateTime']
                bpm = entry['value']['bpm']
                confidence = entry['value']['confidence']

                # Prepare raw data to insert using SQL directly
                heart_rate_entries.append(f"({participant_obj.id}, '{date_time}', {bpm}, {confidence})")

                # Bulk insert entries using raw SQL
                if len(heart_rate_entries) >= BATCH_SIZE:
                    self.bulk_insert_heart_rate(heart_rate_entries)
                    heart_rate_entries = []  # Clear the list after batch insertion

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing entry for {participant_obj.participant_id}: {e}"))

        # Insert the remaining entries if any
        if heart_rate_entries:
            self.bulk_insert_heart_rate(heart_rate_entries)

        # Log success message after the participant's heart rate data has been imported
        self.stdout.write(self.style.SUCCESS(f'Imported heart rate data for {participant_obj.participant_id}'))


    def bulk_insert_heart_rate(self, heart_rate_entries):
        """
        This helper function inserts heart rate data using raw SQL for faster performance.
        """
        if heart_rate_entries:
            # Formulate the raw SQL insert statement
            insert_statement = """
            INSERT INTO quality_checks_fitbitheartrate (participant_id, dateTime, bpm, confidence)
            VALUES {}
            """.format(",".join(heart_rate_entries))

            # Execute the SQL statement
            with connection.cursor() as cursor:
                cursor.execute(insert_statement)




    

    def import_sleep(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'Fitbit', 'sleep.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Load the JSON data
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Batch lists for bulk insertion
        sleep_log_entries = []
        sleep_summary_entries = []
        sleep_level_data_entries = []
        sleep_short_data_entries = []
        BATCH_SIZE = 5000

        for entry in data:
            try:
                # Create or get the sleep log entry
                sleep_log, created = SleepLog.objects.get_or_create(
                    participant=participant_obj,
                    logId=entry['logId'],
                    defaults={
                        'dateOfSleep': entry['dateOfSleep'],
                        'startTime': entry['startTime'],
                        'endTime': entry['endTime'],
                        'duration': entry['duration'],
                        'minutesToFallAsleep': entry['minutesToFallAsleep'],
                        'minutesAsleep': entry['minutesAsleep'],
                        'minutesAwake': entry['minutesAwake'],
                        'minutesAfterWakeup': entry['minutesAfterWakeup'],
                        'timeInBed': entry['timeInBed'],
                        'efficiency': entry['efficiency'],
                        'sleep_type': entry['type'],
                        'infoCode': entry['infoCode'],
                        'mainSleep': entry['mainSleep']
                    }
                )

                # Process sleep level summary if present
                if 'summary' in entry['levels']:
                    summary = entry['levels']['summary']
                    SleepLevelSummary.objects.create(
                        sleep_log=sleep_log,
                        deep_count=summary.get('deep', {}).get('count', 0),  # Handle missing 'deep' key
                        deep_minutes=summary.get('deep', {}).get('minutes', 0),  # Handle missing 'deep' key
                        deep_thirty_day_avg_minutes=summary.get('deep', {}).get('thirtyDayAvgMinutes', 0),  # Handle missing key
                        wake_count=summary.get('wake', {}).get('count', 0),
                        wake_minutes=summary.get('wake', {}).get('minutes', 0),
                        wake_thirty_day_avg_minutes=summary.get('wake', {}).get('thirtyDayAvgMinutes', 0),
                        light_count=summary.get('light', {}).get('count', 0),
                        light_minutes=summary.get('light', {}).get('minutes', 0),
                        light_thirty_day_avg_minutes=summary.get('light', {}).get('thirtyDayAvgMinutes', 0),
                        rem_count=summary.get('rem', {}).get('count', 0),
                        rem_minutes=summary.get('rem', {}).get('minutes', 0),
                        rem_thirty_day_avg_minutes=summary.get('rem', {}).get('thirtyDayAvgMinutes', 0)
                    )

                # Process sleep level data
                for level_data in entry['levels']['data']:
                    sleep_level_data_entries.append(SleepLevelData(
                        sleep_log=sleep_log,
                        dateTime=level_data['dateTime'],
                        level=level_data['level'],
                        seconds=level_data['seconds']
                    ))

                # Process short sleep data if present
                if 'shortData' in entry['levels']:
                    for short_data in entry['levels']['shortData']:
                        sleep_short_data_entries.append(SleepShortData(
                            sleep_log=sleep_log,
                            dateTime=short_data['dateTime'],
                            level=short_data['level'],
                            seconds=short_data['seconds']
                        ))

                # Bulk insertion if batch size is reached
                if len(sleep_level_data_entries) >= BATCH_SIZE:
                    SleepLevelData.objects.bulk_create(sleep_level_data_entries)
                    sleep_level_data_entries = []

                if len(sleep_short_data_entries) >= BATCH_SIZE:
                    SleepShortData.objects.bulk_create(sleep_short_data_entries)
                    sleep_short_data_entries = []

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing sleep log for {participant_obj.participant_id}: {e}"))

        # Insert remaining entries after loop
        if sleep_level_data_entries:
            SleepLevelData.objects.bulk_create(sleep_level_data_entries)

        if sleep_short_data_entries:
            SleepShortData.objects.bulk_create(sleep_short_data_entries)

        self.stdout.write(self.style.SUCCESS(f'Imported sleep data for {participant_obj.participant_id}'))


     

    def import_sleep_score(self, participant_obj, participant_folder):
        # Path to the sleep_score.csv file
        file_path = os.path.join(participant_folder, 'Fitbit', 'sleep_score.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and read the CSV file
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            sleep_score_entries = []

            # Process each row in the CSV file
            for row in reader:
                try:
                    sleep_score_entries.append(
                        FitbitSleepScore(
                            participant=participant_obj,
                            timestamp=parse_datetime(row['timestamp']),
                            sleep_log_entry_id=int(row['sleep_log_entry_id']),
                            overall_score=int(row['overall_score']),
                            composition_score=int(row['composition_score']),
                            revitalization_score=int(row['revitalization_score']),
                            duration_score=int(row['duration_score']),
                            deep_sleep_in_minutes=int(row['deep_sleep_in_minutes']),
                            resting_heart_rate=float(row['resting_heart_rate']),
                            restlessness=float(row['restlessness']),
                        )
                    )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing sleep score entry for {participant_obj.participant_id}: {e}"))

            # Bulk create entries for improved performance
            if sleep_score_entries:
                FitbitSleepScore.objects.bulk_create(sleep_score_entries, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f'Imported sleep score data for {participant_obj.participant_id}'))



    ### Importing data from the pmsys folder
    def import_injury(self, participant_obj, participant_folder):
        # Path to the injury.csv file
        file_path = os.path.join(participant_folder, 'pmsys', 'injury.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and read the CSV file
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            injury_entries = []

            # Process each row in the CSV file
            for row in reader:
                try:
                    injury_entries.append(
                        Injury(
                            participant=participant_obj,
                            effective_time_frame=parse_datetime(row['effective_time_frame']),
                            injuries=json.loads(row['injuries'])  # Assuming injuries are stored as JSON strings in the CSV
                        )
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing injury entry for {participant_obj.participant_id}: {e}"))

            # Bulk create entries for improved performance
            if injury_entries:
                Injury.objects.bulk_create(injury_entries, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f'Imported injury data for {participant_obj.participant_id}'))
    


    def import_srpe(self, participant_obj, participant_folder):
        # Path to the srpe.csv file
        file_path = os.path.join(participant_folder, 'pmsys', 'srpe.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and read the CSV file
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            srpe_entries = []

            # Process each row in the CSV file
            for row in reader:
                try:
                    # Handle Python-style lists by replacing single quotes with double quotes for JSON parsing
                    activity_names_str = row['activity_names'].replace("'", '"')  # Replace single quotes with double quotes
                    activity_names = json.loads(activity_names_str) if activity_names_str else []  # Parse into a JSON object

                    # Ensure that the parsed data is valid
                    if not isinstance(activity_names, list):
                        activity_names = []

                    srpe_entries.append(
                        SRPE(
                            participant=participant_obj,
                            end_date_time=parse_datetime(row['end_date_time']),
                            activity_names=activity_names,  # Use parsed activity_names
                            perceived_exertion=int(row['perceived_exertion']),
                            duration_min=int(row['duration_min'])
                        )
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing SRPE entry for {participant_obj.participant_id}: {e}"))

            # Bulk create entries for improved performance
            if srpe_entries:
                SRPE.objects.bulk_create(srpe_entries, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f'Imported SRPE data for {participant_obj.participant_id}'))



    def import_wellness(self, participant_obj, participant_folder):
        file_path = os.path.join(participant_folder, 'pmsys', 'wellness.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        # Open and read the CSV file
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                try:
                    # Create and save a Wellness record
                    Wellness.objects.create(
                        participant=participant_obj,
                        effective_time_frame=row['effective_time_frame'],
                        fatigue=int(row['fatigue']),
                        mood=int(row['mood']),
                        readiness=int(row['readiness']),
                        sleep_duration_h=float(row['sleep_duration_h']),  # Use the correct column name
                        sleep_quality=int(row['sleep_quality']),
                        soreness=int(row['soreness']),
                        soreness_area=json.loads(row['soreness_area']),  # Parse the JSON field
                        stress=int(row['stress'])
                    )
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f"Error processing wellness entry for {participant_obj.participant_id}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Unexpected error for {participant_obj.participant_id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Imported wellness data for {participant_obj.participant_id}'))

    
    def import_reporting(self, participant_obj, participant_folder):
        # Path to reporting.csv file in googledocs folder
        file_path = os.path.join(participant_folder, 'googledocs', 'reporting.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'Skipping missing file: {file_path}'))
            return

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Treat date and timestamp as strings for now
                    date_str = row['date']
                    timestamp_str = row['timestamp']

                    # Handle weight field, allow empty values
                    weight = row['weight']
                    if weight == '' or weight is None:
                        weight = None
                    else:
                        weight = float(weight)

                    # Create a Reporting instance for each row in the CSV
                    Reporting.objects.create(
                        participant=participant_obj,
                        date=date_str,  # Store as string
                        timestamp=timestamp_str,  # Store as string
                        meals=row['meals'],
                        weight=weight,
                        glasses_of_fluid=row['glasses_of_fluid'],
                        alcohol_consumed=row['alcohol_consumed']
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing reporting entry for {participant_obj.participant_id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Imported reporting data for {participant_obj.participant_id}'))






