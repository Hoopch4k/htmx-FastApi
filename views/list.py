# from data.books import books
from views.book import createBookTemplate

async def list(books):

    result = ''
    for book in books:
        result += await createBookTemplate(book)
    return result


async def createListTemplate(books):

    return f'''
<ul>
    {await list(books)}
</ul>
'''
