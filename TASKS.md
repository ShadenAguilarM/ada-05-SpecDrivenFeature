# Tasks — Customer Search

## T-01 — Set up the Python project

- Create the basic Python project structure.
- Configure the project to use Python 3.11 or higher.
- Configure pytest for automated testing.
- Create the directories required for source code and tests.

**Verification:**
- The project runs with the required Python version.
- pytest can be executed successfully.
- The project structure is present.

**Requirements Covered:**
- C-01

---

## T-02 — Implement the customer model

- Create the customer model with the required fields:
  - `name`
  - `surname`
  - `email`
- Provide a way to derive the customer's full name from `name` and `surname`.

**Verification:**
- A customer can be created with the required fields.
- The full name is correctly derived from the customer's name and surname.

**Requirements Covered:**
- FR-01
- FR-07

---

## T-03 — Implement the JSON customer data loader

- Create the local JSON data source for customer records.
- Implement the customer data loader.
- Load customer records from the JSON file.
- Validate that loaded customer records contain the fields required by the customer model.
- Handle invalid customer records without causing an unhandled application error during a search.
- Keep the JSON data source read-only.

**Verification:**
- Valid customer records are loaded correctly.
- Invalid customer records do not cause an unhandled application error.
- The application does not modify the JSON data source.

**Requirements Covered:**
- A-01
- NFR-02
- C-02

---

## T-04 — Implement search matching

- Implement the search service.
- Accept a single search term.
- Search the following customer fields:
  - `name`
  - `surname`
  - `full name`
  - `email`
- Support partial matches.
- Perform comparisons without distinguishing between uppercase and lowercase letters.
- Identify exact matches separately from partial matches.

**Verification:**
- Searches by name, surname, full name, and email return the expected customers.
- Partial matches are returned.
- Searches with different character casing return the same results.
- Exact and partial matches are correctly identified.

**Requirements Covered:**
- FR-01
- FR-02
- FR-03
- FR-04

---

## T-05 — Implement result ordering and limit

- Order exact matches before partial matches.
- Sort customers alphabetically when they have the same match priority.
- Limit the search results to a maximum of 10 customers.

**Verification:**
- Exact matches appear before partial matches.
- Customers with the same match priority are sorted alphabetically.
- A search never returns more than 10 displayed customers.

**Requirements Covered:**
- FR-04
- FR-06

---

## T-06 — Implement search input validation and error handling

- Validate the search term before executing the search.
- Reject empty search input.
- Reject search input containing only whitespace characters.
- Display `Please enter a search term` when the input is invalid.
- Display `No customers found` when no customers match the search criteria.
- Ensure invalid customer data does not produce an unhandled application error.

**Verification:**
- Empty input displays the required validation message.
- Whitespace-only input displays the required validation message.
- The search is not executed for invalid input.
- No matching customers display `No customers found`.
- Invalid customer records do not cause an unhandled application error.

**Requirements Covered:**
- FR-05
- FR-08
- NFR-02

---

## T-07 — Implement the command-line interface

- Implement the CLI search field.
- Allow the user to enter one search term.
- Execute the search when the user presses Enter.
- Display the search results through the CLI.
- Display only each customer's full name and email address.
- Display the required validation and no-results messages.

**Verification:**
- The user can enter a search term through the CLI.
- Pressing Enter executes a valid search.
- Search results display only the customer's full name and email.
- Required messages are displayed in the corresponding situations.

**Requirements Covered:**
- FR-07
- NFR-03

---

## T-08 — Implement automated tests

Create pytest tests covering the defined test scenarios:

- Exact search by customer name.
- Search by surname.
- Search by full name.
- Search by email.
- Partial matches.
- Case-insensitive searches.
- Exact matches before partial matches.
- Alphabetical ordering for equal match priority.
- No matching customers.
- More than 10 matching customers.
- Maximum of 10 displayed results.
- Only full name and email displayed.
- Empty search input.
- Whitespace-only search input.
- Search execution using Enter.
- Invalid customer data.
- Search with up to 10,000 customers.
- Search response time within 2 seconds.

**Verification:**
- All implemented pytest tests pass.
- Tests provide coverage for the acceptance criteria and test scenarios defined in `SPEC.md`.

**Requirements Covered:**
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- FR-07
- FR-08
- NFR-01
- NFR-02
- NFR-03

---

## T-09 — Verify acceptance criteria and traceability

- Verify that each acceptance criterion in `SPEC.md` is satisfied by the implementation.
- Verify that the automated tests provide evidence for the applicable acceptance criteria.
- Verify the traceability between requirements, acceptance criteria, tasks, implementation, and tests.
- Run the complete pytest test suite after implementation.

**Verification:**
- All applicable acceptance criteria are verified.
- Every functional and non-functional requirement is covered by at least one task.
- The complete test suite passes.
- The requirement-to-test traceability is documented.

**Requirements Covered:**
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- FR-07
- FR-08
- NFR-01
- NFR-02
- NFR-03