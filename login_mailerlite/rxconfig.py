import reflex as rx

config = rx.Config(
    app_name="login_mailerlite",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)