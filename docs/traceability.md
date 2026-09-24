# Traceability Matrix

| Requirement | SPEC / AC | Task | Implementation Files | Test Files / Scenarios | Status | Notes |
|---|---|---|---|---|---|---|
| FR-01 | AC-01, AC-02, AC-03, AC-04 | T-02, T-04, T-08 | `src/customer_search/customer.py`, `src/customer_search/search_service.py` | `tests/test_scenarios.py` (TS-01, TS-02, TS-03, TS-04), `tests/test_search_matching.py` | ✓ | Matches by name, surname, full name, or email. |
| FR-02 | AC-03 | T-04, T-08 | `src/customer_search/search_service.py` | `tests/test_scenarios.py` (TS-05), `tests/test_search_matching.py` | ✓ | Substring partial matching across all searchable fields. |
| FR-03 | AC-04 | T-04, T-08 | `src/customer_search/search_service.py` | `tests/test_scenarios.py` (TS-06), `tests/test_search_matching.py` | ✓ | Case-insensitive comparison via text normalization. |
| FR-04 | AC-06 | T-04, T-05, T-08 | `src/customer_search/search_service.py` | `tests/test_scenarios.py` (TS-07), `tests/test_ordering_and_limit.py` | ✓ | Exact matches displayed before partial; alphabetical tie-breaking. |
| FR-05 | AC-05 | T-06, T-07, T-08 | `src/customer_search/search_service.py`, `src/customer_search/cli.py` | `tests/test_scenarios.py` (TS-08), `tests/test_validation_and_errors.py`, `tests/test_cli.py` | ✓ | Displays "No customers found" when no records match. |
| FR-06 | AC-07 | T-05, T-08 | `src/customer_search/search_service.py` | `tests/test_scenarios.py` (TS-09), `tests/test_ordering_and_limit.py` | ✓ | Limits displayed results to a maximum of 10. |
| FR-07 | AC-08 | T-02, T-07, T-08 | `src/customer_search/customer.py`, `src/customer_search/cli.py` | `tests/test_scenarios.py` (TS-10), `tests/test_cli.py` | ✓ | Displays only customer full name and email address. |
| FR-08 | AC-09 | T-06, T-07, T-08 | `src/customer_search/search_service.py`, `src/customer_search/cli.py` | `tests/test_scenarios.py` (TS-11), `tests/test_validation_and_errors.py`, `tests/test_cli.py` | ✓ | Displays "Please enter a search term" without executing search. |
| NFR-01 | AC-11 | T-08 | `src/customer_search/search_service.py`, `src/customer_search/data_loader.py` | `tests/test_scenarios.py` (TS-13), `tests/test_data_loader.py` | ✓ | Processes 10,000 customers in < 0.1s (limit: 2.0s). |
| NFR-02 | AC-11 | T-03, T-06, T-08 | `src/customer_search/data_loader.py`, `src/customer_search/search_service.py` | `tests/test_scenarios.py` (TS-13), `tests/test_data_loader.py`, `tests/test_validation_and_errors.py` | ✓ | Handles up to 10,000 records and invalid records gracefully. |
| NFR-03 | AC-10 | T-07, T-08 | `src/customer_search/cli.py` | `tests/test_scenarios.py` (TS-12), `tests/test_cli.py` | ✓ | Search triggers upon Enter in CLI interactive prompt. |