from moving_ai.moving_ai_map import *

def check_ai_map(m_str, i, j, expected_cnt):
    lines = m_str.split('|')
    assert all(len(l) == len(lines[0]) for l in lines)
    m = MapMAI(len(lines[0]), len(lines), lines)
    neighbors = list(m.get_neighbors(i, j))
    for n in neighbors:
        compute_cost(i, j, *n)
    assert len(neighbors) == expected_cnt, f'expected cnt: {expected_cnt}, found: {neighbors}'

def test_ai_gen_neighbors():
    check_ai_map('...|...|...', 0, 0, 3)
    check_ai_map('.#.|...|...', 0, 0, 1)

    check_ai_map('...|...|...', 1, 1, 8)
    check_ai_map('.#.|...|.#.', 1, 1, 2)
    check_ai_map('...|...|.#.', 1, 1, 5)
    
    check_ai_map('....|....|....|....', 1, 2, 8)
    
    check_ai_map('.W.|..S|...', 1, 1, 5)
    check_ai_map('WS|..', 0, 0, 1)
    check_ai_map('SSS|SWS|SSS', 1, 1, 8)
    check_ai_map('SSS|S.S|SSS', 1, 1, 8)
    print('Success!')
    
test_ai_gen_neighbors()
