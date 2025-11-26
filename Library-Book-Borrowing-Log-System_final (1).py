import re

borrowed_books = []

book_list = [
    {"title": "Python", "quantity": 1},
    {"title": "Java", "quantity": 2},
    {"title": "C++ Programming Guide", "quantity": 1},
    {"title": "JavaScript Fundamentals", "quantity": 1},
    {"title": "Hdmi", "quantity": 1}
]

book_copies = {
    book['title']: [{'borrowed': False} for _ in range(book['quantity'])]
    for book in book_list
}

waitlist = {book['title']: [] for book in book_list}

accounts = {
    "librarian": {"username": "lib01", "password": "12345"},
}

students = {
    "02-2526-032589": "ASANULLA AMINA MOLINA",
    "02-2526-020171": "BACORNAY, VERHEL",
    "02-2324-05266": "BELTRAN, ANDRIE JAY A.",
    "02-2324-03381": "CABAHUG, BENCH M.",
    "02-2526-031913": "CABANES PHOEBE JADE MARAON",
    "02-2526-000422": "CAGATIN, FRITZ DENVER JOHN",
    "02-2526-015028": "CASUMPANG PRINCESS DIVINE C.",
    "02-2526-032069": "CIELO, Eliza Nina Marie P.",
    "02-2526-012898": "CUYNO, DEXTER P.",
    "02-2526-032411": "FLORENDO, JOSUA E.",
    "02-2526-031862": "GUBAT MEL ANJELO L.",
    "02-2526-032010": "HAMILI MARCJHON A.",
    "02-2324-12849":  "JAMAR, JOHN CLINT A.",
    "02-2526-031945": "LOPENA, NOEL JOHN B.",
    "02-2526-032295": "LUSTERIO, KERBY ADRIENE H.",
    "03-2526-015026": "MORALES, HERCIE JEAN Y.",
    "02-2526-020166": "OCO, HERSHEY GABRIELLE C.",
    "02-2526-032282": "PADILLA, NICOLE",
    "02-2526-017718": "PAGTALUNAN VINCENT DAVE E",
    "02-2526-032012": "PAYOT, LEEPRIL",
    "02-2526-032033": "RANAO, CLYDE MARK D.",
    "02-2526-032068": "SACAY, APRIL MAE M.",
    "02-2526-000251": "SALVALEON, FELY M.",
    "02-2526-030760": "UY, PRINCE RUSSEL D.",
    "02-2526-032104": "TAN, ANDREW L.",
    "02-2526-011675": "LONGOS, EZEQUEL KASHMER",
    "02-2526-017243": "JEMENIA, MELVIN L.",
    "02-2526-032146": "GO, EZEKEIL LEO P.",
    "02-2526-032400": "ARENDAIN, QUEEN PRINCESS L.",
    "02-2324-08493": "LLABAN, ALLISON B."
}

pending_requests = []
approved_students = []

def validate_id(id_str):
    return bool(re.match(r"^\d{2}-\d{4}-\d{5,6}$", id_str))

def login():
    print("\n== LIBRARY BOOK BORROWING LOG ==")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        for acc in accounts.values():
            if username == acc["username"] and password == acc["password"]:
                print(f"\nLogin Successful! Welcome {username}\n")
                return
        print("Invalid Username or Password! Try again.\n")

def library_menu():
    while True:
        print("\n== LIBRARY MENU ==")
        print("1. Librarian")
        print("2. Student")
        print("3. Back to Main Menu")
        choice = input("\nEnter choice (1-3): ")

        if choice == '1':
            librarian_functions()
        elif choice == '2':
            student_functions()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

def librarian_functions():
    while True:
        print("\n --LIBRARIAN-- ")
        print("1. Record borrower and book")
        print("2. Update borrowed list / Mark book as returned")
        print("3. Back to Library Menu")
        choice = input("\nEnter choice (1-3): ")

        if choice == '1':
            record_borrower()
        elif choice == '2':
            update_borrowed_books()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

def record_borrower():
    if not pending_requests:
        print("No pending requests.")
        return

    print("\nPending Student Requests:")
    for i, req in enumerate(pending_requests, start=1):
        print(f"{i}. {req['id']} | {req['name']} | Book: {req['book']}")

    selected = input("Enter Student IDs to approve (comma-separated) or 'N' to skip: ")
    if selected.upper() == 'N':
        return

    selected_ids = [s.strip() for s in selected.split(",")]

    for sid in selected_ids:
        found = False
        for req in pending_requests:
            if req['id'] == sid:

                available_copy = next((copy for copy in book_copies[req['book']] if not copy['borrowed']), None)

                if available_copy:
                    due = input(f"Set due date for {req['name']} (YYYY-MM-DD): ")
                    available_copy['borrowed'] = True
                    borrowed_books.append({
                        'id': req['id'],
                        'name': req['name'],
                        'book': req['book'],
                        'due': due,
                        'returned': False
                    })
                    print(f"{req['name']} has successfully borrowed {req['book']}.")
                else:
                    waitlist[req['book']].append(req)
                    print(f"No copy available. {req['name']} added to waitlist for {req['book']}.")

                pending_requests.remove(req)
                found = True
                break

        if not found:
            print(f"ID {sid} not found in pending requests.")

