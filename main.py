from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor

class AppGame(ShowBase):
    def __init__(self):
        super().__init__()



game = AppGame()
game.run()
