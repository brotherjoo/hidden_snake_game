import pygame as pg
from random import randrange


def get_random_position():
    return [randrange(*RANGE), randrange(*RANGE)]


WINDOW = 500
TILE_SIZE = 20

# randrange 에 들어가면 TILE_SIZE//2 부터 WINDOW - TILE_SIZE//2 바로 앞까지
# TILE_SIZE를 간격으로 난수가 반환됨
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)

# 뱀 생성
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1

# 뱀 꼬리 생성
tail = [snake.copy()]

# 뱀의 방향 설정
snake_dir = (0, 0)

time, time_step = 0, 100

# 뱀이 먹을 음식
food = snake.copy()
food.center = get_random_position()


screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()

dont = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

while True:
    is_real = False

    for event in pg.event.get():
        if event.type == pg.QUIT:  # 창닫기를 눌렀을때
            exit()
        if event.type == pg.KEYDOWN:  # 키를 눌렀을때
            if event.key == pg.K_o and dont[pg.K_w]:  # 누른 키가 w일때
                snake_dir = (0, -TILE_SIZE)
                dont = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_l and dont[pg.K_s]:  # 누른 키가 s일때
                snake_dir = (0, TILE_SIZE)
                dont = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_k and dont[pg.K_a]:  # 누른 키가 a때
                snake_dir = (-TILE_SIZE, 0)
                dont = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_SEMICOLON and dont[pg.K_d]:  # 누른 키가 d일때
                snake_dir = (TILE_SIZE, 0)
                dont = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
            if event.key == pg.K_PAGEDOWN:
                is_real = True

    screen.fill("black")

    self_eating = pg.Rect.collidelist(snake, tail[:-1]) != -1

    if (  # 벽과 충돌했을 때
        snake.left < 0
        or snake.right > WINDOW
        or snake.top < 0
        or snake.bottom > WINDOW
        or self_eating
    ):
        snake.center, food.center = (
            get_random_position(),
            get_random_position(),
        )  # 뱀과 먹이의 위치를 랜덤으로 재 지정
        length, snake_dir = 1, (0, 0)  # 길이 초기화
        tail = [snake.copy()]
        dont = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
        time_step = 100

    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
        if time_step > 40:
            time_step -= 1

    if is_real:
        pg.draw.rect(screen, "yellow", food)
    else:
        pg.draw.rect(screen, "black", food)

    [pg.draw.rect(screen, "green", body) for body in tail]

    time_now = pg.time.get_ticks()

    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)  # snake_dir은 벡터값이며 벡터값대로 이동
        tail.append(snake.copy())
        tail = tail[-length:]

    pg.display.flip()
    # flip()은 전체를 업데이트할 때 사용~~
    # pg.display.update() 이렇게도 사용 가능함

    # fps 60으로 설정
    clock.tick(240)
