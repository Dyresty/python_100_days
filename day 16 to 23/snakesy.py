from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]

class Snakey:
    def __init__(self):
        self.segments = []
        self.move_distance = 20
        self.create_snake()

    def create_snake(self):
        for i in STARTING_POSITIONS:
            new1 = Turtle("square")
            new1.penup()
            new1.color("white")
            new1.goto(i)
            self.segments.append(new1)

    def add_seg(self):
        new1 = Turtle("square")
        new1.penup()
        new1.color("white")
        new1.goto(self.segments[-1].xcor(), self.segments[-1].ycor())
        self.segments.append(new1)

    def move_snake(self):
        for i in range(len(self.segments) - 1, 0, -1):
            newx = self.segments[i - 1].xcor()
            newy = self.segments[i - 1].ycor()
            self.segments[i].goto(newx, newy)
        self.segments[0].forward(self.move_distance)

    def move_right(self):
        if self.segments[0].heading()!=180:
            self.segments[0].setheading(0)

    def move_left(self):
        if self.segments[0].heading()!= 0:

            self.segments[0].setheading(180)


    def move_up(self):
        if self.segments[0].heading()!= 270:
            self.segments[0].setheading(90)


    def move_down(self):
        if self.segments[0].heading()!= 90:
            self.segments[0].setheading(270)
