# Stopwatch Application

## Table of Contents

- [About ](#about-)
- [Getting Started ](#getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [Usage ](#usage-)
- [Code Explanation](#code-explanation)
  - [Class `TimeDisplay`](#class-timedisplay)
  - [Class `Stopwatch`](#class-stopwatch)
  - [Class `StopwatchApp`](#class-stopwatchapp)
  - [Entry Point](#entry-point)

## About <a name = "about"></a>

This project is a simple yet functional stopwatch application built using the `textual` Python framework. Designed with a textual user interface, the application allows users to start, pause, reset, and keep track of multiple stopwatches. It is suitable for scenarios where multiple time-tracking sessions are required, or for users looking for a minimalist and terminal-based stopwatch utility.

## Getting Started <a name = "getting_started"></a>

These instructions will guide you on how to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. Additionally, the `textual` library is essential. You can install it via pip:

```
pip install textual
```

### Installing

1. Clone the repository to your local machine.
   ```
   git clone https://github.com/ericksantos12/Stopwatch_TUI.git
   ```

2. Navigate to the directory containing the project.
   ```
   cd Stopwatch_TUI
   ```

3. Run the application.
   ```
   python stopwatch.py
   ```

After these steps, the application should be up and running, presenting you with multiple stopwatches and their respective controls.

## Usage <a name = "usage"></a>

Upon launching the application, you'll see multiple stopwatches with "Start", "Stop", and "Reset" buttons. 

- Click "Start" to begin the stopwatch.
- Click "Stop" to pause it.
- Click "Reset" to reset the stopwatch.

Additionally, there are keyboard shortcuts defined:
- `d`: Toggle Dark Mode
- `a`: Add a new stopwatch
- `s`: Remove a stopwatch

These shortcuts enhance the user experience, making interactions faster and more intuitive.

## Code Explanation

### Class `TimeDisplay`

```python
class TimeDisplay(Static):
    # Initialize reactive properties
    time_start = reactive(monotonic)  # Start time of the timer
    time_elapsed = reactive(0.0)  # Elapsed time since the timer started
    total_elapsed = reactive(0.0)  # Total accumulated time (including paused time)

    def on_mount(self):
        # Start the timer
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self):
        # Calculate the elapsed time since the timer started
        self.time_elapsed = self.total_elapsed + (monotonic() - self.time_start)

    def watch_time_elapsed(self):
        # Convert the elapsed time to hours, minutes, and seconds
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60)
        time_string = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"

        # Update the time string
        self.update(time_string)

    def start(self):
        # Start the timer
        self.time_start = monotonic()
        self.update_timer.resume()

    def stop(self):
        # Pause the timer and update the total time
        self.update_timer.pause()
        self.total_elapsed += monotonic() - self.time_start
        self.time_elapsed = self.total_elapsed

    def reset(self):
        # Reset the timer
        self.total_elapsed = 0
        self.time_elapsed = 0
```
The `TimeDisplay` class inherits from `Static` and is used to display and manage the time of a stopwatch. It uses reactive properties to automatically update the display when the time changes.

---

### Class `Stopwatch`

```python
class Stopwatch(Static):
    """Custom Stopwatch Widget"""

    @on(Button.Pressed, "#start-button")
    def start_stopwatch(self):
        self.add_class("started")
        self.query_one(TimeDisplay).start()

    @on(Button.Pressed, "#stop-button")
    def stop_stopwatch(self):
        self.remove_class("started")
        self.query_one(TimeDisplay).stop()

    @on(Button.Pressed, "#reset-button")
    def reset_stopwatch(self):
        self.query_one(TimeDisplay).reset()

    def compose(self):
        yield Button("Start", variant="success", id="start-button")
        yield Button("Stop", variant="error", id="stop-button", classes="hidden")
        yield Button("Reset", id="reset-button")
        yield TimeDisplay("00:00:00.00")
```
The `Stopwatch` class also inherits from `Static` and manages the control buttons and the display of the stopwatch. It responds to button press events to start, stop, and reset the stopwatch.

---

### Class `StopwatchApp`

```python
class StopwatchApp(App):
    """The Main App"""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("a", "add_stopwatch", "Add Stopwatch"),
        ("s", "remove_stopwatch", "Remove Stopwatch"),
    ]
    CSS_PATH = "style.tcss"

    def compose(self):
        yield Header(show_clock=True)
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch()
            yield Stopwatch()
            yield Stopwatch()
        yield Footer()

    def action_toggle_dark(self):
        self.dark = not self.dark
        
    def action_add_stopwatch(self):
        new_stopwatch = Stopwatch()
        self.query_one("#stopwatches").mount(new_stopwatch)
        new_stopwatch.scroll_visible()
        
    def action_remove_stopwatch(self):
        stopwatches = self.query(Stopwatch)
        if stopwatches:
            stopwatches.last().remove()
```
The `StopwatchApp` is the main class that inherits from `App` and organizes the overall structure and behavior of the application. It defines actions for keyboard shortcuts and manages the addition and removal of stopwatches.

---

### Entry Point

```python
if __name__ == "__main__":
    StopwatchApp().run()
```
This code block checks if the script is being executed directly, and if so, creates an instance of `StopwatchApp` and runs it.

