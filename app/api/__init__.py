
url_prefix = '/v1'


def init_blueprint(app):

    @app.route('/')
    def hello():
        return 'web api v1'

    for name in __all__:
        module = __import__(
            "app.api.{}".format(name),
            fromlist=["bp", "url_prefix"]
        )

        app.register_blueprint(
            getattr(module, "bp"),
            url_prefix="{}{}".format(
                url_prefix,
                getattr(module, "url_prefix", "")
            )
        )


__all__ = (
    'test',
    'user',
)
