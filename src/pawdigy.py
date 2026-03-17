import tkinter as tk
from PIL import Image, ImageTk
import os, random, sys

def resource_path(p):
    try: return os.path.join(sys._MEIPASS, p)
    except: return os.path.join(os.path.abspath("."), p)

# ---------- STATE ----------
state="walk"
frame=0
anim_counter=0
idle_timer=0
idle_frame=0
fall_velocity=0
fall_frame=0
stunned_timer=0
robo_break_frame=0

typed_buffer=""
current_form="normal"
dejavu_awakened=False

# ---------- DIALOGUE ----------
revive_lines=["I'm back!","Alive again!","Screw that suit!"]

normal_lines=[
    "stop tryna do what everybody else doin yo",
    "ah shit, here we go again",
    "AI finna get you",
    "Sub 2 Pewds",
    "I hate Tuesdays."
]

dejavu_lines=[
    "Human beings are a disease, cancer of this planet",
    "You have to let it all go. Fear, doubt, and disbelief, Free your mind",
    "To deny our impulses is to deny the very thing that makes us human",
    "Free your mind",
    "Ever had that feeling where you’re not sure if you’re awake or dreaming?"
]

# ---------- WINDOW ----------
root=tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost",True)

MAGIC_COLOR="#ff00ff"
root.config(bg=MAGIC_COLOR)
root.wm_attributes("-transparentcolor",MAGIC_COLOR)

root.bind("<Escape>",lambda e:root.destroy())

# ---------- LOAD ----------
scale=2
ASSETS=resource_path("../assets")

def load(n):
    i=Image.open(os.path.join(ASSETS,n)).convert("RGBA")
    i=i.resize((i.width*scale,i.height*scale),Image.NEAREST)
    return ImageTk.PhotoImage(i)

def flip(n):
    i=Image.open(os.path.join(ASSETS,n)).convert("RGBA")
    i=i.resize((i.width*scale,i.height*scale),Image.NEAREST)
    return ImageTk.PhotoImage(i.transpose(Image.FLIP_LEFT_RIGHT))

# NORMAL
walkL=[load("pawdigywalking.png"),load("pawdigywalking2.png")]
walkR=[flip("pawdigywalking.png"),flip("pawdigywalking2.png")]
idleN=[load("pawdigy.png"),load("pawdigy2.png")]

fallL=[load("pawdigyfalling1.png"),load("pawdigyfalling2.png")]
fallR=[flip("pawdigyfalling1.png"),flip("pawdigyfalling2.png")]

stunL=[load("pawdigyfallen1.png"),load("pawdigyfallen2.png")]
stunR=[flip("pawdigyfallen1.png"),flip("pawdigyfallen2.png")]

dragL=[load("pawdigypickedup.png"),load("pawdigypickedup1.png")]
dragR=[flip("pawdigypickedup.png"),flip("pawdigypickedup1.png")]

# ROBO
r_walkL=[load("robopawdigywalking.png"),load("robopawdigywalking2.png")]
r_walkR=[flip("robopawdigywalking.png"),flip("robopawdigywalking2.png")]
r_idle=[load("robopawdigy.png"),load("robopawdigy2.png")]
r_drag=[load("robopawdigypickedup.png"),load("robopawdigypickedup1.png")]
r_fallL=[load("robopawdigyfalling1.png"),load("robopawdigyfalling2.png")]
r_fallR=[flip("robopawdigyfalling1.png"),flip("robopawdigyfalling2.png")]
r_break=[
load("robopawdigyfallen1.png"),
load("robopawdigyfallen2.png"),
load("robopawdigyfallen3.png"),
load("robopawdigyfallen4.png"),
load("robopawdigyfallen5.png"),
]

# DEJAVU
dejavu_idle=[load("dejavupawdigy.png"),load("dejavupawdigy2.png")]
dejavu_walkL=[load("dejavupawdigywalking.png"),load("dejavupawdigywalking2.png")]
dejavu_walkR=[flip("dejavupawdigywalking.png"),flip("dejavupawdigywalking2.png")]
dejavu_drag=[load("dejavupawdigypickedup.png"),load("dejavupawdigypickedup1.png")]

idle_frames=idleN

# ---------- POSITION ----------
label=tk.Label(root,bg=MAGIC_COLOR)
label.pack()

sw,sh=root.winfo_screenwidth(),root.winfo_screenheight()
w,h=walkL[0].width(),walkL[0].height()

x,y=100,sh-h-2
ground=y
direction=1
speed=5

# ---------- SPEECH ----------
bubble_win=tk.Toplevel()
bubble_win.overrideredirect(True)
bubble_win.attributes("-topmost",True)
bubble_win.config(bg=MAGIC_COLOR)
bubble_win.wm_attributes("-transparentcolor",MAGIC_COLOR)

bubble=tk.Label(bubble_win,text="",bg="#f0f0f0",fg="black",bd=2,relief="solid",
font=("Comic Sans MS",10),wraplength=200,justify="center",padx=6,pady=3)
bubble.pack()

tail=tk.Canvas(bubble_win,width=20,height=10,bg=MAGIC_COLOR,highlightthickness=0)
tail.create_polygon(0,0,20,0,10,10,fill="#f0f0f0",outline="black")
tail.pack()

bubble_win.withdraw()

