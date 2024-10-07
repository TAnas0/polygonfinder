from locust import HttpUser, between, task
import random


lat_steps = 40  # Number of steps in the latitude direction
lng_steps = 80  # Number of steps in the longitude direction


class ServiceAreaUser(HttpUser):
    wait_time = between(1, 2)

    # Define the grid parameters

    # Generate evenly distributed latitude and longitude values
    latitudes = [i * (180 / (lat_steps - 1)) - 90 for i in range(lat_steps)]
    longitudes = [i * (360 / (lng_steps - 1)) - 180 for i in range(lng_steps)]

    @task
    def check_point_in_polygon(self):
        # Choose a random lat/lng from the generated grid
        lat = random.choice(self.latitudes)
        lng = random.choice(self.longitudes)
        self.client.get(f"/api/v1/serviceareas/check?lat={lat}&lng={lng}")
