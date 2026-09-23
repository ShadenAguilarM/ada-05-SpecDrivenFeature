# Customer Search Feature - Specification

## Goal

Provide a command-line customer search feature that allows users to find customer records using the search criteria defined in `REQUIREMENTS.md`.

## Requirements Covered

This specification implements:

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

## Scope

The feature includes:

- A single search field for entering the search term.
- Searching customers by name, surname, full name, or email address.
- Partial and exact matches.
- Case-insensitive searching.
- Ordering exact matches before partial matches.
- Displaying a maximum of 10 results per search.
- Displaying only the customer's name and email address in search results.
- Rejecting empty or whitespace-only search input.
- Displaying a message when no customers match the search criteria.
- Executing searches through the command-line interface.
- Loading customer data from a local JSON file.

## Out of Scope

The following functionality is outside the scope of this feature:

- Creating, editing, or deleting customers.
- Customer authentication or account management.
- Database integration.
- External APIs or paid services.
- Displaying customer information other than name and email in search results.
- Defining a graphical or web interface.
- Modifying customer data.
- Pagination or navigation between multiple result pages.

## Domain Model

### Customer

A customer record shall contain at least the following fields:

- `name`: customer's first name.
- `surname`: customer's last name.
- `email`: customer's email address.

Customer records shall be stored in a local JSON file.

The JSON data source is read-only for this feature. Customer records are not created, edited, or deleted by the search functionality.

## Search Rules

### SR-01 — Single Search Field

Requirement: FR-01

The CLI shall provide one search field for entering the search term.

The same search field shall be used to search by:

- Name.
- Surname.
- Full name.
- Email address.

### SR-02 — Search Fields

Requirement: FR-01

The search term shall be evaluated against the customer's:

- name
- surname
- full name
- email

The full name shall be represented as the customer's name, followed by a single space, followed by the customer's surname.

### SR-03 — Partial Matching

Requirement: FR-02

A partial match occurs when the search string is contained within the normalized value of at least one searchable field.

### SR-04 — Case Insensitivity

Requirement: FR-03

Search comparison shall be case-insensitive. The search string and searchable customer values shall be normalized before comparison.

### SR-05 — Exact Match

Requirement: FR-04

An exact match occurs when the normalized search string is equal to the normalized value of at least one searchable field.

### SR-06 — Result Ordering

Requirement: FR-04

Search results shall be ordered so that customers with an exact match are displayed before customers with only partial matches. When multiple customers have the same match priority, they shall be sorted alphabetically.

### SR-07 — Result Limit

Requirement: FR-06

The search results displayed for a search shall contain no more than 10 customers. If more than 10 customers match the search, only the first 10 matching customers shall be displayed.

### SR-08 — Displayed Fields

Requirement: FR-07

Each search result shall display only:

- Customer full name.
- Customer email address.

### SR-09 — No Results

Requirement: FR-05

When no customers match the search criteria, the CLI shall display:

`No customers found`.

### SR-10 — Search Execution

Requirement: NFR-03

The user shall be able to execute the search by pressing Enter after entering a search term in the search field.

### SR-11 — Empty and Whitespace-Only Input

Requirement: FR-08

A search input containing no characters or only whitespace characters shall not be executed. The CLI shall display:

`Please enter a search term`.

## Validation Rules

### VR-01 — Search Input

Requirement: FR-08

The search field shall accept text input.

### VR-02 — Empty Input

Requirement: FR-08

An empty search field shall be rejected before the search operation is executed.

### VR-03 — Whitespace-Only Input

Requirement: FR-08

A search field containing only whitespace characters shall be rejected before the search operation is executed.

### VR-04 — Customer Data

Requirement: NFR-02

Customer records loaded from the JSON file shall provide the fields required by the domain model.

Invalid customer records shall not cause an unhandled application error during a search.

## Error Handling

### EH-01 — Empty Search

Requirement: FR-08

If the search field is empty, the application shall display:

`Please enter a search term`.

The search shall not be executed.

### EH-02 — Whitespace-Only Search

Requirement: FR-08

If the search field contains only whitespace characters, the application shall display:

`Please enter a search term`.

The search shall not be executed.

### EH-03 — No Matches

Requirement: FR-05

If no customer matches the search criteria, the application shall display:

`No customers found`.

### EH-04 — Invalid Customer Data

Requirement: NFR-02

Invalid customer data shall be handled without producing an unhandled application error.

## Acceptance Criteria

### AC-01

Given there are registered customers in the system,

When the user enters a customer's name into the search field,

Then the system shall display the corresponding customer.

### AC-02

Given a registered customer exists with a specific email address,

When the user enters that email address into the search field,

Then the system shall display the corresponding customer.

### AC-03

Given there are customers whose names or email addresses contain a specific text string,

When the user enters only a substring of that text,

Then the system shall display customers whose first name, last name, full name, or email address contains that string.

### AC-04

Given a customer exists whose first name, last name, or email address contains a specific text string,

When the user performs a search using that string in uppercase, lowercase, or a combination of both,

Then the system shall display the same results regardless of character casing.

### AC-05

Given no customer matches the entered search term,

When the user performs the search,

Then the system shall display the message "No customers found".

### AC-06

Given there are customers with both exact and partial matches for the entered term,

When the user performs the search,

Then the system shall display exact matches first, followed by partial matches.

### AC-07

Given more than 10 customers match the entered search term,

When the user performs the search,

Then the system shall display no more than 10 customers.

### AC-08

Given one or more customers match the entered search term,

When the search results are displayed,

Then each result shall contain only the customer's full name and email address.

### AC-09

Given the search field is empty or contains only whitespace characters,

When the user performs the search,

Then the system shall display "Please enter a search term" and shall not execute the search.

### AC-10

Given the user has entered a valid search term,

When the user presses Enter,

Then the system shall execute the search.

### AC-11

Given the system contains up to 10,000 registered customers,

When the user performs a search,

Then the system shall process the search without generating an application error and return the results within 2 seconds.

## Test Scenarios

| ID | Scenario | Expected Result |
|---|---|---|
| TS-01 | Search using an exact customer name | The matching customer is displayed. |
| TS-02 | Search using a surname | Customers matching the surname are displayed. |
| TS-03 | Search using a full name | The corresponding customer is displayed. |
| TS-04 | Search using an email address | The corresponding customer is displayed. |
| TS-05 | Search using part of a name | Customers containing the search string are displayed. |
| TS-06 | Search using uppercase and lowercase variations | The same matching customers are returned. |
| TS-07 | Search producing exact and partial matches | Exact matches appear before partial matches. |
| TS-08 | Search with no matching customers | "No customers found" is displayed. |
| TS-09 | Search producing more than 10 results | A maximum of 10 results is displayed. |
| TS-10 | Display search results | Only customer full name and email are displayed. |
| TS-11 | Search with an empty or whitespace-only input | "Please enter a search term" is displayed and the search is not executed. |
| TS-12 | Execute a valid search using Enter | The search is executed. |
| TS-13 | Search using up to 10,000 customers | The search completes without an application error and within 2 seconds. |

## Constraints

- C-01
- C-02
- C-03

The implementation shall use the assumption:

- A-01

## Open Questions

No open questions remain.