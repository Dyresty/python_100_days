from turtle import Turtle


class scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.y_coor = 300
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, self.y_coor - 30)
        self.score(0,0)

    def score(self,x,y):
        self.clear()
        self.goto(0, self.y_coor - 60)
        self.write(f"{x}       {y}", False, align="center", font=("arial", 26, "normal"))


    def game_over(self,player_num):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        if player_num == 1:
            self.write("Player Red wins", False, align="center", font=("arial", 16, "normal"))
        if player_num == 2:
            self.write("Player Blue wins", False, align="center", font=("arial", 16, "normal"))
