from swampy.TurtleWorld import *
import random

class Disco(Turtle):
    """a Disco is a kind of Turtle that dances and changes colors"""

    def __init__(self, world, speed=1):
        Turtle.__init__(self, world, type='wanderer')
        self.delay = 0
        self.speed = speed
        self.shape = 'Turtle'

        # move to the starting position
        self.pu() 
        self.rt(random.randint(0,360))
        self.bk(150)
        self.type = type

    def wander(self):
        # pick a direction randomly


    def stalk(self):
        # pick a direction facing another turtle

    def step(self):
        """step is invoked by TurtleWorld on every Turtle, once
        per time step."""        
        
        if self.type == 'wanderer':
            self.wander()

        elif elf.type == 'stalker':
            self.stalk()

        self.move()


    def move(self):
        """move forward in proportion to self.speed"""
        self.fd(self.speed)

    def steer(self):
        """Coose a random direction for optimum dancing"""
        self.rt(random.randint(-360,360))

def make_world():

    # create TurtleWorld
    world = TurtleWorld()
    world.delay = .01
    world.setup_run()

    # create three dancers
    Disco(world, 1, 'stalker')
    Disco(world, 2)
    Disco(world, 10)

    return world

if __name__ == '__main__':
    world = make_world()
    world.mainloop() # calls Turtle.step() repeatedly