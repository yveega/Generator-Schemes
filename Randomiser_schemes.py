

def make_field(sch):
    min_x = float("INF")
    min_y = float("INF")
    max_x = -float("INF")
    max_y = -float("INF")
    for cell in sch.keys():
        if cell[0] < min_x:
            min_x = cell[0]
        if cell[0] > max_x:
            max_x = cell[0]
        if cell[1] < min_y:
            min_y = cell[1]
        if cell[1] > max_y:
            max_y = cell[1]
    print(min_x, max_x, min_y, max_y)
    res = [["- 0 0 0 0"] * (max_y - min_y + 1) for _ in range(max_x - min_x + 1)]
    print(len(res), len(res[0]))
    for cell in sch.keys():
        if sch[cell][0] == -1:
            el = '-'
        elif sch[cell][0] == -2:
            el = '+'
        else:
            el = els[sch[cell][0]][0]
        w1 = ' 1' if sch[cell][1] else ' 0'
        w2 = ' 1' if sch[cell][2] else ' 0'
        w3 = ' 1' if sch[cell][3] else ' 0'
        w4 = ' 1' if sch[cell][4] else ' 0'
        print(cell[0] - min_x, cell[1] - min_y)
        res[cell[0] - min_x][cell[1] - min_y] = el + w1 + w2 + w3 + w4
    return res


def print_in_file(name, field):
    with open(name, "w") as fo:
        for line in field:
            print('\t'.join(line), file=fo)


def conns(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return False, False, False, False
    if x1 == x2 + 1:
        return True, False, False, False
    if x1 == x2 - 1:
        return False, False, True, False
    if y1 == y2 + 1:
        return False, False, False, True
    if x1 == y2 - 1:
        return False, True, False, False


def go(group, x, y, x_last, y_last):
    if len(connections[group]) == 0:
        return False
    used.add((x, y))
    c = conns(x, y, x_last, y_last)
    print(x, y, ':', c, connections[group])
    if (x, y) in scheme:
        print(scheme[(x, y)])
    if (x, y) not in scheme and (2 * x_last - x, 2 * y_last - y) not in scheme and len(connections[group]) > 0 and not (
        x == x_last and y == y_last
    ):
        scheme[(x, y)] = (connections[group].pop(), c[0], c[1], c[2], c[3])
        print('+', scheme[(x, y)][0])
        used.remove((x, y))
        return True
    elif (x, y) not in scheme:
        now = [-1, c[0], c[1], c[2], c[3]]
        use_cell = False
        if (x + 1, y) not in used and go(group, x + 1, y, x, y):
            use_cell = True
            now[3] = True
        if (x - 1, y) not in used and go(group, x - 1, y, x, y):
            use_cell = True
            now[1] = True
        if (x, y + 1) not in used and go(group, x, y + 1, x, y):
            use_cell = True
            now[2] = True
        if (x, y - 1) not in used and go(group, x, y - 1, x, y):
            use_cell = True
            now[4] = True
        used.remove((x, y))
        if use_cell:
            scheme[(x, y)] = tuple(now)
            return True
        else:
            return False
    elif scheme[(x, y)][0] >= 0 and scheme[(x, y)][0] in connections[group] and (
            (scheme[(x, y)][1] or scheme[(x, y)][3]) == (c[0] or c[2])
    ):
        now = scheme[(x, y)]
        connections[group].remove(now[0])
        scheme[(x, y)] = (now[0], now[1] or c[0], now[2] or c[1], now[3] or c[2], now[4] or c[3])
        used.remove((x, y))
        return True
    elif scheme[(x, y)][0] == -1:
        now = scheme[(x, y)]
        if not ((now[1] and c[0]) or (now[2] and c[1]) or (now[3] and c[2]) or (now[4] and c[3])):
            if (2 * x - x_last, 2 * y - y_last) not in used and go(group, 2 * x - x_last, 2 * y - y_last, x, y):
                scheme[(x, y)] = (-2, True, True, True, True)
                used.remove((x, y))
                return True
            else:
                used.remove((x, y))
                return False
        else:
            used.remove((x, y))
            return False
    else:
        used.remove((x, y))
        return False


els = [("lamp", 0, 2), ("switch", 0, 1), ("resister", 1, 5), ("battery", 1, 2),
       ("lamp", 1, 2), ("resister", 2, 3), ("resister", 3, 4), ("resister", 4, 5)]
connections = [{0, 1},
               {1, 2, 3, 4},
               {0, 3, 5, 4},
               {5, 6},
               {6, 7},
               {2, 7}]

scheme = dict()
used = set()
go(2, 0, 0, 0, 0)

print()
for i in scheme.keys():
    print(i, ':', scheme[i])

print_in_file("sch2.txt", make_field(scheme))

import Generator_schemes
