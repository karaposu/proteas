"""
Combination utilities for generating multiple Proteas instances.

Useful when you need to generate prompts for all possible combinations
of a set of units.
"""

from itertools import combinations
from typing import Iterator

from proteas.unit import PromptTemplateUnit
from proteas.proteas import Proteas


def generate_combinations(
    units: list[PromptTemplateUnit],
    min_size: int = 1,
    max_size: int | None = None,
    base_units: list[PromptTemplateUnit] | None = None,
    separator: str = "\n\n",
) -> Iterator[tuple[tuple[str, ...], Proteas]]:
    """
    Generate Proteas instances for all combinations of units.

    Args:
        units: List of units to combine
        min_size: Minimum number of units per combination (default: 1)
        max_size: Maximum number of units per combination (default: len(units))
        base_units: Optional units to include in ALL combinations (e.g., header, footer)
        separator: Separator for Proteas instances

    Yields:
        Tuples of (unit_names, proteas_instance) for each combination.
        unit_names is a tuple of the unit names in this combination.

    Example:
        units = [unit_a, unit_b, unit_c]
        for names, p in generate_combinations(units, min_size=2, max_size=2):
            print(names)  # ('a', 'b'), ('a', 'c'), ('b', 'c')
            prompt = p.compile()
    """
    if max_size is None:
        max_size = len(units)

    # Validate
    if min_size < 1:
        raise ValueError("min_size must be at least 1")
    if max_size > len(units):
        max_size = len(units)
    if min_size > max_size:
        raise ValueError("min_size cannot be greater than max_size")

    base_units = base_units or []

    # Generate combinations for each size
    for size in range(min_size, max_size + 1):
        for combo in combinations(units, size):
            # Create Proteas instance
            p = Proteas(separator=separator)

            # Add base units first
            for unit in base_units:
                p.add(unit)

            # Add combination units
            for unit in combo:
                p.add(unit)

            # Yield names and instance
            names = tuple(unit.name for unit in combo)
            yield names, p


def count_combinations(
    n: int,
    min_size: int = 1,
    max_size: int | None = None,
) -> int:
    """
    Count how many combinations will be generated.

    Args:
        n: Total number of units
        min_size: Minimum combination size
        max_size: Maximum combination size (default: n)

    Returns:
        Total number of combinations
    """
    from math import comb

    if max_size is None:
        max_size = n

    total = 0
    for size in range(min_size, max_size + 1):
        total += comb(n, size)
    return total
