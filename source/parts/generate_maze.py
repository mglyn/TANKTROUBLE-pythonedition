import random
from .. import constants as C
from . import cell


def get_idx(x, y):
    return x+y*C.COLUMN_NUM


def predeal(arena):
    for i in range(0, C.COLUMN_NUM*C.ROW_NUM):
        arena.cells.append(cell.Cell(
            C.LEFT_SPACE+i % C.COLUMN_NUM*C.BLOCK_SIZE,
            C.TOP_SPACE+int(i/C.COLUMN_NUM)*C.BLOCK_SIZE,
            walls_sign=C.BOTTOM | C.RIGHT))
        arena.cells[i].draw_cell(arena.map_surface)

    for x in range(0, C.COLUMN_NUM):
        i = get_idx(x, 0)
        arena.cells[i] = cell.Cell(
            C.LEFT_SPACE+i % C.COLUMN_NUM*C.BLOCK_SIZE,
            C.TOP_SPACE+int(i/C.COLUMN_NUM)*C.BLOCK_SIZE,
            walls_sign=C.TOP | C.BOTTOM | C.RIGHT)
        arena.cells[i].draw_cell(arena.map_surface)

    for y in range(0, C.ROW_NUM):
        i = get_idx(0, y)
        arena.cells[i] = cell.Cell(
            C.LEFT_SPACE+i % C.COLUMN_NUM*C.BLOCK_SIZE,
            C.TOP_SPACE+int(i/C.COLUMN_NUM)*C.BLOCK_SIZE,
            walls_sign=C.BOTTOM | C.LEFT | C.RIGHT)
        arena.cells[i].draw_cell(arena.map_surface)

    arena.cells[0] = cell.Cell(
        C.LEFT_SPACE, C.TOP_SPACE, walls_sign=C.TOP | C.BOTTOM | C.LEFT | C.RIGHT)
    arena.cells[0].draw_cell(arena.map_surface)


def Generage_Maze(arena, x, y, x_, y_):
    if x_-x == 0:
        for u in range(y, y_):
            for wall in arena.cells[get_idx(x, u)].walls:
                if wall.type == C.BOTTOM:
                    wall.kill()
        for u in range(y_, y, -1):
            for wall in arena.cells[get_idx(x, u)].walls:
                if wall.type == C.TOP:
                    wall.kill()
        return
    if y_-y == 0:
        for v in range(x, x_):
            for wall in arena.cells[get_idx(v, y)].walls:
                if wall.type == C.RIGHT:
                    wall.kill()
        for v in range(x_, x, -1):
            for wall in arena.cells[get_idx(v, y)].walls:
                if wall.type == C.LEFT:
                    wall.kill()
        return

    u = random.randint(x, x_-1)
    v = random.randint(y, y_-1)

    Generage_Maze(arena, x, y, u, v)
    Generage_Maze(arena, u+1, y, x_, v)
    Generage_Maze(arena, x, v+1, u, y_)
    Generage_Maze(arena, u+1, v+1, x_, y_)

    choose = [1, 1, 1, 1]
    choose[random.randint(0, 3)] = 0
    randfix = random.uniform(0.8, 1)

    if choose[0] or random.random() < randfix:
        p = random.randint(x, u)
        for wall in arena.cells[get_idx(p, v)].walls:
            if wall.type == C.BOTTOM:
                wall.kill()

    if choose[1] or random.random() < randfix:
        p = random.randint(y, v)
        arena.cells[get_idx(u, p)]
        for wall in arena.cells[get_idx(u, p)].walls:
            if wall.type == C.RIGHT:
                wall.kill()

    if choose[2] or random.random() < randfix:
        p = random.randint(u+1, x_)
        arena.cells[get_idx(p, v)]
        for wall in arena.cells[get_idx(p, v)].walls:
            if wall.type == C.BOTTOM:
                wall.kill()

    if choose[3] or random.random() < randfix:
        p = random.randint(v+1, y_)
        arena.cells[get_idx(u, p)]
        for wall in arena.cells[get_idx(u, p)].walls:
            if wall.type == C.RIGHT:
                wall.kill()