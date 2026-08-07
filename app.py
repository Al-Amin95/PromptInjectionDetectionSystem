from flask import Flask, render_template

from backend.routes import main as mainBlueprint


def createApp():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static",
    )
    app.register_blueprint(mainBlueprint)

    @app.errorhandler(404)
    def notFound(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def serverError(e):
        return render_template("500.html"), 500

    return app


app = createApp()

if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
