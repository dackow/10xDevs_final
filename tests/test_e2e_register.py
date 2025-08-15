import re
from playwright.sync_api import Page, expect
import pytest

@pytest.mark.e2e
def test_register_page_elements(page: Page):
    """
    Test that the register page has all the expected elements.
    """
    # Navigate to the register page
    page.goto("/register")

    # Check for the main heading
    heading = page.get_by_role("heading", name="Rejestracja")
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
    register_button = page.get_by_role("button", name="Zarejestruj się")
    expect(register_button).to_be_visible()
    expect(register_button).to_be_enabled()

    # Check for the link to the login page
    login_link = page.get_by_role("link", name="Zaloguj się")
    expect(login_link).to_be_visible()
