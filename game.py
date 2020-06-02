# coding=utf-8
import time
from sprites import *
from os import *
import sys
from image import load_image
import sqlite3


count_laser = COUNT_LASER


def show_energy_bar(energy):  # Шкала энергии
    color = 2.55 * energy

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -1 * energy))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110), 2)


def show_laser_bar(laser):  # Шкала лазеров
    color = 5.1 * laser

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -1 * laser * 2))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110), 2)


def draw_text(text, source, surface, x, y):
    # Временный объект, используемый только для получения прямоугольника (text_obj.get_rect ())
    text_object = source.render(text, True, TEXTCOLOR)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(source.render(text, True, TEXTCOLOR), text_rect)


def show_game_result(points):
    global destroyed_enemy_counter, game_challenge, lvl, count_laser, index_nick, score_top
    if destroyed_enemy_counter >= game_challenge:
        sound = game_won_sound
        img = load_image(path.join('static', 'img', 'background', 'game_won.jpg'), True, DISPLAYMODE)
        lvl += 1
        game_challenge += 5
    else:
        sound = game_over_sound
        img = load_image(path.join('static', 'img', 'background', 'game_lost.jpg'), True, DISPLAYMODE)
        lvl = 1
        game_challenge = 3
    destroyed_enemy_counter = 0
    new_data(lvl, game_challenge, index_nick, score_top, destroyed_enemy_counter)
    window.blit(img, (0, 0))
    pygame.display.update()
    draw_text(str(points), font_2, window, (WINDOW_WIDTH / 2) - 20, (WINDOW_HEIGHT / 2) - 20)
    pygame.display.update()
    music_channel.play(sound, loops=0, maxtime=0, fade_ms=0)


def exit_game():
    pygame.quit()
    sys.exit()


def pause_game():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Нажав клавишу esc, мы выходим из игры
                    exit_game()
                if event.key == pygame.K_p:
                    pause = False

        draw_text("PAUSE", font_1, window, (WINDOW_WIDTH / 2) - 50, (WINDOW_HEIGHT / 2))
        pygame.display.update()


def wait_for_keystroke():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return


def wait_for_keystroke_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_SPACE:
                    return


def show_help():
    img_help = load_image(path.join('static', 'img', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    window.blit(img_help, (0, 0))  # Изображение для покрытия фона
    pygame.display.update()
    wait_for_keystroke()  # Мы не выйдем из цикла, пока не нажмем любую клавишу


def show_list_nick():
    global index_nick
    img_nick = load_image(path.join('static', 'img', 'background', 'background_nick.jpg'), True, DISPLAYMODE)
    window.blit(img_nick, (0, 0))  # Изображение для покрытия фона
    list_nick = []
    for j in range(NUMBER_NIK):  # Загружаем картинки
        path_image = os.path.join('static', 'img', 'spaceship', str(j + 1), "spaceship_3.png")
        list_nick.append(load_image(path_image, False, (LENGTH_SPACESHIP, WIDTH_SPACESHIP)))
        image_nick = list_nick[j]
        window.blit(image_nick, (150 * (j + 1), 150))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_1]:
            index_nick = 1
            return update_player(index_nick)
        if key_pressed[pygame.K_2]:
            index_nick = 2
            return update_player(index_nick)


def update_player(index):
    player = Player(index)  # Настраиваем игрока
    group_laser_player = pygame.sprite.RenderUpdates()
    player_team = pygame.sprite.RenderUpdates(player)
    enemy_team = pygame.sprite.RenderUpdates()
    return player, group_laser_player, player_team, enemy_team


def new_game():
    pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=4096)
    music_channel.play(intro_sound, loops=-1, maxtime=0, fade_ms=0)
    pygame.display.set_caption("Star Wars")
    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # Фоновое изображение
    background = load_image(path.join('static', 'img', 'background', 'background_1.jpg'), True, DISPLAYMODE)
    window.blit(background, (0, 0))
    pygame.mouse.set_visible(False)  # Прячем мышку на поле
    pygame.display.update()
    wait_for_keystroke_menu()
    music_channel.stop()


