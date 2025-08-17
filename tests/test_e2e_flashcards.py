import re
from playwright.sync_api import Page, expect
import pytest
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def login_user(page: Page):
    """Helper function to log in a user."""
    random_string = get_random_string(10)
    email = f"test_user_{random_string}@example.com"
    password = "password123"

    # Register a new user
    page.goto("/register")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Hasło").fill(password)
    page.get_by_role("button", name="Zarejestruj się").click()

    # Log in with the new user
    page.goto("/login")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Hasło").fill(password)
    page.get_by_role("button", name="Zaloguj się").click()
    expect(page).to_have_url(re.compile(r".*/dashboard"))


@pytest.mark.e2e
def test_generate_flashcards(page: Page):
    """
    Test generating flashcards from text.
    """
    login_user(page)

    page.goto("/generate")

    # Fill the form
    page.get_by_label("Tekst źródłowy").fill("The quick brown fox jumps over the lazy dog. This sentence is famous because it contains all of the letters of the English alphabet. It is often used for touch-typing practice, and for testing typewriters and computer keyboards. The earliest known appearance of the phrase is from The Boston Journal in 1885. The phrase has been used in many different contexts, from a Microsoft font viewer to a song by the band The Books.")
    page.get_by_label("Ilość fiszek").select_option("5")
    page.get_by_role("button", name="Generuj fiszki").click()
    page.locator("button", has_text=re.compile(r"Zapisz\s*zestaw")).wait_for(state="visible")

    # Assert that there are 5 question and 5 answer fields (due to mock)
    question_textareas = page.locator("textarea[name='questions']")
    answer_textareas = page.locator("textarea[name='answers']")
    expect(question_textareas).to_have_count(5)
    expect(answer_textareas).to_have_count(5)