import tkinter as tk
import vehicle_detection as vhd
vehicle_det_obj = None
def startDetection():
    global vehicle_det_obj

    vehicle_det_obj.runner()
def config():
    global vehicle_det_obj
    vehicle_det_obj = vhd.vehicle_detection(STREAM_URL="./data/{clip}.mp4".format(clip=selectClip.get()),
                                            skip_steps=skip_steps.get())
    vehicle_det_obj.configure(True, create_bg.get())
m=tk.Tk(className='Vehicle Counter')

rw = 0
tk.Label(text='Create Dynamic Background : ').grid(row=rw)
selectClip = tk.IntVar()
tk.Radiobutton(m, text='Clip 1' , variable=selectClip, value=1).grid(row=rw,column = 1)
tk.Radiobutton(m, text='Clip 2' , variable=selectClip, value=2).grid(row=rw,column = 2)
tk.Radiobutton(m, text='Clip 3' , variable=selectClip, value=3).grid(row=rw,column = 3)
tk.Radiobutton(m, text='Clip 4' , variable=selectClip, value=4).grid(row=rw,column = 4)
tk.Radiobutton(m, text='Clip 5' , variable=selectClip, value=5).grid(row=rw,column = 5)
rw+=1

tk.Label(text='Clip Selection : ').grid(row=rw,column=0)
create_bg = tk.BooleanVar()
tk.Radiobutton(m, text='True' , variable=create_bg, value=True).grid(row=rw,column = 1)
tk.Radiobutton(m, text='False', variable=create_bg, value=False).grid(row=rw,column = 2)
rw+=1

tk.Label(text='Skip Steps : ').grid(row=rw,column = 0)
skip_steps = tk.Scale(m, from_=1, to=15, orient=tk.HORIZONTAL)
skip_steps.grid(row=rw,column = 1)
rw+=1


tk.Label(text='Gamma Value : ').grid(row=rw,column = 0)
gamma = tk.Scale(m, from_=0.8, to=2.1,resolution = 0.1,orient=tk.HORIZONTAL)
gamma.grid(row=rw,column = 1)
rw+=1


tk.Label(text='Threshold Value : ').grid(row=rw,column = 0)
threshold= tk.Scale(m, from_=0, to=255, orient=tk.HORIZONTAL)
threshold.grid(row=rw,column = 1)
rw+=1

startButton = tk.Button(m,activebackground= '#0f0', text='Config', width=25,command = config)#command
startButton.grid(row=rw,column=0)

startButton = tk.Button(m,activebackground= '#0f0', text='Start', width=25,command = startDetection)#command
startButton.grid(row=rw,column=5)
rw+=1

m.mainloop()






