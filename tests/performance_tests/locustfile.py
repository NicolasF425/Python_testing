from locust import HttpUser, task, between
from utilities import load_clubs, load_competitions


class LocustTestServer(HttpUser):
    wait_time = between(1, 3)
    competition = load_competitions()[2]
    club = load_clubs()[0]

    def on_start(self):
        self.client.get("/", name="index")
        self.client.post("/showSummary", data={'email': self.club["email"]}, name="login")

    @task
    def get_booking(self):
        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}",
            name="booking"
        )

    @task
    def post_booking(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": self.club["name"],
                "competition": self.competition["name"]
            },
            name="purchase_places"
        )

    @task
    def get_board(self):
        self.client.get("/points", name="view_club_points")
