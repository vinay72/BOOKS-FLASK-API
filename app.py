from flask import Flask, jsonify,request, Response
import json

app = Flask(__name__)

books= [ {
        'name':'Rich Dad Poor Dad',
        'price': 198,
        'isbn': 9781612680019
    },

    {
        'name':'Think & Grow Rich',
        'price':99,
        'isbn':9788192910918
    }
]
#GET /books/9781612680019
#GET /books

@app.route('/books')
def get_books():
    return jsonify({'books': books})

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
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrMsg = {
            "error": "Invalid book object  passed in request",
            "helpString": "{'name': 'bookName','price': 100,'isbn': 9788195343410918}"
        }
        response = Response(json.dumps(invalidBookObjectErrMsg), status=400, mimetype='application/json')
        return response


# right hand side isbn is a variable
# left hand side isbn is an isbn from books dictionary
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
app.run(port=5000)  
        
