import cv2
import threading
import grip
from djitellopy import Tello

pipeline = grip.GripPipeline()
frame = None

# Initialize Tello object
tello = Tello()

# Connect to Tello
tello.connect()

# Start video stream
tello.streamon()

# Create OpenCV window
cv2.namedWindow("Tello Live Video", cv2.WINDOW_NORMAL)
cv2.namedWindow("Tello Computed Video", cv2.WINDOW_NORMAL)

def update_continuous():
    pass


# Loop to continuously receive and display video frames
while True:
    # Get the current frame from Tello's video stream
    frame = tello.get_frame_read().frame
    
    pipeline.process(frame)
    print(pipeline.find_blobs_output)
    computed_frame = pipeline.blur_output

    # Display the frame in the OpenCV window
    cv2.imshow("Tello Live Video", frame)
    cv2.imshow("Tello Computed Video", computed_frame)

    # Wait for a key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
tello.streamoff()
tello.end()
