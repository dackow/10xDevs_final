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

@pytest.mark.e2e
def test_logout(page: Page):
    """
    Test that a logged in user can logout.
    """
    # Generate a unique email for the test user
    random_string = get_random_string(10)
    email = f"test_user_{random_string}@example.com"
    password = "password123"

    # Register a new user
    page.goto("/register")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Hasło").fill(password)
    page.get_by_role("button", name="Zarejestruj się").click()

    # Expect to be redirected to the login page
    expect(page).to_have_url(re.compile(r".*/login"))

    # Log in with the new user
    page.get_by_label("Email").fill(email)
    page.get_by_label("Hasło").fill(password)
    page.get_by_role("button", name="Zaloguj się").click()

    # Expect to be redirected to the dashboard
    expect(page).to_have_url(re.compile(r".*/dashboard"))

    # Logout
    page.get_by_role("button", name="Wyloguj").click()

    # Expect to be redirected to the login page
    expect(page).to_have_url(re.compile(r".*/login"))

@pytest.mark.e2e
def test_register_existing_user(page: Page):
    """
    Test that registering with an existing email shows an error.
    """
    # Generate a unique email for the test user
    random_string = get_random_string(10)
    email = f"test_user_{random_string}@example.com"
    password = "password123"

    # Register a new user
    page.goto("/register")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Hasło").fill(password)
    page.get_by_role("button", name="Zarejestruj się").click()

    # Try to register again with the same email
    page.goto("/register")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Hasło").fill(password)
    page.get_by_role("button", name="Zarejestruj się").click()

    # Expect to stay on the register page and see an error message
    expect(page).to_have_url(re.compile(r".*/register"))
    error_message = page.locator("div.alert.alert-danger")
    expect(error_message).to_be_visible()