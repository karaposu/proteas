# Proteas

## What is Proteas?

Proteas is a prompt composition library. It helps you build large, complex prompts from smaller, reusable pieces.

The name comes from the Greek god Proteus (as well as prompt template assembler initials), who could change shape at will. Like Proteus, prompts built with Proteas can take many forms by combining different pieces in different ways.

## The Problem

When working with LLMs, prompts often grow large and complex. You end up with:

- Long prompt strings that are hard to read and maintain
- Copy-pasting sections between similar prompts
- Difficulty testing individual parts of a prompt
- No easy way to swap out sections based on conditions

For example, imagine you have 7 different extraction categories. A user might want to extract any combination of them. Writing a separate prompt for every combination (127 possibilities) is not practical.

## The Solution

Proteas breaks prompts into small, independent units. Each unit is a self-contained piece of prompt content. You then combine units to create the final prompt.

Think of it like building with blocks. Each block is a unit. You stack the blocks you need to create the structure you want.

## Core Concepts

### Prompt Unit

A prompt unit is a single, reusable piece of prompt content. It has:

- A name (for identification)
- Content (the actual text)
- An order number (determines position when combined)
- Optional prefix and suffix (headers and footers)

Units are independent. They know nothing about other units. This makes them easy to test, reuse, and maintain.

### Combiner

The combiner takes multiple units and assembles them into a final prompt. It:

- Accepts any number of units
- Sorts them by their order number
- Renders each unit
- Joins them together with a separator

The combiner does not care what the units contain. It just puts them together in the right order.

## Key Features

### Composability

Build complex prompts from simple pieces. Add, remove, or swap units without touching other parts.

### Reusability

Define a unit once, use it in many prompts. When you update the unit, all prompts using it get the update.

### Order Control

Each unit has an order number. The combiner sorts units by this number before joining. This lets you insert units at specific positions without changing other units.

### Conditional Assembly

Include or exclude units based on runtime conditions. Only add the units you need for a specific use case.

### Domain Agnostic

Proteas knows nothing about your domain. It works with text blocks. Whether you are building prompts for extraction, chat, analysis, or anything else, Proteas works the same way.

### Testability

Test units in isolation. Each unit renders independently. You can verify a unit's output without building the full prompt.

## Use Cases

### Multi-Dimension Extraction

You have 7 extraction dimensions. Users can select any combination. Instead of 127 static prompts, define 7 units (one per dimension) plus shared units (header, instructions, schema). Combine only the selected dimension units at runtime.

### Configurable System Prompts

Your AI assistant has different modes: helpful, concise, creative. Define a unit for each mode. Swap in the right unit based on user preference.

### A/B Testing Prompts

Testing two versions of an instruction? Define both as units. Swap between them without changing the rest of the prompt.

### Layered Context

You have static context (always included) and dynamic context (changes per request). Define static parts as units with low order numbers. Add dynamic units with higher order numbers. The combiner handles the assembly.

## Design Principles

### Simplicity

Proteas does one thing: compose text blocks. No magic, no hidden behavior. You control what goes in and how it combines.

### Transparency

The final prompt is predictable. Units render in order. What you add is what you get.

### Independence

Units do not depend on each other. The combiner does not depend on unit content. Each piece works in isolation.

### No Framework Lock-in

Proteas is a library, not a framework. You call it when you need it. It does not take over your application.
