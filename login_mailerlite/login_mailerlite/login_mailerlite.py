import reflex as rx

# Assuming rxconfig.py exists and has a config.app_name
from rxconfig import config

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

def form() -> rx.Component:
    """The login form inspired by the newsletter components."""
    return rx.center( # Center the card on the page
        rx.card(
            rx.form(
                rx.vstack(
                    rx.hstack( # Mimic the image and heading layout
                        rx.image(src="/avatar.png", width="50px", height="50px"), # Placeholder for a login icon
                        rx.vstack(
                            rx.heading("Welcome Back!"),
                            rx.text("Please log in to continue."),
                        ),
                        align_items="center", # Align items vertically in the hstack
                    ),
                    rx.divider(), # Add a subtle separator

                    rx.vstack(
                        rx.text(
                            "Your Name ",
                            rx.text.span("*", color="red"),
                        ),
                        rx.input(
                            name="name",
                            placeholder="Enter your name",
                            required=True,
                        ),
                        align_items="flex-start", # Align text and input to the left
                    ),
                    rx.vstack(
                        rx.text(
                            "Your Email ",
                            rx.text.span("*", color="red"),
                        ),
                        rx.input(
                            name="email",
                            type="email",
                            placeholder="Enter your email",
                            required=True,
                        ),
                        align_items="flex-start", # Align text and input to the left
                    ),
                    rx.button("Login", type="submit", width="100%"), # Full width button
                    spacing="4", # Adjust spacing between elements
                ),
                on_submit=State.handle_submit,
            ),
            # Optional: Add max width to the card for better aesthetics
            max_width="400px",
            width="100%",
        ),
        height="100vh", # Center the card vertically on the screen
    )

def index() -> rx.Component:
    """The main app."""
    return rx.cond(
        State.submitted,
        welcome_page(),
        form(),
    )

app = rx.App()
app.add_page(index)