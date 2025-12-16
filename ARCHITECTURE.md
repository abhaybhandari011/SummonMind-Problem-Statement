# Architecture Overview

Overview of the execution!
---

## Schema Validation Approach

The service accepts a simple, declarative schema defining:
- A `version` number
- A set of required fields with primitive data types (`string`, `number`, `boolean`)
- Optional computed fields defined using string templates

Schema validation is performed in two steps:
1. **Schema structure validation**  
   Ensures the presence and correctness of `version`, `fields`, and optional `computed` objects.
2. **Data validation**  
   Each schema field is required and validated against its declared type.

Validation produces a sanitized data object that is guaranteed to conform to the schema and is passed to downstream stages.

---

## Computed Fields Resolution

Computed fields are defined as template strings using `{{field}}` placeholders.

Example: fullName = "{{firstName}} {{lastName}}"

Resolution is performed iteratively:
- Templates are resolved only when all referenced fields are available
- Computed fields may depend on other computed fields
- Results are merged back into the validated data object

---

## Recursion Safety (Depth Guard)

To prevent infinite dependency loops between computed fields:
- Resolution is re-run only when progress is made
- A maximum recursion depth of **5** is enforced
- If exceeded, evaluation stops with an error:

```json
{
  "error": "Max evaluation depth reached"
}
```

## Rule Execution Model

Rules are declarative JSON objects executed after schema validation and computed field resolution.

Supported rules:

- Field-level validation rules only.
- Condition expressions evaluated against a single field value.

## Execution Flow Summary

```
Request
  ↓
Schema Structure Validation
  ↓
Data Type Validation
  ↓
Computed Field Resolution (Depth Guarded)
  ↓
Rule Execution
  ↓
Response (validatedData OR errors)
```

