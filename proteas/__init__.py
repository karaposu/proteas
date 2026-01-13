"""
Proteas - Prompt Template Assembler.

A domain-agnostic library for composing prompts from reusable units.
"""

from proteas.unit import PromptTemplateUnit
from proteas.proteas import Proteas
from proteas.combinations import generate_combinations, count_combinations

__all__ = [
    "PromptTemplateUnit",
    "Proteas",
    "generate_combinations",
    "count_combinations",
]
