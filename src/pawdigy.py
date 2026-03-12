import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

state = "walk"
idle_timer = 0
idle_frame = 0
talking = False
stunned_timer = 0
fall_velocity = 0
fall_frame = 0

lines = [
    "stop tryna do what everybody else doin yo",
    "ah shit, here we go again",
    "AI finna get you",
    "Sub 2 Pewds",
    "I hate Tuesdays."
]

print("🐾 Pawdigy running — press ESC to exit")

ASSETS = resource_path("assets")

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

def keep_on_top():
    root.attributes("-topmost", True)
    bubble_win.attributes("-topmost", True)
    root.after(2000, keep_on_top)

root.config(bg="white")
root.wm_attributes("-transparentcolor", "white")

root.bind("<Escape>", lambda e: root.destroy())

# ---------- LOAD SPRITES ----------

scale = 2

def load(name):
    img = Image.open(os.path.join(ASSETS, name)).convert("RGBA")
    img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    return ImageTk.PhotoImage(img)

walk1 = load("pawdigywalking.png")
walk2 = load("pawdigywalking2.png")

idle1 = load("pawdigy.png")
idle2 = load("pawdigy2.png")

drag1 = load("pawdigypickedup.png")
drag2 = load("pawdigypickedup1.png")

drag_frames = [drag1, drag2]
drag_frame = 0

fall1 = load("pawdigyfalling1.png")
fall2 = load("pawdigyfalling2.png")

fallen1 = load("pawdigyfallen1.png")
fallen2 = load("pawdigyfallen2.png")

left_frames = [walk1, walk2]
right_frames = [
    ImageTk.PhotoImage(Image.open(os.path.join(ASSETS,"pawdigywalking.png")).transpose(Image.FLIP_LEFT_RIGHT).resize((walk1.width(), walk1.height()), Image.NEAREST)),
    ImageTk.PhotoImage(Image.open(os.path.join(ASSETS,"pawdigywalking2.png")).transpose(Image.FLIP_LEFT_RIGHT).resize((walk1.width(), walk1.height()), Image.NEAREST))
]

idle_frames = [idle1, idle2]
fall_frames = [fall1, fall2]
fallen_frames = [fallen1, fallen2]

# ---------- CAT WINDOW ----------

label = tk.Label(root, bg="white", bd=0)
label.pack()

# ---------- SPEECH WINDOW ----------

bubble_win = tk.Toplevel()
bubble_win.overrideredirect(True)
bubble_win.attributes("-topmost", True)
bubble_win.config(bg="white")
bubble_win.wm_attributes("-transparentcolor", "white")

bubble = tk.Label(
    bubble_win,
    text="",
    bg="#f0f0f0",
    fg="black",
    bd=2,
    relief="solid",
    font=("Comic Sans MS", 10),
    wraplength=200,
    justify="center",
    padx=6,
    pady=3
)

bubble.pack()

tail = tk.Canvas(
    bubble_win,
    width=20,
    height=10,
    bg="white",
    highlightthickness=0,
    bd=0
)

tail.create_polygon(
    0,0,
    20,0,
    10,10,
    fill="#f0f0f0",
    outline="black"
)

tail.pack()

bubble_win.withdraw()

frame = 0
direction = 1
speed = 5

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

sprite_w = walk1.width()
sprite_h = walk1.height()

x = 100
y = screen_h - sprite_h - 2
ground = y

# ---------- DRAG SYSTEM ----------

def start_drag(event):
    global state, drag_frame
    state = "drag"
    drag_frame = 0

def dragging(event):
    global x, y
    if state == "drag":
        x = event.x_root - sprite_w//2
        y = event.y_root - 10

def stop_drag(event):
    global state, fall_velocity
    if state == "drag":
        state = "fall"
        fall_velocity = 5

label.bind("<Button-1>", start_drag)
label.bind("<B1-Motion>", dragging)
label.bind("<ButtonRelease-1>", stop_drag)

# ---------- SPEECH ----------

def speak(text):
    global talking
    talking = True

    bubble.config(text=text)

    bubble_win.deiconify()
    bubble_win.geometry(f"+{x+20}+{y-35}")

    def hide():
        global talking
        talking = False
        bubble_win.withdraw()

    root.after(4000, hide)

# ---------- BEHAVIOR ----------

def update():
    global frame,x,y,direction,state,idle_timer,idle_frame,stunned_timer,fall_velocity,fall_frame,drag_frame

    if state == "walk":

        frames = right_frames if direction == 1 else left_frames
        label.config(image=frames[frame])
        frame = (frame + 1) % len(frames)

        x += speed * direction

        if x <= 0:
            direction = 1
        elif x >= screen_w - sprite_w:
            direction = -1

        if random.random() < 0.02:
            state = "idle"
            idle_timer = random.randint(30,80)
            idle_frame = 0
            speak(random.choice(lines))

    elif state == "idle":

        label.config(image=idle_frames[idle_frame])
        idle_frame = (idle_frame + 1) % len(idle_frames)

        idle_timer -= 1

        if idle_timer <= 0:
            state = "walk"
            frame = 0

    elif state == "drag":

        label.config(image=drag_frames[drag_frame])
        drag_frame = (drag_frame + 1) % 2

    elif state == "fall":

        label.config(image=fall_frames[fall_frame])
        fall_frame = (fall_frame + 1) % 2

        fall_velocity += 1
        y += fall_velocity

        if y >= ground:
            y = ground
            state = "stunned"
            stunned_timer = 40

    elif state == "stunned":

        label.config(image=fallen_frames[frame % 2])
        frame += 1

        stunned_timer -= 1

        if stunned_timer <= 0:
            state = "idle"
            idle_timer = 40
            idle_frame = 0

    root.geometry(f"+{x}+{y}")

    if bubble_win.state() == "normal":
        bubble_win.geometry(f"+{x+20}+{y-35}")

    root.after(120, update)

update()
keep_on_top()

root.mainloop()
