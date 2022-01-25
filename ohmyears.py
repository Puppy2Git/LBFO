class soundManager():
    base = None
    Music_Idle = None
    Music_Tugging = None
    MusicState = False
    vol1 = 1.0
    vol2 = 0.0
    speed = 1
    def __init__(self,base):
        self.base = base
        self.manager = self.base.musicManager
        self.manager.setConcurrentSoundLimit(2)
        self.Music_Idle = self.base.loader.loadMusic("Sounds/Idle.wav")
        self.Music_Tugging = self.base.loader.loadMusic("Sounds/Tugging.wav")
        self.Music_Idle.setLoop()
        self.Music_Tugging.setLoop()
        self.Music_Idle.setVolume(self.vol1)
        self.Music_Tugging.setVolume(self.vol2)
        self.Music_Idle.play()
        self.Music_Tugging.play()

    def update_musicshift(self, task):
        '''
        Handles the smooth transition between the Idle and Tugging wav files\n
        This should be called in the main update function
        '''
        
        #modifier
        if self.MusicState:
            mod = globalClock.getDt()
        else:
            mod = globalClock.getDt() * -1
        #Update vol1
        self.vol1 = self.vol1 - mod * self.speed
        if (self.vol1 < 0):
            self.vol1 = 0
        elif (self.vol1 > 1):
            self.vol1 = 1
        #Update vol2
        self.vol2 = self.vol2 + mod * self.speed
        if (self.vol2 < 0):
            self.vol2 = 0
        elif (self.vol2 > 1):
            self.vol2 = 1
        self.Music_Idle.setVolume(self.vol1)
        self.Music_Tugging.setVolume(self.vol2)
        return task.cont
        
    def ToggleMusic(self, state):
        '''
        Switches the priority of the music given the state\n
        Should be called when tugging variable in gameWorld is changed\n
        >>> my_sound.ToggleMusic(False)\n
        Go back to Idle music
        '''
        self.MusicState = state