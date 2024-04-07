import menu
import mysql_manager

while True:
    menu.menu()
    choice = int(input())

    if choice == 0: # Exit from the App
        break
    if choice == 1: # This option prints all the books present in library
        mysql_manager.show_all_books()
    elif choice == 2: # Shows all Issued books
        mysql_manager.show_issued_books()
    elif choice == 3: # Issue book
        mysql_manager.issue_book()
    elif choice == 4: # Return book
        mysql_manager.return_book()
    elif choice == 5: # Add a book
        mysql_manager.add_book()
    else:
        print("Please enter a valid choice")
