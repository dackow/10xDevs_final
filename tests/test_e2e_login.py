import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.e2e
def test_login_page_elements(page: Page):
    """
    Test that the login page has all the expected elements.
    """
    # Navigate to the login page
    page.goto("/login")

    # Check for the main heading
    heading = page.get_by_role("heading", name="Logowanie")
    expect(heading).to_be_visible()

    # Check for the email input field
    email_input = page.get_by_label("Email")
    expect(email_input).to_be_visible()
    expect(email_input).to_be_editable()

    # Check for the password input field
    password_input = page.get_by_label("Hasło")
    expect(password_input).to_be_visible()
    expect(password_input).to_be_editable()

    # Check for the submit button
    login_button = page.get_by_role("button", name="Zaloguj się")
    expect(login_button).to_be_visible()
    expect(login_button).to_be_enabled()

    # Check for the link to the registration page
    register_link = page.get_by_role("link", name="Zarejestruj się tutaj")
    expect(register_link).to_be_visible()
