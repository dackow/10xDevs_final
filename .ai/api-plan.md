# REST API Plan

## 1. Resources

-   **User**: Represents user accounts. Mapped to the `users` table.
-   **Token**: Represents the authentication token for a user. Not a database table, used for authentication.
-   **FlashcardSet**: Represents a collection of flashcards. Mapped to the `flashcard_sets` table.
-   **Flashcard**: Represents a single flashcard. Mapped to the `flashcards` table.
-   **AI**: A non-RESTful resource for handling specific business logic like AI-powered generation.

## 2. Endpoints

### Authentication

#### POST /token

-   **Description**: Authenticates a user and returns an access token.
-   **Request Body**: `application/x-www-form-urlencoded`
    -   `username`: The user's username.
    -   `password`: The user's password.
-   **Response Body**:
    ```json
    {
      "access_token": "string",
      "token_type": "bearer"
    }
    ```
-   **Success Code**: `200 OK`
-   **Error Codes**:
    -   `400 Bad Request`: If credentials are not valid.

### Users

#### POST /users

-   **Description**: Creates a new user account.
-   **Request Body**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
-   **Response Body**:
    ```json
    {
      "id": 1,
      "username": "string",
      "created_at": "2025-08-04T10:00:00Z"
    }
    ```
-   **Success Code**: `201 Created`
-   **Error Codes**:
    -   `400 Bad Request`: If the username already exists.
    -   `422 Unprocessable Entity`: If the request payload is invalid.

### AI Generation

#### POST /ai/generate-flashcards

-   **Description**: Generates a list of flashcard pairs (question/answer) from a given text. This endpoint is protected and requires authentication.
-   **Request Body**:
    ```json
    {
      "text": "string",
      "count": "integer"
    }
    ```
-   **Response Body**:
    ```json
    {
      "flashcards": [
        {
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
-   **Success Code**: `200 OK`
-   **Error Codes**:
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `422 Unprocessable Entity`: If the request payload is invalid (e.g., empty text).
    -   `500 Internal Server Error`: If communication with the Ollama service fails.

### Flashcard Sets

#### POST /flashcard-sets

-   **Description**: Creates a new flashcard set from a list of generated flashcards. This endpoint is protected.
-   **Request Body**:
    ```json
    {
      "name": "string",
      "flashcards": [
        {
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
-   **Response Body**:
    ```json
    {
      "id": 1,
      "user_id": 1,
      "name": "string",
      "created_at": "2025-08-04T10:00:00Z",
      "flashcards": [
        {
          "id": 1,
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
-   **Success Code**: `201 Created`
-   **Error Codes**:
    -   `400 Bad Request`: If a set with the same name already exists for this user.
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `422 Unprocessable Entity`: If the request payload is invalid.

#### GET /flashcard-sets

-   **Description**: Retrieves a list of all flashcard sets for the authenticated user. This endpoint is protected.
-   **Query Parameters**:
    -   `skip` (integer, optional, default: 0): Number of records to skip for pagination.
    -   `limit` (integer, optional, default: 100): Maximum number of records to return.
-   **Response Body**:
    ```json
    [
      {
        "id": 1,
        "user_id": 1,
        "name": "string",
        "created_at": "2025-08-04T10:00:00Z"
      }
    ]
    ```
-   **Success Code**: `200 OK`
-   **Error Codes**:
    -   `401 Unauthorized`: If the user is not authenticated.

#### GET /flashcard-sets/{set_id}

-   **Description**: Retrieves a single flashcard set by its ID, including all its flashcards. This endpoint is protected.
-   **Response Body**:
    ```json
    {
      "id": 1,
      "user_id": 1,
      "name": "string",
      "created_at": "2025-08-04T10:00:00Z",
      "flashcards": [
        {
          "id": 1,
          "set_id": 1,
          "question": "string",
          "answer": "string"
        }
      ]
    }
    ```
-   **Success Code**: `200 OK`
-   **Error Codes**:
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `403 Forbidden`: If the user does not own the flashcard set.
    -   `404 Not Found`: If the flashcard set does not exist.

#### DELETE /flashcard-sets/{set_id}

-   **Description**: Deletes a flashcard set and all its associated flashcards. This endpoint is protected.
-   **Response Body**:
    ```json
    {
      "message": "Flashcard set deleted successfully"
    }
    ```
-   **Success Code**: `200 OK`
-   **Error Codes**:
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `403 Forbidden`: If the user does not own the flashcard set.
    -   `404 Not Found`: If the flashcard set does not exist.

### Flashcards

#### PUT /flashcards/{card_id}

-   **Description**: Updates the content of a single flashcard. This endpoint is protected.
-   **Request Body**:
    ```json
    {
      "question": "string",
      "answer": "string"
    }
    ```
-   **Response Body**:
    ```json
    {
      "id": 1,
      "set_id": 1,
      "question": "string",
      "answer": "string",
      "updated_at": "2025-08-04T11:00:00Z"
    }
    ```
-   **Success Code**: `200 OK`
-   **Error Codes**:
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `403 Forbidden`: If the user does not own the flashcard.
    -   `404 Not Found`: If the flashcard does not exist.
    -   `422 Unprocessable Entity`: If the request payload is invalid.

## 3. Authentication and Authorization

-   **Authentication Mechanism**: The API will use **OAuth2 Password Flow with Bearer Tokens**. A user sends their `username` and `password` to the `/token` endpoint to receive a JWT `access_token`.
-   **Implementation**: This token must be included in the `Authorization` header for all protected endpoints (e.g., `Authorization: Bearer <token>`). FastAPI's `OAuth2PasswordBearer` will be used to manage token extraction.
-   **Authorization**: Application-level logic will ensure users can only access or modify their own resources. After a user is authenticated via their token, API service functions will query for resources by their ID *and* the `user_id` from the token, preventing access to other users' data.

## 4. Validation and Business Logic

-   **Validation**: Input validation will be handled by **Pydantic** models within FastAPI. This enforces data types and constraints (e.g., required fields) automatically, returning a `422 Unprocessable Entity` response for invalid payloads.
    -   **User**: `username` must be a non-empty string. `password` must be a non-empty string.
    -   **FlashcardSet**: `name` must be a non-empty string. `flashcards` must be a list of valid flashcard objects.
    -   **Flashcard**: `question` and `answer` must be non-empty strings.
-   **Database Constraints**: Unique constraints (e.g., `users.username`, `flashcard_sets(user_id, name)`) are enforced at the database level. The API will catch `IntegrityError` exceptions and convert them into user-friendly `400 Bad Request` error responses.
-   **Business Logic**:
    -   **AI Generation**: The `POST /ai/generate-flashcards` endpoint encapsulates the logic of communicating with the Ollama service. It will use the `HTTPX` library for asynchronous HTTP requests to avoid blocking the server.
    -   **Timestamp Updates**: The `updated_at` fields in the database will be updated by the application logic within the corresponding `UPDATE` service functions.
