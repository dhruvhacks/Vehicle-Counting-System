import cv2


class vehicle_detection(object):
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
        x, y, w, h = box_cord
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)
        if draw_contour:
            cv2.drawContours(frame, contour,-1,(255,0,0),3)


    def detect_motion(self, prev_frame, frame):
        """
        This is the primary method to detect the motion between a old
        snapshot and current frame (separated by skip_steps number of frames)
        """
        frameDeltaLast = cv2.absdiff(prev_frame, frame)
        threshLast = cv2.threshold(frameDeltaLast, 25, 255, cv2.THRESH_BINARY)[1]
        threshLast = cv2.dilate(threshLast, None, iterations=5)
        contoursLast, hierL = cv2.findContours(threshLast.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for ct in contoursLast:
            contour_area = cv2.contourArea(ct)
            (x, y, w, h) = cv2.boundingRect(ct)
            ct_area = contour_area / (h * w)
            self.draw_bounding_Box(frame=self.frame,
                                   contour=ct,
                                   box_cord=(x, y, w, h))
            if (ct_area < 0.01 or ct_area > 0.9) or (float(h) / w >= 1.8):
                continue
        cv2.imshow("Boxed frame", self.frame)


    def runner(self):
        """
        Primary runner function to perform vehicle detection on Video Stream
        """
        count = 0
        self.get_frame()
        prev_frame_BGR = self.frame
        prev_frame_ppr = self.pre_process_frame()
        while True:
            while count != self.skip_steps:
                self.get_frame()
                count += 1
            frame_ppr = self.pre_process_frame()
            count = 0
            self.detect_motion(prev_frame_ppr, frame_ppr)
            prev_frame_ppr = frame_ppr.copy()
            if cv2.waitKey(100) == ord('q'):
                print("Runner stopped")
                break


if __name__ == "__main__":
    vehicle_detection_obj = vehicle_detection(STREAM_URL="./data/3.mp4", skip_steps=15)
    vehicle_detection_obj.runner()
