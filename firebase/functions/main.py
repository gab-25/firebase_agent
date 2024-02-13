# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import scheduler_fn
from firebase_admin import initialize_app

initialize_app()


@scheduler_fn.on_schedule(schedule="0 * * * *")
def on_run_example(event: scheduler_fn.ScheduledEvent) -> None:
    print("Hello Gab!")
