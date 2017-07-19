import sys
from asyncio import ensure_future, get_event_loop
from os.path import abspath as ap, dirname as dn

sys.path.append(dn(dn(ap(__file__))))

import click

click.disable_unicode_literals_warning = True


async def __main():
    from kdeploy.utils.app import Application
    from kdeploy.utils import red
    from kdeploy.utils import pp
    app = Application.current()

    from kdeploy.app.main import init_app
    await init_app()
    await pp("info:\n  url: http://localhost:{}".format(app.port), red, print)
    await app.create_server(host="0.0.0.0", port=app.port, debug=app.debug)


@click.command()
@click.option('--env', '-e', default='local', help=u'开发环境设置', show_default=True)
@click.option('--port', '-p', default=80, help=u'端口', show_default=True)
@click.option('--name', '-n', default="test", help=u'服务名称', show_default=True)
def main(env, port, name):
    """启动服务"""

    from kdeploy.utils import pp
    from kdeploy.utils.colors import red
    from kdeploy.utils.net_tool import get_open_port
    from kdeploy.utils import when
    from kdeploy.utils.app import Application

    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = Application.instance()
    app.env = env
    app.root_path = dn(dn(ap(__file__)))
    app.port = when(port == 80, get_open_port(), port)

    if name == 'test':
        ensure_future(pp("warning:\n  service name is default: {}".format(name), red, print))

    app.name = name

    app.debug = when(env == 'pro', False, True)

    if app.debug:
        from aoiklivereload.aoiklivereload import LiveReloader
        reloader = LiveReloader()
        reloader.start_watcher_thread()

    asyncio.ensure_future(__main())
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
