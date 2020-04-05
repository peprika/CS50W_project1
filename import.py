# CS50W - Project 1
# This code will import books.csv into Heroku Postgress database
# It assumes you have a file called 'books.csv' and a datatable called 'books'

import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    # Open the file
    with open("books.csv", "r") as f:
        reader = csv.reader(f)
        count = 0
        print("File opened, import starting...")
        # Insert data into database
        for isbn, title, author, year in reader:
            if isbn == "isbn":
                print("Header row ignored")
            else:
                db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn":isbn, "title":title, "author":author, "year":year})
                # Progress indicator
                count += 1
                if count % 100 == 0:
                    print(f"{count} books added")
        # Commit to database
        db.commit()
        print(f"All done! {count} boooks added to database")
        
if __name__ == "__main__":
    main()