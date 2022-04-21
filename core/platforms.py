from pathlib import Path
import platform
import json


class UnknownPlatformError(Exception):
    pass


class Platform:
    @property
    def _name(self) -> str:
        ...

    @property
    def _match_names(self) -> tuple:
        ...

    @property
    def _locations_key(self) -> str:
        ...

    def get_bindings_path(self, config_dir: Path) -> Path:
        with open(config_dir / "locations.json", "r") as _file:
            data: dict = json.loads(_file.read())
            return Path(data.get(self._locations_key))

    def __eq__(self, other: str) -> bool:
        for match in self._match_names:
            if match in other.lower():
                return True
        return False

    def __str__(self):
        return self._name


class LinuxPlatform(Platform):
    _name = "Linux"
    _locations_key = "linux"
    _match_names = (
        "linux",
        "posix",
    )


class MacPlatform(Platform):
    _name = "MacOS"
    _locations_key = "mac"
    _match_names = (
        "mac",
        "darwin",
    )


class WindowsPlatform(Platform):
    _name = "Windows"
    _locations_key = "windows"
    _match_names = ("windows",)


def get_platform() -> Platform:
    platform_system = platform.system()

    if platform_system == LinuxPlatform():
        return LinuxPlatform()
    elif platform_system == WindowsPlatform():
        return WindowsPlatform()
    elif platform_system == MacPlatform():
        return MacPlatform()
    else:
        raise UnknownPlatformError(
            f"Unable to parse {platform_system} to known platform."
        )
