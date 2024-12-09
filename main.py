import pygame
import random

# Ініціалізація pygame
pygame.init()

# Параметри вікна гри
WIDTH, HEIGHT = 800, 600  # Розміри вікна гри
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Створення вікна гри
pygame.display.set_caption("Гра \"Змійка\"")  # Заголовок вікна

# Кольори (формат: RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Розмір клітинки для змійки та їжі
CELL_SIZE = 20

# Годинник для контролю FPS
clock = pygame.time.Clock()

# Швидкість гри
speed = 10


def message(msg, color, x, y):
    """
    Функція для відображення повідомлення на екрані.
    :param msg: Текст повідомлення
    :param color: Колір тексту (RGB)
    :param x: Позиція по осі X
    :param y: Позиція по осі Y
    """
    font = pygame.font.SysFont("Arial", 35)  # Створення шрифта
    screen.blit(font.render(msg, True, color), (x, y))  # Відображення тексту на екрані


def game_loop():
    """
    Головна функція, яка запускає гру. Оновлює екран, перевіряє введення користувача та логіку гри.
    """
    game_over = False  # Прапорець для визначення, чи закінчена гра
    game_close = False  # Прапорець для визначення, чи гра закрита після програшу

    # Початкові координати змійки
    x = WIDTH // 2
    y = HEIGHT // 2

    # Початкові зміни координат (рух змійки)
    dx, dy = 0, 0

    # Список для зберігання координат тіла змійки
    snake = []
    snake_length = 1  # Початкова довжина змійки

    # Початкові координати їжі
    food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
    food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE

    # Основний цикл гри
    while not game_over:
        while game_close:
            screen.fill(BLACK)  # Очищення екрану
            message("Гру закінчено! Q - вийти з гри, C - почати заново", RED, WIDTH // 7, HEIGHT // 4)
            pygame.display.update()  # Оновлення екрану

            # Обробка подій після завершення гри (натискання клавіш Q або C)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Вихід з гри
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # Початок нової гри
                        game_loop()

        # Обробка подій (клавіші)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Обробка напрямків змійки (ліво, право, вгору, вниз)
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE

        # Оновлення координат змійки
        x += dx
        y += dy

        # Перевірка на зіткнення з стінками
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        # Перевірка на зіткнення з тілом змійки
        for segment in snake[:-1]:
            if segment == [x, y]:
                game_close = True

        # Додавання нового сегмента змійки
        snake.append([x, y])
        if len(snake) > snake_length:
            del snake[0]  # Видалення останнього сегмента (якщо довжина змійки зменшується)

        # Очищення екрану та малювання їжі
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, CELL_SIZE, CELL_SIZE])

        # Малювання змійки
        for segment in snake:
            pygame.draw.rect(screen, BLUE, [segment[0], segment[1], CELL_SIZE, CELL_SIZE])

        # Перевірка на з'їдання їжі
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            snake_length += 1  # Збільшення довжини змійки

        # Відображення кількості очок
        message(f"Очки: {snake_length - 1}", WHITE, 10, 10)

        # Оновлення екрану
        pygame.display.update()

        # Контроль FPS
        clock.tick(speed)

    # Завершення гри
    pygame.quit()
    quit()


# Запуск гри
game_loop()
