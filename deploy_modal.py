import os

from modal import App, Image, Mount, asgi_app

from main import app

image = Image.debian_slim(python_version="3.12.5", force_build=False).pip_install(
    ["python-fasthtml", "markdown", "uvicorn>=0.29"], extra_options="-U"
)

modal_app = App("fasthtml-website")


@modal_app.function(
    image=image,
    mounts=[
        Mount.from_local_file("globals.css", remote_path="/root/globals.css"),
        Mount.from_local_dir("content", remote_path="/root/content"),
        Mount.from_local_dir(
            "images/multimodal", remote_path="/root/images/multimodal"
        ),
    ],
)
@asgi_app()
def get():
    print(os.listdir("/"))
    print(os.listdir("/root"))
    return app


# Quite Slow, needs to spin up a container first, but can scale up to multiple instances
