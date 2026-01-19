"""
Prompt Template Unit - A single, reusable piece of prompt content.

A unit is the building block of Proteas. It holds content and knows how to render itself.
Units are independent and know nothing about other units.
"""

from dataclasses import dataclass, field
from string import Template


@dataclass
class PromptTemplateUnit:
    """
    A single, reusable piece of prompt content.

    Attributes:
        name: Identifier for this unit (for debugging and lookup)
        content: The actual prompt text (use $variable for placeholders)
        order: Optional position when combining (lower = earlier).
               If None, combiner uses insertion order.
        prefix: Optional header text added before content
        suffix: Optional footer text added after content
        enabled: Whether this unit should be included when rendering

    Placeholder syntax:
        Use $variable or ${variable} for placeholders in content.
        This allows JSON braces {} to be used without escaping.
        Example: content="Analyze: $messages" → render(messages="Hello")
    """

    name: str
    content: str = ""
    order: int | None = None
    prefix: str | None = None
    suffix: str | None = None
    enabled: bool = True

    def render(self, **kwargs) -> str:
        """
        Render this unit to a string.

        Args:
            **kwargs: Values to fill placeholders in content.
                      e.g., render(messages="...") fills $messages

        Returns:
            The combined prefix + content + suffix, or empty string if disabled.
        """
        if not self.enabled:
            return ""

        parts = []

        if self.prefix:
            parts.append(self.prefix)

        if self.content:
            if kwargs:
                # Use safe_substitute to leave unknown placeholders unchanged
                content = Template(self.content).safe_substitute(**kwargs)
            else:
                content = self.content
            parts.append(content)

        if self.suffix:
            parts.append(self.suffix)

        return "\n".join(parts)

    def enable(self) -> "PromptTemplateUnit":
        """Enable this unit. Returns self for chaining."""
        self.enabled = True
        return self

    def disable(self) -> "PromptTemplateUnit":
        """Disable this unit. Returns self for chaining."""
        self.enabled = False
        return self

    def with_content(self, content: str) -> "PromptTemplateUnit":
        """Return a copy with different content."""
        return PromptTemplateUnit(
            name=self.name,
            content=content,
            order=self.order,
            prefix=self.prefix,
            suffix=self.suffix,
            enabled=self.enabled,
        )

    def with_order(self, order: int | None) -> "PromptTemplateUnit":
        """Return a copy with different order."""
        return PromptTemplateUnit(
            name=self.name,
            content=self.content,
            order=order,
            prefix=self.prefix,
            suffix=self.suffix,
            enabled=self.enabled,
        )

    def __str__(self) -> str:
        status = "enabled" if self.enabled else "disabled"
        order_str = f"order={self.order}" if self.order is not None else "order=auto"
        return f"PromptTemplateUnit(name={self.name!r}, {order_str}, {status})"

    def __repr__(self) -> str:
        return self.__str__()