def speak(text):
    bubble.config(text=text)
    bubble_win.deiconify()
    bubble_win.geometry(f"+{x+20}+{y-35}")
    root.after(4000,bubble_win.withdraw)

# ---------- INPUT ----------
def on_key(e):
    global typed_buffer,current_form,idle_frames,state,fall_velocity,idle_frame,idle_timer,dejavu_awakened

    if not e.char: return
    typed_buffer=(typed_buffer+e.char.lower())[-30:]

    if typed_buffer.endswith("deja vu"):
        current_form="dejavu"
        idle_frames=dejavu_idle
        dejavu_awakened=False
        state="idle"
        idle_frame=0
        idle_timer=50
        typed_buffer=""
        return

    if typed_buffer.endswith("replaced"):
        current_form="robo"
        idle_frames=r_idle
        state="idle"
        idle_frame=0
        idle_timer=50
        dejavu_awakened=False
        typed_buffer=""
        return

    if typed_buffer.endswith("pawdigy"):
        current_form="normal"
        idle_frames=idleN
        state="fall" if y<ground else "idle"
        fall_velocity=5
        idle_frame=0
        idle_timer=50
        dejavu_awakened=False
        typed_buffer=""
        return

root.bind("<Key>",on_key)

# ---------- DRAG ----------
def start_drag(e):
    global state,x,y

    if current_form=="dejavu" and dejavu_awakened:
        x=random.randint(0,sw-w)
        y=random.randint(0,sh-h-40)
        speak("dodged that")
        return

    state="drag"

def dragging(e):
    global x,y
    if state=="drag":
        x=e.x_root-w//2
        y=e.y_root-10

def stop_drag(e):
    global state,fall_velocity,dejavu_awakened

    if state=="drag":

        if current_form=="dejavu" and not dejavu_awakened:
            dejavu_awakened=True
            state="idle"
            speak("I've begun to believe")
            return

        state="fall"
        fall_velocity=5

label.bind("<Button-1>",start_drag)
label.bind("<B1-Motion>",dragging)
label.bind("<ButtonRelease-1>",stop_drag)

# ---------- UPDATE ----------
def update():
    global frame,anim_counter,x,y,state,idle_timer,idle_frame,fall_velocity,fall_frame,stunned_timer,robo_break_frame,current_form,idle_frames,direction

    lines = dejavu_lines if (current_form=="dejavu" and dejavu_awakened) else normal_lines

    # WALK
    if state=="walk":

        if current_form=="robo":
            frames=r_walkR if direction==1 else r_walkL
            anim_speed=3
        elif current_form=="dejavu":
            frames=dejavu_walkR if direction==1 else dejavu_walkL
            anim_speed=1
        else:
            frames=walkR if direction==1 else walkL
            anim_speed=1

        label.config(image=frames[frame])

        anim_counter+=1
        if anim_counter>=anim_speed:
            frame=(frame+1)%len(frames)
            anim_counter=0

        x+=speed*direction

        if x<=0 or x>=sw-w:
            direction*=-1

        if random.random()<0.02:
            state="idle"
            idle_timer=random.randint(30,80)
            idle_frame=0
            speak(random.choice(lines))

    # IDLE
    elif state=="idle":
        label.config(image=idle_frames[idle_frame%len(idle_frames)])
        idle_frame+=1
        idle_timer-=1

        if idle_timer<=0:
            state="walk"
            frame=0

    # DRAG
    elif state=="drag":
        if current_form=="robo":
            frames=r_drag
        elif current_form=="dejavu":
            frames=dejavu_drag
        else:
            frames=dragR if direction==1 else dragL

        label.config(image=frames[frame%len(frames)])
        frame+=1

    # FALL
    elif state=="fall":

        if current_form=="dejavu":
            state="idle"
            return

        frames = (r_fallR if direction==1 else r_fallL) if current_form=="robo" else (fallR if direction==1 else fallL)

        label.config(image=frames[fall_frame])
        fall_frame=(fall_frame+1)%2

        fall_velocity+=1
        y+=fall_velocity

        if y>=ground:
            y=ground

            if current_form=="robo":
                state="robo_break"
                robo_break_frame=0
                anim_counter=0
            else:
                state="stunned"
                stunned_timer=40

    # ROBO BREAK
    elif state=="robo_break":

        if robo_break_frame <= 2:
            delay = 1
        elif robo_break_frame == 3:
            delay = 6
        else:
            delay = 3

        if anim_counter < delay:
            anim_counter += 1
        else:
            anim_counter = 0
            robo_break_frame += 1

        if robo_break_frame < len(r_break):
            label.config(image=r_break[robo_break_frame])
        else:
            speak(random.choice(revive_lines))
            current_form="normal"
            idle_frames=idleN
            state="idle"
            idle_timer=50
            idle_frame=0

    # STUNNED
    elif state=="stunned":
        frames=stunR if direction==1 else stunL
        label.config(image=frames[frame%2])
        frame+=1
        stunned_timer-=1

        if stunned_timer<=0:
            state="idle"
            idle_timer=40
            idle_frame=0

    root.geometry(f"+{x}+{y}")

    if bubble_win.state()=="normal":
        bubble_win.geometry(f"+{x+20}+{y-35}")

    root.after(120,update)

update()
root.mainloop()