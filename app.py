
from flask import Flask, render_template, request, redirect, url_for, jsonify,abort
from pydantic import BaseModel, Field, ValidationError

# Initialize the Flask application instance.
app = Flask(__name__)

# Maintain an in-memory counter for generating unique user IDs.
next_id = 3

# In-memory data store containing the initial user records.
# Dictionary keys represent unique user IDs, while values contain user details.
users = {
    1: {
        "username": "johndoe",
        "email": "johndoe@example.com"
    },
    2: {
        "username": "amit",
        "email": "amit@example.com"
    }
}

# -------------------------------------------------------------------
# GET /users
# Retrieve all registered users.
# -------------------------------------------------------------------
@app.route('/users', methods=['GET'])
def get_items():
    # Serialize the user records into a JSON-compatible HTTP response.
    return jsonify({"message": "Success", "users": list(users.values())})


# Define the request validation schema using Pydantic.
# Enforce mandatory fields and minimum input length requirements.
class ItemSchema(BaseModel):
    username: str = Field(..., min_length=2)
    email: str = Field(..., min_length=5)  


# -------------------------------------------------------------------
# POST /users
# Create a new user using the standard Flask route decorator.
# -------------------------------------------------------------------
@app.route('/users', methods=['POST'])
def create_item_standard():
    # Extract the JSON payload submitted by the client.
    data = request.get_json()

    # Verify that the request body contains a valid JSON object.
    if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid or missing JSON body"
            }), 400
    
    try:
        # Validate incoming request data against the Pydantic schema.
        item = ItemSchema(**data)
        
    except ValidationError as e:
        # Return structured validation details when input validation fails.
        return jsonify({"validation_errors": e.errors()}), 422

    # Access the application-level ID counter for unique ID generation.
    global next_id
        

    # Persist the validated user information in the in-memory data store.
    users[next_id] = {"username": item.username,
            "email":item.email}

    # Capture the assigned user ID and increment the counter for subsequent records.
    generated_id = next_id
    next_id += 1

   
    # Return the creation result with the generated ID and HTTP 201 status.
    return jsonify({
        "status": "success",
        "id": generated_id,
        "received": {
            "username": item.username,
            "email": item.email
        }
    }), 201



# -------------------------------------------------------------------
# PUT /users/<user_id>
# Update an existing user record identified by its unique ID.
# -------------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Verify that the requested user ID exists in the data store.
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404


    # Extract the JSON request payload without raising an exception
    # when the request body is missing or cannot be parsed.
    data = request.get_json(silent=True)

    # Ensure that the extracted payload is a valid JSON object.
    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    try:
        # Validate the updated user information against the defined schema.
        item = ItemSchema(**data)

    except ValidationError as e:
        # Return detailed validation errors with HTTP 422 status.
        return jsonify({
            "validation_errors": e.errors()
        }), 422

    # Replace the existing user record with the validated information.
    users[user_id] = {
        "username": item.username,
        "email": item.email
    }


    # Return the updated resource with HTTP 200 OK status.
    return jsonify({"message": "User updated successfully", "User": users[user_id]}), 200


# -------------------------------------------------------------------
# DELETE /users/<user_id>
# Remove an existing user record using its unique ID.
# -------------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_item(user_id):

    # Verify that the requested user exists before attempting deletion.
    if user_id not in users:
        return jsonify({
            "error": "User not found"
        }), 404

    # Remove the specified user record from the in-memory data store.
    del users[user_id]

    # Confirm successful deletion with an HTTP 200 OK response.
    return jsonify({
        "message": f"User {user_id} has been deleted"
    }), 200


# -------------------------------------------------------------------
# Application Entry Point
# Start the Flask development server when this script is executed directly.
# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
