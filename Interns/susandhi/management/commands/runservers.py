import subprocess
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management import CommandError

class Command(RunserverCommand):
    def add_arguments(self, parser):
        # Allow users to specify multiple ports for both projects
        parser.add_argument(
            '--project1-ports',
            type=str,
            help="Comma-separated list of ports for Project 1 (e.g. '8000,8001')",
            default="8000,8001"  # Default ports for Project 1
        )
        parser.add_argument(
            '--project2-ports',
            type=str,
            help="Comma-separated list of ports for Project 2 (e.g. '9000,9001')",
            default="9000,9001"  # Default ports for Project 2
        )
        parser.add_argument(
            'Bhuvan_django_project/Docketrun/',
            type=str,
            help="Path to Project 1's directory",
            required=True
        )
        parser.add_argument(
            'Interns/susandhi/',
            type=str,
            help="Path to Project 2's directory",
            required=True
        )

    def handle(self, *args, **options):
        # Get the ports for both projects
        project1_ports = options['project1_ports'].split(',')
        project2_ports = options['project2_ports'].split(',')

        project1_path = options['project1_path']
        project2_path = options['project2_path']

        # Run Project 1 on multiple ports
        for port in project1_ports:
            try:
                print(f"Starting Project 1 on port {port}...")
                subprocess.Popen(
                    ['python', 'manage.py', 'runserver', f'0.0.0.0:{port}'],
                    cwd=project1_path,  # Specify the directory for Project 1
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f"Started Project 1 on port {port}")
            except Exception as e:
                raise CommandError(f"Error starting Project 1 on port {port}: {e}")

        # Run Project 2 on multiple ports
        for port in project2_ports:
            try:
                print(f"Starting Project 2 on port {port}...")
                subprocess.Popen(
                    ['python', 'manage.py', 'runserver', f'0.0.0.0:{port}'],
                    cwd=project2_path,  # Specify the directory for Project 2
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f"Started Project 2 on port {port}")
            except Exception as e:
                raise CommandError(f"Error starting Project 2 on port {port}: {e}")
