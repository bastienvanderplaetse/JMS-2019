def load_grid(filename):
    f = open(filename)
    lines = f.readlines()
    grid = []
    for index, line in enumerate(lines):
        row = []
        for column in line.replace('\n', ''):
            row.append(int(column))
        grid.append(row)
    f.close()

    return grid
