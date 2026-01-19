# Proteas

A domain-agnostic library for composing prompts from reusable units.

## Installation

```bash
pip install proteas
```

## Quick Start

```python
from proteas import Proteas, PromptTemplateUnit

# Define reusable units
header = PromptTemplateUnit(
    name="header",
    content="You are a helpful assistant.",
    order=1
)

task = PromptTemplateUnit(
    name="task",
    content="Analyze the following data: $data",
    order=2
)

# Compose and compile
prompt = (Proteas()
    .add(header)
    .add(task)
    .compile(data="user input here"))

print(prompt)
# Output:
# You are a helpful assistant.
#
# Analyze the following data: user input here
```

## Core Concepts

### PromptTemplateUnit

A unit is a single, reusable piece of prompt content:

```python
from proteas import PromptTemplateUnit

unit = PromptTemplateUnit(
    name="greeting",           # Identifier for lookup
    content="Hello $name!",    # The actual text (with optional placeholders)
    order=10,                  # Position when combining (lower = earlier)
    prefix="=== START ===",    # Optional text before content
    suffix="=== END ===",      # Optional text after content
    enabled=True               # Whether to include when rendering
)
```

### Placeholder Syntax

Proteas uses `$variable` syntax for placeholders (via Python's `string.Template`). This allows JSON and other content with curly braces to work without escaping:

```python
unit = PromptTemplateUnit(
    name="schema",
    content='Return JSON: {"result": $value}'
)

# JSON braces are preserved, only $value is substituted
result = unit.render(value='"hello"')
# Output: Return JSON: {"result": "hello"}
```

Both `$variable` and `${variable}` syntaxes are supported.

### Proteas Combiner

The `Proteas` class combines multiple units into a single prompt:

```python
from proteas import Proteas, PromptTemplateUnit

p = Proteas(separator="\n\n")  # Default separator is double newline

# Add units (method chaining supported)
p.add(PromptTemplateUnit(name="a", content="First"))
p.add(PromptTemplateUnit(name="b", content="Second"))

# Or add many at once
p.add_many([unit1, unit2, unit3])

# Compile with placeholder values
prompt = p.compile(messages="...", context="...")
```

## Ordering

Units can be ordered explicitly or by insertion order:

```python
# Explicit order (lower numbers first)
header = PromptTemplateUnit(name="header", content="...", order=1)
body = PromptTemplateUnit(name="body", content="...", order=50)
footer = PromptTemplateUnit(name="footer", content="...", order=100)

# order=None uses insertion order
p = Proteas()
p.add(footer)   # Added first, but order=100
p.add(header)   # Added second, but order=1
p.add(body)     # Added third, order=50

# Result: header, body, footer (by explicit order)
```

When orders are equal or all None, insertion order is the tiebreaker.

## Enable/Disable Units

Units can be toggled on or off:

```python
unit = PromptTemplateUnit(name="optional", content="...", enabled=False)

# Enable/disable on the unit
unit.enable()
unit.disable()

# Or via Proteas by name
p = Proteas()
p.add(unit)
p.disable("optional")
p.enable("optional")
```

## Unit Management

```python
p = Proteas()
p.add(unit1)
p.add(unit2)

# Get a unit by name
unit = p.get_unit("unit1")

# Remove a unit
p.remove("unit1")

# Clear all units
p.clear()

# Properties
p.units          # All units in insertion order
p.enabled_units  # Only enabled units
len(p)           # Number of units
```

## Generating Combinations

For scenarios where you need all combinations of units:

```python
from proteas import generate_combinations, count_combinations, PromptTemplateUnit

units = [
    PromptTemplateUnit(name="a", content="A"),
    PromptTemplateUnit(name="b", content="B"),
    PromptTemplateUnit(name="c", content="C"),
]

# Count combinations
total = count_combinations(n=3, min_size=2, max_size=2)  # 3

# Generate combinations
for names, proteas_instance in generate_combinations(units, min_size=2, max_size=2):
    print(names)  # ('a', 'b'), ('a', 'c'), ('b', 'c')
    prompt = proteas_instance.compile()
```

You can also include base units that appear in all combinations:

```python
header = PromptTemplateUnit(name="header", content="Header", order=1)
footer = PromptTemplateUnit(name="footer", content="Footer", order=100)

for names, p in generate_combinations(
    units=dimension_units,
    min_size=2,
    max_size=4,
    base_units=[header, footer]
):
    prompt = p.compile(messages="...")
```

## Immutable Copies

Create modified copies without mutating the original:

```python
original = PromptTemplateUnit(name="test", content="Hello", order=10)

# Create copies with modifications
with_new_content = original.with_content("Goodbye")
with_new_order = original.with_order(99)

# Original is unchanged
assert original.content == "Hello"
assert original.order == 10
```

## API Reference

### PromptTemplateUnit

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Identifier for the unit |
| `content` | `str` | The prompt text (supports `$placeholder` syntax) |
| `order` | `int \| None` | Sort position (None = use insertion order) |
| `prefix` | `str \| None` | Text added before content |
| `suffix` | `str \| None` | Text added after content |
| `enabled` | `bool` | Include in output when True |

| Method | Returns | Description |
|--------|---------|-------------|
| `render(**kwargs)` | `str` | Render with placeholder substitution |
| `enable()` | `self` | Enable the unit |
| `disable()` | `self` | Disable the unit |
| `with_content(str)` | `PromptTemplateUnit` | Copy with new content |
| `with_order(int)` | `PromptTemplateUnit` | Copy with new order |

### Proteas

| Method | Returns | Description |
|--------|---------|-------------|
| `add(unit)` | `self` | Add a unit |
| `add_many(units)` | `self` | Add multiple units |
| `compile(**kwargs)` | `str` | Assemble all enabled units |
| `get_unit(name)` | `Unit \| None` | Find unit by name |
| `remove(name)` | `self` | Remove unit by name |
| `clear()` | `self` | Remove all units |
| `enable(name)` | `self` | Enable unit by name |
| `disable(name)` | `self` | Disable unit by name |

| Property | Type | Description |
|----------|------|-------------|
| `units` | `list[Unit]` | All units |
| `enabled_units` | `list[Unit]` | Only enabled units |

### Combination Functions

| Function | Description |
|----------|-------------|
| `generate_combinations(units, min_size, max_size, base_units)` | Yield `(names, Proteas)` for all combinations |
| `count_combinations(n, min_size, max_size)` | Count total combinations |

## License

MIT
