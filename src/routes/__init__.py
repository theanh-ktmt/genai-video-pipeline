def register_routes(app):

    # for check connection
    @app.route("/ping")
    def ping():
        return "PONG!"
