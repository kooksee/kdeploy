def init_url():
    from kdeploy.utils.app import Application
    app = Application.current()

    from kdeploy.app.handlers import ok
    app.route("/", methods=["GET"])(ok)
    app.route("/health", methods=["GET"])(ok)
