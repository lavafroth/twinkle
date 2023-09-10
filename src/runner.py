import uasyncio as asyncio


def main(entrypoint):
    try:
        asyncio.run(entrypoint())
    except KeyboardInterrupt:
        asyncio.new_event_loop()
