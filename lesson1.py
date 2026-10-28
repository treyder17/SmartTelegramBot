import turtle

turtle.speed(1)
turtle.shape("classic")
turtle.color("blue")
turtle.pensize(2)
turtle.fillcolor("turquoise")

turtle.begin_fill()

for t in range(4):

    turtle.forward(50)
    turtle.left(90)

turtle.up()


turtle.backward(150)

turtle.down()

for t in range(4):

    turtle.forward(50)
    turtle.left(90)

turtle.end_fill()

turtle.done()