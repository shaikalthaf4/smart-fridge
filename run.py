''' 
Entry function of the smart fridge:
The main function runs the light sensor
'''
import cv2
import glob
import argparse
import threading
import video_process
ON, OFF = 1, -1
video_id = 0
light = OFF
in_analysis = False

def get_video_name(folder):
    global video_id
    video_id += 1
    return f"{folder}/capture{video_id}.mp4"

def get_analysis_video_name(folder):
    path = folder + '/*.mp4'
    videos = glob.glob(path)
    videos.sort()
    return videos[0] if len(videos) > 0 else None

def capture_video(lock, args):
    global light
    vid_capture = cv2.VideoCapture(0)
    vid_writer = cv2.VideoWriter(get_video_name(args.save_folder), cv2.VideoWriter_fourcc(*'mp4v'), 30, (args.frameWidth, args.frameHeight))
    while(vid_capture.isOpened()):
        ret, frame = vid_capture.read()
        if ret==True:
            vid_writer.write(frame)
            lock.acquire()
            if light == OFF:
                lock.release()
                break
            else:
                lock.release()
        else:
            break
    vid_capture.release()
    vid_writer.release()

def analyze_video(lock, args, source):
    global in_analysis
    print("The source is: ", source)
    video_process.run(args, source)
    print("Finish running video analysis......")
    lock.acquire()
    in_analysis = False
    lock.release()

def light_sensor_simulation(arguments):
    global light
    global in_analysis
    lock_light = threading.Lock()
    lock_in_analysis = threading.Lock()
    try:  
        while True:  
            val= int(input("Enter Light Sensor Value (0 or 1):\n")) 
            if val == 1: # simulate when the light sensor is ON
                light = ON
                t = threading.Thread(target=capture_video, args=(lock_light, arguments))
                t.start()
            else:
                lock_light.acquire()
                light = OFF
                lock_light.release()
                # Start analysis when the light is off
                lock_in_analysis.acquire()
                if in_analysis == False:
                    analysis_video_name = get_analysis_video_name(arguments.save_folder)
                    if not analysis_video_name is None:
                        in_analysis = True
                        t = threading.Thread(target=analyze_video, args=(lock_in_analysis, arguments, analysis_video_name))
                        t.start()
                lock_in_analysis.release()
    except KeyboardInterrupt:  
        print ("Exiting Program")      

# light_sensor_simulation()
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model', help='Path of the object detection model.', required=False, default='models/model.tflite')
    parser.add_argument('--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument('--frameWidth', help='Width of frame to capture from camera.', required=False, type=int, default=640)
    parser.add_argument('--frameHeight', help='Height of frame to capture from camera.', required=False, type=int, default=480)
    parser.add_argument('--numThreads', help='Number of CPU threads to run the model.', required=False, type=int, default=4)
    parser.add_argument('--stride', help='Stride when processing the video', required=False, type=int, default=1)
    parser.add_argument('--batchsize', help='Batchsize when processing the video', required=False, type=int, default=8)
    parser.add_argument('--save-folder', help='Path to save the video', required=False, default='videos')
    parser.add_argument('--output-folder', help='Path to save the video', required=False, default='output')
    args = parser.parse_args()
    light_sensor_simulation(args)


if __name__ == '__main__':
    main()
 
