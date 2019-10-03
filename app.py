from flask import Flask, jsonify,request,Response
import test

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

 

@app.route('/books', methods=['POST'])
def add_book():
    return jsonify(request.get_json())


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