from pygame import mixer

# Init mixer
mixer.init()

# Load music
bullet1_sound = mixer.Sound("./assets/music/bulletmusic.mp3")
space_music = mixer.Sound("./assets/music/spacemusic.mp3") # This sucks
rocket_sound = mixer.Sound("./assets/music/rocketsound.wav")

# Configure the sounds
space_music.set_volume(0.2)
bullet1_sound.set_volume(0.1)
rocket_sound.set_volume(0.15)