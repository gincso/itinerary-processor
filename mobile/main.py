
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.mapview import MapView, MapMarker
from kivy.clock import Clock
import requests
import json

class ItineraryApp(App):
    def build(self):
        self.api_url = ""
        self.driver_id = 1
        self.route = []
        self.markers = []

        # Create layout
        layout = BoxLayout(orientation='vertical')

        # API URL input
        self.url_input = TextInput(
            hint_text='Enter Agent Zero server URL',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.url_input)

        # Driver ID input
        self.id_input = TextInput(
            hint_text='Enter Driver ID',
            input_type='number',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.id_input)

        # Connect button
        connect_btn = Button(
            text='Connect',
            size_hint_y=None,
            height=50
        )
        connect_btn.bind(on_press=self.connect)
        layout.add_widget(connect_btn)

        # Status label
        self.status_label = Label(text='Not connected')
        layout.add_widget(self.status_label)

        # Map view
        self.mapview = MapView(zoom=13, lat=34.73, lon=-112.0)
        layout.add_widget(self.mapview)

        # Location update button
        update_btn = Button(
            text='Update Location',
            size_hint_y=None,
            height=50
        )
        update_btn.bind(on_press=self.update_location)
        layout.add_widget(update_btn)

        # Schedule periodic updates
        Clock.schedule_interval(self.update_location_auto, 30)

        return layout

    def connect(self, instance):
        self.api_url = self.url_input.text
        self.driver_id = int(self.id_input.text)

        try:
            # Get driver route
            response = requests.get(
                f"{self.api_url}/api/itinerary/mobile/driver_route/{self.driver_id}"
            )

            if response.status_code == 200:
                data = response.json()
                self.route = data['stops']
                self.plot_route()
                self.status_label.text = f"Connected - {len(self.route)} stops"
            else:
                self.status_label.text = f"Error: {response.text}"
        except Exception as e:
            self.status_label.text = f"Connection failed: {str(e)}"

    def plot_route(self):
        # Clear existing markers
        for marker in self.markers:
            self.mapview.remove_marker(marker)
        self.markers = []

        # Add route markers
        for stop in self.route:
            marker = MapMarker(
                lat=stop['lat'],
                lon=stop['lng']
            )
            self.mapview.add_marker(marker)
            self.markers.append(marker)

        # Center map on first stop
        if self.route:
            self.mapview.center_on(
                self.route[0]['lat'],
                self.route[0]['lng']
            )

    def update_location(self, instance):
        if not self.api_url:
            self.status_label.text = "Not connected to server"
            return

        try:
            # Get current location (simulated for demo)
            lat = self.mapview.lat + 0.001
            lon = self.mapview.lon + 0.001

            # Send to server
            response = requests.post(
                f"{self.api_url}/api/itinerary/location",
                json={
                    "driver_id": self.driver_id,
                    "lat": lat,
                    "lng": lon
                }
            )

            if response.status_code == 200:
                self.status_label.text = f"Location updated: {lat}, {lon}"
            else:
                self.status_label.text = f"Update failed: {response.text}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def update_location_auto(self, dt):
        # Auto-update location every 30 seconds
        if self.api_url and self.driver_id:
            self.update_location(None)

if __name__ == '__main__':
    ItineraryApp().run()
