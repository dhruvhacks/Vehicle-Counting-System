import vehicle_detection as vhd
if __name__ == "__main__":
    vehicle_det_obj = vhd.vehicle_detection(STREAM_URL="./data/3.mp4",skip_steps=15)
    vehicle_det_obj.runner()
