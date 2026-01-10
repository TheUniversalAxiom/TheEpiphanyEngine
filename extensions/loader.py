"""
Extension loading utilities.
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import List, Optional
from .base import BaseExtension
from .registry import get_registry


def load_extension(
    extension_class: type,
    *args,
    auto_register: bool = True,
    **kwargs
) -> BaseExtension:
    """
    Load an extension from a class.

    Args:
        extension_class: Extension class to instantiate
        *args: Positional arguments for extension constructor
        auto_register: Whether to automatically register with global registry
        **kwargs: Keyword arguments for extension constructor

    Returns:
        Instantiated extension

    Raises:
        TypeError: If extension_class is not a BaseExtension subclass
    """
    if not issubclass(extension_class, BaseExtension):
        raise TypeError(
            f"{extension_class} must be a subclass of BaseExtension"
        )

    extension = extension_class(*args, **kwargs)

    if auto_register:
        registry = get_registry()
        registry.register(extension)

    return extension


def load_extension_from_file(
    filepath: str,
    extension_name: str,
    auto_register: bool = True
) -> BaseExtension:
    """
    Load an extension from a Python file.

    Args:
        filepath: Path to Python file containing extension
        extension_name: Name of extension class in the file
        auto_register: Whether to automatically register

    Returns:
        Loaded extension instance

    Raises:
        ImportError: If file cannot be loaded
        AttributeError: If extension class not found in module
    """
    spec = importlib.util.spec_from_file_location("extension_module", filepath)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load extension from {filepath}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["extension_module"] = module
    spec.loader.exec_module(module)

    if not hasattr(module, extension_name):
        raise AttributeError(
            f"Extension class '{extension_name}' not found in {filepath}"
        )

    extension_class = getattr(module, extension_name)
    return load_extension(extension_class, auto_register=auto_register)


def load_extensions_from_directory(
    directory: str,
    pattern: str = "*_extension.py",
    auto_register: bool = True
) -> List[BaseExtension]:
    """
    Load all extensions from a directory.

    Looks for Python files matching the pattern and attempts to load
    extensions from them. By convention, each file should define an
    extension class with a name ending in "Extension".

    Args:
        directory: Directory path to search
        pattern: Glob pattern for extension files
        auto_register: Whether to automatically register

    Returns:
        List of loaded extension instances
    """
    directory_path = Path(directory)
    extension_files = directory_path.glob(pattern)

    loaded_extensions = []

    for filepath in extension_files:
        try:
            # Try to find extension class in module
            spec = importlib.util.spec_from_file_location(
                f"ext_{filepath.stem}", str(filepath)
            )
            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Look for classes that end with "Extension" and are BaseExtension subclasses
            for attr_name in dir(module):
                if not attr_name.endswith("Extension"):
                    continue

                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    issubclass(attr, BaseExtension) and
                    attr is not BaseExtension):

                    try:
                        extension = load_extension(
                            attr, auto_register=auto_register
                        )
                        loaded_extensions.append(extension)
                    except Exception as e:
                        print(f"Warning: Failed to load {attr_name} from "
                              f"{filepath}: {e}")

        except Exception as e:
            print(f"Warning: Failed to process {filepath}: {e}")

    return loaded_extensions


def discover_extensions(search_paths: Optional[List[str]] = None) -> List[str]:
    """
    Discover available extension files in search paths.

    Args:
        search_paths: List of directory paths to search
                     If None, uses ['./extensions', '~/.epiphany/extensions']

    Returns:
        List of discovered extension file paths
    """
    if search_paths is None:
        search_paths = [
            "./extensions",
            str(Path.home() / ".epiphany" / "extensions")
        ]

    discovered = []

    for search_path in search_paths:
        path = Path(search_path)
        if not path.exists():
            continue

        for ext_file in path.glob("*_extension.py"):
            discovered.append(str(ext_file))

    return discovered
