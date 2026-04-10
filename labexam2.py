# Task 1: Library Management Class

class Library:
    """Manages a library's book inventory."""  # stores books as {title: bool}

    def __init__(self):
        self.books = {}                          # True=available, False=issued

    def add_book(self, title):
        """Add a book; warn if duplicate."""
        if title in self.books:
            print(f"'{title}' already exists.")
        else:
            self.books[title] = True
            print(f"'{title}' added.")

    def issue_book(self, title):
        """Issue a book; raise ValueError if missing or already issued."""
        if title not in self.books:
            raise ValueError(f"'{title}' not found.")
        if not self.books[title]:
            raise ValueError(f"'{title}' already issued.")
        self.books[title] = False
        print(f"'{title}' issued.")

    def return_book(self, title):
        """Return a book; raise ValueError if missing or not issued."""
        if title not in self.books:
            raise ValueError(f"'{title}' not found.")
        if self.books[title]:
            raise ValueError(f"'{title}' was not issued.")
        self.books[title] = True
        print(f"'{title}' returned.")

    def display_inventory(self):
        """Print all books with Available/Issued status."""
        print("\n--- Inventory ---")
        for title, avail in self.books.items():
            print(f"  {title:<25}: {'Available' if avail else 'Issued'}")
        print()


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    lib = Library()

    lib.add_book("The Alchemist")
    lib.add_book("1984")
    lib.add_book("1984")                     # duplicate warning
    lib.display_inventory()

    lib.issue_book("1984")
    lib.issue_book("The Alchemist")
    lib.display_inventory()

    for op, title in [(lib.issue_book, "1984"),          # already issued
                      (lib.issue_book, "Harry Potter"),  # not found
                      (lib.return_book, "The Alchemist"),
                      (lib.return_book, "The Alchemist")]:  # not issued
        try:
            op(title)
        except ValueError as e:
            print(f"Error: {e}")

    lib.display_inventory()

# ── Q4: How does documentation improve code usability? ───────────────────────
# Documentation makes code easier to understand and use.
# It helps developers work faster, avoid mistakes, and maintain code better.



