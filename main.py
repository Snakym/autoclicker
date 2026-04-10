import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Button, Controller
from pynput import keyboard

# ---------------- STATE ----------------
running = False
exit_event = threading.Event()

mouse = Controller()
click_count = 0


# ---------------- LOOP ----------------
def click_loop(get_params, update_ui):
    global running, click_count

    while not exit_event.is_set():

        if not running:
            time.sleep(0.1)
            continue

        params = get_params()

        button = params["button"]
        interval = params["interval"]

        while running and not exit_event.is_set():

            mouse.click(button)

            click_count += 1
            update_ui(click_count)

            time.sleep(interval)


# ---------------- HOTKEYS ----------------
def on_press(key):
    global running

    try:
        if key == keyboard.Key.f6:
            running = not running
            print("[F6] toggle:", running)

        elif key == keyboard.Key.f12:
            print("[F12] exit")
            exit_event.set()
            running = False
            return False

    except:
        pass


# ---------------- APP ----------------
class AutoClicker:
    def __init__(self, root):
        self.root = root
        root.title("🖱 AutoClicker PRO MAX")
        root.geometry("460x360")
        root.resizable(False, False)
        root.configure(bg="#121212")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#121212")
        style.configure("TLabel", background="#121212", foreground="white")
        style.configure("TButton", font=("Segoe UI", 10))

        # ---------------- TITLE ----------------
        ttk.Label(root, text="AUTOCLICKER PRO MAX",
                  font=("Segoe UI", 16, "bold")).pack(pady=10)

        # ---------------- BUTTON TYPE ----------------
        frame = ttk.Frame(root)
        frame.pack(pady=5)

        ttk.Label(frame, text="Button").grid(row=0, column=0)

        self.button_var = tk.StringVar(value="left")
        ttk.Combobox(frame, textvariable=self.button_var,
                     values=["left", "right"], state="readonly",
                     width=10).grid(row=0, column=1)

        # ---------------- CPS INPUT ----------------
        cps_frame = ttk.Frame(root)
        cps_frame.pack(pady=10)

        ttk.Label(cps_frame, text="Clicks Per Second (CPS)").grid(row=0, column=0)

        self.cps_var = tk.StringVar(value="10")
        ttk.Entry(cps_frame, textvariable=self.cps_var, width=10).grid(row=0, column=1)

        # ---------------- PRESETS ----------------
        preset = ttk.Frame(root)
        preset.pack(pady=5)

        ttk.Button(preset, text="5 CPS", command=lambda: self.set_cps(5)).grid(row=0, column=0, padx=3)
        ttk.Button(preset, text="10 CPS", command=lambda: self.set_cps(10)).grid(row=0, column=1, padx=3)
        ttk.Button(preset, text="20 CPS", command=lambda: self.set_cps(20)).grid(row=0, column=2, padx=3)
        ttk.Button(preset, text="50 CPS", command=lambda: self.set_cps(50)).grid(row=0, column=3, padx=3)

        # ---------------- STATUS ----------------
        self.status = ttk.Label(root, text="Status: OFF 🔴")
        self.status.pack(pady=5)

        self.counter = ttk.Label(root, text="Clicks: 0")
        self.counter.pack()

        # ---------------- BUTTONS ----------------
        btns = ttk.Frame(root)
        btns.pack(pady=10)

        ttk.Button(btns, text="▶ Start (F6)", command=self.start).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="⏹ Stop", command=self.stop).grid(row=0, column=1, padx=5)

        # HOTKEYS
        keyboard.Listener(on_press=on_press).start()

    # ---------------- CPS ----------------
    def set_cps(self, value):
        self.cps_var.set(str(value))

    # ---------------- PARAMS ----------------
    def get_params(self):
        cps = float(self.cps_var.get())

        if cps <= 0:
            cps = 1

        interval = 1 / cps   # 🔥 CPS → delay

        return {
            "button": Button.left if self.button_var.get() == "left" else Button.right,
            "interval": interval
        }

    # ---------------- UPDATE UI ----------------
    def update_counter(self, value):
        self.counter.config(text=f"Clicks: {value}")

    # ---------------- CONTROL ----------------
    def start(self):
        global running
        running = True
        self.status.config(text="Status: RUNNING 🟢")

    def stop(self):
        global running
        running = False
        self.status.config(text="Status: STOPPED 🔴")


# ---------------- MAIN ----------------
def main():
    root = tk.Tk()
    app = AutoClicker(root)

    threading.Thread(
        target=click_loop,
        args=(app.get_params, app.update_counter),
        daemon=True
    ).start()

    root.mainloop()


if __name__ == "__main__":
    main()