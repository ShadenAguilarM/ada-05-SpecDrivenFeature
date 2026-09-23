# Architecture

## Overview

The Customer Search feature will be implemented as a small Python command-line application.

The application will use a local JSON file as its customer data source. The JSON file will be read-only for the search feature and will not require a database or external services.

The application will receive a search term through the CLI, validate the input, load the customer data from the JSON file, perform the search according to the rules defined in `SPEC.md`, order the matching customers, limit the results to a maximum of 10 customers, and display the results through the CLI.

The architecture is intentionally simple because the feature is a small local application and does not require persistent database infrastructure, external APIs, or a graphical interface.

## Components

The application will be divided into the following components:

- **CLI:** Receives the search input from the user and displays search results or validation/error messages.
- **Search Service:** Processes the search request and applies the search, matching, ordering, and result-limit rules.
- **Customer Data Loader:** Loads customer records from the local JSON file and provides them to the search service.
- **Customer Model:** Represents the customer data required by the search feature.
- **Tests:** pytest tests that verify the defined functional and non-functional behavior.

## Responsibilities

### CLI

The CLI is responsible for:

- Receiving the search term from the user.
- Allowing the user to execute the search by pressing Enter.
- Sending the search term to the Search Service.
- Displaying search results.
- Displaying validation and error messages.

The CLI shall not implement the search matching rules directly.

### Search Service

The Search Service is responsible for:

- Receiving the search term.
- Validating that the search term is not empty or whitespace-only.
- Performing case-insensitive searches.
- Searching by name, surname, full name, or email.
- Supporting exact and partial matches.
- Ordering exact matches before partial matches.
- Sorting results alphabetically when customers have the same match priority.
- Limiting the results to a maximum of 10 customers.
- Returning the matching customer records to the CLI.

### Customer Data Loader

The Customer Data Loader is responsible for:

- Reading customer records from the local JSON file.
- Providing the customer records to the Search Service.
- Handling invalid customer records without causing an unhandled application error during a search.

The Customer Data Loader shall not create, modify, or delete customer records.

### Customer Model

The Customer Model represents a customer using the fields required by the feature:

- `name`
- `surname`
- `email`

The full name used for searching and display shall be derived from `name` and `surname`.

### Tests

The test suite is responsible for:

- Verifying the functional requirements.
- Verifying validation rules.
- Verifying error handling.
- Verifying acceptance criteria.
- Verifying the result limit.
- Verifying the behavior with up to 10,000 customer records.
- Verifying the search response time requirement.

## Data Flow

The search operation will follow this flow:

1. The user enters a search term through the CLI.
2. The CLI receives the search term.
3. The CLI sends the search term to the Search Service.
4. The Search Service validates the search term.
5. If the search term is empty or contains only whitespace, the Search Service reports the validation error.
6. If the search term is valid, the Customer Data Loader loads the customer records from the local JSON file.
7. The Search Service evaluates the search term against the customer's name, surname, full name, and email.
8. The Search Service performs the comparison without distinguishing between uppercase and lowercase letters.
9. Matching customers are classified as exact or partial matches.
10. Exact matches are ordered before partial matches.
11. Customers with the same match priority are sorted alphabetically.
12. The Search Service limits the result set to a maximum of 10 customers.
13. The Search Service returns the results to the CLI.
14. The CLI displays each customer's full name and email address.
15. If no customers match the search term, the CLI displays `No customers found`.

## Interfaces

### Command-Line Interface

The application will provide a command-line interface through which the user enters a search term.

Conceptually:

```text
Enter search term: <query>
```

The user executes the search by pressing Enter.

The CLI displays either:

- The matching customers.
- `No customers found`.
- `Please enter a search term`.

### Search Service Interface

The Search Service will expose an operation that receives a search term and returns the matching customer records.

Conceptually:

```text
search(query) -> results
```

The returned result set will contain no more than 10 customers.

### Customer Data Interface

The Customer Data Loader will provide customer records loaded from the local JSON file.

Conceptually:

```text
load_customers() -> customers
```

The customer records will contain:

```text
name
surname
email
```

## Error Handling

The application shall handle the following cases:

- **Empty search string:** The search shall be rejected and the CLI shall display `Please enter a search term`.
- **Whitespace-only search string:** The search shall be rejected and the CLI shall display `Please enter a search term`.
- **No matching customers:** The CLI shall display `No customers found`.
- **Invalid customer data:** Invalid customer records shall not cause an unhandled application error during a search.
- **Unexpected input:** Invalid input shall be handled without producing an unhandled application error.

Sensitive customer information shall not be included in search results.

## Testing Strategy

Testing will be implemented using pytest.

Tests shall cover:

- Search by name.
- Search by surname.
- Search by full name.
- Search by email.
- Partial matches.
- Case-insensitive searches.
- Exact matches before partial matches.
- Alphabetical ordering for results with the same match priority.
- Searches with no results.
- Empty search strings.
- Whitespace-only search strings.
- Searches producing more than 10 matching customers.
- Verification that only full name and email are displayed.
- Search execution using Enter.
- Searches using up to 10,000 customers.
- Search response time according to NFR-01.

The test suite shall provide evidence for the acceptance criteria defined in `SPEC.md`.

## Dependencies

The application will depend on:

- Python 3.11 or higher.
- pytest for automated testing.
- Python standard libraries required to implement the feature.

The application shall not depend on:

- A database.
- Paid APIs.
- External services.
- A web or graphical interface.

## Design Decisions

### Local JSON Data Source

Customer records will be stored in a local JSON file.

This decision satisfies the requirement that the solution not require a database while providing a concrete and repeatable data source for the application.

The JSON file will be read-only for the Customer Search feature.

### Command-Line Interface

The minimum implementation will use a CLI.

A graphical or web interface is outside the scope of the feature, so a CLI provides the required interaction with less implementation complexity.

### Single Search Field

The CLI will provide one search field for all supported search criteria.

The same input will be evaluated against the customer's name, surname, full name, and email.

### Case-Insensitive Search

Search comparisons will not distinguish between uppercase and lowercase letters.

The search term and searchable customer values will be normalized before comparison.

### Exact Matches Before Partial Matches

Exact matches will be displayed before partial matches.

Customers with the same match priority will be sorted alphabetically to provide deterministic ordering.

### Result Limit

The application will display a maximum of 10 customers for each search.

Pagination and navigation between additional result pages are outside the scope of the feature.

### Minimal Dependencies

The implementation will use Python and pytest without requiring a database, paid API, or external service.

## Trade-offs

### JSON File vs. Database

Using a local JSON file keeps the implementation simple and satisfies the no-database constraint. However, it does not provide the persistence, concurrent access, or scalability characteristics of a database-based solution.

### CLI vs. Graphical Interface

A CLI reduces implementation complexity and is sufficient for the feature requirements. However, it does not provide the usability of a graphical or web interface.

### Fixed Result Limit vs. Pagination

Limiting each search to 10 results keeps the feature small and avoids implementing pagination. The trade-off is that customers beyond the first 10 matching results are not displayed by this feature.

### Local Data vs. External Service

Using a local JSON file keeps the application self-contained and avoids external dependencies. The trade-off is that the customer data is limited to the records contained in the local file.