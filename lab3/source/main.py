import pygame
import sys
from managers.ConfigManager import ConfigManager
from view.GameRenderer import GameRenderer
from model.Board import Board
from GameController import GameController
from ui.UIManager import UIManager
from managers.RecordManager import RecordManager
from managers.SoundManager import SoundManager
from Network import Network

# состояния игры (меню, игра, справка, рекорды)
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_HELP = "help"
STATE_RECORDS = "records"


# главная функция
def main():
    # инициализация
    pygame.init()
    config = ConfigManager()
    window_settings = config.get_window_settings()

    screen = pygame.display.set_mode(
        (window_settings["width"], window_settings["height"]), pygame.RESIZABLE
    )
    pygame.display.set_caption(window_settings["title"])
    clock = pygame.time.Clock()

    # создание менеджеров
    sound_manager = SoundManager()
    sound_manager.play_music("menu.mp3")
    record_manager = RecordManager()

    # игровые объекты (создаются при старте игры)
    game_board = None
    renderer = None
    controller = None

    # интерфейс
    screen_w, screen_h = screen.get_size()
    ui = UIManager(screen_w, screen_h)

    # начальное состояние
    current_state = STATE_MENU
    is_running = True

    # главный игровой цикл
    while is_running:
        mouse_pos = pygame.mouse.get_pos()

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # изменение размера окна
            elif event.type == pygame.VIDEORESIZE:
                screen_w, screen_h = event.w, event.h
                screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
                ui.build(screen_w, screen_h, ui.input_box.text)
                if renderer:
                    renderer.screen = screen
                    renderer.update_dimensions()

            # прокрутка колесиком мыши в справке
            elif event.type == pygame.MOUSEWHEEL:
                if current_state == STATE_HELP:
                    ui.scroll_y += event.y * 30
                    # защита от прокрутки выше начала
                    if ui.scroll_y > 0:
                        ui.scroll_y = 0

            # события в главном меню
            elif current_state == STATE_MENU:
                for btn in ui.menu_buttons:
                    btn.check_hover(mouse_pos)
                    if btn.is_clicked(event):
                        if btn == ui.btn_start:
                            # запуск локальной игры
                            game_board = Board()
                            renderer = GameRenderer(screen, config)
                            controller = GameController(
                                game_board, renderer, sound_manager
                            )
                            current_state = STATE_PLAYING
                            sound_manager.play_music("game.mp3")
                        elif btn == ui.btn_online:
                            # запуск онлайн игры
                            net = Network()
                            assigned_color = net.connect()
                            if assigned_color:
                                game_board = Board()
                                renderer = GameRenderer(screen, config)
                                controller = GameController(
                                    game_board, renderer, sound_manager
                                )

                                controller.network = net
                                controller.my_color = assigned_color
                                # связываем сетевые ходы с контроллером
                                net.set_callback(
                                    lambda start, end: controller.incoming_moves.append(
                                        (start, end)
                                    )
                                )

                                current_state = STATE_PLAYING
                                sound_manager.play_music("game.mp3")
                            else:
                                print("Сервер недоступен. Запустите server.py!")
                        elif btn == ui.btn_records:
                            current_state = STATE_RECORDS
                        elif btn == ui.btn_help:
                            current_state = STATE_HELP
                            ui.scroll_y = 0  # сброс прокрутки
                        elif btn == ui.btn_exit:
                            is_running = False

            # события в справке и рекордах
            elif current_state in (STATE_HELP, STATE_RECORDS):
                ui.btn_back.check_hover(mouse_pos)
                if ui.btn_back.is_clicked(event):
                    current_state = STATE_MENU

            # события в игре
            elif current_state == STATE_PLAYING:
                # если игра окончена
                if game_board.game_over:
                    if game_board.winner == "draw":
                        if ui.btn_to_menu.is_clicked(event):
                            current_state = STATE_MENU
                            sound_manager.play_music("menu.mp3")
                    else:
                        # обработка ввода имени победителя
                        ui.input_box.handle_event(event)
                        if ui.btn_save.is_clicked(event):
                            record_manager.add_win(ui.input_box.text)
                            ui.input_box.text = ""
                            ui.input_box.txt_surface = ui.input_box.font.render(
                                "", True, ui.input_box.color
                            )
                            current_state = STATE_MENU
                            sound_manager.play_music("menu.mp3")
                else:
                    # обработка кликов по доске
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        flip_board = game_board.current_turn == "b"
                        controller.handle_mouse_click(mouse_pos, flip_board)

        # отрисовка
        screen.fill((45, 30, 20))  # фон

        # отрисовка меню
        if current_state == STATE_MENU:
            font = pygame.font.SysFont("Arial", int(screen_h * 0.1), bold=True)
            title = font.render("ШАХМАТЫ", True, (255, 215, 0))
            screen.blit(
                title, (screen_w // 2 - title.get_width() // 2, int(screen_h * 0.1))
            )
            for btn in ui.menu_buttons:
                btn.draw(screen)

        # отрисовка справки
        elif current_state == STATE_HELP:
            ui.btn_back.draw(screen)
            ui.draw_help_screen(screen, screen_w, screen_h)

        # отрисовка рекордов
        elif current_state == STATE_RECORDS:
            ui.btn_back.draw(screen)
            font_title = pygame.font.SysFont(
                "Arial", max(int(screen_h * 0.06), 24), bold=True
            )
            title = font_title.render("Топ-10 Победителей", True, (255, 215, 0))
            screen.blit(
                title,
                (screen_w // 2 - title.get_width() // 2, max(int(screen_h * 0.05), 20)),
            )

            top_players = record_manager.get_top_players()
            if not top_players:
                font = pygame.font.SysFont("Arial", 32)
                text = font.render("Таблица пока пуста", True, (200, 200, 200))
                screen.blit(text, (screen_w // 2 - text.get_width() // 2, 250))
            else:
                y_offset = int(screen_h * 0.2)
                font_rec = pygame.font.SysFont(
                    "Arial", max(int(screen_h * 0.04), 18), bold=True
                )

                # заголовки таблицы
                screen.blit(
                    font_rec.render("ИГРОК", True, (180, 140, 100)),
                    (screen_w // 2 - int(screen_w * 0.25), y_offset),
                )
                screen.blit(
                    font_rec.render("ПОБЕДЫ", True, (180, 140, 100)),
                    (screen_w // 2 + int(screen_w * 0.1), y_offset),
                )

                pygame.draw.line(
                    screen,
                    (180, 140, 100),
                    (screen_w // 2 - int(screen_w * 0.27), y_offset + 40),
                    (screen_w // 2 + int(screen_w * 0.27), y_offset + 40),
                    width=2,
                )
                y_offset += int(screen_h * 0.08)

                # вывод игроков
                font_name = pygame.font.SysFont("Arial", max(int(screen_h * 0.035), 16))
                for i, (name, wins) in enumerate(top_players):
                    color = (255, 215, 0) if i < 3 else (220, 200, 180)
                    screen.blit(
                        font_name.render(f"{i + 1}. {name}", True, color),
                        (screen_w // 2 - int(screen_w * 0.25), y_offset),
                    )
                    screen.blit(
                        font_name.render(str(wins), True, color),
                        (screen_w // 2 + int(screen_w * 0.15), y_offset),
                    )
                    y_offset += int(screen_h * 0.05)

        # отрисовка игры
        elif current_state == STATE_PLAYING:
            # обработка сетевых ходов
            controller.update()

            # переворот доски для черных в локальной игре
            flip_board = game_board.current_turn == "b"
            # в онлайн игре доска всегда повернута к игроку
            if controller.my_color == "w":
                flip_board = False
            elif controller.my_color == "b":
                flip_board = True

            # отрисовка всех элементов игры
            renderer.draw_board(
                board=game_board,
                flip_board=flip_board,
                selected_square=controller.selected_square,
            )
            renderer.draw_coordinates(flip_board=flip_board)
            renderer.draw_pieces(game_board, flip_board=flip_board)
            renderer.draw_move_hints(
                controller.valid_moves, game_board, flip_board=flip_board
            )

            # если игра окончена, рисуем модальное окно
            if game_board.game_over:
                # затемнение фона
                overlay = pygame.Surface((screen_w, screen_h))
                overlay.set_alpha(150)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                # рамка модального окна
                pygame.draw.rect(screen, (50, 30, 20), ui.modal_rect, border_radius=15)
                pygame.draw.rect(
                    screen, (255, 215, 0), ui.modal_rect, width=3, border_radius=15
                )

                # текст о результате игры
                font = pygame.font.SysFont("Arial", int(screen_h * 0.06), bold=True)
                winner_text = (
                    "ПАТ (НИЧЬЯ)!"
                    if game_board.winner == "draw"
                    else f"ПОБЕДИЛИ {'БЕЛЫЕ' if game_board.winner == 'w' else 'ЧЕРНЫЕ'}!"
                )
                text_surface = font.render(winner_text, True, (255, 215, 0))
                screen.blit(
                    text_surface,
                    text_surface.get_rect(
                        center=(
                            screen_w // 2,
                            ui.modal_rect.y + int(ui.modal_rect.height * 0.15),
                        )
                    ),
                )

                # если ничья, показываем кнопку "в меню"
                if game_board.winner == "draw":
                    ui.btn_to_menu.check_hover(mouse_pos)
                    ui.btn_to_menu.draw(screen)
                else:
                    # если есть победитель, показываем поле для ввода имени
                    font_hint = pygame.font.SysFont(
                        "Arial", max(int(screen_h * 0.03), 16)
                    )
                    hint = font_hint.render(
                        "Введите имя победителя:", True, (220, 200, 180)
                    )
                    screen.blit(
                        hint,
                        hint.get_rect(
                            center=(
                                screen_w // 2,
                                ui.modal_rect.y + int(ui.modal_rect.height * 0.35),
                            )
                        ),
                    )

                    ui.input_box.draw(screen)
                    ui.btn_save.check_hover(mouse_pos)
                    ui.btn_save.draw(screen)

        # обновление экрана
        pygame.display.flip()
        clock.tick(window_settings["fps"])

    # выход из игры
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
