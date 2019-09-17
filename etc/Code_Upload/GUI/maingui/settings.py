from PySide2.QtCore import QSettings
from loguru import logger
from pathlib import Path
from attr import attrs, attrib

ORGANISATION = "UCD_Project"
APPLICATION = "RF_Tool"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@attrs
class ServerLoginDetails(metaclass=Singleton):
    server = attrib(default="")
    username = attrib(default="")
    password = attrib(default="")


@attrs
class Report:

    technician = attrib(default=None)
    date = attrib(default=None)
    location = attrib(default=None)
    report_id = attrib(default=0)
    details = attrib(default=None)
    photos = attrib(default=None)
    signoff = attrib(default="")

    def generate(self):
        pass


class AppSettings:

    def __init__(self):
        logger.info("Init Settings")
        self._settings = QSettings(ORGANISATION, APPLICATION)
        self._settings_file = Path(self._settings.fileName())

    def write_server_settings(self, serversettings: ServerLoginDetails):
        logger.info("Write Server Settings")
        self._settings.beginGroup("Server")
        self._settings.setValue("server", serversettings.server)
        self._settings.setValue("username", serversettings.username)
        self._settings.endGroup()

    def read_server_settings(self):
        logger.info("Read Settings")
        self._settings.beginGroup("Server")
        server = self._settings.value("server", "")
        username = self._settings.value("username", "")
        logger.info("server: " + server)
        logger.info("username: " + username)
        self._settings.endGroup()
        serversettings = ServerLoginDetails()
        serversettings.server=server
        serversettings.username=username
        return serversettings

    @property
    def config_path(self):
        settings_dir = self._settings_file.parent
        return str(settings_dir)
