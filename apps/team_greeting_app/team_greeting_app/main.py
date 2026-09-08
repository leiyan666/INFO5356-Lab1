import threading
import time
from datetime import datetime

import numpy as np

from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.utils import create_head_pose


class TeamGreetingApp(ReachyMiniApp):

    custom_app_url: str | None = None
    request_media_backend: str | None = None

    # Named motion/timing parameters
    HEAD_YAW_DEG = 20.0          # head yaw degrees
    ANTENNA_ANGLE_DEG = 25.0     # antennas degrees
    MOVE_DURATION_SEC = 1.5      # moving duration in seconds
    PAUSE_SEC = 0.5              # pausing seconds

    def log_stage(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def wait_with_stop(self, duration, stop_event):
        start = time.time()

        while time.time() - start < duration:
            if stop_event.is_set():
                return False

            time.sleep(0.02)

        return True

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        completed = False

        try:
            # Stage 1
            self.log_stage("Stage 1: Orienting toward user")

            head_pose = create_head_pose(
                yaw=self.HEAD_YAW_DEG,
                degrees=True
            )

            reachy_mini.set_target(
                head=head_pose,
                antennas=np.deg2rad([0.0, 0.0]),
            )

            if not self.wait_with_stop(self.MOVE_DURATION_SEC, stop_event):
                return

            # Stage 2
            self.log_stage("Stage 2: Performing greeting")

            antennas = np.deg2rad([
                self.ANTENNA_ANGLE_DEG,
                -self.ANTENNA_ANGLE_DEG
            ])

            reachy_mini.set_target(
                head=head_pose,
                antennas=antennas,
            )

            if not self.wait_with_stop(self.MOVE_DURATION_SEC, stop_event):
                return

            antennas = np.deg2rad([
                -self.ANTENNA_ANGLE_DEG,
                self.ANTENNA_ANGLE_DEG
            ])

            reachy_mini.set_target(
                head=head_pose,
                antennas=antennas,
            )

            if not self.wait_with_stop(self.PAUSE_SEC, stop_event):
                return

            # Stage 3
            self.log_stage("Stage 3: Returning to neutral")
            completed = True

        finally:
            self.log_stage("Cleanup: Returning to neutral")
            self.return_to_neutral(reachy_mini)

            # Give MuJoCo time to visibly reach neutral
            time.sleep(1.0)

            if completed:
                self.log_stage("Greeting sequence complete")

    def return_to_neutral(self, reachy_mini: ReachyMini):
        neutral_head = create_head_pose(
            yaw=0.0,
            pitch=0.0,
            roll=0.0,
            degrees=True
        )

        neutral_antennas = np.deg2rad([0.0, 0.0])

        reachy_mini.set_target(
            head=neutral_head,
            antennas=neutral_antennas,
        )


if __name__ == "__main__":
    app = TeamGreetingApp()

    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()