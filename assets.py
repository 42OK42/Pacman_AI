from rendering import load_and_scale_image
from settings import scale_factor

# Bilder laden und Größe anpassen
player_image = load_and_scale_image('assets/images/player.png', scale_factor/8)
opponent_image = load_and_scale_image('assets/images/opponent.png', scale_factor/10)
coin_image = load_and_scale_image('assets/images/coin.png', scale_factor/15)
end_image = load_and_scale_image('assets/images/end.png', scale_factor/8)
wall_image = load_and_scale_image('assets/images/wall.png', scale_factor/20)
bullet_image = load_and_scale_image('assets/images/bullet.png', scale_factor/20)
