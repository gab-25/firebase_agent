# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import pubsub_fn
from firebase_admin import initialize_app

initialize_app()


@pubsub_fn.on_message_published(topic="hello")
def on_message_example(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
    print("hello Gab!")
