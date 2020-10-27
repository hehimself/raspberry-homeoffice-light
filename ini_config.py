"""Load configuration from .ini file."""
import configparser


# Read local `config.ini` file.
config = configparser.ConfigParser()                                     
config.read('config.ini')

# Get values from our .ini file
config.get('DATABASE', 'HOST')
config['DATABASE']['HOST']