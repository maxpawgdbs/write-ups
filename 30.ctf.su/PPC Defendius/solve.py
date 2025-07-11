import telnetlib3
import asyncio
from pprint import pprint


def algos(x1, y1):
    global volna
    nums = list()
    for el in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = el
        try:
            nums.append(volna[y1 + y][x1 + x])
        except Exception:
            pass

    nums = [val for val in nums if val > 0]

    if len(nums) == 0:
        return
    before = volna[y1][x1]
    volna[y1][x1] = min(min(nums) + 1, volna[y1][x1] if volna[y1][x1] != 0 else 10000)
    if before != volna[y1][x1]:
        for el in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = el
            try:
                algos(x1 + x, y1 + y)
            except Exception:
                pass


def get(x1, y1, l=None):
    if l is None:
        l = []
    global volna
    out = 1000
    x2, y2 = x1, y1
    for el in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = el
        try:
            n = volna[y1 + y][x1 + x]
            if n == -1:
                continue
            elif n < out:
                out = n
                x2, y2 = x1 + x, y1 + y

        except Exception:
            pass

    if y2 - y1 == 1:
        l.append('s')
    elif y2 - y1 == -1:
        l.append('w')
    elif x2 - x1 == 1:
        l.append('d')
    elif x2 - x1 == -1:
        l.append('a')
    if out == 1:
        return l
    else:
        return get(x2, y2, l)


async def shell():
    global volna
    reader, writer = await telnetlib3.open_connection("hackyou-ppc300.ctf.su", 11111)
    for i in range(1, 338, 1):
        inp = ""
        while "level" not in inp:
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=0.5)
            except asyncio.TimeoutError:
                break
            if not data:
                break
            inp += data
        while True:
            try:
                data = await asyncio.wait_for(reader.readline(), timeout=0.5)
            except asyncio.TimeoutError:
                break
            if not data:
                break
            inp += data
        field = inp.split("\r\n\r\n")[-2].split("\r\n")[1:]
        print(f"level {i}:")
        pprint(field)
        width = len(field[0])
        height = len(field)
        volna = field
        for y in range(0, height):
            volna[y] = list(volna[y])
            for x in range(0, width):
                if volna[y][x] != "O" and volna[y][x] != " ":
                    volna[y][x] = -1
                else:
                    volna[y][x] = 0
        #start = (1, height - 2)
        volna[1][width - 2] = 1
        x1, y1 = width - 2, 1
        for el in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = el
            try:
                algos(x1 + x, y1 + y)
            except Exception:
                pass
        #[print(_) for _ in volna]
        moves = get(1, height - 2)
        print(len(moves), moves)
        writer.write(''.join(moves) + '\r\n')
        await writer.drain()
    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=0.5)
        except asyncio.TimeoutError:
            break
        if not data:
            break
        print(data)
volna = []
asyncio.run(shell())
