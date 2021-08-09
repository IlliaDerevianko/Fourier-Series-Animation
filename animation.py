from get_fourier_coefficients import get_fourier
from tkinter import *
import tkinter as tk
import math


coefficients = get_fourier('fourier.svg', 200)

# scale the coefficients so the picture can fit on the screen
for i in range(len(coefficients)):
    coefficients[i][1] = (coefficients[i][1][0] * 0.8, coefficients[i][1][1] * 0.8)

root = Tk(className="Circles")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
canvas = Canvas(root, width=screen_width, height=screen_height, bg="black")
canvas.pack()


spacing = 30
cur_x = screen_width / 2
cur_y = screen_height / 2
while cur_x >=0 or cur_y >=0:
    canvas.create_line(cur_x, 0, cur_x, screen_height, fill='gray', width='0.01m')
    canvas.create_line(screen_width - cur_x, 0, screen_width - cur_x, screen_height, fill='gray', width='0.01m')
    canvas.create_line(0, cur_y, screen_width, cur_y, fill='gray', width='0.01m')
    canvas.create_line(0, screen_height - cur_y, screen_width, screen_height - cur_y, fill='gray', width='0.01m')
    cur_x -= spacing
    cur_y -= spacing

canvas.create_oval(screen_width/2-4, screen_height/2-4, screen_width/2+4, screen_height/2+4, fill='red')

prev_pos = [screen_width / 2, screen_height / 2]
for each in coefficients:
    prev_pos[0] += each[1][0]
    prev_pos[1] += (-each[1][1])
total_time = 20
refresh_rate = 16
iterations = total_time / refresh_rate * 1000
angle_step = 2 * math.pi / iterations
angle = 0
arrows = []
circles = []


def refresh():
    global angle, prev_pos
    angle += angle_step
    end_pt = (screen_width / 2, screen_height / 2)
    for j in range(len(arrows)):
        canvas.delete(arrows[j])
        canvas.delete(circles[j])
    arrows.clear()
    circles.clear()
    cur_pos = [screen_width / 2, screen_height / 2]
    for each in coefficients:
        theta = angle * each[0]
        vector_x = math.cos(theta) * each[1][0] - math.sin(theta) * each[1][1] * -1
        vector_y = math.sin(theta) * each[1][0] + math.cos(theta) * each[1][1] * -1
        cur_pos[0] += vector_x
        cur_pos[1] += vector_y
        rad = math.sqrt(vector_x ** 2 + vector_y ** 2)
        _ = canvas.create_oval(end_pt[0] - rad, end_pt[1] - rad, end_pt[0] + rad, end_pt[1] + rad, outline='#ADD8E6')
        circles.append(_)
        _ = canvas.create_line(*end_pt, end_pt[0] + vector_x, end_pt[1] + vector_y, fill='white', arrow=tk.LAST)
        arrows.append(_)
        end_pt = (end_pt[0] + vector_x, end_pt[1] + vector_y)
    canvas.create_line(*prev_pos, *cur_pos, fill='yellow', width=3)
    prev_pos = cur_pos
    root.after(refresh_rate, refresh)


for j in range(len(arrows)):
    canvas.delete(arrows[j])
    canvas.delete(circles[j])
arrows.clear()
circles.clear()

refresh()
root.mainloop()
