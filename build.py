import mpy_cross
from subprocess import Popen, PIPE
import os
import esptool
import glob
from pathlib import Path


DIR = Path('src')


def lib_files(s: Path) -> Path:
    if s.stem != "main" and s.suffix == ".py":
        return s.stem
    return None


def build_libs():
    for file in filter(None, map(lib_files, DIR.iterdir())):
        mpy_cross.run(
            DIR / f"{file}.py",
            "-o",
            DIR / 'lib' / f'{file}.mpy',
            stdout=PIPE
        )


def erase_flash():
    cmd = ('--port', '/dev/ttyUSB0', 'erase_flash')
    print('erasing board flash using {}'.format(' '.join(cmd)))
    esptool.main(cmd)


def write_flash():
    bin = glob.glob("esp8266-*.bin")[0]
    cmd = ['--port', '/dev/ttyUSB0', '--baud', '460800',
           'write_flash', '--flash_size=detect', '-fm',
           'dout', '0', bin]
    print('writing firmware to board using {}'.format(' '.join(cmd)))
    esptool.main(cmd)


def copy_files():
    for entry in ("main.py", "config.json", "index.html", "lib"):
        stdout, stderr = Popen(
            ('ampy', '--port', '/dev/ttyUSB0', 'put', DIR / entry),
            stdout=PIPE, stderr=PIPE
        ).communicate()
        print(stdout)
        print(stderr)


def main():
    reflash = input("reflash? [y/N] ")
    if reflash and reflash.lower() in 'yes':
        erase_flash()
        write_flash()
    build_libs()
    while not os.path.exists("/dev/ttyUSB0"):
        continue
    copy_files()


if __name__ == "__main__":
    main()
