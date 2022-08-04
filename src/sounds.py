from pygame import mixer

# Init mixer
mixer.init()

# Load music
bullet1_sound = mixer.Sound("./assets/music/bulletmusic.mp3")
space_music = mixer.Sound("./assets/music/spacemusic.mp3") # This sucks

# Configure the sounds
space_music.set_volume(0.2)