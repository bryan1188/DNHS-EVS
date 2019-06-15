from __future__ import unicode_literals
import csv
from django.core.management.base import BaseCommand
from registration.models import School

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

class Command(BaseCommand):
    help = (
        "Import School from a loval csv file."
        "Expects School_id, Name, Region, Division and Principal Name"
    )

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            "file_path",
            nargs=1,
            # type=unicode_literals,
        )

    def handle(self, *args, **options):
        verbosity = options.get("verbosity", NORMAL)
        file_path = options["file_path"][0]

        if verbosity >= NORMAL:
            self.stdout.write("=== School imported ===")

        with open(file_path) as f:
            reader =  csv.reader(f)
            for rownum, (school_id, name, region, division, principal_name) in enumerate(reader):
                if rownum == 0:
                    #skip the coloumn captions
                    continue
                school, created = School.objects.get_or_create(
                    school_id = school_id,
                    name = name,
                    region = region,
                    division = division,
                    principal_name = principal_name,
                )
                if verbosity >= NORMAL:
                    self.stdout.write("{}. {}".format(rownum, school.name))
