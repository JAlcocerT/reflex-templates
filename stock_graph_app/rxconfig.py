import reflex as rx

config = rx.Config(
    app_name="stock_graph_app",
    #api_url="http://192.168.1.11:8000", #No need, just use reflex run --env prod and visit the front end port used
    plugins=[rx.plugins.TailwindV3Plugin()],
)
