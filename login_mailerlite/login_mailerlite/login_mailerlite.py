import reflex as rx

class FormState(rx.State):

    @rx.event
    def submit(self, form_data):
        return rx.toast(form_data)

def form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.hstack(
                rx.image(src="/envelope.png"),
                rx.vstack(
                    rx.heading("Join Newsletter"),
                    rx.text(
                        "Get the latest updates and news about Reflex.",
                    ),
                ),
            ),
            rx.vstack(
                rx.text(
                    "Name ",
                    rx.text.span("*", color="red"),
                ),
                rx.input(
                    name="name",
                    required=True,
                ),
            ),
            rx.vstack(
                rx.text(
                    "Email ",
                    rx.text.span("*", color="red"),
                ),
                rx.input(
                    name="email",
                    type="email",
                    required=True,
                ),
            ),
            rx.vstack(
                rx.text("Message"),
                rx.textarea(
                    name="message",
                ),
            ),
            rx.button("Send", type="submit"),
            on_submit=FormState.submit,
        )
    )