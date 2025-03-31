from turtle import Turtle
class P1Stick(Turtle):
    def __init__(self,xcors,ycors):
        super().__init__()
        self.inst=[]
        self.move_distance = 20
        self.x1 = xcors
        self.y1 = ycors
        self.create_p1()

    def create_p1(self):
        new1 = Turtle("square")
        new1.penup()
        new1.shapesize(stretch_wid=5, stretch_len=1)
        new1.color("blue")
        if self.x1<0:
            new1.color("red")
        new1.goto(self.x1, self.y1)
        self.inst.append(new1)

    def move_up(self):
        if self.inst[0].ycor()<240:
            ycoor = self.inst[0].ycor() + 40
            self.inst[0].goto(self.inst[0].xcor(), ycoor)

    def move_down(self):
        if self.inst[0].ycor() >-240:
            ycoor = self.inst[0].ycor() - 40
            self.inst[0].goto(self.inst[0].xcor(), ycoor)