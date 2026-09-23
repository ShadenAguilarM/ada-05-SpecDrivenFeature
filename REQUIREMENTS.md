# Requirements — Customer Search 
 
## User Story 
As a user, 
I want to search customers by name or email, 
so that I can quickly find the customer record I need. 
 
## Functional Requirements 
* FR-01: The system shall allow users to search customers by name, surname, full name, or email address.
* FR-02: The system shall accept partial matches and display customers whose name, surname, or email address contains the search string entered by the user. 
* FR-03: The system shall perform searches without distinguishing between uppercase and lowercase letters.
* FR-04: The system shall display exact matches before partial matches.
* FR-05: The system shall display the message "No customers found" when no customers match the search criteria.
* FR-06:The system shall display a maximum of 10 results per search.
* FR-07: The system shall only display each customer's name and email address in the search results.
* FR-08: The system shall display the message "Please enter a search term" when the search field is empty or contains only whitespace characters.

## Non-Functional Requirements 
* NFR-01: The system shall return search results within 2 seconds.
* NFR-02: The system shall support searches with up to 10,000 registered customers without generating errors.
* NFR-03: The system should allow users to perform a search by pressing Enter after entering the text. 

## Open Questions 
No open questions remain.

## Constraints / Assumptions 
* C-01: The minimum implementation shall use Python 3.11+, CLI, and pytest.
* C-02: The solution shall not require a database.
* C-03: No paid APIs or external services.
* A-01: Customer data shall be stored in a local JSON file. The application shall load the customer records from the JSON file when performing a search.
