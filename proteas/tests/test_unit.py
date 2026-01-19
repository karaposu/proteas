"""Tests for PromptTemplateUnit."""

import pytest
from proteas.unit import PromptTemplateUnit


class TestPromptTemplateUnitBasic:
    """Basic rendering tests."""

    def test_render_content_only(self):
        unit = PromptTemplateUnit(name="test", content="Hello world")
        assert unit.render() == "Hello world"

    def test_render_empty_content(self):
        unit = PromptTemplateUnit(name="test", content="")
        assert unit.render() == ""

    def test_render_with_prefix(self):
        unit = PromptTemplateUnit(
            name="test",
            content="Body text",
            prefix="=== HEADER ==="
        )
        assert unit.render() == "=== HEADER ===\nBody text"

    def test_render_with_suffix(self):
        unit = PromptTemplateUnit(
            name="test",
            content="Body text",
            suffix="--- END ---"
        )
        assert unit.render() == "Body text\n--- END ---"

    def test_render_with_prefix_and_suffix(self):
        unit = PromptTemplateUnit(
            name="test",
            content="Body text",
            prefix="=== START ===",
            suffix="=== END ==="
        )
        assert unit.render() == "=== START ===\nBody text\n=== END ==="


class TestPromptTemplateUnitEnabled:
    """Enable/disable tests."""

    def test_enabled_by_default(self):
        unit = PromptTemplateUnit(name="test", content="Hello")
        assert unit.enabled is True

    def test_disabled_returns_empty(self):
        unit = PromptTemplateUnit(name="test", content="Hello", enabled=False)
        assert unit.render() == ""

    def test_disable_method(self):
        unit = PromptTemplateUnit(name="test", content="Hello")
        unit.disable()
        assert unit.enabled is False
        assert unit.render() == ""

    def test_enable_method(self):
        unit = PromptTemplateUnit(name="test", content="Hello", enabled=False)
        unit.enable()
        assert unit.enabled is True
        assert unit.render() == "Hello"

    def test_enable_disable_chaining(self):
        unit = PromptTemplateUnit(name="test", content="Hello")
        result = unit.disable().enable()
        assert result is unit  # Returns self
        assert unit.enabled is True


class TestPromptTemplateUnitPlaceholders:
    """Placeholder/kwargs tests using $variable syntax."""

    def test_single_placeholder(self):
        unit = PromptTemplateUnit(
            name="test",
            content="Hello $name!"
        )
        assert unit.render(name="World") == "Hello World!"

    def test_multiple_placeholders(self):
        unit = PromptTemplateUnit(
            name="test",
            content="$greeting $name, welcome to $place!"
        )
        result = unit.render(greeting="Hello", name="Alice", place="Wonderland")
        assert result == "Hello Alice, welcome to Wonderland!"

    def test_no_placeholders_no_kwargs(self):
        unit = PromptTemplateUnit(name="test", content="Static content")
        assert unit.render() == "Static content"

    def test_placeholder_in_multiline(self):
        unit = PromptTemplateUnit(
            name="test",
            content="Messages:\n$messages\n\nEnd of messages."
        )
        result = unit.render(messages="msg1\nmsg2\nmsg3")
        assert result == "Messages:\nmsg1\nmsg2\nmsg3\n\nEnd of messages."

    def test_unused_kwargs_ignored(self):
        unit = PromptTemplateUnit(name="test", content="Hello $name!")
        # Extra kwargs should not cause error
        result = unit.render(name="World", unused="ignored")
        assert result == "Hello World!"

    def test_no_kwargs_leaves_placeholders_unfilled(self):
        """When no kwargs passed, placeholders remain as-is."""
        unit = PromptTemplateUnit(name="test", content="Hello $name!")
        assert unit.render() == "Hello $name!"

    def test_partial_kwargs_leaves_missing_unchanged(self):
        """When some kwargs passed but placeholder missing, it remains as-is (safe_substitute)."""
        unit = PromptTemplateUnit(name="test", content="Hello $name from $place!")
        result = unit.render(name="World")  # Missing 'place'
        assert result == "Hello World from $place!"

    def test_json_braces_not_affected(self):
        """JSON braces {} are NOT treated as placeholders."""
        unit = PromptTemplateUnit(
            name="test",
            content='{"key": "value", "data": $data}'
        )
        result = unit.render(data='"test"')
        assert result == '{"key": "value", "data": "test"}'

    def test_braced_placeholder_syntax(self):
        """${variable} syntax also works."""
        unit = PromptTemplateUnit(
            name="test",
            content="Hello ${name}!"
        )
        assert unit.render(name="World") == "Hello World!"


class TestPromptTemplateUnitCopy:
    """Immutable copy method tests."""

    def test_with_content(self):
        original = PromptTemplateUnit(
            name="test",
            content="Original",
            order=10,
            prefix="PRE"
        )
        copy = original.with_content("New content")

        assert copy.content == "New content"
        assert copy.name == "test"
        assert copy.order == 10
        assert copy.prefix == "PRE"
        # Original unchanged
        assert original.content == "Original"

    def test_with_order(self):
        original = PromptTemplateUnit(name="test", content="Hello", order=10)
        copy = original.with_order(99)

        assert copy.order == 99
        assert original.order == 10  # Original unchanged

    def test_with_order_none(self):
        original = PromptTemplateUnit(name="test", content="Hello", order=10)
        copy = original.with_order(None)

        assert copy.order is None


class TestPromptTemplateUnitStr:
    """String representation tests."""

    def test_str_enabled(self):
        unit = PromptTemplateUnit(name="myunit", content="...", order=5)
        assert "myunit" in str(unit)
        assert "order=5" in str(unit)
        assert "enabled" in str(unit)

    def test_str_disabled(self):
        unit = PromptTemplateUnit(name="myunit", content="...", enabled=False)
        assert "disabled" in str(unit)

    def test_str_order_auto(self):
        unit = PromptTemplateUnit(name="myunit", content="...")
        assert "order=auto" in str(unit)
