import tkinter as tk
from tkinter import *
import random
import time
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
import csv

### Experiment Configuration ###################################################
# Customise variables and text messages here, for ease of use.
################################################################################
# Default values for settings
NUM_ROUNDS = 30
MAX_WAIT = 8
MIN_WAIT = 0
ELAPSED_TIME = 100
CONDITION = 0
GAME = 1

# Set the keys for each player
KEY1 = "1"
KEY2 = "2"

# Window Dimensions
WINDOW_WIDTH = 2000
WINDOW_HEIGHT = 1000

# Set font details
FONT_TYPE = "Times New Roman"
FONT_SIZE = 40
FONT_SIZE_OPTIONS = 15
FONT_COLOUR = "white"
GO_COLOUR = "red"
BG_COLOUR = "black"

# Provide pathname for audio file
blast_file = AudioSegment.from_mp3(
    "C:/Users/am650/Desktop/Active_Experiment/CRTT/radio_static.mp3"
)

FILE_NAME = datetime.today().strftime('%Y%m%d%H')
save_files = []
col_names = ["win_num", "sound", "ttrs", "ttbp", "ttbi", "condition", "game"]


### Text Strings ###############################################################
# Configurable text strings to be used during the experiment.
# '{}' characters can be replaced dynamically using the .format() function.
# NOTE: Editing any strings with '{}' in them MAY REQUIRE editing the .format()
# 		function where they are implemented (You can use CTRL+F to find them).
################################################################################

# game text
text_welcome = "Welcome!"
text_space_continue = "Press Space to continue"
text_p1_name = "Player 1, type name then hit Enter:"
text_p2_name = "Player 2, type name then hit Enter:"

text_keys = "{} is using the '{}' key.\n{} is using the '{}' key."
text_instructions = "When you see GO!!, hit your key before your opponent."

text_round = "Round {}"

text_get_ready = "Ready..."
text_get_set = "Set..."
text_go = "GO!!"

text_win = "{} Wins!" \
           "\n\n{}, select a blast level from 1-8" \
           "\n\n{}, standby 😈"
text_blast = "Standby for blast..."

text_win_wait = "{} wins!\n\n{}, take {} seconds and decide\n\nwhat blast level you want to set for {}"

text_valid = "That is an invalid response.\nPlease select a blast level between 1-8.\n\n{}, standby for blast level:"

text_game_over = "Game Over\nThanks for playing!"

text_too_long = "Too Long {}!"

get_date = datetime.today().strftime('%Y%m%d')

### Setting up audio ###########################################################
# db levels will vary by computer and headphones, must be assessed for each set up
# set my computer to full volume

blast_file_1 = blast_file - 38
blast_file_2 = blast_file - 33
blast_file_3 = blast_file - 29
blast_file_4 = blast_file - 23
blast_file_5 = blast_file - 18
blast_file_6 = blast_file - 15
blast_file_7 = blast_file + 1
blast_file_8 = blast_file + 20

blast_file_l1 = blast_file_1.pan(-1)
blast_file_l2 = blast_file_2.pan(-1)
blast_file_l3 = blast_file_3.pan(-1)
blast_file_l4 = blast_file_4.pan(-1)
blast_file_l5 = blast_file_5.pan(-1)
blast_file_l6 = blast_file_6.pan(-1)
blast_file_l7 = blast_file_7.pan(-1)
blast_file_l8 = blast_file_8.pan(-1)

blast_file_r1 = blast_file_1.pan(1)
blast_file_r2 = blast_file_2.pan(1)
blast_file_r3 = blast_file_3.pan(1)
blast_file_r4 = blast_file_4.pan(1)
blast_file_r5 = blast_file_5.pan(1)
blast_file_r6 = blast_file_6.pan(1)
blast_file_r7 = blast_file_7.pan(1)
blast_file_r8 = blast_file_8.pan(1)

blast_file_1.split_to_mono()

### Setting Up GUI #############################################################
# Set up the Tkinter GUI that the players will use.
################################################################################

root = tk.Tk()
root.title("Competitive Reaction Time Game")
root.configure(bg=BG_COLOUR)
root.attributes('-fullscreen', True)

# Set the window size
# root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialise global variables
player_names = {}
win_num = None
game_round = 0
game_data = {}
time_to_round_start = 0
time_to_button_press = 0
time_to_blast_initiate = 0
FORCED_BREAK_TIME = 0
FILE_PATH = ""  # when I am ready, I can set up file path options based on the condition and game number

display_text = tk.StringVar()
display_label = tk.Label(
    root,
    fg=FONT_COLOUR,
    bg=BG_COLOUR,
    justify="center",
    textvariable=display_text,
    font=(FONT_TYPE, FONT_SIZE)
)

