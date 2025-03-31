from turtle import Turtle


class scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 270)
        self.score = 0
        self.write(f"Score : {self.score}", False, align="center", font=("arial",16,"normal"))

    def scored(self):
        self.score += 1
        self.clear()
        self.write(f"Score : {self.score}", False, align="center", font=("arial",16,"normal"))

    def game_over(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.write(f"GAME OVER!!!\n Final Score : {self.score}", False, align="center", font=("arial", 16, "normal"))
