"""Customer model representation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Represents a customer record.

    Attributes:
        name: Customer's first name.
        surname: Customer's last name.
        email: Customer's email address.
    """

    name: str
    surname: str
    email: str

    @property
    def full_name(self) -> str:
        """Derive the customer's full name from name and surname.

        According to SR-02, the full name is represented as the customer's name,
        followed by a single space, followed by the customer's surname.
        """
        return f"{self.name} {self.surname}"
