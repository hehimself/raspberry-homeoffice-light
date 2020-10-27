"""Load configuration from .ini file."""
import configparser
import unittest

# Read local `config.ini` file.
config = configparser.ConfigParser()                                     
config.read('config.ini')

# Get values from our .ini file
# config.get('DATABASE', 'HOST')
# config['DATABASE']['HOST']


class TestStringMethods(unittest.TestCase):
    def config(self):
        MQTT_SERVER = config.get('MQTT','SERVER')
        # MQTT_PATH = config.get('MQTT','PATH')
        # MQTT_CLIENT_NAME = config.get('MQTT','CLIENT_NAME')
        # MQTT_CLIENT_USERNAME = config.get('MQTT','CLIENT_USERNAME')
        # MQTT_CLIENT_PW = config.get('MQTT','CLIENT_PASSWORD')
        # MQTT_PORT = config.get('MQTT','PORT')
        return MQTT_SERVER
    def test_config(self):
        self.assertEqual(self.config(), 'iobrokerpi')


if __name__ == '__main__':
    unittest.main()