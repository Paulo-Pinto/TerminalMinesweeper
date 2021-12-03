import numpy as np

HEIGHT = 8
FIRST_MOVE = 0


def generate_map(cols, bomb_quant):
    empty_map = np.zeros(shape=(cols, cols)).astype(int).astype(str)

    for bomb in range(bomb_quant):
        bomb_placed = False
        while not bomb_placed:
            rand1, rand2 = np.random.randint(cols), np.random.randint(cols)
            # print(rand1, rand2)
            if empty_map[rand1, rand2] == "*":
                # bomb already placed here
                pass
            else:
                empty_map[rand1, rand2] = "*"
                bomb_placed = True

    bomb_map = empty_map

    # middle
    for a in range(0, cols):
        for b in range(0, cols):

            # if its a bomb go to next cell
            if bomb_map[a, b] == "*":
                continue

            neighbours = get_neighbours(a, b, get_coords_position(a, b))
            bomb_count = 0
            for pair in neighbours:
                # print(bomb_map[pair])
                bomb_count += bomb_map[pair] == "*"

            bomb_map[a, b] = str(bomb_count)

    return bomb_map


def gen_hidden_map(cols):
    hidden_map = np.zeros(shape=(cols, cols)).astype(int).astype(str)

    for a in range(0, cols):
        for b in range(0, cols):
            hidden_map[a, b] = "#"

    return hidden_map


def prompt() -> (int, int):
    print("   0,  1,  2,  3,  4,  5,  6,  7")
    print(revealed_map)

    x = int(input("Choose the col "))
    y = int(input("Choose the row "))

    if x >= col or y >= col:
        print("Out of bounds")
        return prompt()
    return x, y


def first_move(r_map):
    # iterates rows
    for cells in r_map:
        # if any cell isnt a bomb (has been revealed)
        if not any(cells) == "#":
            return False
    return True


def play(map, r_map, x, y):
    while map[x, y] != "0" and first_move(r_map):
        map = generate_map(cols=col, bomb_quant=int(col ** 2 / 5))

    if map[x, y] == "*":
        print("You lost :(")
        return False

    r_map[x, y] = map[x, y]

    if r_map[x, y] == "0":
        r_map = reveal(r_map, map, x, y)

    return True


def get_neighbours(x, y, option):
    nbrs = (
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1)
    )

    if option == "right":
        return [pair for pair in nbrs if pair[1] <= y]

    if option == "left":
        return [pair for pair in nbrs if pair[1] >= y]

    if option == "top":
        return [pair for pair in nbrs if pair[0] >= x]

    if option == "bottom":
        return [pair for pair in nbrs if pair[0] <= x]

    if option == "top_left":
        return [pair for pair in nbrs if x - 1 not in pair]

    if option == "bottom_right":
        return [pair for pair in nbrs if x + 1 not in pair]

    if option == "bottom_left":
        return nbrs[1:3] + nbrs[4:5]

    if option == "top_right":
        return nbrs[3:4] + nbrs[5:7]

    return nbrs


def get_coords_position(x, y):
    if x == 0:
        if y == 0:
            return "top_left"
        elif y == HEIGHT - 1:
            return "top_right"
        else:
            return "top"

    if x == HEIGHT - 1:
        if y == 0:
            return "bottom_left"
        elif y == HEIGHT - 1:
            return "bottom_right"
        else:
            return "bottom"

    if y == 0:
        return "left"

    if y == HEIGHT - 1:
        return "right"

    return "center"


def reveal(r_map, map, x, y):
    neighbours = get_neighbours(x, y, get_coords_position(x, y))

    # get neighbours
    for pair in neighbours:
        # if the cell has already been analysed, skip
        # recursion base case (prevents endless recursion)
        if r_map[pair] == "0":
            continue

        r_map[pair] = map[pair]

        # recursion -> 0 spotted another 0
        if r_map[pair] == "0":
            reveal(r_map, map, pair[0], pair[1])

    return r_map


if __name__ == '__main__':
    col = 8
    map = generate_map(cols=col, bomb_quant=int(col ** 2 / 5))
    # print(map)
    revealed_map = gen_hidden_map(col)
    x, y = prompt()

    while play(map, revealed_map, x, y):
        x, y = prompt()

    print(map)
