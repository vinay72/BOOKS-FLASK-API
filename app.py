from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)

books = [
    {
        'name': 'Think & Grow Rich',
        'price': 7.99,
        'isbn': 987654321098
    },
    {
        'name': 'Rework',
        'price': 6.99,
        'isbn': 945673292394
    }
]


#GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})


#POST /books
# {
#     'name': 'fweve',
#     'price': 4.67,
#     'isbn': 745321609824
# }
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

#books/isbn_number
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers["Location"] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in the request",
            "helpString": "{'name': 'Think & Grow Rich','price': 7.99,'isbn': 987654321098}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


    

#GET /books/987654321098
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    print(type(isbn))
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

#PATCH /books/987654321098
# {
#     'name': 'Harry Potter and The Chamber of Secrets',
# }
# {
#     'price': '8.99',
# }
@app.route('/books/<int:isbn>', methods = ['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data['name']
    if("price" in request_data):
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


#PATCH /books/987654321098

@app.route('/books/<int:isbn>', methods=["PUT"])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


#DELETE /books/945673292394
#Body { 'name': 'dfbgbgbdb'}
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response
        


app.run(port=5001,debug='true')    
