"""
Extension and plugin system for The EPIPHANY Engine.

This module provides infrastructure for extending the engine with:
- Custom update rules
- Domain-specific intelligence models
- Custom event handlers
- Integration adapters
"""

from .base import BaseExtension, EventHandlerExtension, IntegrationExtension, UpdateRuleExtension
from .loader import load_extension, load_extensions_from_directory
from .registry import ExtensionRegistry, get_registry

__all__ = [
    'BaseExtension',
    'UpdateRuleExtension',
    'EventHandlerExtension',
    'IntegrationExtension',
    'ExtensionRegistry',
    'get_registry',
    'load_extension',
    'load_extensions_from_directory'
]
