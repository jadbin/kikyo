class NamespacedClient:
    def __init__(self, client):
        from kikyo.client import Kikyo

        self.client: Kikyo = client
