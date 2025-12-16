from pydantic import BaseModel, Field
from typing import Dict, Any, List

'''
sample schema:

{
  "schema": {
    "version": 1,
    "fields": {
      "firstName": "string",
      "lastName": "string",
      "age": "number",
      "isActive": "boolean"
    },
    "computed": {
      "fullName": "{{firstName}} {{lastName}}"
    }
  },
  "rules": [
    {
      "id": "r1",
      "level": "field",
      "field": "age",
      "condition": "value >= 18",
      "action": "validate"
    }
  ],
  "data": {
    "firstName": "Abhay",
    "lastName": "Bhandari",
    "age": 25,
    "isActive": true
  }
}
'''


class ValidateRequest(BaseModel):
    schema: Dict[str, Any] = Field(..., description="Validation schema definition")
    rules: List[Dict[str, Any]] = Field(default_factory=list)
    data: Dict[str, Any]
