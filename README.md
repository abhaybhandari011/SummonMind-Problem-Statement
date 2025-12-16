# SummonMind Backend Screening Assignment

Minimal backend service to validate data against a simple schema and execute declarative validation rules.

---

## Tech Stack

- Python 3.12
- FastAPI
- Poetry (dependency management)
- Pydantic-core

---

## Setup & Run

### Prerequisites

- Python 3.12
- Poetry installed

### Install Dependencies

```bash
poetry install
````

### Run the Server

```bash
python main.py
```

The server will start at:

```
http://localhost:8000
```

---

## API Endpoint

### POST /validate

Validates input data against a provided schema and executes declarative rules.

#### Request Body

```json
{
  "schema": { },
  "rules": [ ],
  "data": { }
}
```

#### Response

* **Success**

```json
{
  "validatedData": { }
}
```

* **Failure**

```json
{
  "errors": [ "error message" ]
}
```

---

## Sample Requests

Sample request payloads are available in the `samples/` directory:

* `valid.json` – passes all validations and rules
* `invalid.json` – fails at least one rule

---

## Notes

* The service uses a depth guard to prevent infinite evaluation loops.
* Only field-level validation rules are supported.
* The design prioritizes deterministic behavior and simplicity.

---

## Project Structure

```
.
├── main.py
├── src/
│   ├── routes/
│   ├── schemas/
│   └── utils/
├── samples/
├── pyproject.toml
└── poetry.lock
```
