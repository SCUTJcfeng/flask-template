
import click
import IPython
from flask.cli import FlaskGroup
from app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """web manage"""


@cli.command()
def ipython():
    """
    basic ipython shell
    """
    IPython.start_ipython(argv=())


@cli.command(short_help="Runs an ipython shell in current_app context with some pre-import modules.")
def shell():
    """
    overwrite default shell command with ipython support
    """
    import sys
    import IPython
    from traitlets.config import Config
    from flask import current_app

    banner = f'Python {sys.version} on {sys.platform}\n' \
             f'IPython: {IPython.__version__}\n' \
             f'App: {current_app.import_name} [{current_app.env}]\n' \
             f'Instance: {current_app.instance_path}\n'
    # see https://ipython.readthedocs.io/en/stable/config/index.html
    c = Config()
    c.InteractiveShell.banner1 = banner
    c.InteractiveShellApp.exec_lines = [
        'print("\\nPre-import: current_app, g, all tasks and schedules. Enjoy:)")',
        'from flask import current_app, g',
        'from app.task import *'
        'from app.schedule import *'
    ]
    c.InteractiveShell.confirm_exit = False

    IPython.start_ipython(
        argv=(),
        user_ns=current_app.make_shell_context(),
        config=c,
    )


if __name__ == '__main__':
    cli()