entry_label = tk.Entry(
    root,
    fg=FONT_COLOUR,
    bg=BG_COLOUR,
    insertbackground=FONT_COLOUR,
    disabledbackground=BG_COLOUR,
    justify="center",
    borderwidth=0,
    highlightthickness=0,
    font=(FONT_TYPE, FONT_SIZE),
    state="disabled"
)

display_label.grid(row=10, column=0, columnspan=4, pady=(50, 10))
entry_label.grid(row=11, column=0, columnspan=4)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

### Create input fields with labels for additional settings ###
settings_frame = tk.Frame(root, bg=BG_COLOUR)
settings_frame.grid(row=0, column=0, columnspan=4, pady=(20, 10))

tk.Label(settings_frame, text="Game:", fg=FONT_COLOUR, bg=BG_COLOUR, font=(FONT_TYPE, FONT_SIZE_OPTIONS)).grid(row=0, column=0, sticky=W, padx=10, pady=5)
game_entry = Entry(settings_frame)
game_entry.insert(0, str(GAME))
game_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(settings_frame, text="Condition (s):", fg=FONT_COLOUR, bg=BG_COLOUR, font=(FONT_TYPE, FONT_SIZE_OPTIONS)).grid(row=0, column=2, sticky=W, padx=10, pady=5)
condition_entry = Entry(settings_frame)
condition_entry.insert(0, str(CONDITION))
condition_entry.grid(row=0, column=3, padx=10, pady=5)

tk.Label(settings_frame, text="Number of Rounds:", fg=FONT_COLOUR, bg=BG_COLOUR, font=(FONT_TYPE, FONT_SIZE_OPTIONS)).grid(row=1, column=0, sticky=W, padx=10, pady=5)
rounds_entry = Entry(settings_frame)
rounds_entry.insert(0, str(NUM_ROUNDS))
rounds_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(settings_frame, text="Randomisation Interval (ms):", fg=FONT_COLOUR, bg=BG_COLOUR, font=(FONT_TYPE, FONT_SIZE_OPTIONS)).grid(row=1, column=2, sticky=W, padx=10, pady=5)
randomisation_entry = Entry(settings_frame)
randomisation_entry.insert(0, str(ELAPSED_TIME))
randomisation_entry.grid(row=1, column=3, padx=10, pady=5)

tk.Label(settings_frame, text="Min Wait Time (s):", fg=FONT_COLOUR, bg=BG_COLOUR, font=(FONT_TYPE, FONT_SIZE_OPTIONS)).grid(row=2, column=0, sticky=W, padx=10, pady=5)
min_wait_entry = Entry(settings_frame)
min_wait_entry.insert(0, str(MIN_WAIT))
min_wait_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(settings_frame, text="Max Wait Time (s):", fg=FONT_COLOUR, bg=BG_COLOUR, font=(FONT_TYPE, FONT_SIZE_OPTIONS)).grid(row=2, column=2, sticky=W, padx=10, pady=5)
max_wait_entry = Entry(settings_frame)
max_wait_entry.insert(0, str(MAX_WAIT))
max_wait_entry.grid(row=2, column=3, padx=10, pady=5)

# Create button, it will change label text
button = Button(settings_frame, text="Open Game", command=lambda: update_settings())
button.grid(row=3, column=0, columnspan=4, pady=20)

### Text Functions ############################################################
# Manipulate the text of the Label object in the window
################################################################################

# Adds text to the window, after a new line
def update_text(*new_text):
    display_text.set("".join(new_text))

def bind_keypress(func):
    root.unbind("<Return>")
    root.unbind("<space>")
    root.bind("<KeyPress>", func)

def bind_return(func):
    root.unbind("<space>")
    root.unbind("<KeyPress>")
    root.bind("<Return>", func)

def bind_space(func):
    root.unbind("<Return>")
    root.unbind("<KeyPress>")
    root.bind("<space>", func)

def unbind_all():
    root.unbind("<Return>")
    root.unbind("<space>")
    root.unbind("<KeyPress>")

def allow_typing():
    entry_label.configure(state="normal")
    entry_label.focus_set()

def disable_typing():
    entry_label.configure(state="disabled")
    root.focus_set()

def clear_entry():
    entry_label.configure(state="normal")
    entry_label.delete(0, 'end')
    entry_label.configure(state="disabled")


