from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(
    app,
    version="1.0",
    title="Book Library API",
    description=(
        "A documented REST API for managing books, with validation, "
        "filtering, interactive Swagger UI, and OpenAPI specification export."
    ),
    doc="/docs",
)

books_namespace = api.namespace(
    "books",
    description="Book management operations",
)

books_db = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "isbn": "978-0451524935",
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "isbn": "978-0061120084",
    },
]

book_model = api.model(
    "Book",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique book identifier",
            example=1,
        ),
        "title": fields.String(
            required=True,
            description="Book title",
            example="The Great Gatsby",
        ),
        "author": fields.String(
            required=True,
            description="Author name",
            example="F. Scott Fitzgerald",
        ),
        "year": fields.Integer(
            required=True,
            description="Publication year",
            min=1000,
            max=2100,
            example=1925,
        ),
        "isbn": fields.String(
            description="ISBN number",
            example="978-0743273565",
        ),
    },
)

book_input_model = api.model(
    "BookInput",
    {
        "title": fields.String(
            required=True,
            description="Book title",
            example="Brave New World",
        ),
        "author": fields.String(
            required=True,
            description="Author name",
            example="Aldous Huxley",
        ),
        "year": fields.Integer(
            required=True,
            description="Publication year",
            min=1000,
            max=2100,
            example=1932,
        ),
        "isbn": fields.String(
            description="ISBN number",
            example="978-0060850524",
        ),
    },
)

error_model = api.model(
    "Error",
    {
        "message": fields.String(
            description="Human-readable error message",
            example="Book not found",
        )
    },
)

search_parser = reqparse.RequestParser()
search_parser.add_argument(
    "author",
    type=str,
    location="args",
    help="Filter by author name",
)
search_parser.add_argument(
    "year",
    type=int,
    location="args",
    help="Filter by publication year",
)


def find_book(book_id: int):
    return next(
        (book for book in books_db if book["id"] == book_id),
        None,
    )


@api.route("/")
class Health(Resource):
    @api.doc("service_health")
    def get(self):
        """Check whether the API is running."""
        return {
            "service": "Book Library API",
            "status": "operational",
            "documentation": "/docs",
            "openapi_specification": "/swagger.json",
        }


@books_namespace.route("/")
class BookList(Resource):
    @books_namespace.doc(
        "list_books",
        params={
            "author": "Filter results by author name",
            "year": "Filter results by publication year",
        },
        responses={
            200: "Books returned successfully",
        },
    )
    @books_namespace.expect(search_parser)
    @books_namespace.marshal_list_with(book_model)
    def get(self):
        """List books with optional author and year filters."""
        arguments = search_parser.parse_args()
        result = books_db

        if arguments.get("author"):
            author = arguments["author"].strip().lower()
            result = [
                book
                for book in result
                if author in book["author"].lower()
            ]

        if arguments.get("year") is not None:
            result = [
                book
                for book in result
                if book["year"] == arguments["year"]
            ]

        return result, 200

    @books_namespace.doc(
        "create_book",
        responses={
            201: "Book created successfully",
            400: "Invalid request or duplicate book",
        },
    )
    @books_namespace.expect(book_input_model, validate=True)
    @books_namespace.marshal_with(book_model, code=201)
    def post(self):
        """Create a new book."""
        payload = api.payload

        duplicate = next(
            (
                book
                for book in books_db
                if book["title"].strip().lower()
                == payload["title"].strip().lower()
                and book["author"].strip().lower()
                == payload["author"].strip().lower()
            ),
            None,
        )

        if duplicate:
            api.abort(400, "A book with this title and author already exists")

        next_id = max(
            (book["id"] for book in books_db),
            default=0,
        ) + 1

        new_book = {
            "id": next_id,
            "title": payload["title"].strip(),
            "author": payload["author"].strip(),
            "year": payload["year"],
            "isbn": payload.get("isbn"),
        }

        books_db.append(new_book)
        return new_book, 201


@books_namespace.route("/<int:book_id>")
@books_namespace.param(
    "book_id",
    "Unique book identifier",
)
class Book(Resource):
    @books_namespace.doc(
        "get_book",
        responses={
            200: "Book returned successfully",
            404: "Book not found",
        },
    )
    @books_namespace.marshal_with(book_model)
    def get(self, book_id):
        """Retrieve a book by ID."""
        book = find_book(book_id)

        if book is None:
            api.abort(404, f"Book {book_id} not found")

        return book, 200

    @books_namespace.doc(
        "update_book",
        responses={
            200: "Book updated successfully",
            404: "Book not found",
        },
    )
    @books_namespace.expect(book_input_model, validate=True)
    @books_namespace.marshal_with(book_model)
    def put(self, book_id):
        """Replace an existing book."""
        book = find_book(book_id)

        if book is None:
            api.abort(404, f"Book {book_id} not found")

        payload = api.payload

        book.update(
            {
                "title": payload["title"].strip(),
                "author": payload["author"].strip(),
                "year": payload["year"],
                "isbn": payload.get("isbn"),
            }
        )

        return book, 200

    @books_namespace.doc(
        "delete_book",
        responses={
            204: "Book deleted successfully",
            404: "Book not found",
        },
    )
    def delete(self, book_id):
        """Delete a book."""
        book = find_book(book_id)

        if book is None:
            api.abort(404, f"Book {book_id} not found")

        books_db.remove(book)
        return "", 204


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )
