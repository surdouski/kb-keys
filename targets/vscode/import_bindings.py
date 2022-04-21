from pathlib import Path
from core.platforms import get_platform


platform = get_platform()

location = platform.get_bindings_path(Path(__file__).parent)

print(location)
