from time import monotonic

from textual import on
from textual.app import App
from textual.widgets import Static, Button, Footer, Header
from textual.reactive import reactive
from textual.containers import ScrollableContainer

from time import monotonic


class TimeDisplay(Static):
    # Initialize reactive properties
    time_start = reactive(monotonic)  # Start time of the timer
    time_elapsed = reactive(0.0)  # Elapsed time since the timer started
    total_elapsed = reactive(0.0)  # Total time accumulated (paused time included)

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


if __name__ == "__main__":
    StopwatchApp().run()
