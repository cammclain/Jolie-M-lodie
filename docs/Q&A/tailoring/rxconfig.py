import reflex as rx

config = rx.Config(
    app_name="tailoring",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)