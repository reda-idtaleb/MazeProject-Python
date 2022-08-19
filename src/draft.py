import glob as gl
from pydub import AudioSegment
from pydub.playback import play

dir = "musics/"
extension = "mp3"
music_list = [file for file in gl.glob(dir + "*.%s" %(extension))]

AudioSegment.from_mp3(music_list[0])
print(music_list)