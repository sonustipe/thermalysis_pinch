from thermalysis_pinch.app import init_app
from thermalysis_pinch.config.main import PROJECT_NAME, PROJECT_SLUG
from flask import Flask

if __name__ == "__main__":

    dash_app = init_app(
        server=True,
        project_slug=PROJECT_SLUG,
        app_title=PROJECT_NAME,
    )

    dash_app.run(
        debug=True,
        port=5500,
        host="10.29.1.180",
    )
