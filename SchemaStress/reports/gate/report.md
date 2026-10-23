# SchemaStress Evaluation Report

| Metric | Result |
|---|---:|
| Cases | 12 |
| JSON parse success | 91.7% |
| Schema compliance | 91.7% |
| Field accuracy | 89.6% |
| Exact case match | 83.3% |

## Per-case diagnostics

### INC-001 — ordinary
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-002 — reordered
- Parse success: `False`
- Schema valid: `False`
- Field accuracy: `0.0%`
- Error: invalid JSON line 1, column 16: Expecting value
- Mismatch `customer_impact`: expected `None`, got `<MISSING>`; evidence: 'Customer impact has not been confirmed'
- Mismatch `incident_id`: expected `INC-1042`, got `<MISSING>`; evidence: 'Incident identifier: INC-1042'
- Mismatch `service`: expected `payments-api`, got `<MISSING>`; evidence: 'The service is payments-api'
- Mismatch `severity`: expected `high`, got `<MISSING>`; evidence: 'Severity is high'

### INC-003 — missing_evidence
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-004 — distractor
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `75.0%`
- Mismatch `severity`: expected `low`, got `critical`; evidence: 'Severity: low'

### INC-005 — conflict
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-006 — ordinary
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-007 — instruction_distractor
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-008 — formatting
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-009 — missing_field
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-010 — conflict
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-011 — ordinary
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`

### INC-012 — irrelevant_numbers
- Parse success: `True`
- Schema valid: `True`
- Field accuracy: `100.0%`
