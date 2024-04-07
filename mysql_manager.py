import mysql.connector

# Replace these values with your MySQL server information
host = "localhost" #enter your host name
user = "root" #enter user
password = "1234" #enter password
database = "library" #enter table name

def show_all_books():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Check if the connection was successful
    if connection.is_connected():
        print("Connected to MySQL")
    else:
        print("Connection to MySQL failed")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Execute a query to select all rows from the table
    query = "SELECT * FROM books"  # Assuming your table is named "books"
    cursor.execute(query)

    # Fetch and print the results
    for row in cursor.fetchall():
        print(row)

    # Close the cursor and the connection
    cursor.close()
    connection.close()

def show_issued_books():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # Check if the connection was successful
    if connection.is_connected():
        print("Connected to MySQL")
    else:
        print("Connection to MySQL failed")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Execute a query to select all rows from the table
    query = "SELECT * FROM issued_books where sr_no >0"  # Assuming your table is named "books"
    cursor.execute(query)

    # Fetch and print the results
    print("Sr No. \tBook-ID \tStudent-ID")
    for row in cursor.fetchall():
        print("{} \t{} \t\t{}".format(row[0], row[1], row[2]))

    # Close the cursor and the connection
    cursor.close()
    connection.close()

def add_book():
    # 1. ask user to provide book and author name
    book_name = input("Enter name of the book: ")
    author_name = input("Enter name of the author: ")
    total_copies = int(input("Enter total no. of copies: "))
    current_copied = total_copies
    
    # 2. connect to database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # 3. insert into table
    cursor = connection.cursor()
    insert_query = "INSERT INTO books (book_name, author_name, total_copies, current_copies) VALUES (%s, %s, %s, %s)"
    data = (book_name, author_name, total_copies, current_copied)

    cursor.execute(insert_query, data)
    connection.commit()

    # 4. close the connection
    cursor.close()
    connection.close()

def issue_book():
    # 1. books -> issued->issued_books
    book_serial_no = int(input("Enter Book-ID: "))
    student_id = int(input("Please enter student_id: "))
   # 2. connect to database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Check if student issued any copy of the same book earlier
    query = "SELECT * FROM issued_books WHERE book_id = {} AND student_id = {}".format(book_serial_no, student_id)
    cursor.connection()
    cursor.execute(query)
    existing_rows = cursor.fetchall()

    if existing_rows:
        print("Student has already issued this book")

    # Find the sr no
    query  = "SELECT current_copies, issued_copies FROM books where books.sr_no = {}".format(book_serial_no)
    cursor = connection.cursor()
    cursor.execute(query)

    copies_count = cursor.fetchall()
    current_copies, issued_copies = copies_count[0][0], copies_count[0][1]
    

    if current_copies == 0: 
        print("Book is not availble yet, all copies are issued")
        return
    
    #change current to current-1
    current_copies = current_copies - 1
    query = "Update books set current_copies = {} where books.sr_no = {}".format(current_copies, book_serial_no)
    cursor.execute(query)
    connection.commit()

    #change issued to issued+1
    issued_copies = issued_copies + 1
    query = "Update books set issued_copies = {} where books.sr_no = {}".format(issued_copies, book_serial_no)
    cursor.execute(query)
    connection.commit()

    #insert users data into issued_books tables
    query = "insert into issued_books(book_id, student_id) values({}, {})".format(book_serial_no, student_id)
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def return_book():
    book_serial_no = int(input("Enter Book-ID: "))
    student_id = int(input("Please enter student_id: "))
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    #find the sr no
    query  = "SELECT current_copies, issued_copies FROM books where books.sr_no = {}".format(book_serial_no)
    cursor = connection.cursor()
    cursor.execute(query)

    copies_count = cursor.fetchall()
    current_copies, issued_copies = copies_count[0][0], copies_count[0][1]
    
    if issued_copies == 0: 
        print("No copies are issued, Please enter a valid book and student id")
        return
    
    #change current to current+1
    current_copies = current_copies + 1
    query = "Update books set current_copies = {} where books.sr_no = {}".format(current_copies, book_serial_no)
    cursor.execute(query)
    connection.commit()

    #change issued to issued-1
    issued_copies = issued_copies - 1
    query = "Update books set issued_copies = {} where books.sr_no = {}".format(issued_copies, book_serial_no)
    cursor.execute(query)
    connection.commit()

    #insert users data into issued_books tables
    query = "DELETE FROM issued_books WHERE book_id = {} AND student_id = {}".format(book_serial_no, student_id)
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


