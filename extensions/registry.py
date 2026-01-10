"""
Extension registry for managing loaded extensions.
"""

from typing import Dict, List, Optional, Type

from .base import BaseExtension


class ExtensionRegistry:
    """
    Global registry for managing extensions.

    Provides registration, lookup, and lifecycle management for
    all loaded extensions.
    """

    def __init__(self):
        """Initialize empty registry."""
        self._extensions: Dict[str, BaseExtension] = {}
        self._extensions_by_type: Dict[str, List[BaseExtension]] = {}

    def register(self, extension: BaseExtension) -> None:
        """
        Register an extension.

        Args:
            extension: Extension instance to register

        Raises:
            ValueError: If extension with same name already registered
        """
        if extension.name in self._extensions:
            raise ValueError(
                f"Extension '{extension.name}' is already registered. "
                f"Use unregister() first if you want to replace it."
            )

        # Register by name
        self._extensions[extension.name] = extension

        # Register by type
        extension_type = type(extension).__name__
        if extension_type not in self._extensions_by_type:
            self._extensions_by_type[extension_type] = []
        self._extensions_by_type[extension_type].append(extension)

        # Initialize the extension
        extension.initialize()

    def unregister(self, name: str) -> None:
        """
        Unregister an extension by name.

        Args:
            name: Extension name

        Raises:
            KeyError: If extension not found
        """
        if name not in self._extensions:
            raise KeyError(f"Extension '{name}' not found in registry")

        extension = self._extensions[name]
        extension_type = type(extension).__name__

        # Remove from type registry
        if extension_type in self._extensions_by_type:
            self._extensions_by_type[extension_type].remove(extension)
            if not self._extensions_by_type[extension_type]:
                del self._extensions_by_type[extension_type]

        # Remove from main registry
        del self._extensions[name]

    def get(self, name: str) -> Optional[BaseExtension]:
        """
        Get extension by name.

        Args:
            name: Extension name

        Returns:
            Extension instance or None if not found
        """
        return self._extensions.get(name)

    def get_by_type(self, extension_type: Type[BaseExtension]) -> List[BaseExtension]:
        """
        Get all extensions of a specific type.

        Args:
            extension_type: Extension class type

        Returns:
            List of matching extensions
        """
        type_name = extension_type.__name__
        return self._extensions_by_type.get(type_name, [])

    def list_all(self) -> List[BaseExtension]:
        """
        List all registered extensions.

        Returns:
            List of all extension instances
        """
        return list(self._extensions.values())

    def list_enabled(self) -> List[BaseExtension]:
        """
        List all enabled extensions.

        Returns:
            List of enabled extension instances
        """
        return [ext for ext in self._extensions.values() if ext.enabled]

    def enable(self, name: str) -> None:
        """
        Enable an extension.

        Args:
            name: Extension name

        Raises:
            KeyError: If extension not found
        """
        if name not in self._extensions:
            raise KeyError(f"Extension '{name}' not found")
        self._extensions[name].enable()

    def disable(self, name: str) -> None:
        """
        Disable an extension.

        Args:
            name: Extension name

        Raises:
            KeyError: If extension not found
        """
        if name not in self._extensions:
            raise KeyError(f"Extension '{name}' not found")
        self._extensions[name].disable()

    def clear(self) -> None:
        """Unregister all extensions."""
        self._extensions.clear()
        self._extensions_by_type.clear()

    def get_metadata_all(self) -> Dict[str, Dict]:
        """
        Get metadata for all registered extensions.

        Returns:
            Dict mapping extension names to their metadata
        """
        return {
            name: ext.get_metadata()
            for name, ext in self._extensions.items()
        }


# Global registry instance
_global_registry: Optional[ExtensionRegistry] = None


def get_registry() -> ExtensionRegistry:
    """
    Get the global extension registry.

    Returns:
        Global ExtensionRegistry instance
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = ExtensionRegistry()
    return _global_registry


def reset_registry() -> None:
    """
    Reset the global registry (useful for testing).
    """
    global _global_registry
    _global_registry = None