def new_data(l, challenge, nick, score, destroyed_enemy):
    global count_laser
    count_laser = COUNT_LASER
    con = sqlite3.connect(path.join('db', 'player data.db'))
    cur = con.cursor()
    cur.execute("""INSERT INTO game (lvl, challenge, index_nick, score, destroyed_enemy_counter)
                VALUES(?, ?, ?, ?, ?)""", (l, challenge, nick, score, destroyed_enemy))
    con.commit()
    con.close()


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        new_game()
        self.time = pygame.time.Clock()

    def run(self):
        global destroyed_enemy_counter, count_laser, index_nick, lvl, game_challenge, score_top
        con = sqlite3.connect(path.join('db', 'player data.db'))
        cur = con.cursor()
        result = cur.execute('''SELECT lvl, challenge, index_nick, score, destroyed_enemy_counter FROM game
                                    WHERE ID = (SELECT MAX(ID) FROM game)''')
        for elem in result:
            lvl = elem[0]  # Текущий уровень
            game_challenge = elem[1]  # Количество дронов которых необходимо убить
            index_nick = elem[2]  # Индекс ника
            score_top = elem[3]  # Лучший счет
            destroyed_enemy_counter = elem[4]  # Количество уничтоженых дроидов
        con.commit()
        con.close()
        delay_laser = 0
        fps_laser = 0
        time_elapsed = time.clock()

        while True:
            if not time.clock():
                start_time = time.perf_counter()
            else:
                start_time = time.clock()

            enemy_creation_period = 2
            energy = INIT_ENERGY
            points = 0
            counter_asteroid = 0

            # Настраиваем игрока и врага
            player, group_laser_player, player_team, enemy_team = update_player(index_nick)
            for _ in range(3):
                enemy_team.add(Enemy())
            group_asteroids = pygame.sprite.RenderUpdates()  # Настраиваем врагов
            group_energy = pygame.sprite.RenderUpdates()
            group_explosion = pygame.sprite.RenderUpdates()  # Имитация взрыва

            # Фоновое изображение
            background_game = load_image(path.join('static', 'img', 'background', 'background_2.jpg'),
                                         True, DISPLAYMODE)

            # Меню игрока
            energy_box = TextBox("Жизненная энергия: {}".format(energy), font_1, 10, 80)
            score_top_box = TextBox("Лучший счет: {}".format(score_top), font_1, 10, 120)
            objectives_box = TextBox("Вы уничтожили: {} дроидов".format(destroyed_enemy_counter), font_1, 10, 160)
            challenge_box = TextBox("Осталось: {} дроидов".format(game_challenge - destroyed_enemy_counter),
                                    font_1, 10, 200)
            time_box = TextBox("Время: {0:.2f}".format(start_time), font_1, 10, 240)
            points_box = TextBox("Счёт: {}".format(points), font_1, 10, 280)
            lvl_box = TextBox("Уровень: {}".format(lvl), font_1, 10, 320)
            group_box = pygame.sprite.RenderUpdates(points_box, score_top_box, objectives_box, challenge_box,
                                                    time_box, energy_box, lvl_box)

            counter_loop = 0
            check_on_press_keys = True
            while True:
                # Отрисовываем задний фон
                window.blit(background_game, (0, 0))
                # После проигрыша доступ к клавишам ограничивается
                if check_on_press_keys:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:
                                show_help()
                            if event.key == pygame.K_F2:
                                player.kill()
                                player, group_laser_player, player_team, enemy_team = show_list_nick()
                            if event.key == pygame.K_p:
                                pause_game()
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_ESCAPE:
                                exit_game()
                            if event.key == pygame.K_n:
                                lvl, game_challenge,  index_nick, score_top, destroyed_enemy_counter = 1, 3, 1, 0, 0
                                new_data(lvl, game_challenge,  index_nick, score_top, destroyed_enemy_counter)
                                new_game()
                            if event.key == pygame.K_SPACE:
                                delay_laser = 9
                        elif event.type == pygame.KEYUP:
                            player.x_speed, player.y_speed = 0, 0
                    # Перемещение игрока в пространстве(на экране)
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
                        player.x_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
                        player.x_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                        player.y_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_SPACE]:
                        delay_laser += 1
                        fps_laser = 0
                        if delay_laser == 10 and count_laser - 1 > 0:
                            group_laser_player.add(PlayerLaser(player.rect.midtop))
                            delay_laser = 0
                            count_laser -= 1
                    else:
                        fps_laser += 1
                        if fps_laser == 25 and count_laser < COUNT_LASER:
                            count_laser += 1
                            fps_laser = 0

                else:  # Мы входим в блок сразу после того, как энергия заканчивается
                    # (ЗАДЕРЖКА * 6 - количество изображений анимации) + еще 20 циклов, чтобы иметь момент паузы
                    total_loops = (DELAY_EXPLOSION * 6) + 20
                    if counter_loop == total_loops:
                        break  # Мы оставили левый цикл
                    counter_loop += 1  # Увеличиваем счетчик
                counter_asteroid += 1
                if counter_asteroid == ADDNEW_ASTEROID_RATE:
                    counter_asteroid = 0
                    group_asteroids.add(Asteroid())

                # Создайте вражеских дроидов
                # Служит для добавления дроидов всякий раз, когда его значение больше или равно 500
                # Затем он сбрасывается. Нельзя насильно добавлять дроидов
                enemy_creation_period += 12

                if len(enemy_team) <= MAX_NUMBER_DROIDS:
                    # Мы ограничиваем максимальное количество дроидов, которые будут созданы
                    if enemy_creation_period >= 450:
                        enemy_creation_period = 0
                        enemy_team.add(Enemy())
                    elif enemy_creation_period == 210:
                        for _ in range(2):
                            enemy_team.add(Enemy())
                    elif enemy_creation_period == 50:
                        for _ in range(3):
                            enemy_team.add(Enemy())

                # Считаем время
                if not time.clock():
                    time_current = time.perf_counter()
                else:
                    time_current = time.clock()
                # Устонавливаем конечное время
                time_elapsed = time_current - start_time

                # Смерть персонажа. Мы проверяем, что это сделано один раз
                if energy == 0 and check_on_press_keys:
                    explosion_player.play()
                    check_on_press_keys = False  # Чтобы отключить ввод нажатий клавиш
                    group_explosion.add(Explosion(player.rect))
                    player.kill()  # Мы убиваем персонажа
                # Игрок выигрывает
                elif destroyed_enemy_counter >= game_challenge:
                    player.kill()
                    break

                # =========================
                # СПРАЙТ СТОЛКНОВЕНИЯ
                # =========================

                # Урон, нанесенный врагом игроку
                for player in pygame.sprite.groupcollide(player_team, group_laser_enemy, False, True):
                    energy -= 15
                # Лазер уничтожает вражеский корабль
                for droid in pygame.sprite.groupcollide(enemy_team, group_laser_player, True, True):
                    points += 15
                    group_explosion.add(Explosion(droid.rect, "explosion"))  # Исчезает во взрыве
                    explosion_droid.play()
                    destroyed_enemy_counter += 1
                # Лазер уничтожает астероиды
                for asteroid in pygame.sprite.groupcollide(group_asteroids, group_laser_player, False, True):
                    points += 5
                    group_explosion.add(Explosion(asteroid.rect, "smoke"))  # Исчезает в облаке дыма
                    explosion_asteroid.play()
                    # Мы спрашиваем, является ли это астероидом (астероид дает энергию для изменения изображения)
                    if asteroid.is_energetic:
                        asteroid.image = asteroid.select_image(path.join('resources', 'energy.png'), True)
                        asteroid.x_speed = 0  # Падать вертикально
                        asteroid.y_speed = 2  # Чтобы замедлить
                        group_energy.add(asteroid)
                        group_asteroids.remove(asteroid)
                    else:
                        asteroid.kill()
                # Когда астероид попадает на корабль
                for asteroid in pygame.sprite.groupcollide(group_asteroids, player_team, True, False):
                    energy -= 10  # Уменьшить энергию, которую имеет корабль
                    group_explosion.add(Explosion(asteroid.rect, "smoke"))
                    explosion_asteroid.play()
                # Когда дроид попадает на корабль
                for droid in pygame.sprite.groupcollide(enemy_team, player_team, True, False):
                    energy -= 10  # Уменьшить энергию, которую имеет корабль
                    group_explosion.add(Explosion(droid.rect, "explosion"))
                    explosion_droid.play()
                # Когда мы прикасаемся к энергии
                for e in pygame.sprite.groupcollide(group_energy, player_team, True, False):
                    energy += e.energy_lvl  # Пополняем энергию игрока
                    energy_sound.play()

                # =============================
                # ОБНОВЛЯЕМ ВСЕ ГРУППЫ
                # =============================
                player_team.update()
                group_laser_player.update()
                enemy_team.update()
                group_laser_enemy.update()
                group_asteroids.update()
                group_energy.update()
                group_box.update()
                group_explosion.update()
                # =======================
                # ОЧИЩАЕМ СПРАЙТЫ
                # =======================
                player_team.clear(window, background_game)
                group_laser_player.clear(window, background_game)
                enemy_team.clear(window, background_game)
                group_laser_enemy.clear(window, background_game)
                group_asteroids.clear(window, background_game)
                group_energy.clear(window, background_game)
                group_box.clear(window, background_game)
                group_explosion.clear(window, background_game)
                player_team.draw(window)
                group_laser_player.draw(window)
                enemy_team.draw(window)
                group_laser_enemy.draw(window)
                group_asteroids.draw(window)
                group_energy.draw(window)
                group_box.draw(window)
                group_explosion.draw(window)

                # Вносим новые значения в меню игрока
                energy_box.text = "Энергия: {0}%".format(int(energy))
                points_box.text = "Счёт: {}".format(points)
                score_top_box.text = "Лучший счет: {}".format(score_top)
                objectives_box.text = "Вы уничтожили: {} дроидов".format(destroyed_enemy_counter)
                challenge_box.text = "Осталось: {} дроидов".format(game_challenge - destroyed_enemy_counter)
                time_box.text = "Время: %.2f" % time_elapsed
                lvl_box.text = "Уровень: {}".format(lvl)

                if energy < 0:
                    energy = 0
                elif energy > 100:
                    energy = 100
                show_energy_bar(energy)
                show_laser_bar(count_laser)

                pygame.display.update()
                self.time.tick(FPS)

            # Мы печатаем счет
            if points > score_top:  # Мы проверяем, превышает ли он лучший результат
                score_top = points
            show_game_result(points)
            time_lapse = 1000
            pygame.time.delay(time_lapse)
            wait_for_keystroke()
