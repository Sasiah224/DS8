class Contact:
    """Represent a contact with a name and phone number."""

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    """Store a contact in a linked list."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """Store contacts using separate chaining for collisions."""

    def __init__(self, size=10):
        if size <= 0:
            raise ValueError("Table size must be greater than zero.")

        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        total = 0
        for character in key:
            total += ord(character)
        return total % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        current = self.data[index]

        # Update an existing contact instead of adding a duplicate.
        while current is not None:
            if current.key == key:
                current.value.number = value
                return
            current = current.next

        # Add the new contact to the beginning of the linked list.
        contact = Contact(key, value)
        new_node = Node(key, contact)
        new_node.next = self.data[index]
        self.data[index] = new_node

    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def print_table(self):
        for index in range(self.size):
            current = self.data[index]
            print(f"Index {index}:", end="")

            if current is None:
                print(" Empty")
            else:
                while current is not None:
                    print(f" - {current.value}", end="")
                    current = current.next
                print()


if __name__ == "__main__":
    # Test Contact and Node.
    contact_1 = Contact("Riley", "123-456-7890")
    node_1 = Node(contact_1.name, contact_1)
    assert str(contact_1) == "Riley: 123-456-7890"
    assert node_1.key == "Riley"
    assert node_1.value is contact_1
    assert node_1.next is None

    # Test an empty table.
    table = HashTable(10)
    print("EMPTY TABLE")
    table.print_table()
    assert table.search("John") is None

    # Insert contacts.
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")

    print("\nAFTER INSERTING CONTACTS")
    table.print_table()

    contact = table.search("John")
    print("\nSearch result:", contact)
    assert contact.number == "909-876-1234"

    # Amy and May have the same character sum, so they collide.
    assert table.hash_function("Amy") == table.hash_function("May")
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")

    print("\nAFTER COLLISION TEST")
    table.print_table()
    assert table.search("Amy").number == "111-222-3333"
    assert table.search("May").number == "222-333-1111"

    # Update an existing contact.
    table.insert("Rebecca", "999-444-9999")

    print("\nAFTER UPDATING REBECCA")
    table.print_table()
    assert table.search("Rebecca").number == "999-444-9999"

    # Check that updating did not create a duplicate.
    current = table.data[table.hash_function("Rebecca")]
    matches = 0
    while current is not None:
        if current.key == "Rebecca":
            matches += 1
        current = current.next
    assert matches == 1

    # Test a missing contact.
    print("\nMissing contact:", table.search("Chris"))
    assert table.search("Chris") is None

    print("\nAll tests passed!")

