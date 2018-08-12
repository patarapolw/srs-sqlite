import click

from . import load_srs


@click.command()
@click.argument('filename')
@click.option('--host', default='localhost')
@click.option('--port', default=8000)
@click.option('--debug', is_flag=True)
def cli(filename, host, port, debug):
    load_srs(filename, host, port, debug)


if __name__ == '__main__':
    cli()
