# Project Onboarding: AI Flashcard Generator

## Welcome

Welcome to the AI Flashcard Generator project! This is a Minimum Viable Product (MVP) of a web application designed to help elementary school students quickly create educational flashcards from their notes using AI. The goal is to streamline the study process by automating the often time-consuming task of flashcard creation.

## Project Overview & Structure

The project is a Python-based web application built with FastAPI, utilizing a clean and modular structure. It follows a typical web application pattern with distinct directories for different concerns:

*   **`app/`**: Contains the core application logic, including API routes, database models, data schemas, business services, and HTML templates.
*   **`tests/`**: Houses unit and integration tests for the application.
*   **`.ai/`**: Stores various project documentation, plans, and product requirements.
*   **`.github/workflows/`**: Defines Continuous Integration/Continuous Deployment (CI/CD) pipelines using GitHub Actions.
*   **`scripts/`**: Contains utility scripts.
*   **`gil-log-analysis/`**: Stores results from git log analysis.

## Core Modules

### `app/main.py`

-   **Role:** The main entry point for the FastAPI application. It initializes the application, includes API routers, sets up templating, and defines global exception handlers.
-   **Key Files/Areas:** Application startup, router inclusion (`auth`, `flashcards`), Jinja2 template configuration, custom exception handling.
-   **Recent Focus:** Stable, core application setup.

### `app/routers/`

-   **Role:** Defines the API endpoints and web routes for different functionalities.
-   **Key Files/Areas:**
    *   `auth.py`: Handles user registration, login, and logout using Supabase authentication.
    *   `flashcards.py`: Manages flashcard sets and individual flashcards, including viewing, editing, AI-powered generation, and deletion.
-   **Recent Focus:** Active development and refinement of flashcard management and AI generation features.

### `app/models/models.py`

-   **Role:** Defines the SQLAlchemy ORM models (`User`, `FlashcardSet`, `Flashcard`) that represent the database schema.
-   **Key Files/Areas:** Database table definitions, relationships between entities.
-   **Recent Focus:** Core data structure definition.

### `app/schemas/schemas.py`

-   **Role:** Defines Pydantic schemas for data validation and serialization (Data Transfer Objects - DTOs). These are used for API request and response bodies.
-   **Key Files/Areas:** `Flashcard`, `FlashcardSet`, `User`, `Token`, and AI-related request/response schemas.
-   **Recent Focus:** Data contract definitions for API interactions.

### `app/crud/crud.py`

-   **Role:** Provides Create, Read, Update, and Delete (CRUD) operations for direct interaction with the Supabase database.
-   **Key Files/Areas:** Functions for creating, retrieving, updating, and deleting flashcard sets and flashcards.
-   **Recent Focus:** Database interaction logic.

### `app/services/`

-   **Role:** Contains the business logic and orchestrates interactions between different components, including external services like Ollama.
-   **Key Files/Areas:**
    *   `flashcard_service.py`: Handles the generation and saving of flashcards, integrating with the Ollama AI model.
    *   `ollama.py`: Specific integration logic for the Ollama AI model.
-   **Recent Focus:** Core business logic, especially around AI flashcard generation.

## Key Contributors

*   **Waldemar Dacko:** The primary developer, actively contributing to core features, documentation, and CI/CD.

## Overall Takeaways & Recent Focus

The project is in its MVP stage, focusing on delivering core functionalities: user authentication, AI-powered flashcard generation from text, and CRUD operations for flashcard sets. Recent development has concentrated on refining the flashcard generation and management features, updating documentation (including deployment plans), and enhancing the CI/CD pipeline. The project leverages Supabase for backend-as-a-service, simplifying database and authentication management.

## Potential Complexity/Areas to Note

*   **AI Integration:** Interacting with the Ollama AI model (`app/services/ollama.py`) involves handling external API calls, potential latency, and parsing AI responses, which can be a source of complexity and error handling.
*   **Supabase Interactions:** While Supabase simplifies many aspects, managing authentication flows (tokens, sessions) and ensuring robust database operations within `app/crud/crud.py` requires careful attention.
*   **Mixed Rendering:** The application uses FastAPI for both API endpoints and server-side rendered HTML templates. Understanding the flow between form submissions, API calls, and template rendering is crucial.
*   **Error Handling:** Custom exceptions and global exception handlers are in place, but ensuring comprehensive error coverage and user-friendly messages across all features can be challenging.

## Questions for the Team

1.  Are there any specific guidelines for interacting with the Supabase database beyond what's in `app/crud/crud.py`?
2.  What are the current performance expectations for the AI flashcard generation, and how are we monitoring it?
3.  Are there any plans to expand the AI capabilities beyond text-based generation (e.g., image-to-flashcard)?
4.  How are UI/UX decisions typically made, given the current focus on a minimal Bootstrap frontend?
5.  What is the process for deploying new features to the Railway hosting environment?
6.  Are there any specific security considerations or best practices to be aware of when developing new features?
7.  What is the preferred method for debugging issues in the development and production environments?

## Next Steps

1.  Familiarize yourself with the `app/` directory structure and the role of each subdirectory.
2.  Review the `app/routers/auth.py` and `app/routers/flashcards.py` files to understand the main application flows.
3.  Explore the `app/services/ollama.py` and `app/crud/crud.py` files to grasp the AI and database interaction logic.
4.  Run the application locally using the provided setup instructions to get a hands-on feel for the features.
5.  Review the `test-plan.md` to understand the testing strategy and how to run tests.

## Development Environment Setup

To set up and run the project on your local machine:

1.  **Prerequisites:**
    *   Python 3.8+
    *   `pip` package manager

2.  **Installation & Setup:**
    *   **Clone the repository:**
        ```sh
        git clone https://github.com/your-username/ai-flashcard-generator.git
        cd ai-flashcard-generator
        ```
    *   **Create and activate a virtual environment:**
        *   On macOS and Linux:
            ```sh
            python3 -m venv .venv
            source .venv/bin/activate
            ```
        *   On Windows:
            ```sh
            python -m venv .venv
            .\.venv\Scripts\activate
            ```
    *   **Install dependencies:**
        ```sh
        pip install -r requirements.txt
        ```
    *   **Run the application:**
        ```sh
        uvicorn app.main:app --reload
        ```
        The application will be available at `http://127.0.0.1:8000`.

## Helpful Resources

*   **Project Documentation:**
    *   `README.md` (Project overview, setup, tech stack)
    *   `.ai/prd.md` (Product Requirements Document - detailed functional requirements)
    *   `.ai/test-plan.md` (Comprehensive testing strategy)
    *   `.ai/tech-stack.md` (Detailed justification of technology choices)
    *   Other `.ai/` files for specific implementation plans and API designs.
*   **External Services:**
    *   Railway: `https://railway.app/` (Hosting platform)
    *   Supabase: (Official documentation for database and authentication)
    *   FastAPI: (Official documentation for the web framework)
    *   Ollama: (Official documentation for the local LLM server)