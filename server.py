from fastapi import FastAPI, Response, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


# from pydantic import BaseModel

from typing import *
import random



from views.list import createListTemplate
from views.book import createBookTemplate
from views.edit import editFormBook
from data.books import books


# from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



async def sendHtml(html):
    return Response(content=html, media_type="text/plain")




@app.get("/")
async def home():
    return FileResponse("templates/index.html")



@app.get("/books")
async def Books():
    return await sendHtml(await createListTemplate(books))




@app.delete("/books/{id}")
async def deleteBook(id: str):
    item = next(book for book in books if book["id"] == id)
    books.remove(item)

    return await sendHtml("")



@app.post("/books")
async def createBook(title: str = Form(), author: str = Form()):

    books.append({
        "id": str(random.randint(1, 10000000)),
        "title": title,
        "author": author
    })
    
    return await sendHtml(await createListTemplate(books))



@app.get("/books/edit/{id}")
async def editBook(id: str):
    item = next(book for book in books if book["id"] == id)
    
    return await sendHtml(await editFormBook(item))



@app.put("/books/{id}")
async def updateBook(id: str, title: str = Form(), author: str = Form()):
    
    item = next(book for book in books if book["id"] == id)
    idx = books.index(item)
    books[idx] = {
        "id": id,
        "title": title,
        "author": author
    }
    
    return await sendHtml(await createBookTemplate(books[idx]))



@app.post("/books/search")
async def searchBook(search: str = Form()):

    if search:
        try:
            items = next(book for book in books if search.lower() in book["title"].lower())
            return await sendHtml(await createListTemplate([items]))

        except Exception as e:
            return await sendHtml("<article>Книга не найдена</article>")
    else:
        return await sendHtml(await createListTemplate(books))
    
    





