from rendering import load_and_scale_image
from settings import original_tile_size, scale_factor

# Bilder laden und Größe anpassen
pacman_image = load_and_scale_image('pacman.png', scale_factor/10)
opponent_image = load_and_scale_image('opponent.png', scale_factor/10)
coin_image = load_and_scale_image('coin.png', scale_factor/10)
end_image = load_and_scale_image('end.png', scale_factor/10)
wall_image = load_and_scale_image('wall.png', scale_factor/10)
