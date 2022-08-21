import glob
import random
import pygame

from pygame.locals import *
from pygame import mixer

from constants import MUSIC_DIR

class MusicPlayer():
    def __init__(self, dir=MUSIC_DIR, randomize=True, music_name=""):
        pygame.init()
        mixer.init()
        self.is_playing = False
        self.__music = self.__get_sound(dir, randomize, music_name)

    def __get_sound(self, dir=MUSIC_DIR, randomize=True, music_name=""):
        extension = "ogg"
        default_index = 0
        
        music_list = [file for file in glob.glob(dir + "*.%s" %(extension))]
        if not music_list:
            return ""
        
        if randomize:
            random_index = random.randint(0, len(music_list)-1)
            song = music_list[random_index]
        else:
            music_names = [file[file.rindex('/')+1:] for file in glob.glob(dir + "*.%s" %(extension))]
            if music_name and (music_name in music_names):
                song = dir + music_name
            else:
                song = music_list[default_index]   
        return song
    
    def playsound(self): 
        if not self.__music:
            return
         
        mixer.music.load(self.__music)
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        
        self.is_playing = True
        
    def pause(self):
        mixer.music.pause()
        self.is_playing = False
    