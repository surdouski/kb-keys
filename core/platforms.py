from abc import ABC, abstractproperty

from attrs import define
from enum import Enum
from pathlib import Path
import platform
import json


class UnknownPlatformError(Exception):
    pass


class Platform(ABC):
    @abstractproperty
    def name(self) -> str:
        ...

    @abstractproperty
    def locations_key(self) -> str:
        ...

    @abstractproperty
    def match_names(self) -> tuple:
        ...

    @classmethod
    def get_bindings_path(cls, config_dir: Path) -> Path:
        with open(config_dir / "locations.json", "r") as _file:
            data: dict = json.loads(_file.read())
            return Path(data.get(cls.locations_key))

    @classmethod
    def equals(cls, value: str) -> bool:
        for match in cls.match_names:
            if match in value.lower():
                return True
        return False


Platform.register(Enum)


class LinuxPlatform(Platform):
    name = "Linux"
    locations_key = "linux"
    match_names = (
        "linux",
        "posix",
    )


class MacPlatform(Platform):
    name = "MacOS"
    locations_key = "mac"
    match_names = (
        "mac",
        "darwin",
    )


class WindowsPlatform(Platform):
    name = "Windows"
    locations_key = "windows"
    match_names = ("windows",)


def get_platform() -> Platform:
    platform_system = platform.system().lower()
    match platform_system:
        case (x) if x in LinuxPlatform.match_names:
            return LinuxPlatform
        case (x) if x in WindowsPlatform.match_names:
            return WindowsPlatform
        case (x) if x in MacPlatform.match_names:
            return MacPlatform
        case _:
            raise UnknownPlatformError("Unable to parse platform.")


print(get_platform().name)
