from turtle import Turtle
import random

class balls(Turtle):
    def __init__(self,xcors,ycors):
        super().__init__()
        self.inst = []
        self.move_distance = 20
        self.x1 = xcors
        self.y1 = ycors
        self.create_p1()
        self.xmove=2
        self.ymove=2

    def create_p1(self):
        new1 = Turtle("circle")
        new1.penup()
        new1.color("yellow")
        new1.goto(self.x1, self.y1)
        self.inst.append(new1)

    def move(self):
        newx = self.inst[0].xcor()+self.xmove
        newy = self.inst[0].ycor()+self.ymove
        self.inst[0].goto(newx, newy)

    def restart(self):
        self.xmove=2
        self.ymove=2
        self.inst[0].goto(0,0)
        r = random.randint(0, 3)
        if r == 0:
            pass
        if r == 1:
            self.xmove *= -1
        if r == 2:
            self.ymove *= -1
        if r == 3:
            self.xmove *= -1
            self.ymove *= -1


    def bounce(self):
        self.ymove *= -1

    def change_direction(self):
        self.xmove *= -1




