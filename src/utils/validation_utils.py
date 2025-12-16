import re
import json


TEMPLATE_PATTERN = re.compile(r"\{\{(.*?)\}\}")

def validate_schema(schema: dict, data: dict) -> dict:
    """
    Validates input data against a simple schema definition.

    Schema format:
    {
        "version": number,
        "fields": {
            "fieldName": "string" | "number" | "boolean"
        }
    }
    """

    if "version" not in schema or not isinstance(schema["version"], (int, float)):
        raise ValueError("Schema version must be a number")

    if "fields" not in schema or not isinstance(schema["fields"], dict):
        raise ValueError("Schema must contain a 'fields' object")

    if "computed" in schema:
        if not isinstance(schema["computed"], dict):
            raise ValueError("'computed' must be an object if present!")

    fields = schema["fields"]

    validated_data = {} #as fields is a nested block in schema, we need to validate each field inside it and use a subset of data.

    for field_name, field_type in fields.items():
        if field_name not in data:
            raise ValueError(f"Missing required field: {field_name}")

        value = data[field_name]

        if field_type == "string":
            if not isinstance(value, str):
                raise ValueError(f"Field '{field_name}' must be a string")

        elif field_type == "number":
            if not isinstance(value, (int, float)):
                raise ValueError(f"Field '{field_name}' must be a number")

        elif field_type == "boolean":
            if not isinstance(value, bool):
                raise ValueError(f"Field '{field_name}' must be a boolean")

        else:
            raise ValueError(f"Unsupported field type: {field_type}")

        validated_data[field_name] = value

    return validated_data


def apply_computed_fields(schema: dict, data: dict, depth: int = 0) -> dict:
    """
    Resolves computed fields using {{field}} templates.
    Enforces max recursion depth of 5.
    """

    if depth > 5:
        raise ValueError("Max evaluation depth reached")

    computed = schema.get("computed", {})
    if not computed:
        return data

    result = data.copy()
    resolved_any = False

    for field_name, template in computed.items():
        if field_name in result:
            continue  # already resolved

        if not isinstance(template, str):
            raise ValueError(f"Computed field '{field_name}' must be a string")

        matches = TEMPLATE_PATTERN.findall(template)

        value = template
        for match in matches:
            if match not in result:
                break
            value = value.replace(f"{{{{{match}}}}}", str(result[match]))
        else:
            result[field_name] = value
            resolved_any = True

    if resolved_any:
        return apply_computed_fields(schema, result, depth + 1)

    return result


def execute_rules(rules: list, data: dict) -> list:
    """
    - Execute field-level rules
    - Evaluate conditions safely
    - Return list of error messages
    """
    errors = []

    for rule in rules:
        rule_id = rule.get("id", "unknown")
        level = rule.get("level")
        field = rule.get("field")
        condition = rule.get("condition")
        action = rule.get("action")

        if level != "field" or action != "validate":
            continue  # only field-level validate rules supported

        if field not in data:
            errors.append(f"Rule {rule_id} failed: field '{field}' missing")
            continue

        value = data[field]

        # Safe evaluation context
        safe_globals = {"__builtins__": {}}
        safe_locals = {"value": value}

        try:
            if not eval(condition, safe_globals, safe_locals):
                errors.append(f"Rule {rule_id} failed: condition '{condition}' not met for field '{field}'")
        except Exception as e:
            errors.append(f"Rule {rule_id} error: {str(e)}")

    return errors