def update_borrowed_books():
    print("\n1. Display Borrowed Books")
    print("2. Mark as Returned")
    sub = input("Enter choice (1-2): ")

    if sub == '1':
        display_books_status_due()
        return

    elif sub == '2':
        book_name = input("Enter book title: ")

        for b in borrowed_books:
            if b['book'].lower() == book_name.lower() and not b['returned']:
                b['returned'] = True

                for copy in book_copies[book_name]:
                    if copy['borrowed']:
                        copy['borrowed'] = False
                        break

                print(f"{book_name} has been marked as returned.")

                if waitlist[book_name]:
                    next_s = waitlist[book_name].pop(0)
                    due = input(f"Assign returned copy to waitlisted {next_s['name']}. Enter due date: ")
                    for copy in book_copies[book_name]:
                        if not copy['borrowed']:
                            copy['borrowed'] = True
                            break
                    borrowed_books.append({
                        'id': next_s['id'],
                        'name': next_s['name'],
                        'book': next_s['book'],
                        'due': due,
                        'returned': False
                    })
                    print(f"Waitlisted student {next_s['name']} has now borrowed {book_name}.")
                return

        print("Book not found or already returned.")
    else:
        print("Invalid input!")

def display_books_status_due():
    print("\n== LIST OF BOOKS ==")
    print(f"{'No.':<5}{'Title':<30}{'Status':<40}{'Due Date'}")
    print("-" * 95)

    for i, book in enumerate(book_list, start=1):
        borrowed_list = [b for b in borrowed_books if b['book'] == book['title'] and not b['returned']]

        if borrowed_list:
            names = ", ".join([b['name'] for b in borrowed_list])
            due = ", ".join([b['due'] for b in borrowed_list])
            status = f"Borrowed by {names}"
        else:
            status = "Available"
            due = "-"

        if waitlist[book['title']]:
            wait_names = ", ".join([s['name'] for s in waitlist[book['title']]])
            status += f" | Waitlist: {wait_names}"

        print(f"{i:<5}{book['title']:<30}{status:<40}{due}")

def student_functions():
    while True:
        print("\n-- STUDENT --")
        print("1. Request Book")
        print("2. View Due Date")
        print("3. Back to Library Menu")
        choice = input("\nEnter choice (1-3): ")

        if choice == '1':
            request_book()
        elif choice == '2':
            view_due_date()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

def request_book():
    while True:
        id = input("Enter Your ID: ")
        if validate_id(id):
            break
        print("Invalid ID format! Example: 02-2526-012345")

    if id not in students:
        print("ID does not exist in system.")
        return

    if any(req['id'] == id for req in pending_requests):
        print("You already have a pending request.")
        return

    book = input("Enter Book Title: ")

    pending_requests.append({'id': id, 'name': students[id], 'book': book})
    print("Book request submitted. Waiting for librarian approval.")

def view_due_date():
    id = input("Enter your ID: ")

    found_books = [b for b in borrowed_books if b['id'] == id and not b['returned']]

    if not found_books:
        print("No borrowed books found.")
        return

    print(f"\nBorrowed Books for {students[id]}:")
    print(f"{'No.':<5}{'Book Title':<35}{'Due Date'}")
    print("-" * 60)

    for i, b in enumerate(found_books, start=1):
        print(f"{i:<5}{b['book']:<35}{b['due']}")

while True:
    print("\n== LIBRARY BOOK BORROWING LOG ==")
    print("1. Login")
    print("2. Exit")
    first_choice = input("\nEnter choice (1-2): ")

    if first_choice == '1':
        login()

        while True:
            print("\n== MAIN MENU ==")
            print("1. Library")
            print("2. Log Out")
            main_choice = input("\nEnter choice (1-2): ")

            if main_choice == '1':
                library_menu()
            elif main_choice == '2':
                print("Logging out...")
                break
            else:
                print("Invalid option!")

    elif first_choice == '2':
        print("\nThank you for using the Library Book Borrowing Log System!")
        break

    else:
        print("Invalid input!")

