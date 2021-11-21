import cv2


class vehicle_detection(object):
	def __init__(self, STREAM_URL, skip_steps=15):
        self.cam = cv2.VideoCapture(STREAM_URL)
        self.frame = None
        self.skip_steps = skip_steps

        
    def __init__(self, STREAM_URL, skip_steps=15):
        """
        > a frame-stream object
        > frame object- keeping it central to entire class
        > skip_steps to take snapshots at certain steps to
          detect motion.
        """
        self.cam = cv2.VideoCapture(STREAM_URL)
        self.frame = None
        self.skip_steps = skip_steps


    def get_frame(self):
        """
        Function to read the frames from the stream-object
        created as a class-member.
        """
        frame = None
        fail_count = 0
        while True:
            frame = self.cam.read()[1]
            if frame is None:
                fail_count += 1
                if fail_count == 100:
                    print("Failed to read the frames multiple times")
                    break
                continue
            break
        self.frame = frame


    def pre_process_frame(self):
        """
        This method applies all the pre-processing steps on the
        frame required for optimum performance.
        """
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        return blurred

    def draw_bounding_Box(self, frame, contour, box_cord, draw_contour=False):
        """
        This method draws the bounding box on the frame at given
        locaiton.
        """


    def detect_motion(self, prev_frame, frame):
        """
        This is the primary method to detect the motion between a old
        snapshot and current frame (separated by skip_steps number of frames)
        """



    def runner(self):
        """
        Primary runner function to perform vehicle detection
        """



if __name__ == "__main__":
    vehicle_detection_obj = vehicle_detection(STREAM_URL="./data/3.mp4", skip_steps=15)
    vehicle_detection_obj.runner()
