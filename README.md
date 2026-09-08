# INFO5356-Lab1
# INFO 5356 Lab 1 - Introduction to Reachy Mini

This repository contains our implementation for Lab 1 of INFO 5356: Introduction to Human-Robot Interaction.

The project includes a custom Reachy Mini application, `team_greeting_app`, developed and tested in the MuJoCo simulator.

## Environment

- Operating System: macOS
- Architecture: arm64
- Python Version: 3.12.10
- Reachy Mini Version: 1.10.0
- MuJoCo Version: 3.3.0
- Virtual Environment: `reachy_mini_env`

## Repository Structure

```text
INFO5356-Lab1/
├── README.md
├── .gitignore
└── apps/
    └── team_greeting_app/
        ├── README.md
        ├── pyproject.toml
        ├── index.html
        ├── style.css
        └── team_greeting_app/
            ├── __init__.py
            ├── main.py
            └── static/

Setup
1. Clone the repository
  git clone <https://github.com/leiyan666/INFO5356-Lab1>
  cd INFO5356-Lab1

2. Create the virtual environment
  python3.12 -m venv reachy_mini_env
  Activate it:
  source reachy_mini_env/bin/activate

3. Install Reachy Mini and MuJoCo
  python -m pip install --upgrade pip
  pip install "reachy-mini[mujoco]"

4. Install the custom app in editable mode
  pip install -e apps/team_greeting_app

5. Validate the app
  reachy-mini-app-assistant check apps/team_greeting_app
A successful validation should report:
  [OK] App 'team_greeting_app' passed all checks!

Run the MuJoCo Simulation
On macOS, start the simulator using:
  mjpython -m reachy_mini.daemon.app.main --sim
Keep this terminal running.

Run team_greeting_app
Open a second terminal:
  cd INFO5356-Lab1
  source reachy_mini_env/bin/activate
  cd apps/team_greeting_app
  python -m team_greeting_app.main
The application performs three stages:
Orient toward the implied user
The robot rotates its head toward the user.
Perform a greeting
The robot uses its head and antennas to produce an expressive greeting.
Return to neutral
The robot returns its head and antennas to their neutral positions.
The terminal prints timestamped stage markers that correspond to the observed behavior in MuJoCo.
Example:
  [21:36:03] Stage 1: Orienting toward user
  [21:36:05] Stage 2: Performing greeting
  [21:36:07] Stage 3: Returning to neutral
  [21:36:07] Cleanup: Returning to neutral
  [21:36:08] Greeting sequence complete

Stop Behavior
The application checks stop_event during waits and supports graceful stopping.
Press:
  Ctrl+C
to request a normal stop.
When a stop is requested, the application executes its cleanup behavior and returns the simulated robot to the neutral pose before exiting.
Motion and Timing Parameters


The application exposes the following parameters:
  HEAD_YAW_DEG = 20.0          # degrees
  ANTENNA_ANGLE_DEG = 25.0     # degrees
  MOVE_DURATION_SEC = 1.5      # seconds
  PAUSE_SEC = 0.5              # seconds
These parameters control the motion amplitude and timing of the greeting behavior.