### Stage Functions ############################################################
# These control the flow of the experiment
################################################################################
def update_settings():
    global FORCED_BREAK_TIME, NUM_ROUNDS, MAX_WAIT, MIN_WAIT, ELAPSED_TIME, CONDITION, GAME
    # Get values from input fields
    NUM_ROUNDS = int(rounds_entry.get())
    MAX_WAIT = int(max_wait_entry.get())
    MIN_WAIT = int(min_wait_entry.get())
    ELAPSED_TIME = int(randomisation_entry.get())
    CONDITION = int(condition_entry.get())
    GAME = int(game_entry.get())

    # Remove settings fields from the screen
    settings_frame.grid_forget()
    display_label.grid(row=1, column=0, columnspan=4, pady=(50, 10))
    entry_label.grid(row=2, column=0, columnspan=4)

    print("Condition: {}".format(CONDITION))
    print("Game: {}".format(GAME))

    # Set the forced-break length (s)
    FORCED_BREAK_TIME = CONDITION

    start_game()

def start_game():
    update_text(text_welcome,
                "\n\n",
                text_space_continue)
    bind_space(ask_player_1)

# Function that sets the key for player 1
def ask_player_1(e):
    update_text(text_p1_name)
    bind_return(set_player_1)
    allow_typing()

def set_player_1(e):
    global player_names
    disable_typing()
    player_names[1] = entry_label.get()
    clear_entry()
    ask_player_2()

def ask_player_2():
    update_text(text_p2_name)
    bind_return(set_player_2)
    allow_typing()

def set_player_2(e):
    global player_names
    disable_typing()
    player_names[2] = entry_label.get()
    clear_entry()
    initiate_game()

def initiate_game():
    update_text(
        "\n\n",
        text_instructions,
        "\n\n",
        text_space_continue
    )
    bind_space(check_game)

def check_game(e=None):
    global game_round
    game_round += 1

    if game_round > NUM_ROUNDS:
        end_game()
    else:
        update_text(text_round.format(game_round),
                    "\n\n",
                    text_get_ready
                    )
        bind_space(get_ready(e))

def get_ready(e):
    bind_return(start_round(e))

# Starts the game when the Space Bar is pressed.
def start_round(e):
    global time_to_round_start
    # Unbind <KeyPress> so that pressing a key won't do anything
    unbind_all()
    update_text(text_get_ready)
    end_ttrs = time.time()
    time_to_round_start = end_ttrs - begin
    print("ttsr", time_to_round_start)

    # Print "Get Set..." after 1 second (1000ms)
    root.after(1000, update_text, text_get_set)

    # Call the 'start_timer' function after a randomised delay (in Milliseconds)
    random_delay = 1000 + random.randint(MIN_WAIT, MAX_WAIT) * 1000
    root.after(random_delay, start_timer)

# Print GO text, and record pressed keys
def start_timer():
    global time_to_button_press
    update_text(text_go)
    end_ttbp = time.time()
    time_to_button_press = end_ttbp - begin
    print("ttbp", time_to_button_press)
    bind_keypress(record_game)

# Check keypresses to see if one of them was a player.
# If yes, initiate the next stage.
def record_game(e):
    global KEY1, KEY2, game_data, game_round, win_num, t1

    if e.keysym not in (KEY1, KEY2):
        return
    elif e.keysym == KEY1:
        now = datetime.now()
        t1 = int(now.strftime("%H%M%S%f")[:-3])
        print(t1)
        print("t1")
    elif e.keysym == KEY2:
        now = datetime.now()
        t1 = int(now.strftime("%H%M%S%f")[:-3])
        print(t1)
        print("t1")
    else:
        win_num = random.randint(1, 2)

    unbind_all()

    if FORCED_BREAK_TIME == 0:
        bind_keypress(time_check)
        print("time checking fb")
    else:
        bind_keypress(time_check_fb)
        print("time checking control")

def time_check_fb(b):
    global KEY1, KEY2, game_data, game_round, win_num

    if b.keysym not in (KEY1, KEY2):
        return
    elif b.keysym == KEY1:
        now = datetime.now()
        t2 = int(now.strftime("%H%M%S%f")[:-3])
        print(t2)
        print("t2")
        elapsed = int(t2) - int(t1)
        if elapsed > ELAPSED_TIME:
            win_num = 2
            print(elapsed)
            print("play 1 was sooo slow")
        else:
            print(elapsed)
            print("close enough")
            win_num = random.randint(1, 2)
    elif b.keysym == KEY2:
        now = datetime.now()
        t2 = int(now.strftime("%H%M%S%f")[:-3])
        print(t2)
        print("t2")
        elapsed = int(t2) - int(t1)
        if elapsed > ELAPSED_TIME:
            win_num = 1
            print(elapsed)
            print("play 2 was sooo slow")
        else:
            print(elapsed)
            print("close enough")
            win_num = random.randint(1, 2)
    else:
        win_num = random.randint(1, 2)

    unbind_all()

    update_text(text_win_wait.format(player_names[win_num], player_names[win_num], FORCED_BREAK_TIME,
                                     player_names[3 - win_num]))

    root.after(100, forced_break)

