class soundManager():
    base = None
    Music_Idle = None
    Music_Tugging = None
    MusicState = False
    def __init__(self,base):
        self.base = base
        self.manager = self.base.musicManager
        self.manager.setConcurrentSoundLimit(2)
        self.Music_Idle = self.base.loader.loadMusic("Sounds/Idle.wav")
        self.Music_Tugging = self.base.loader.loadMusic("Sounds/Tugging.wav")
        self.Music_Idle.loop()
        self.Music_Tugging.loop()
        self.Music_Idle.setVolume(1)
        self.Music_Tugging.setVolume(0)
    
    def update_music(self):
        pass
        

    def ToggleMusic(self):
        self.MusicState = not self.MusicState
        if self.MusicState:
            self.Music_Tugging.setVolume(1)
            self.Music_Idle.setVolume(0)
        else:
            self.Music_Tugging.setVolume(1)
            self.Music_Idle.setVolume(0)