import speech_recognition as sr
import asyncio
from dash.robot import DashRobot, discover_and_connect
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def voice_command_to_action(robot, command):
    """
    Convert a voice command to an action executed by the robot.
    """
    logging.debug(f"Processing command: {command}")
    command = command.lower()
    if 'forward' in command:
        logging.debug("Executing: move forward")
        await robot.drive(340)  # Move forward at speed 100
        await asyncio.sleep(1)  # Adjust as needed
        await robot.stop()
    elif 'back' in command:
        logging.debug("Executing: move back")
        await robot.drive(-100)  # Move back at speed 100
        await asyncio.sleep(1)  # Adjust as needed
        await robot.stop()
    elif 'left' in command:
        logging.debug("Executing: turn left")
        await robot.turn(-90)  # Turn left
    elif 'right' in command:
        logging.debug("Executing: turn right")
        await robot.turn(90)  # Turn right
    elif 'stop' in command:
        logging.debug("Executing: stop")
        await robot.stop()
    else:
        logging.warning(f"Command '{command}' not recognized.")

async def listen_and_execute(robot):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        logging.info("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        logging.info("Ready for voice command.")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        logging.info(f"Recognized command: {command}")
        await voice_command_to_action(robot, command)
    except sr.UnknownValueError:
        logging.error("Could not understand audio")
    except sr.RequestError as e:
        logging.error(f"Speech recognition request failed; {e}")

async def main():
    robot = await discover_and_connect()
    if robot:
        logging.info("Robot connected. Starting voice control.")
        try:
            while True:
                await listen_and_execute(robot)
        except KeyboardInterrupt:
            logging.info("Voice control stopped by user")
        finally:
            await robot.disconnect()
            logging.info("Robot disconnected.")
    else:
        logging.error("Failed to connect to the robot.")

if __name__ == "__main__":
    asyncio.run(main())
