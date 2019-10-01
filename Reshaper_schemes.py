h_or_v_els = {"battery", "switch", "resister"}


class Cell:
    def __init__(self, s, row, column):
        data_cell = s.split()
        self.is_el = data_cell[0] != '-'
        self.up = bool(int(data_cell[1]))
        self.right = bool(int(data_cell[2]))
        self.down = bool(int(data_cell[3]))
        self.left = bool(int(data_cell[4]))
        if self.is_el:
            if data_cell[0] in h_or_v_els:
                if self.up or self.down:
                    self.img_name = "Im_el/" + data_cell[0] + "/v.png"
                else:
                    self.img_name = "Im_el/" + data_cell[0] + "/h.png"
            else:
                self.img_name = "Im_el/" + data_cell[0] + ".png"
        self.x = row * (EL_SIZE + 2 * TAB) + TAB
        self.y = column * (EL_SIZE + 2 * TAB) + TAB


with open("sch1.txt", 'r') as fi:
    max_row = 0
    data = []
    for line in fi:
        data.append(line.strip().split('\t'))
        max_row = max(max_row, len(data[-1]))

scheme = [[None] * max_row for _ in range(len(data))]

for i in range(len(data)):
    for j in range(len(data[i])):
        scheme[i][j] = Cell(data[i][j], j, i)