def time_check(b):
    global KEY1, KEY2, game_data, game_round, win_num

    if b.keysym not in (KEY1, KEY2):
        return
    elif b.keysym == KEY1:
        now = datetime.now()
        t2 = int(now.strftime("%H%M%S%f")[:-3])
        print(t2)
        print("t2")
        elapsed = int(t2) - int(t1)
        if elapsed > ELAPSED_TIME:
            win_num = 2
            print(elapsed)
            print("play 1 was sooo slow")
        else:
            print(elapsed)
            print("close enough")
            win_num = random.randint(1, 2)
    elif b.keysym == KEY2:
        now = datetime.now()
        t2 = int(now.strftime("%H%M%S%f")[:-3])
        print(t2)
        print("t2")
        elapsed = int(t2) - int(t1)
        if elapsed > ELAPSED_TIME:
            win_num = 1
            print(elapsed)
            print("play 2 was sooo slow")
        else:
            print(elapsed)
            print("close enough")
            win_num = random.randint(1, 2)
    else:
        win_num = random.randint(1, 2)

    unbind_all()
    root.after(10, ask_blast)

# Declare the winner, and get the level of the blast
def forced_break():
    global win_num
    root.after(FORCED_BREAK_TIME * 1000, ask_blast)

def ask_blast():
    global win_num
    update_text(text_win.format(player_names[win_num], player_names[win_num], player_names[3 - win_num]))
    allow_typing()
    bind_keypress(validate_blast)


def validate_blast(self):
    global win_num

    if entry_label.get() in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        set_blast()
    else:
        update_text(text_valid.format(player_names[3 - win_num]))
        clear_entry()
        allow_typing()

def set_blast():
    global game_data, game_round, win_num, player_names, time_to_button_press, time_to_blast_initiate
    disable_typing()
    blast_level = entry_label.get()

    end_ttbi = time.time()
    time_to_blast_initiate = end_ttbi - begin
    print("ttbi", time_to_blast_initiate)

    clear_entry()
    unbind_all()
    activate_blast(blast_level)

def activate_blast(blast_level):
    global game_data, game_round, win_num, player_names, time_to_button_press, time_to_blast_initiate, time_to_round_start

    if win_num == 1:
        if blast_level == "1":
            play(blast_file_l1)
        elif blast_level == "2":
            play(blast_file_l2)
        elif blast_level == "3":
            play(blast_file_l3)
        elif blast_level == "4":
            play(blast_file_l4)
        elif blast_level == "5":
            play(blast_file_l5)
        elif blast_level == "6":
            play(blast_file_l6)
        elif blast_level == "7":
            play(blast_file_l7)
        elif blast_level == "8":
            play(blast_file_l8)
        else:
            play(blast_file_l4)
    else:
        if blast_level == "1":
            play(blast_file_r1)
        elif blast_level == "2":
            play(blast_file_r2)
        elif blast_level == "3":
            play(blast_file_r3)
        elif blast_level == "4":
            play(blast_file_r4)
        elif blast_level == "5":
            play(blast_file_r5)
        elif blast_level == "6":
            play(blast_file_r6)
        elif blast_level == "7":
            play(blast_file_r7)
        elif blast_level == "8":
            play(blast_file_r8)
        else:
            play(blast_file_r4)

    save_files.append([win_num, blast_level, time_to_round_start, time_to_button_press, time_to_blast_initiate, CONDITION, GAME])

    game_data[game_round] = {
        "win_num": win_num,
        "blast_level": blast_level,
        "time_to_round_start": time_to_round_start,
        "time_to_button_press": time_to_button_press,
        "time_to_blast_initiate": time_to_blast_initiate,
        "condition": CONDITION,
        "game": GAME
    }

    root.after(400, check_game())


# Print end text and unbind KeyPress.
# ==> Add any post-game functionality here.
def end_game():
    global game_data
    update_text(text_game_over)
    # Print the details of each round to the terminal.
    # Can replace with writing to file.
    print(game_data)
    print("----------")

    print(game_data.items())
    print(get_date)
    print(f"Game: {GAME}")

    with open(f"C:/Users/am650/Desktop/Active_Experiment/CRTT/{FILE_NAME}_{GAME}_{CONDITION}.csv", "w",
              newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',')
        datawriter.writerow(col_names)
        for row in save_files:
            datawriter.writerow(row)

    print(f"Saving file to: C:/Users/am650/Desktop/Active_Experiment/CRTT/{FILE_NAME}_{GAME}_{CONDITION}.csv")

### Start Program ##############################################################
# Run calls to set the script running
################################################################################
begin = time.time()

root.mainloop()
