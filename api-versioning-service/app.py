from datetime import datetime, timezone

from flask import Flask, jsonify, request

from versioning_utils import deprecated_version, version_response


app = Flask(__name__)


users_db = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "created_at": "2026-01-15T10:30:00+00:00",
    },
    2: {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@example.com",
        "created_at": "2026-02-10T14:45:00+00:00",
    },
}


def format_user_v1(user):
    """Return the stable v1 response contract."""
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
    }


def format_user_v2(user):
    """Return the enhanced v2 response contract."""
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "version": "v2",
    }


@app.get("/")
def health_check():
    return jsonify(
        {
            "service": "API Versioning Service",
            "status": "healthy",
            "supported_versions": ["v1", "v2"],
        }
    )


@app.get("/api/v1/users")
@deprecated_version("Fri, 31 Dec 2027 23:59:59 GMT")
def get_users_v1():
    users = [format_user_v1(user) for user in users_db.values()]

    return version_response(
        {
            "data": users,
            "count": len(users),
        },
        "v1",
    )


@app.get("/api/v1/users/<int:user_id>")
@deprecated_version("Fri, 31 Dec 2027 23:59:59 GMT")
def get_user_v1(user_id):
    user = users_db.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return version_response(format_user_v1(user), "v1")


@app.get("/api/v2/users")
def get_users_v2():
    users = [format_user_v2(user) for user in users_db.values()]

    return jsonify(
        {
            "data": users,
            "count": len(users),
            "version": "v2",
        }
    )


@app.get("/api/v2/users/<int:user_id>")
def get_user_v2(user_id):
    user = users_db.get(user_id)

    if user is None:
        return jsonify(
            {
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": "User not found",
                },
                "version": "v2",
            }
        ), 404

    return jsonify(format_user_v2(user))


@app.post("/api/v2/users")
def create_user_v2():
    if not request.is_json:
        return jsonify(
            {
                "error": {
                    "code": "UNSUPPORTED_MEDIA_TYPE",
                    "message": "Content-Type must be application/json",
                },
                "version": "v2",
            }
        ), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            {
                "error": {
                    "code": "INVALID_JSON",
                    "message": "Request body must contain a valid JSON object",
                },
                "version": "v2",
            }
        ), 400

    name = data.get("name")
    email = data.get("email")

    if not isinstance(name, str) or not name.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "The name field is required",
                },
                "version": "v2",
            }
        ), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "The email field is required",
                },
                "version": "v2",
            }
        ), 400

    normalised_email = email.strip().lower()

    if any(
        existing_user["email"].lower() == normalised_email
        for existing_user in users_db.values()
    ):
        return jsonify(
            {
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "A user with this email already exists",
                },
                "version": "v2",
            }
        ), 409

    new_user_id = max(users_db.keys(), default=0) + 1

    new_user = {
        "id": new_user_id,
        "name": name.strip(),
        "email": normalised_email,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    users_db[new_user_id] = new_user

    response = jsonify(format_user_v2(new_user))
    response.status_code = 201
    response.headers["Location"] = f"/api/v2/users/{new_user_id}"

    return response


@app.errorhandler(404)
def handle_not_found(_error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def handle_method_not_allowed(_error):
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
