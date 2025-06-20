import reflex as rx
from rxconfig import config # Import config
from utils import check_formbricks_subscription # Import your validation function

class State(rx.State):
    """The app state."""
    name: str = ""
    email: str = ""
    submitted: bool = False
    validation_error: str = "" # New state variable for validation messages

    async def handle_submit(self, form_data: dict): # Use async if fetching external data
        """Handle the form submission and validate the email."""
        self.name = form_data.get("name", "")
        self.email = form_data.get("email", "")
        self.validation_error = "" # Clear previous errors

        if not self.email:
            self.validation_error = "Email is required."
            return rx.toast("Email is required.", color="red")

        # Perform the email validation
        # The check_formbricks_subscription function might take time
        # so consider making this state method async and awaiting the call
        # if the external data fetch is significant.
        is_valid_email = await rx.background(check_formbricks_subscription, self.email)

        if is_valid_email:
            self.submitted = True
            return rx.toast(f"Welcome, {self.name}!", color="green")
        else:
            self.validation_error = "This email is not authorized. Please try again or contact support."
            return rx.toast(self.validation_error, color="red")

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
                            value=State.name, # Bind input value to state for sticky form
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
                            value=State.email, # Bind input value to state
                        ),
                        align_items="flex-start", # Align text and input to the left
                    ),
                    # Display validation error message if any
                    rx.cond(
                        State.validation_error,
                        rx.text(State.validation_error, color="red", font_size="0.9em"),
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