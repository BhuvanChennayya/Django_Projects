
import subprocess
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management import CommandError

class Command(RunserverCommand):
    def add_arguments(self, parser):
        # Allow users to specify multiple ports in command-line arguments
        parser.add_argument(
            '--ports',
            type=str,
            help="Comma-separated list of ports to run the server on",
        )

    def handle(self, *args, **options):
        # Get the ports passed via command line or use default ports
        ports = options['ports'] if options['ports'] else "8000,8001,8002,8003,8443,8080,9000,9001,9002,9003,1024"
        ports = ports.split(',')

        # Run the Django development server on multiple ports
        for port in ports:
            try: 
                subprocess.Popen(
                    ['python', 'manage.py', 'runserver', f'0.0.0.0:{port}'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(f"Started server on port {port}")
            except Exception as e:
                raise CommandError(f"Error starting server on port {port}: {e}")
