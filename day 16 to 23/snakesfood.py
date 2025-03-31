from turtle import Turtle
import random

class foods(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("cyan")
        self.shapesize(0.5, 0.5)
        self.speed(0)
        self.refresh()

    def refresh(self):
        self.goto(random.randint(-280,280),random.randint(-280,280))