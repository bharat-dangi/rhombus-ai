"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

def main():
    """Run administrative tasks."""
    # Load environment variables from .env file
    load_dotenv()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Get the port from environment variable, defaulting to 8000 if not set
    port = os.getenv("DJANGO_PORT", "8000")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Pass the port to the runserver command if it's the default `runserver` call
    if len(sys.argv) == 1 or (len(sys.argv) >= 2 and sys.argv[1] == 'runserver'):
        sys.argv = [sys.argv[0], 'runserver', f'0.0.0.0:{port}']
        
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
