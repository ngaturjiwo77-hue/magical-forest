import pygame

# Inisialisasi awal untuk mengambil resolusi layar
pygame.init()
info = pygame.display.Info()
WIDTH = info.current_w if info.current_w > 0 else 1080
HEIGHT = info.current_h if info.current_h > 0 else 2200

# Skalasi Ukuran Berdasarkan Layar HP
BASE_UNIT = min(WIDTH, HEIGHT)
JOYSTICK_RADIUS = int(BASE_UNIT * 0.13)
STICK_RADIUS = int(JOYSTICK_RADIUS * 0.4)
PLAYER_RADIUS = int(BASE_UNIT * 0.035)
STAR_MAX_RADIUS = int(BASE_UNIT * 0.025)

# Ukuran Font
FONT_LARGE = int(HEIGHT * 0.035)
FONT_SMALL = int(HEIGHT * 0.02)

# Tema Warna Berdasarkan Level (Atas, Bawah)
LEVEL_THEMES = {
    1: ((22, 18, 41), (50, 35, 74)),    # Indigo & Ungu Mistik
    2: ((10, 35, 46), (25, 74, 82)),    # Deep Blue & Toska Lembah
    3: ((46, 15, 34), (82, 35, 60))     # Misteri Magenta / Pink Malam
}

# Palet Warna Objek
PLAYER_COLOR = (143, 240, 217)
STAR_COLORS = [
    (255, 201, 113),  # Emas
    (255, 154, 162),  # Pink Pastel
    (181, 234, 215),  # Hijau Mint
    (226, 202, 239)   # Lavender
]
TEXT_COLOR = (245, 239, 255)
