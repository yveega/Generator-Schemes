import sys
sys.setrecursionlimit(30)


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
    res = [["- 0 0 0 0"] * (max_y - min_y + 1) for _ in range(max_x - min_x + 1)]
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
    if y1 == y2 - 1:
        return False, True, False, False


def go(group, x, y, x_last, y_last, straight=0):
    if straight > 12:
        return False
    if len(connections[group]) == 0:  # end of part of scheme
        return False
    used.add((x, y))
    c = conns(x, y, x_last, y_last)
    # print(x, y, 'from', x_last, y_last, ':', c, connections[group])
    # if (x, y) in scheme:
        # print(scheme[(x, y)])
    if (x, y) not in scheme and (2 * x_last - x, 2 * y_last - y) not in scheme and (
        len(connections[group] - placed.keys()) > 0
    ) and not (
        x == x_last and y == y_last  # place element
    ):
        scheme[(x, y)] = ((connections[group] - placed.keys()).pop(), c[0], c[1], c[2], c[3])
        connections[group].remove(scheme[(x, y)][0])
        print('+', scheme[(x, y)][0])
        placed[scheme[(x, y)][0]] = (x, y)
        used.remove((x, y))
        return True
    elif (x, y) not in scheme:  # place wire
        now = [-1, c[0], c[1], c[2], c[3]]
        use_cell = False
        if (x, y + 1) not in used and go(group, x, y + 1, x, y, straight + 1):
            use_cell = True
            now[2] = True
        if (x + 1, y) not in used and go(group, x + 1, y, x, y, straight + 1):
            use_cell = True
            now[3] = True
        if (x, y - 1) not in used and go(group, x, y - 1, x, y, straight + 1):
            use_cell = True
            now[4] = True
        if (x - 1, y) not in used and go(group, x - 1, y, x, y, straight + 1):
            use_cell = True
            now[1] = True
        used.remove((x, y))
        if use_cell:
            scheme[(x, y)] = tuple(now)
            return True
        else:
            return False
    elif scheme[(x, y)][0] >= 0 and scheme[(x, y)][0] in connections[group] and (
            (scheme[(x, y)][1] or scheme[(x, y)][3]) == (c[0] or c[2])  # connect with placed earlier element
    ):
        now = scheme[(x, y)]
        connections[group].remove(now[0])
        scheme[(x, y)] = (now[0], now[1] or c[0], now[2] or c[1], now[3] or c[2], now[4] or c[3])
        used.remove((x, y))
        return True
    elif scheme[(x, y)][0] == -1:  # place + on wire
        now = scheme[(x, y)]
        if ((c[0] or c[2]) and not (now[1] or now[3])) or ((c[1] or c[3]) and not (now[2] or now[4])):
            if (2 * x - x_last, 2 * y - y_last) not in used and \
                    go(group, 2 * x - x_last, 2 * y - y_last, x, y, straight + 1):
                scheme[(x, y)] = (-2, True, True, True, True)
                used.remove((x, y))
                return True
            else:
                used.remove((x, y))
                return False
        else:
            used.remove((x, y))
            return False
    else:  # if can't use this cell
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
placed = dict()
go(1, 0, 0, 0, 0)
# go(2, -1, 3, -1, 3)
# go(0, 4, 4, 4, 4)
# go(3, -2, -2, -2, -2)
# go(4, 4, -4, 4, -4)
placed_conns = set()
for i in range(len(connections) - 1):
    for el in placed:
        if els[el][1] not in placed_conns or els[el][2] not in placed_conns:
            start_el = el
            break
    if els[start_el][1] not in placed_conns:
        if scheme[placed[start_el]][1]:  # if up
            go(els[start_el][1], placed[start_el][0] + 1, placed[start_el][1],
               placed[start_el][0] + 1, placed[start_el][1])
            placed_conns.add(els[start_el][1])
        elif scheme[placed[start_el]][2]:  # if right
            go(els[start_el][1], placed[start_el][0], placed[start_el][1] - 1,
               placed[start_el][0], placed[start_el][1] - 1)
            placed_conns.add(els[start_el][1])
        elif scheme[placed[start_el]][3]:  # if down
            go(els[start_el][1], placed[start_el][0] + 1, placed[start_el][1],
               placed[start_el][0] + 1, placed[start_el][1])
            placed_conns.add(els[start_el][1])
        elif scheme[placed[start_el]][4]:  # if left
            go(els[start_el][1], placed[start_el][0], placed[start_el][1] + 1,
               placed[start_el][0], placed[start_el][1] + 1)
            placed_conns.add(els[start_el][1])
    elif els[start_el][2] not in placed_conns:
        if scheme[placed[start_el]][1]:  # if up
            go(els[start_el][2], placed[start_el][0] + 1, placed[start_el][1],
               placed[start_el][0] + 1, placed[start_el][1])
            placed_conns.add(els[start_el][2])
        elif scheme[placed[start_el]][2]:  # if right
            go(els[start_el][2], placed[start_el][0], placed[start_el][1] - 1,
               placed[start_el][0], placed[start_el][1] - 1)
            placed_conns.add(els[start_el][2])
        elif scheme[placed[start_el]][3]:  # if down
            go(els[start_el][2], placed[start_el][0] + 1, placed[start_el][1],
               placed[start_el][0] + 1, placed[start_el][1])
            placed_conns.add(els[start_el][2])
        elif scheme[placed[start_el]][4]:  # if left
            go(els[start_el][2], placed[start_el][0], placed[start_el][1] + 1,
               placed[start_el][0], placed[start_el][1] + 1)
            placed_conns.add(els[start_el][2])


print()
for i in scheme.keys():
    print(i, ':', scheme[i])

for i in make_field(scheme):
    for j in i:
        print(j, end='\t')
    print()

print_in_file("sch2.txt", make_field(scheme))

sys.setrecursionlimit(1000)

import Generator_schemes
