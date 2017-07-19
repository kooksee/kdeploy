# -*- coding: utf-8 -*-
import asyncio
import sys
import time
import ujson as json
from uuid import uuid4

from kdeploy.utils import pp, rm_pid_name, init_pid_name
from kdeploy.utils.app import Application
from kdeploy.utils.colors import yellow, red
from kdeploy.utils.net_tool import get_host_ip


async def close_service(sig, stack_frame):
    await pp('catched singal: {},{}'.format(sig, stack_frame), red, print)

    app = Application.current()

    # 服务推出后，从redis删除注册地址
    st, _res = await app.redis.execute("srem", "{}.urls".format(app.name), app.url)
    if not st:
        print(_res)
    await pp("warning:\n  删除服务{} ok".format(app.url), yellow, print)

    # 删除服务进程
    rm_pid_name()

    sys.exit(0)


event = asyncio.Event()


async def service_handler():
    pp("info:\n  启动服务 ok").then(yellow).then(print)
    app = Application.current()
    while True:
        await event.wait()

        st, d = await app.redis.execute('rpop', 'services.{}.q.1'.format(app.name))
        if not st:
            print("st:", d)
            await asyncio.sleep(1)
            continue

        if not d:
            print('队列为空 {}'.format(time.time()))
            event.set()
            continue

        d = json.loads(d)


async def service_check():
    await pp("info:\n  服务状态检测 ok", yellow, print)
    app = Application.current()
    while True:
        try:
            print(event.is_set())
            st, _res = await app.redis.execute("srem", "{}.url".format(app.name), app.url)
            if not st:
                print(_res)
            print(uuid4())
            await asyncio.sleep(1)
        except Exception as e:
            print(e)


async def init_app():
    # 初始化服务进程
    init_pid_name()

    app = Application.current()

    from sanic_cors import CORS

    # 跨域处理
    CORS(app, automatic_options=True)

    from kdeploy.app.config import init_config
    init_config()

    from kdeploy.utils.redis_util import init_redis
    init_redis()

    from kdeploy.app.urls import init_url
    init_url()

    from kdeploy.utils.log_util import KLog
    from kdeploy.bussiness.log import log_callback
    KLog(callback=log_callback).init_log()

    # 把服务添加到redis
    app.url = "{}:{}".format(get_host_ip(), app.port)
    st, _ = await app.redis.execute("sadd", "{}.urls".format(app.name), app.url)
    assert st != 0

    await pp("info:\n  注册服务{} ok".format(app.url), yellow, print)

    # 检查服务状态，检查配置更改，检查队列
    asyncio.run_coroutine_threadsafe(service_check(), asyncio.get_event_loop())
    asyncio.run_coroutine_threadsafe(service_handler(), asyncio.get_event_loop())

    # 处理服务退出后的问题
    from signal import signal, SIGTERM, SIGINT, SIGQUIT
    _func = lambda sig, stack_frame: asyncio.ensure_future(close_service(sig, stack_frame))
    signal(SIGTERM, _func)
    signal(SIGINT, _func)
    signal(SIGQUIT, _func)

    @app.middleware('response')
    async def custom_banner(request, response):
        response.headers["content-type"] = "application/json"
