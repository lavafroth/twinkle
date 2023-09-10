import socket
import uasyncio


async def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(False)
    s.bind(('0.0.0.0', 53))

    while True:
        try:
            yield uasyncio.core._io_queue.queue_read(s)
            data, addr = s.recvfrom(256)
            response = (
                data[:2]
                + b'\x81\x80'
                + data[4:6] * 2
                + b'\x00\x00\x00\x00'  # questions and answers counts
                + data[12:]  # original query
                + b'\xC0\x0C'  # pointer to domain name above
                + b'\x00\x01\x00\x01'  # type and class (A record / IN class)
                + b'\x00\x00\x00\x3C'  # time to live
                + b'\x00\x04'  # response length (4 bytes = 1 IPv4 address)
                + bytes([192, 168, 0, 1])
            )
            s.sendto(response, addr)
        except Exception as e:
            print("DNS server error:", e)
            await uasyncio.sleep_ms(1000)
    s.close()
