from rendering import load_and_scale_image
from settings import original_tile_size, scale_factor

# Bilder laden und Größe anpassen
player_image = load_and_scale_image('assets/images/player.png', scale_factor/10)
opponent_image = load_and_scale_image('assets/images/opponent.png', scale_factor/10)
coin_image = load_and_scale_image('assets/images/coin.png', scale_factor/10)
end_image = load_and_scale_image('assets/images/end.png', scale_factor/10)
wall_image = load_and_scale_image('assets/images/wall.png', scale_factor/10)
