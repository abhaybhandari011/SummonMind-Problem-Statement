from fastapi import APIRouter, HTTPException
from src.schemas.validation_schemas import ValidateRequest
from src.utils.validation_utils import (validate_schema, apply_computed_fields, execute_rules)

router = APIRouter()

@router.post("/validate")
def validate(payload: ValidateRequest):
    try:
        schema = payload.schema
        rules = payload.rules
        data = payload.data

        if not schema or data is None:
            raise HTTPException(status_code=400, detail="Invalid payload")

        validated_data = validate_schema(schema, data)
        computed_data = apply_computed_fields(schema, validated_data)
        rule_errors = execute_rules(rules, computed_data)

        if rule_errors:
            return {"errors": rule_errors}

        return {"validatedData": computed_data}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
