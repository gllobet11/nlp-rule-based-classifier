# 🧠 Part 4 — Flexible Email Classification System

## 🎯 Objective

Implement a system capable of **translating natural language descriptions** (in Spanish or English) into a **functional email classifier** that evaluates incoming messages based on configurable criteria.

The system supports:

* Conditional rules using `contains` / `equals` over `subject`, `body`, or `sender`.

* Rules written in natural language, for example:

  > “If the subject contains the word *urgent*, classify it as *urgent*.”
  > “Otherwise, use the default classifier.”

* A **default classifier** that connects to the API implemented in **Part 1**.

---

## ⚙️ Project Structure

```
parte4/
│
├── src/
│   └── nlrules/
│       ├── __init__.py
│       ├── parsing.py           # Translates natural language → JSON rule config
│       ├── deserializer.py      # Builds classifiers from the JSON config
│       └── classifiers.py       # APIClassifier, ConditionClassifier, SequentialClassifier
│
├── examples/
│   ├── demo.py                  # Simple usage example
│   ├── demo2.py                 # Intermediate example with multiple criteria
│   ├── demo3.py                 # Mixed conditional rules
│   └── demo_profesional_1.py    # Business-oriented example
│
├── tests/
│   └── test.py                  # Official unit tests
│
├── base.py                      # Provided abstract base classes
├── dependencies.py              # Dynamic dependency loading
├── requirements.txt             # Minimal dependencies
└── README.md
```

---

## 🧩 Installation

It is recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**`requirements.txt`:**

```
requests>=2.31.0
```

---

## 🚀 Usage

### 1️⃣ Run the official unit tests

```bash
python -m unittest tests/test.py
```

Expected output:

```
Ran 7 tests in X.XXXs
OK
```

---

### 2️⃣ Try a custom rule set

```bash
python examples/demo.py
```

Expected output:

```
CONFIG: {'rules': [...]}
RESULT: urgent
```

---

## ⚙️ API Configuration (optional)

The default classifier (`APIClassifier`) can be parameterized via environment variables:

```bash
export DEFAULT_API_URL="http://localhost:8000/classify-email"
export DEFAULT_API_TIMEOUT=6
export DEFAULT_API_RETRIES=2
export DEFAULT_API_BACKOFF=0.4
```

> 🔸 If **no environment variables** are defined, defaults will be used:
> `URL=http://localhost:8000/classify-email`, `timeout=5s`, `retries=1`, `backoff=0.3s`.

---

## 🧠 Realistic Example

Natural language input:

```
Assign the category "regulatory" if the sender is "inspecciones@cnmc.es".
If the subject contains the word "reclamation", classify it as "reclamacion".
If the body contains the word "outage", classify it as "incident".
```

Resulting JSON:

```json
{
  "rules": [
    {"type": "condition", "field": "sender", "operator": "equals", "value": "inspecciones@cnmc.es", "category": "regulatory"},
    {"type": "condition", "field": "subject", "operator": "contains", "value": "reclamacion", "category": "reclamacion"},
    {"type": "condition", "field": "body", "operator": "contains", "value": "avería", "category": "incident"}
  ]
}
```

Expected classification output:

```
Email 1 -> regulatory
Email 2 -> reclamacion
Email 3 -> incident
```

---

## 🧰 Technical Highlights

* **Multilingual parser (ES/EN)** with support for typographic quotes and accented characters.
* **Robust normalization** (`áéíóú` → `aeiou`).
* **Debug logs** enabled via `DEBUG_PART4=1`.
* **Retry & exponential backoff** in the API classifier.
* **Modular design** — clear separation between parsing, deserialization, and classification logic.
* **Easily extensible:** adding new rule expressions or languages only requires editing `parsing.py`.

---

## 🧾 Author

**Developed by:** *Gerard* — Data Scientist in training
**Focus:** Clean, modular, and extensible code.
Fully compliant with all requirements defined for Part 4.

---

> 💡 Tip: to test new rules, edit the text in `examples/demo3.py` and observe how the system dynamically generates classification configurations.

---

