"""Tests for Proteas combiner."""

import pytest
from proteas.unit import PromptTemplateUnit
from proteas.proteas import Proteas


class TestProteasBasic:
    """Basic combiner tests."""

    def test_empty_compile(self):
        p = Proteas()
        assert p.compile() == ""

    def test_single_unit(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="Hello"))
        assert p.compile() == "Hello"

    def test_multiple_units_insertion_order(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second"))
        p.add(PromptTemplateUnit(name="c", content="Third"))
        assert p.compile() == "First\n\nSecond\n\nThird"

    def test_custom_separator(self):
        p = Proteas(separator="\n---\n")
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second"))
        assert p.compile() == "First\n---\nSecond"

    def test_add_chaining(self):
        p = (Proteas()
            .add(PromptTemplateUnit(name="a", content="First"))
            .add(PromptTemplateUnit(name="b", content="Second")))
        assert p.compile() == "First\n\nSecond"

    def test_add_many(self):
        units = [
            PromptTemplateUnit(name="a", content="First"),
            PromptTemplateUnit(name="b", content="Second"),
            PromptTemplateUnit(name="c", content="Third"),
        ]
        p = Proteas().add_many(units)
        assert p.compile() == "First\n\nSecond\n\nThird"


class TestProteasOrdering:
    """Order-based sorting tests."""

    def test_explicit_order_overrides_insertion(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="c", content="Third", order=30))
        p.add(PromptTemplateUnit(name="a", content="First", order=10))
        p.add(PromptTemplateUnit(name="b", content="Second", order=20))
        assert p.compile() == "First\n\nSecond\n\nThird"

    def test_none_order_uses_insertion_order(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))  # order=None
        p.add(PromptTemplateUnit(name="b", content="Second"))  # order=None
        p.add(PromptTemplateUnit(name="c", content="Third"))  # order=None
        assert p.compile() == "First\n\nSecond\n\nThird"

    def test_mixed_explicit_and_none_order(self):
        """Explicit orders come first, then None orders in insertion order."""
        p = Proteas()
        p.add(PromptTemplateUnit(name="middle", content="Middle"))  # order=None
        p.add(PromptTemplateUnit(name="header", content="Header", order=1))
        p.add(PromptTemplateUnit(name="footer", content="Footer", order=100))
        p.add(PromptTemplateUnit(name="body", content="Body"))  # order=None

        # Explicit: Header(1), Footer(100)
        # None (insertion order): Middle, Body
        # Result: Header, Footer, Middle, Body
        assert p.compile() == "Header\n\nFooter\n\nMiddle\n\nBody"

    def test_same_order_uses_insertion_as_tiebreaker(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First", order=10))
        p.add(PromptTemplateUnit(name="b", content="Second", order=10))
        p.add(PromptTemplateUnit(name="c", content="Third", order=10))
        assert p.compile() == "First\n\nSecond\n\nThird"


class TestProteasEnabledDisabled:
    """Enable/disable tests."""

    def test_disabled_units_excluded(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second", enabled=False))
        p.add(PromptTemplateUnit(name="c", content="Third"))
        assert p.compile() == "First\n\nThird"

    def test_disable_by_name(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second"))
        p.disable("b")
        assert p.compile() == "First"

    def test_enable_by_name(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second", enabled=False))
        p.enable("b")
        assert p.compile() == "First\n\nSecond"

    def test_enable_disable_chaining(self):
        p = (Proteas()
            .add(PromptTemplateUnit(name="a", content="First"))
            .add(PromptTemplateUnit(name="b", content="Second"))
            .disable("a")
            .enable("a"))
        assert p.compile() == "First\n\nSecond"

    def test_enabled_units_property(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second", enabled=False))
        p.add(PromptTemplateUnit(name="c", content="Third"))

        enabled = p.enabled_units
        assert len(enabled) == 2
        assert enabled[0].name == "a"
        assert enabled[1].name == "c"


class TestProteasPlaceholders:
    """Placeholder/kwargs tests."""

    def test_compile_with_placeholder(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="greeting", content="Hello {name}!"))
        assert p.compile(name="World") == "Hello World!"

    def test_compile_multiple_units_same_placeholder(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="Dear {name},"))
        p.add(PromptTemplateUnit(name="b", content="Goodbye {name}!"))
        result = p.compile(name="Alice")
        assert result == "Dear Alice,\n\nGoodbye Alice!"

    def test_compile_different_placeholders(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="header", content="Task: {task}"))
        p.add(PromptTemplateUnit(name="body", content="Data: {data}"))
        result = p.compile(task="Extract", data="msg1\nmsg2")
        assert result == "Task: Extract\n\nData: msg1\nmsg2"

    def test_units_without_placeholders_unaffected(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="static", content="Static content"))
        p.add(PromptTemplateUnit(name="dynamic", content="Hello {name}!"))
        result = p.compile(name="World")
        assert result == "Static content\n\nHello World!"


class TestProteasManagement:
    """Unit management tests."""

    def test_get_unit(self):
        p = Proteas()
        unit = PromptTemplateUnit(name="target", content="Found me")
        p.add(PromptTemplateUnit(name="other", content="Other"))
        p.add(unit)

        found = p.get_unit("target")
        assert found is unit

    def test_get_unit_not_found(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="..."))
        assert p.get_unit("nonexistent") is None

    def test_remove_unit(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second"))
        p.add(PromptTemplateUnit(name="c", content="Third"))
        p.remove("b")
        assert p.compile() == "First\n\nThird"

    def test_remove_chaining(self):
        p = (Proteas()
            .add(PromptTemplateUnit(name="a", content="First"))
            .add(PromptTemplateUnit(name="b", content="Second"))
            .remove("a"))
        assert p.compile() == "Second"

    def test_clear(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second"))
        p.clear()
        assert p.compile() == ""
        assert len(p) == 0

    def test_units_property(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="First"))
        p.add(PromptTemplateUnit(name="b", content="Second"))

        units = p.units
        assert len(units) == 2
        assert units[0].name == "a"
        assert units[1].name == "b"

    def test_len(self):
        p = Proteas()
        assert len(p) == 0
        p.add(PromptTemplateUnit(name="a", content="..."))
        assert len(p) == 1
        p.add(PromptTemplateUnit(name="b", content="..."))
        assert len(p) == 2


class TestProteasStr:
    """String representation tests."""

    def test_str(self):
        p = Proteas()
        p.add(PromptTemplateUnit(name="a", content="..."))
        p.add(PromptTemplateUnit(name="b", content="...", enabled=False))
        assert "1/2" in str(p)
