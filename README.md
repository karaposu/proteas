# PROTEAS

**PROTEAS** is a scalable prompt engineering and management library designed to streamline the creation and management of dynamic prompt templates for AI models.

Instead of handling the entire lifecycle of a prompt, **PROTEAS** specializes in the **stacking of prompt templates**—unformatted prompts with placeholders—leaving the task of filling in these templates to common LLM libraries like LangChain. This approach can be seen as a **replacement for prompt chaining** in libraries such as LangChain, offering more flexibility and control.

---

## Table of Contents

- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Creating Your `prompts.yaml`](#creating-your-promptyaml)
  - [Assembling and Formatting Prompts](#assembling-and-formatting-prompts)
  - [Integration into Your Application](#integration-into-your-application)
- [Quick Demo](#quick-demo)
  - [Use Case: Building an LLM-Based Chatbot - Database Whisperer](#use-case-building-an-llm-based-chatbot---database-whisperer)
    - [Objective](#objective)
    - [Problem](#problem)
    - [Solution with PROTEAS](#solution-with-proteas)
    - [Step-by-Step Guide](#step-by-step-guide)
      - [1. Define Prompt Template Units in `prompts.yaml`](#1-define-prompt-template-units-in-promptyaml)
      - [2. Install PROTEAS](#2-install-proteas)
      - [3. Assemble Prompt Templates Using PROTEAS](#3-assemble-prompt-templates-using-proteas)
      - [4. Format the Generated Prompt Templates with LangChain](#4-format-the-generated-prompt-templates-with-langchain)
    - [Summary](#summary)
- [Additional Example: Running SQL Queries](#additional-example-running-sql-queries)
  - [Extending `prompts.yaml`](#extending-promptyaml)
  - [Assembling Prompt Template for SQL Queries](#assembling-prompt-template-for-sql-queries)
  - [Formatting with LangChain](#formatting-with-langchain)
- [Conclusion](#conclusion)
- [License](#license)

---

## Key Features

- **Conditional Prompt Stacking**: Stack prompt templates conditionally, allowing the creation of adaptable prompts based on specific scenarios or use cases.
- **Custom Categories for Templates**: Organize prompt templates into user-defined categories, making it easy to call and merge templates based on modular, structured designs.
- **"Send to Bin" Logic**: Temporarily store parts of a prompt in a "bin" and retrieve or merge them at a later point, enabling more dynamic and flexible prompt building over multiple stages.
- **Statement vs. Question Formatting**: Prompts can be defined in a way that allows them to be formatted as informative statements or questions, enabling you to switch between different styles of interactions without changing the core context.
- **Intuitive Interface**: Designed with simplicity and usability in mind, the library enables users to construct prompts effortlessly without complex chaining or dependencies.

---

## Getting Started

### Installation

To install **PROTEAS**, use the following command:

```bash
pip install proteas
```

**Note**: Ensure that the `proteas` package is available on PyPI. If not, provide instructions on how to install it directly from the source repository.

### Creating Your `prompts.yaml`

Define your prompt template units in a YAML file named `prompts.yaml`. This file will contain all the prompt units that you will assemble dynamically.

```yaml
main:
  - name: "business_documentation"
    statement_suffix: "Here is"
    placeholder_proclamation: "my business documentation:"
    placeholder: "business_documentation"

  - name: "user_input"
    statement_suffix: "Here is"
    placeholder_proclamation: "my question:"
    placeholder: "user_input"

  - name: "answer_style"
    info: >
      Answer should be professional and should not contain assumptions.

  - name: "database_documentation"
    statement_suffix: "Here is"
    placeholder_proclamation: "my database documentation:"
    placeholder: "database_documentation"
```

**Explanation**:

- Each prompt unit has attributes like `name`, `statement_suffix`, `placeholder_proclamation`, `placeholder`, and `info`.
- The `placeholder` is where dynamic data will be inserted when formatting the prompt.
- The `main` category can be customized or extended as needed.

### Assembling and Formatting Prompts

Use **PROTEAS** to craft your prompts and integrate them with LangChain or your preferred LLM library.

### Integration into Your Application

Utilize the formatted prompts within your application logic to interact with AI models seamlessly.

---

## Quick Demo

### Use Case: Building an LLM-Based Chatbot - **Database Whisperer**

Imagine building an LLM-based chatbot called **Database Whisperer**. This chatbot allows users to interact with their business documents, create SQL queries, and run these queries on their databases.

#### Objective

Demonstrate how **PROTEAS** can be used to manage and assemble prompt templates efficiently, avoiding redundancy and adhering to the DRY (Don't Repeat Yourself) principle.

#### Problem

Creating multiple prompt templates with overlapping content can lead to redundancy and maintenance challenges. For instance, crafting separate prompt templates for different user inputs that share common sections violates the DRY principle.

#### Solution with PROTEAS

**PROTEAS** elegantly solves this problem by allowing you to define prompt template units in a YAML file and assemble them dynamically based on your needs.

#### Step-by-Step Guide

##### 1. **Define Prompt Template Units in `prompts.yaml`**

Create a `prompts.yaml` file that contains all the necessary prompt template units.

```yaml
main:
  - name: "business_documentation"
    statement_suffix: "Here is"
    placeholder_proclamation: "my business documentation:"
    placeholder: "business_documentation"

  - name: "user_input"
    statement_suffix: "Here is"
    placeholder_proclamation: "my question:"
    placeholder: "user_input"

  - name: "answer_style"
    info: >
      Answer should be professional and should not contain assumptions.

  - name: "database_documentation"
    statement_suffix: "Here is"
    placeholder_proclamation: "my database documentation:"
    placeholder: "database_documentation"
```

**Explanation**:

- **`business_documentation`**, **`user_input`**, and **`database_documentation`**: These units include placeholders that will be filled with dynamic data.
- **`answer_style`**: This unit provides static instructions for the LLM without requiring a placeholder.

##### 2. **Install PROTEAS**

Ensure you have **PROTEAS** installed:

```bash
pip install proteas
```

##### 3. **Assemble Prompt Templates Using PROTEAS**

Use **PROTEAS** to load the YAML configuration and craft the desired prompt templates.

```python
from proteas import Proteas

# Initialize PROTEAS with the YAML file
proteas = Proteas(yaml_path="prompts.yaml")
# Output: 4 prompt template units loaded

# Define the order of prompt units for Prompt Template 1
order_1 = ["business_documentation", "user_input", "answer_style"]
prompt_template_1 = proteas.craft(order_1)
print("Prompt Template 1:")
print(prompt_template_1)
```

**Output**:

```plaintext
Prompt Template 1:
Here is my business documentation: {business_documentation}

Here is my question: {user_input}

Answer should be professional and should not contain assumptions.
```

```python
# Define the order of prompt units for Prompt Template 2
order_2 = ["business_documentation", "database_documentation", "user_input", "answer_style"]
prompt_template_2 = proteas.craft(order_2)
print("Prompt Template 2:")
print(prompt_template_2)
```

**Output**:

```plaintext
Prompt Template 2:
Here is my business documentation: {business_documentation}

Here is my database documentation: {database_documentation}

Here is my question: {user_input}

Answer should be professional and should not contain assumptions.
```

**Explanation**:

- **`order_1`** assembles `prompt_template_1` by stacking the relevant prompt units.
- **`order_2`** assembles `prompt_template_2` by including the additional `database_documentation` unit.

##### 4. **Format the Generated Prompt Templates with LangChain**

Once you have the assembled prompt templates, you can use LangChain to fill in the placeholders with actual data.

First, ensure that LangChain is installed:

```bash
pip install langchain
```

Then proceed to format the prompts:

```python
from langchain.prompts import PromptTemplate

# Example context data for Prompt Template 1
context_data_1 = {
    "business_documentation": "We specialize in handcrafted chocolates and have 15 stores nationwide.",
    "user_input": "What are your best-selling products?"
}

# Create a PromptTemplate object from the assembled template
prompt_1 = PromptTemplate.from_template(prompt_template_1)

# Format the prompt with the provided data
formatted_prompt_1 = prompt_1.format(**context_data_1)

print("Formatted Prompt Template 1:")
print(formatted_prompt_1)
```

**Output**:

```plaintext
Formatted Prompt Template 1:
Here is my business documentation: We specialize in handcrafted chocolates and have 15 stores nationwide.

Here is my question: What are your best-selling products?

Answer should be professional and should not contain assumptions.
```

```python
# Example context data for Prompt Template 2
context_data_2 = {
    "business_documentation": "We specialize in handcrafted chocolates and have 15 stores nationwide.",
    "database_documentation": "Database includes tables for products, sales, and customer feedback.",
    "user_input": "How can we improve our inventory turnover rate?"
}

# Create a PromptTemplate object from the assembled template
prompt_2 = PromptTemplate.from_template(prompt_template_2)

# Format the prompt with the provided data
formatted_prompt_2 = prompt_2.format(**context_data_2)

print("Formatted Prompt Template 2:")
print(formatted_prompt_2)
```

**Output**:

```plaintext
Formatted Prompt Template 2:
Here is my business documentation: We specialize in handcrafted chocolates and have 15 stores nationwide.

Here is my database documentation: Database includes tables for products, sales, and customer feedback.

Here is my question: How can we improve our inventory turnover rate?

Answer should be professional and should not contain assumptions.
```

**Explanation**:

- **LangChain Integration**: By using LangChain’s `PromptTemplate`, you can seamlessly fill in the placeholders with dynamic data, leveraging **PROTEAS** for the prompt assembly.
- **Flexibility**: You can easily add or remove prompt units in the `order` list to customize the prompts as needed without duplicating code or templates.

#### Summary

Using **PROTEAS**, you can efficiently manage and assemble prompt templates, ensuring adherence to best practices like DRY while maintaining flexibility and scalability. This approach simplifies prompt management, especially as your application grows in complexity.

---

## Additional Example: Running SQL Queries

To further demonstrate **PROTEAS**'s capabilities, let's consider another use case where the chatbot helps users create and run SQL queries based on their business and database documentation.

### Extending `prompts.yaml`

Add a new prompt unit for SQL query creation.

```yaml
main:
  - name: "business_documentation"
    statement_suffix: "Here is"
    placeholder_proclamation: "my business documentation:"
    placeholder: "business_documentation"

  - name: "database_documentation"
    statement_suffix: "Here is"
    placeholder_proclamation: "my database documentation:"
    placeholder: "database_documentation"

  - name: "user_input"
    statement_suffix: "Here is"
    placeholder_proclamation: "my request:"
    placeholder: "user_input"

  - name: "sql_query_instruction"
    info: >
      Based on the provided documentation, create an optimized SQL query.

  - name: "answer_style"
    info: >
      Answer should be professional and should not contain assumptions.
```

### Assembling Prompt Template for SQL Queries

```python
# Define the order for SQL query creation
order_sql = ["business_documentation", "database_documentation", "user_input", "sql_query_instruction", "answer_style"]
prompt_template_sql = proteas.craft(order_sql)
print("Prompt Template for SQL Queries:")
print(prompt_template_sql)
```

**Output**:

```plaintext
Prompt Template for SQL Queries:
Here is my business documentation: {business_documentation}

Here is my database documentation: {database_documentation}

Here is my request: {user_input}

Based on the provided documentation, create an optimized SQL query.

Answer should be professional and should not contain assumptions.
```

### Formatting with LangChain

```python
# Example context data for the SQL prompt
context_data_sql = {
    "business_documentation": "We manage an online bookstore with a diverse range of genres.",
    "database_documentation": "Tables include books, authors, customers, and orders with relevant foreign keys.",
    "user_input": "Find the top 5 bestselling authors in the last quarter."
}

# Create a PromptTemplate object from the assembled template
prompt_sql = PromptTemplate.from_template(prompt_template_sql)

# Format the prompt with the provided data
formatted_prompt_sql = prompt_sql.format(**context_data_sql)

print("Formatted Prompt Template for SQL Queries:")
print(formatted_prompt_sql)
```

**Output**:

```plaintext
Formatted Prompt Template for SQL Queries:
Here is my business documentation: We manage an online bookstore with a diverse range of genres.

Here is my database documentation: Tables include books, authors, customers, and orders with relevant foreign keys.

Here is my request: Find the top 5 bestselling authors in the last quarter.

Based on the provided documentation, create an optimized SQL query.

Answer should be professional and should not contain assumptions.
```

**Integration**

Use `formatted_prompt_sql` as input to your LLM to generate the desired SQL query.

---

## Conclusion

The **PROTEAS** library significantly simplifies the process of managing and assembling prompt templates for AI applications. By leveraging YAML configurations and providing a flexible, modular approach, **PROTEAS** ensures that your prompts remain organized, maintainable, and scalable.

Whether you're building a chatbot like **Database Whisperer** or developing any AI-driven application that relies on dynamic prompts, **PROTEAS** offers the tools you need to streamline your prompt engineering workflows effectively.

---

## License

[MIT License](LICENSE)

