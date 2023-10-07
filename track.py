import djitellopy
import math
import cv2
import threading
import time
from grip import GripPipeline

cv2.namedWindow("Tello Live Video", cv2.WINDOW_NORMAL)
cv2.namedWindow("Tello Computed Video", cv2.WINDOW_NORMAL)

def main(drone: djitellopy.Tello):
    # Connect to the drone
    drone.connect()

    # Start the video stream
    drone.streamon()
    
    # Takeoff
    drone.takeoff()

    # Create a grip pipeline for processing frames
    pipeline = GripPipeline()

    # Continuously read frames from the drone and process them with the grip pipeline
    while True:
        # Read the next frame from the drone
        frame = drone.get_frame_read().frame
        # Process the frame with the grip pipeline
        pipeline.process(frame)
        
        cv2.imshow("Tello Live Video", frame)
        cv2.imshow("Tello Computed Video", pipeline.blur_output)

        # Check if a blob was found in the frame
        if len(pipeline.find_blobs_output) > 0:
            # Get the center of the first blob
            blob_center = pipeline.find_blobs_output[0].pt

            # Get the center of the frame
            frame_center = (frame.shape[1] / 2, frame.shape[0] / 2)

            # Calculate the angle between the blob center and the frame center
            angle = math.degrees(math.atan2(blob_center[1] - frame_center[1], blob_center[0] - frame_center[0]))

            # Update the yaw angle of the drone
            if angle > 0:
                drone.rotate_clockwise(angle)
            elif angle < 0:
                drone.rotate_counter_clockwise(angle)

        # Wait for the next frame
        time.sleep(0.01)

# Create a Tello drone object
drone = djitellopy.Tello()

main(drone)

