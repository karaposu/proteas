"""
Proteas - Prompt Template Assembler.

Combines multiple PromptTemplateUnits into a single prompt.
"""

from proteas.unit import PromptTemplateUnit


class Proteas:
    """
    Combines multiple PromptTemplateUnits into a single prompt.

    Units are assembled in order:
    - Units with explicit order (int) are sorted by that value
    - Units with order=None use their insertion order

    Usage:
        prompt = (Proteas()
            .add(header_unit)
            .add(body_unit)
            .add(footer_unit)
            .compile())
    """

    def __init__(self, separator: str = "\n\n"):
        """
        Initialize the combiner.

        Args:
            separator: String to join units with (default: double newline)
        """
        self._units: list[tuple[int, PromptTemplateUnit]] = []
        self._insertion_counter: int = 0
        self.separator = separator

    def add(self, unit: PromptTemplateUnit) -> "Proteas":
        """
        Add a unit to the combiner.

        Args:
            unit: The PromptTemplateUnit to add

        Returns:
            Self for method chaining
        """
        self._units.append((self._insertion_counter, unit))
        self._insertion_counter += 1
        return self

    def add_many(self, units: list[PromptTemplateUnit]) -> "Proteas":
        """
        Add multiple units at once.

        Args:
            units: List of PromptTemplateUnits to add

        Returns:
            Self for method chaining
        """
        for unit in units:
            self.add(unit)
        return self

    def compile(self, **kwargs) -> str:
        """
        Assemble all enabled units into a single prompt.

        Units are sorted by:
        1. Explicit order (if set)
        2. Insertion order (if order is None)

        Args:
            **kwargs: Values to fill placeholders in unit content.
                      e.g., compile(messages="...") fills {messages} in any unit

        Returns:
            The combined prompt string
        """
        # Sort units: explicit order first, then insertion order for ties/None
        sorted_units = sorted(
            self._units,
            key=lambda x: (
                x[1].order if x[1].order is not None else float('inf'),
                x[0]  # insertion order as tiebreaker
            )
        )

        # Render enabled units
        rendered = []
        for _, unit in sorted_units:
            if unit.enabled:
                content = unit.render(**kwargs)
                if content:  # Skip empty renders
                    rendered.append(content)

        return self.separator.join(rendered)

    def get_unit(self, name: str) -> PromptTemplateUnit | None:
        """
        Get a unit by name.

        Args:
            name: The unit name to find

        Returns:
            The unit if found, None otherwise
        """
        for _, unit in self._units:
            if unit.name == name:
                return unit
        return None

    def remove(self, name: str) -> "Proteas":
        """
        Remove a unit by name.

        Args:
            name: The unit name to remove

        Returns:
            Self for method chaining
        """
        self._units = [(i, u) for i, u in self._units if u.name != name]
        return self

    def clear(self) -> "Proteas":
        """
        Remove all units.

        Returns:
            Self for method chaining
        """
        self._units = []
        self._insertion_counter = 0
        return self

    def enable(self, name: str) -> "Proteas":
        """
        Enable a unit by name.

        Args:
            name: The unit name to enable

        Returns:
            Self for method chaining
        """
        unit = self.get_unit(name)
        if unit:
            unit.enable()
        return self

    def disable(self, name: str) -> "Proteas":
        """
        Disable a unit by name.

        Args:
            name: The unit name to disable

        Returns:
            Self for method chaining
        """
        unit = self.get_unit(name)
        if unit:
            unit.disable()
        return self

    @property
    def units(self) -> list[PromptTemplateUnit]:
        """Get all units in insertion order."""
        return [unit for _, unit in self._units]

    @property
    def enabled_units(self) -> list[PromptTemplateUnit]:
        """Get all enabled units."""
        return [unit for _, unit in self._units if unit.enabled]

    def __len__(self) -> int:
        return len(self._units)

    def __str__(self) -> str:
        enabled = len(self.enabled_units)
        total = len(self._units)
        return f"Proteas({enabled}/{total} units enabled)"

    def __repr__(self) -> str:
        return self.__str__()
