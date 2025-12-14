import turtle
import colorsys
import math

# --- Global Configuration ---
WIDTH, HEIGHT = 600, 600
CONSTANT_SPEED = 3
TURN_SPEED = 15
GAME_STATE = "LOADING" # Can be "LOADING" or "PLAYING"
# Define boundaries based on screen size, adjusting for turtle size (approx 20px)
EDGE_THRESHOLD_X = (WIDTH / 2) - 10 
EDGE_THRESHOLD_Y = (HEIGHT / 2) - 10

# --- Setup Screen ---
wn = turtle.Screen()
wn.title("Bouncing Rainbow Drifting Turtle")
wn.setup(width=WIDTH, height=HEIGHT)
wn.colormode(255) 
wn.tracer(0) 

# --- Game Assets (Turtles) ---
player = turtle.Turtle()
player.shape("turtle")
player.penup()
player.speed(0)
player.hideturtle() # Hide initially for loading screen

# Button Turtle (acts as the clickable button)
play_button = turtle.Turtle()
play_button.speed(0)
play_button.penup()
play_button.shape("square")
play_button.color("green")
play_button.shapesize(stretch_wid=2, stretch_len=5)

# Text Turtle for loading screen messages
text_writer = turtle.Turtle()
text_writer.speed(0)
text_writer.penup()
text_writer.hideturtle()
text_writer.color("white")

# --- State Variables ---
keys_pressed = set()
mouse_target = None
hue_value = 0.0

# --- Function Definitions ---

def start_game(x, y):
    """Callback function when the play button is clicked."""
    global GAME_STATE
    if GAME_STATE == "LOADING":
        GAME_STATE = "PLAYING"
        play_button.hideturtle()
        text_writer.clear()
        player.showturtle()
        wn.onclick(None, 1) # Unbind the main screen click temporarily

def bind_key(key):
    wn.onkeypress(lambda: keys_pressed.add(key), key)
    wn.onkeyrelease(lambda: keys_pressed.remove(key), key)

def handle_mouse_click(x, y):
    global mouse_target
    if GAME_STATE == "PLAYING":
        mouse_target = (x, y)
        player.setheading(player.towards(x, y))

def handle_right_click(x, y):
    global mouse_target
    if GAME_STATE == "PLAYING":
        mouse_target = None 
        player.clear() 

def display_loading_screen():
    """Draw the initial loading screen elements."""
    wn.bgcolor("black")
    text_writer.goto(0, 100)
    text_writer.write("Drifting Turtle Game", align="center", font=("Arial", 30, "bold"))
    text_writer.goto(0, 50)
    text_writer.write("Click 'Play' to start the action!", align="center", font=("Arial", 16, "normal"))
    play_button.goto(0, -50)
    play_button.showturtle()
    play_button.onclick(start_game, 1)

def check_for_bounce():
    """Checks if the turtle is at the edge and reverses its direction."""
    x_pos = player.xcor()
    y_pos = player.ycor()
    heading = player.heading()

    # Check X boundaries
    if abs(x_pos) >= EDGE_THRESHOLD_X:
        # If moving past the right edge or left edge, invert the horizontal component of the heading
        player.setheading(180 - heading)
        # Nudge the turtle slightly inwards to prevent it getting stuck on the edge
        player.forward(CONSTANT_SPEED * 2) 

    # Check Y boundaries
    if abs(y_pos) >= EDGE_THRESHOLD_Y:
        # If moving past the top or bottom edge, invert the vertical component of the heading
        player.setheading(360 - heading)
        # Nudge the turtle slightly inwards
        player.forward(CONSTANT_SPEED * 2) 

# --- Game Loop (Manual Updates) ---
def update_game_state():
    global mouse_target, hue_value

    if GAME_STATE == "PLAYING":
        current_turn = 0

        # 1. Handle Keyboard Input for TURNING ONLY
        if "a" in keys_pressed or "Left" in keys_pressed:
            current_turn = TURN_SPEED
        if "d" in keys_pressed or "Right" in keys_pressed:
            current_turn = -TURN_SPEED
        if current_turn != 0:
            player.right(current_turn) 

        # 2. Handle Mouse Input (overrides direction)
        if mouse_target:
            player.setheading(player.towards(mouse_target))
            if player.distance(mouse_target) < CONSTANT_SPEED:
                player.goto(mouse_target)
                mouse_target = None

        # 3. Apply Constant Movement and Check Bounce
        player.forward(CONSTANT_SPEED)
        check_for_bounce() # Check edges *after* moving

        # 4. Handle Rainbow Colors
        hue_value += 0.005 
        if hue_value > 1.0:
            hue_value = 0.0

        r, g, b = colorsys.hsv_to_rgb(hue_value, 1.0, 1.0)
        rgb_color_turtle = (int(r*255), int(g*255), int(b*255))
        reversed_hue = (hue_value + 0.5) % 1.0 
        r_bg, g_bg, b_bg = colorsys.hsv_to_rgb(reversed_hue, 1.0, 1.0)
        rgb_color_bg = (int(r_bg*255), int(g_bg*255), int(b_bg*255))

        player.color(rgb_color_turtle)
        wn.bgcolor(rgb_color_bg)

    # Update screen and loop
    wn.update()
    wn.ontimer(update_game_state, 1000 // 60) 

# --- Initialize and Start ---
keys_to_bind = ["w", "a", "s", "d", "Up", "Down", "Left", "Right"]
for key in keys_to_bind:
    bind_key(key)

wn.onscreenclick(handle_mouse_click, 1)
wn.onscreenclick(handle_right_click, 3)

display_loading_screen()
wn.listen() 
update_game_state()
wn.mainloop()
