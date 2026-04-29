from turtle import Turtle, Screen
import random

# ---------------- SCREEN ----------------
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Breakout")
screen.tracer(0)

# ---------------- PADDLE ----------------
paddle = Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=8)
paddle.penup()
paddle.goto(0, -250)

# ---------------- UI: LIVES ----------------
life_display = Turtle()
life_display.hideturtle()
life_display.penup()
life_display.color("white")
life_display.goto(0, 260)

message = Turtle()
message.hideturtle()
message.penup()
message.color("white")

# ---------------- GAME STATE ----------------
bricks = []
player_lives = 3

# ---------------- MOVEMENT ----------------
def move_left():
    if paddle.xcor() > -320:
        paddle.setx(paddle.xcor() - 20)

def move_right():
    if paddle.xcor() < 320:
        paddle.setx(paddle.xcor() + 20)

# ---------------- BRICKS ----------------
def create_row(y, count, color, stretch_len, spacing, start_x):
    for i in range(count):
        brick = Turtle("square")
        brick.shapesize(stretch_len=stretch_len, stretch_wid=1)
        brick.penup()
        brick.color(color)

        x = start_x + i * spacing
        brick.goto(x, y)

        bricks.append(brick)

# ---------------- UI FUNCTIONS ----------------
def update_lives():
    life_display.clear()
    life_display.write(f"Lives: {player_lives}", align="center", font=("Arial", 20, "normal"))

def show_game_over():
    message.clear()
    message.goto(0, 0)
    message.write("GAME OVER", align="center", font=("Arial", 60, "bold"))

def show_win():
    message.clear()
    message.goto(0, 0)
    message.write("YOU WIN!", align="center", font=("Arial", 60, "bold"))

# ---------------- CONTROLS ----------------
screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

# ---------------- BALL ----------------
ball = Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)

ball.dx = 3
ball.dy = 3

# ---------------- LEVEL ----------------
create_row(200, 12, "red", 2, 60, -330)
create_row(170, 8, "blue", 2, 60, -270)
create_row(140, 8, "green", 2, 60, -210)
create_row(110, 12, "yellow", 2, 60, -330)
create_row(80, 9, "purple", 2, 60, -270)
create_row(50, 9, "orange", 2, 60, -210)

update_lives()

# ---------------- GAME LOOP ----------------
game_is_on = True

while game_is_on:
    screen.update()

    # BALL MOVE
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # WALLS
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.dx *= -1

    if ball.ycor() > 290:
        ball.dy *= -1

    # PADDLE COLLISION
    if (
        ball.ycor() > -240 and
        ball.distance(paddle) < 50 and
        ball.dy < 0
    ):
        ball.dy *= -1

    # BRICKS COLLISION
    for brick in bricks[:]:
        if ball.distance(brick) < 20:
            brick.hideturtle()
            bricks.remove(brick)
            ball.dy *= -1
            break

    # WIN
    if len(bricks) == 0:
        game_is_on = False
        show_win()

    # LOSE / RESET
    if ball.ycor() < -290:
        ball.goto(0, 0)
        ball.dx = random.choice([-5, 5])
        ball.dy = -5

        player_lives -= 1
        update_lives()

        if player_lives == 0:
            game_is_on = False
            show_game_over()

screen.exitonclick()