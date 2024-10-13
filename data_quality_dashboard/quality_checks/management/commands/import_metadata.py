# quality_checks/management/commands/import_metadata.py

import json
import os
from django.core.management.base import BaseCommand
from quality_checks.models import FileMetadata

class Command(BaseCommand):
    help = 'Import metadata from JSON file into the database'

    def handle(self, *args, **kwargs):
        metadata_file_path = 'quality_checks/data_quality_metadata.json'

        # Check if the file exists
        if not os.path.exists(metadata_file_path):
            self.stdout.write(self.style.ERROR(f'Metadata file not found at {metadata_file_path}'))
            return

        # Load and read the JSON data
        with open(metadata_file_path, 'r') as json_file:
            metadata_list = json.load(json_file)  # Load the list of metadata entries

        # Iterate through the metadata entries and save each as a separate record
        for entry in metadata_list:
            file_name = entry.get('file_name')
            expected_records = entry.get('expected_records', 0)  # Default to 0 if missing
            expected_variables = entry.get('expected_variables', {})
            constraints = entry.get('constraints', {})

            # Create or update the metadata record for each file
            FileMetadata.objects.update_or_create(
                file_name=file_name,
                defaults={
                    'expected_records': expected_records,
                    'expected_variables': expected_variables,
                    'constraints': constraints,
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported metadata into the database.'))
