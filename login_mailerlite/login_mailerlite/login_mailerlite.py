import reflex as rx

# Assuming rxconfig.py exists and has a config.app_name
from rxconfig import config

# Define the state for the app
class State(rx.State):
    """The app state."""
    name: str
    email: str
    submitted: bool = False

    def handle_submit(self, form_data: dict):
        """Handle the form submission."""
        self.name = form_data.get("name", "")
        self.email = form_data.get("email", "")
        self.submitted = True

# Define the welcome page
def welcome_page() -> rx.Component:
    """The welcome page with Reflex intro."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

# Define the form component
def form() -> rx.Component:
    """The form to collect name and email."""
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Enter Your Details"),
                rx.text("Please provide your name and email to continue."),
                rx.text(
                    "Name ",
                    rx.text.span("*", color="red"),
                ),
                rx.input(
                    name="name",
                    required=True,
                ),
                rx.text(
                    "Email ",
                    rx.text.span("*", color="red"),
                ),
                rx.input(
                    name="email",
                    type="email",
                    required=True,
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=State.handle_submit,
        )
    )

# Define the main app
def index() -> rx.Component:
    """The main app."""
    return rx.cond(
        State.submitted,
        welcome_page(),  # Show the welcome page after submission
        form(),          # Show the form initially
    )

# Add the app to the Reflex backend
app = rx.App()
app.add_page(index)