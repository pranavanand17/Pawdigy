import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import sys

def resource_path(relative_path):
    """Get correct path whether running script or PyInstaller exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

state = "walk"
idle_timer = 0
idle_frame = 0

print("🐾 Pawdigy running — press ESC to exit")

ASSETS = resource_path("assets")

root = tk.Tk()

root.overrideredirect(True)
root.attributes("-topmost", True)

# transparency works on Windows
root.config(bg="white")
root.wm_attributes("-transparentcolor", "white")

root.bind("<Escape>", lambda e: root.destroy())

# ---------- LOAD SPRITES ----------

scale = 2

walk1 = Image.open(os.path.join(ASSETS, "pawdigywalking.png")).convert("RGBA")
walk2 = Image.open(os.path.join(ASSETS, "pawdigywalking2.png")).convert("RGBA")

idle1 = Image.open(os.path.join(ASSETS, "pawdigy.png")).convert("RGBA")
idle2 = Image.open(os.path.join(ASSETS, "pawdigy2.png")).convert("RGBA")

walk1 = walk1.resize((walk1.width * scale, walk1.height * scale), Image.NEAREST)
walk2 = walk2.resize((walk2.width * scale, walk2.height * scale), Image.NEAREST)

idle1 = idle1.resize((idle1.width * scale, idle1.height * scale), Image.NEAREST)
idle2 = idle2.resize((idle2.width * scale, idle2.height * scale), Image.NEAREST)

left1 = walk1
left2 = walk2

right1 = walk1.transpose(Image.FLIP_LEFT_RIGHT)
right2 = walk2.transpose(Image.FLIP_LEFT_RIGHT)

left_frames = [ImageTk.PhotoImage(left1), ImageTk.PhotoImage(left2)]
right_frames = [ImageTk.PhotoImage(right1), ImageTk.PhotoImage(right2)]

idle_frames = [
    ImageTk.PhotoImage(idle1),
    ImageTk.PhotoImage(idle2)
]

# ---------- WINDOW ----------

label = tk.Label(root, bg="white", bd=0)
label.pack()

frame = 0
direction = 1
speed = 5

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

sprite_w = left_frames[0].width()
sprite_h = left_frames[0].height()

x = 100
y = screen_h - sprite_h - 10

# ---------- BEHAVIOR ----------

def update():
    global frame, x, direction, state, idle_timer, idle_frame

    if state == "walk":

        frames = right_frames if direction == 1 else left_frames

        label.config(image=frames[frame])
        frame = (frame + 1) % len(frames)

        x += speed * direction

        if x <= 0:
            direction = 1
        elif x >= screen_w - sprite_w:
            direction = -1

        # random chance to idle
        if random.random() < 0.02:
            state = "idle"
            idle_timer = random.randint(20, 60)
            idle_frame = 0   # reset idle animation

    elif state == "idle":

        label.config(image=idle_frames[idle_frame])
        idle_frame = (idle_frame + 1) % len(idle_frames)

        idle_timer -= 1

        if idle_timer <= 0:
            state = "walk"
            frame = 0  # reset walking animation

    root.geometry(f"+{x}+{y}")

    root.after(120, update)

update()

root.mainloop()
