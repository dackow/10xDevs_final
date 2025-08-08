# AI Flashcard Generator

A web application that allows users to automatically generate educational flashcards from their notes using AI.

## Table of Contents

- [Project Description](#project-description)
- [Tech Stack](#tech-stack)
- [Getting Started Locally](#getting-started-locally)
- [Available Scripts](#available-scripts)
- [Project Scope](#project-scope)
- [Project Status](#project-status)
- [License](#license)

## Project Description

This project is a Minimum Viable Product (MVP) of a web application designed to solve the time-consuming problem of creating educational flashcards. The application is aimed at elementary school students, enabling them to automatically generate flashcards from materials like class notes. Users can manage their flashcard sets, edit them, and prepare for learning, streamlining the study process.

## Tech Stack

The technology stack was chosen with a focus on simplicity, speed of MVP implementation, and clearly defined boundaries.

| Component | Technology | Justification |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | Speed, data validation, auto-generated API documentation. |
| **Database** | Supabase (PostgreSQL) | Backend as a Service with a managed PostgreSQL database, authentication, and storage. |
| **ORM** | SQLAlchemy | Industry standard, safe interaction with the database. |
| **HTTP Client (for Ollama)**| HTTPX | Support for asynchronous operations in FastAPI. |
| **HTML Template Engine** | Jinja2 | Simple server-side HTML generation. |
| **CSS Framework** | Bootstrap | Rapid development of a clean and aesthetic user interface. |
| **Application Server** | Uvicorn | The standard server for FastAPI. |
| **Unit/Integration Testing** | Pytest, FastAPI TestClient | Comprehensive testing for backend logic and API endpoints. |
| **E2E Testing (Future)** | Playwright / Selenium | For automated browser-based UI testing. |

## Getting Started Locally

To set up and run the project on your local machine, follow these steps.

### Prerequisites

- Python 3.8+
- `pip` package manager

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/ai-flashcard-generator.git
    cd ai-flashcard-generator
    ```

2.  **Create and activate a virtual environment:**
    - On macOS and Linux:
      ```sh
      python3 -m venv .venv
      source .venv/bin/activate
      ```
    - On Windows:
      ```sh
      python -m venv .venv
      .\.venv\Scripts\activate
      ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    uvicorn app.main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

## Available Scripts

-   `uvicorn app.main:app --reload`: Runs the application in development mode with live reloading.

## Project Scope

### Included Features (MVP)

-   **User Authentication:** Users can create an account and log in.
-   **AI Flashcard Generation:** Provides a text area to paste source content and generates flashcards using an Ollama-based language model.
-   **CRUD for Flashcard Sets:** Users can save, view, edit, and delete their flashcard sets.

### Excluded Features (Out of Scope for MVP)

-   AI generation based on a topic alone (without source text).
-   Implementation of a spaced repetition algorithm (e.g., SM-2).
-   Manual creation of flashcards from scratch.
-   Importing files in formats other than plain text (e.g., PDF, DOCX).
-   Social features like sharing sets between users.
-   Advanced JavaScript-based frontend.

## Project Status

This project is currently in the **MVP (Minimum Viable Product)** development stage. The primary goal is to deliver a working application that fulfills all the core functional requirements defined in the project scope.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
