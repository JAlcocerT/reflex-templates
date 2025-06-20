import reflex as rx

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

# Define the hello world page
def hello_world_page() -> rx.Component:
    """The hello world page."""
    return rx.center(
        rx.text("Hello World", font_size="2em"),
        height="100vh",
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
            on_submit=State.handle_submit, # <--- Corrected placement: on the rx.form
        )
    )

# Define the main app
def index() -> rx.Component:
    """The main app."""
    return rx.cond(
        State.submitted,
        hello_world_page(),
        form(),
    )

# Add the app to the Reflex backend
app = rx.App()
app.add_page(index)