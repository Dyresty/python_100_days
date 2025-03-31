from turtle import Turtle, Screen
from pingpongstick1 import P1Stick
from pingpongscore import scoreboard
from pingpongball import balls
import random
import time

s = Screen()
s.setup(800, 600)
s.bgcolor("black")
s.title("Ping Pong")
s.tracer(0)
p1 = P1Stick(350, 0)
p2 = P1Stick(-350, 0)
ball = balls(0, 0)
sb = scoreboard()
s.update()
sleeptime = 0.01
counter = 0
game_on = 1
score1 = 0
score2 = 0
while game_on == 1:
    s.update()
    time.sleep(sleeptime)
    ball.move()
    s.listen()
    if ball.inst[0].ycor() > 280 or ball.inst[0].ycor() < -280:
        ball.bounce()
    if (ball.inst[0].distance(p1.inst[0]) < 50 and ball.inst[0].xcor() > 340 or ball.inst[0].distance(p2.inst[0]) < 50
            and ball.inst[0].xcor() < -340):
        counter += 1
        ball.change_direction()
        print(sleeptime)
        if counter % 2 == 0:
            sleeptime *= 0.9
    if ball.inst[0].xcor() > 350:
        score1 += 1
        sb.score(score1, score2)
        ball.restart()
        time.sleep(0.5)
        sleeptime=0.01
    if ball.inst[0].xcor() < -350:
        score2 += 1
        sb.score(score1, score2)
        ball.restart()
        time.sleep(0.5)
        sleeptime = 0.01
    if score1>5:
        game_on = 0
        sb.game_over(1)
    if score2>5:
        game_on = 0
        sb.game_over(2)
    s.onkeypress(fun=p1.move_up, key='Up')
    s.onkeypress(fun=p1.move_down, key='Down')
    s.onkeypress(fun=p2.move_up, key='w')
    s.onkeypress(fun=p2.move_down, key='s')

s.exitonclick()
