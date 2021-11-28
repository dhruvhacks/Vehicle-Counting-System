import cv2
import numpy as np


class vehicle_detection(object):
    def __init__(self, STREAM_URL, skip_steps=15, replicate=False, gamma=1.2, binary_threshold = 25):
        """
        > a frame-stream object
        > frame object- keeping it central to entire class
        > skip_steps to take snapshots at certain steps to
          detect motion.
        """
        self.STREAM_URL = STREAM_URL
        self.cam = cv2.VideoCapture(self.STREAM_URL)
        self.frame = None
        self.skip_steps = skip_steps
        self.crop_cord = [1, 1, 100000, 100000]
        self.replicate = replicate
        self.gamma = gamma
        self.threshold = binary_threshold


    def region_selector(self, event, x, y, flags, param):
        """
        Callback function to be triggered by cv2.setMouseCallback
        This function allows creation of box over frame by dragging
        the pointer with left-button pressed.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.first_click:
                self.box_builder[0] = x
                self.box_builder[1] = y
                self.first_click = False
        elif event == cv2.EVENT_LBUTTONUP:
            self.box_builder[2] = x
            self.box_builder[3] = y
            self.first_click = True
            cv2.rectangle(self.frame, (self.box_builder[0], self.box_builder[1]), (x, y), (0, 255, 0), 2)
        if not self.first_click:
            self.get_frame(smooth=True)
            cv2.rectangle(self.frame, (self.box_builder[0], self.box_builder[1]), (x, y), (255, 0, 0), 2)


    def get_frame(self, smooth=False):
        """
        Function to read the frames from the stream-object
        created as a class-member.
        """
        count = 0
        frame = None
        while count != self.skip_steps:
            frame = self.cam.read()[1]
            if smooth:
                break
            count += 1
        self.frame = frame[min(self.crop_cord[1], self.crop_cord[3]):max(self.crop_cord[1], self.crop_cord[3]),
                           min(self.crop_cord[0], self.crop_cord[2]):max(self.crop_cord[0], self.crop_cord[2])]


    def configure(self, region_selection=True, create_bg=False):
        """
        This method is executed before running the project in full capacity.
        Here, we can define a specific region as ROI for vehicle detection and
        also specify the mode of operation- with prev_frames or specified background
        """
        if region_selection:
            self.first_click = True
            self.box_builder = self.crop_cord.copy()
            self.get_frame()
            cv2.namedWindow("region_selector")
            cv2.setMouseCallback('region_selector', self.region_selector)
            text = "(config_mode) Drag mouse to define ROI and press q when complete"
            while True:
                cv2.imshow("region_selector", self.frame)
                cv2.putText(self.frame, text, (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                if cv2.waitKey(1) == ord('q'):
                    break
            self.cam = cv2.VideoCapture(self.STREAM_URL)
            self.crop_cord = self.box_builder.copy()
            cv2.destroyAllWindows()



    def pre_process_frame(self):
        """
        This method applies all the pre-processing steps on the
        frame required for optimum performance.
        """
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        result = cv2.bilateralFilter(gray, 15, 75, 75)
        # result = cv2.GaussianBlur(gray, (21, 21), 0)
        if self.replicate:
            gamma = np.power(255.0,1-self.gamma)
            gamma = np.float64(gamma)*result**(np.float64(self.gamma))
            gamma = np.uint8(gamma)
            sobel_x = cv2.Sobel(result, cv2.CV_8U, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(result, cv2.CV_8U, 0, 1, ksize=3)
            result = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
            result = cv2.threshold(result, self.threshold, 255, cv2.THRESH_BINARY)[1]
        return result


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
        # Taking absolute differece of frames at skip_steps step.
        frameDeltaLast = cv2.absdiff(prev_frame, frame)
        if not self.replicate:
            frameDeltaLast = cv2.threshold(frameDeltaLast, self.threshold, 255, cv2.THRESH_BINARY)[1]
            frameDeltaLast = cv2.dilate(frameDeltaLast, None, iterations=5)
        contoursLast, hierL = cv2.findContours(frameDeltaLast.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

 
    def get_binary_image(self, frame_1, frame_2):
        """

        Parameters
        ----------
        frame_1 : pre-processed frame 1
        frame_2 : pre-processsed frame 2

        Returns
        -------
        Binary image which is the difference of pre-processed frames

        """
        # Apply 'AND' operation to obtain the intersection of edgy binary frames.
        bin_image = cv2.bitwise_and(frame_1, frame_2, mask = None)
        return bin_image


    def original_method(self):
        """
        This method triggers the vehicle detection based on sequence of steps
        performed in the original work.
        """
        # Taking the first frame and pre-processing it
        self.get_frame()
        prev_prev_frame_ppr = self.pre_process_frame()
        
        # Obtain the second frame too and pre-process it.
        self.get_frame()
        prev_frame_ppr = self.pre_process_frame()

        # Calculating the binary image for prev_frames
        bin_img_prev = self.get_binary_image(prev_prev_frame_ppr, prev_frame_ppr)
        while True:
            # obtain the last frame.
            self.get_frame()
            frame_ppr = self.pre_process_frame()
            
            # Calculating the binary image for current frame
            bin_img_curr = self.get_binary_image(prev_frame_ppr, frame_ppr)

            # Detect motion with generated binary images
            self.detect_motion(bin_img_prev, bin_img_curr)
            
            # Move further one step.
            bin_img_prev = bin_img_curr.copy()
            prev_frame_ppr = frame_ppr.copy()
            
            if cv2.waitKey(100) == ord('q'):
                print("Runner stopped")
                break


    def modified_method(self):
        """
        This method triggers the vehicle detection based on the modified version
        with different sequence of operations.
        """
        self.get_frame()
        prev_frame_ppr = self.pre_process_frame()
        while True:
            self.get_frame()
            frame_ppr = self.pre_process_frame()
            self.detect_motion(prev_frame_ppr, frame_ppr)
            prev_frame_ppr = frame_ppr.copy()
            if cv2.waitKey(100) == ord('q'):
                print("Runner stopped")
                break


    def runner(self):
        """
        Runner function to triggered the required pipeline
        """
        if self.replicate:
            self.original_method()
        else:
            self.modified_method()


if __name__ == "__main__":
    vehicle_detection_obj = vehicle_detection(STREAM_URL="./data/3.mp4",
                                              skip_steps=15)
    vehicle_detection_obj.configure(True, False)
    vehicle_detection_obj.runner()
