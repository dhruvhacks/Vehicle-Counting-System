import tkinter as tk
import vehicle_detection as vhd


class gui(object):
    def __init__(self):
        self.vehicle_det_obj = None
        self.selectClip = None
        self.skip_steps = None
        self.threshold_binary = None
        self.threshold_lower = None
        self.threshold_middle = None
        self.threshold_higher = None


    def startDetection(self):
        self.vehicle_det_obj.runner()


    def config(self):
        self.vehicle_det_obj = vhd.vehicle_detection(STREAM_URL="./data/{clip}.mp4".format(clip=self.selectClip.get()),
                                                skip_steps=self.skip_steps.get())
        self.vehicle_det_obj.configure(True)


    def runGui(self):
        m=tk.Tk(className='Vehicle Counter')

        rw = 0
        tk.Label(text='Clip Selection : ').grid(row=rw,column=0)
        self.selectClip = tk.IntVar()
        tk.Radiobutton(m, text='Clip 1' , variable=self.selectClip, value=1).grid(row=rw,column = 1)
        tk.Radiobutton(m, text='Clip 2' , variable=self.selectClip, value=2).grid(row=rw,column = 2)
        tk.Radiobutton(m, text='Clip 3' , variable=self.selectClip, value=3).grid(row=rw,column = 3)
        tk.Radiobutton(m, text='Clip 4' , variable=self.selectClip, value=4).grid(row=rw,column = 4)
        tk.Radiobutton(m, text='Clip 5' , variable=self.selectClip, value=5).grid(row=rw,column = 5)
        rw+=1


        tk.Label(text='Skip Steps : ').grid(row=rw,column = 0)
        skip_steps = tk.Scale(m, from_=1, to=15, orient=tk.HORIZONTAL)
        skip_steps.grid(row=rw,column = 1)
        self.skip_steps = skip_steps
        rw+=1

        tk.Label(text='Binary Threshold : ').grid(row=rw,column = 0)
        self.threshold_binary= tk.Scale(m, from_=25, to=150, orient=tk.HORIZONTAL)# Steps of 5
        self.threshold_binary.grid(row=rw,column = 1)
        rw+=1

        tk.Label(text='Lower Threshold : ').grid(row=rw, column=0)
        self.threshold_lower = tk.Scale(m, from_=10000, to=50000, orient=tk.HORIZONTAL)  # Steps of 5000
        self.threshold_lower.grid(row=rw, column=1)
        rw += 1
        tk.Label(text='Middle Threshold : ').grid(row=rw, column=0)
        self.threshold_middle = tk.Scale(m, from_=35000, to=80000, orient=tk.HORIZONTAL)  # Steps of 5000
        self.threshold_middle.grid(row=rw, column=1)
        rw += 1
        tk.Label(text='Higher Threshold : ').grid(row=rw, column=0)
        self.threshold_higher = tk.Scale(m, from_=60000, to=100000, orient=tk.HORIZONTAL)  # Steps of 5000
        self.threshold_higher.grid(row=rw, column=1)
        rw += 1

        startButton = tk.Button(m,activebackground= '#0f0', text='Config', width=25,command = self.config)#command
        startButton.grid(row=rw,column=0)

        startButton = tk.Button(m,activebackground= '#0f0', text='Start', width=25,command = self.startDetection)#command
        startButton.grid(row=rw,column=5)
        rw+=1

        m.mainloop()


if __name__ == "__main__":
    gui_obj = gui()
    gui_obj.runGui()




