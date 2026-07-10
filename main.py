from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


#  we use pydantic to validate client data
app=FastAPI()
books = [
    {
        "id": 1,
        "title": "The Guide",
        "author": "R K Narayan",
        "genre": "Fiction",
        "language": "English"
    },
    {
        "id": 2,
        "title": "Wings of Fire",
        "author": "A P J Abdul Kalam",
        "genre": "Biography",
        "language": "English"
    }
]

class Bookcreate(BaseModel):
    title: str
    genre: str
    author: str
    language: str

class Bookupdate(BaseModel):
    title: str
    genre: str
    author: str
    language: str


@app.get("/books")
def get_books():
    return books

@app.post("/books",status_code=201)
def create_book(book:Bookcreate):
    new_id=max((book["id"] for book in books),default=0)+1
    new_book={
        "id":new_id,
        "title": book.title,
        "genre": book.genre,
        "author": book.author,
        "language": book.language
    }
    books.append(new_book)
    return {
        "message":"Book Added Sucessfully !!!",
        "book":new_book
    }


@app.put('/books/{book_id}')
def update_book(book_id:int,book:Bookupdate):
    for existing_book in books:
        if existing_book["id"]==book_id:
            # existing_book["title"]=book.title
            # existing_book["author"]=book.author
            # existing_book["genre"]=book.genre
            # existing_book["language"]=book.language
            existing_book.update(book.model_dump()) # --- one line did the work of 4
            return{
                "Message":"Book Updated Succesfully !!!",
                "Book":existing_book
            }
    raise HTTPException(status_code=404,detail="Book Not Found !!!")
