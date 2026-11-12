import random
import tkinter as tk
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Generated sample data: [North-South cars, East-West cars]
random.seed(7)

X = [
    [random.randint(0, 30), random.randint(0, 30)]
    for _ in range(6000)
]

y = [
    "North-South" if ns >= ew else "East-West"
    for ns, ew in X
]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=7
)

model = DecisionTreeClassifier(random_state=7)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))

queues = {
    "North-South": 8,
    "East-West": 5
}

running = False

root = tk.Tk()
root.title("AI Traffic-Light Simulator")
root.geometry("520x410")

tk.Label(
    root,
    text="AI Traffic-Light Controller",
    font=("Arial", 18, "bold")
).pack(pady=10)

tk.Label(
    root,
    text=f"Model test accuracy on generated data: {accuracy:.1%}"
).pack()

canvas = tk.Canvas(
    root,
    width=490,
    height=220,
    bg="#e8eef2"
)
canvas.pack(pady=12)


def draw_car(x, y, color):
    # Car body
    canvas.create_rectangle(
        x, y, x + 30, y + 17,
        fill=color, outline="white", width=1
    )

    # Car roof and windows
    canvas.create_rectangle(
        x + 7, y - 7, x + 23, y + 2,
        fill=color, outline="white", width=1
    )

    # Wheels
    canvas.create_oval(x + 4, y + 13, x + 11, y + 20, fill="black")
    canvas.create_oval(x + 20, y + 13, x + 27, y + 20, fill="black")


def draw_queue(label, count, road_y, green):
    canvas.create_text(
        18, road_y - 25,
        text=f"{label} queue: {count} cars",
        anchor="w",
        font=("Arial", 11, "bold")
    )

    # Road lane
    canvas.create_rectangle(
        15, road_y, 430, road_y + 50,
        fill="#555555", outline=""
    )

    # Dashed lane marking
    canvas.create_line(
        15, road_y + 25, 430, road_y + 25,
        fill="white", dash=(8, 6)
    )

    # Draw up to 9 cars in the queue
    car_colors = ["#1976D2", "#E53935", "#43A047"]
    for i in range(min(count, 9)):
        x = 25 + i * 42
        draw_car(x, road_y + 17, car_colors[i % len(car_colors)])

    # Traffic light
    light_color = "green" if green else "red"
    canvas.create_oval(
        447, road_y + 10, 477, road_y + 40,
        fill=light_color, outline="black"
    )


def update_display(green_direction=None):
    canvas.delete("all")

    draw_queue(
        "North-South",
        queues["North-South"],
        road_y=45,
        green=(green_direction == "North-South")
    )

    draw_queue(
        "East-West",
        queues["East-West"],
        road_y=145,
        green=(green_direction == "East-West")
    )


status_label = tk.Label(root, text="Press Start to begin.")
status_label.pack(pady=4)


def tick():
    global running

    if not running:
        return

    # Simulate new cars arriving
    queues["North-South"] += random.choices(
        [0, 1, 2], weights=[2, 5, 3]
    )[0]

    queues["East-West"] += random.choices(
        [0, 1, 2], weights=[2, 5, 3]
    )[0]

    # AI chooses the direction with more simulated traffic
    green_direction = model.predict([[
        queues["North-South"],
        queues["East-West"]
    ]])[0]

    # Simulate cars passing through the green light
    queues[green_direction] = max(
        0, queues[green_direction] - 3
    )

    update_display(green_direction)
    status_label.config(text=f"Green light: {green_direction}")

    root.after(1000, tick)


def start():
    global running

    if not running:
        running = True
        tick()


def pause():
    global running
    running = False
    status_label.config(text="Paused.")


button_frame = tk.Frame(root)
button_frame.pack(pady=8)

tk.Button(
    button_frame,
    text="Start",
    command=start,
    width=12
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Pause",
    command=pause,
    width=12
).pack(side="left", padx=5)

update_display()
root.mainloop()
