from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import requests
import time

class TradingApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
        # Create labels to display data
        self.signal_label = Label(text="Signal: Waiting...", font_size=24)
        self.price_label = Label(text="Price: N/A", font_size=18)
        self.ema_fast_label = Label(text="EMA Fast: N/A", font_size=18)
        self.ema_slow_label = Label(text="EMA Slow: N/A", font_size=18)
        
        # Add labels to the layout
        self.add_widget(self.signal_label)
        self.add_widget(self.price_label)
        self.add_widget(self.ema_fast_label)
        self.add_widget(self.ema_slow_label)
        
        # Start a thread to fetch data from the backend
        self.trading_thread = threading.Thread(target=self.fetch_data)
        self.trading_thread.daemon = True
        self.trading_thread.start()
        
        # Update the UI every second
        Clock.schedule_interval(self.update_ui, 1)

    def fetch_data(self):
        while True:
            try:
                # Fetch data from the backend
                response = requests.get("https://your-heroku-app.herokuapp.com/data")
                data = response.json()
                
                # Update the labels
                self.signal_label.text = f"Signal: {data.get('signal', 'Hold')}"
                self.price_label.text = f"Price: {data.get('close', 'N/A')}"
                self.ema_fast_label.text = f"EMA Fast: {data.get('ema_fast', 'N/A')}"
                self.ema_slow_label.text = f"EMA Slow: {data.get('ema_slow', 'N/A')}"
            except Exception as e:
                print(f"Error fetching data: {e}")
            time.sleep(5)  # Fetch data every 5 seconds

    def update_ui(self, dt):
        pass  # UI updates are handled in fetch_data

class ForexScalpingApp(App):
    def build(self):
        return TradingApp()

if __name__ == "__main__":
    ForexScalpingApp().run()
    