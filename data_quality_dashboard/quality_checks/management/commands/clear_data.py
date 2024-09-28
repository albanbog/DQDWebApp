from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = 'Batch deletes large tables like FitbitCalories, FitbitSteps, FitbitDistance, and FitbitHeartRate for SQLite using DELETE, and deletes smaller tables incrementally.'

    def handle(self, *args, **kwargs):
        confirm = input("Are you sure you want to delete data from large tables and other records? (yes/no): ")

        if confirm.lower() == 'yes':
            # List of large tables to delete in batches (Calories, Steps, Distance, and HeartRate)
            large_tables = [
                'quality_checks_fitbitcalories',
                'quality_checks_fitbitsteps',
                'quality_checks_fitbitdistance',
                'quality_checks_fitbitheartrate'
            ]

            with connection.cursor() as cursor:
                for table in large_tables:
                    self.stdout.write(f"Deleting from {table} in batches...")

                    # Batch delete for large tables
                    batch_size = 40000000  # Adjust batch size as necessary
                    while True:
                        cursor.execute(f'DELETE FROM "{table}" WHERE rowid IN (SELECT rowid FROM "{table}" LIMIT {batch_size})')
                        deleted_rows = cursor.rowcount

                        if deleted_rows == 0:
                            break  # Stop when no more rows are deleted
                        
                        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_rows} rows from {table}..."))

            # Handle deletion for the remaining models (smaller datasets) using Django ORM
            app_models = apps.get_app_config('quality_checks').get_models()

            for model in app_models:
                if model.__name__ == 'ParticipantOverview':
                    continue  # Skip the ParticipantOverview model

                table_name = model._meta.db_table
                if table_name in large_tables:
                    continue  # Skip the already processed large tables

                self.stdout.write(f"Processing {model.__name__}...")

                try:
                    # Get the primary keys of the first 3000 records
                    pks = model.objects.values_list('pk', flat=True)[:8000000]

                    # Perform batched deletion by primary keys
                    model.objects.filter(pk__in=pks).delete()

                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted {len(pks)} records from {model.__name__}.'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing {model.__name__}: {e}"))

            self.stdout.write(self.style.SUCCESS('Successfully deleted records from all models.'))
        else:
            self.stdout.write(self.style.WARNING('Operation cancelled.'))
