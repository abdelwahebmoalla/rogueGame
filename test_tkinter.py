import tkinter as tk
root = tk.Tk()
root.title('rogue Game')
root.resizable(False, False)
root.configure(background="black")
basePath = "assets/"
hero = tk.PhotoImage(file=basePath + "hero.png")
hero_i = tk.PhotoImage(file=basePath + "hero_i.png")
sol = tk.PhotoImage(file=basePath + "sol_1.png")
brick = tk.PhotoImage(file=basePath + "brick.png")
potion = tk.PhotoImage(file=basePath + "potion.png")
food = tk.PhotoImage(file=basePath + "food.png")
goblin = tk.PhotoImage(file=basePath + "goblin.png")
orc = tk.PhotoImage(file=basePath + "orc.png")
stairs = tk.PhotoImage(file=basePath + "stairs.png")
darkness = tk.PhotoImage(file=basePath + "stairs.png")
canvas = tk.Canvas(root, width=1200, height=800, background="black")
canvas.config(width=1000, height=800)
canvas.create_image(0, 0, image=sol)
canvas.create_image(0, 32, image=sol)
canvas.create_image(0, 64, image=sol)
canvas.create_image(32, 32, image=sol)
canvas.create_image(64, 64, image=sol)
canvas.create_image(32, 0, image=sol)
canvas.create_image(64, 0, image=sol)
canvas.pack()
root.mainloop()

