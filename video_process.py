import os
import cv2
import glob
import numpy as np
import argparse
from utils.plot import Annotator
from utils.database import change_items
from utils.localize import localize
from utils.dataloader import LoadVideos
from utils.general import detection2xyxy,detection2confs, detection2clss, detection2names
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
from track.ocsort import OCSort
COLORS = np.random.randint(0, 255, size=(100, 3), dtype="uint8")


import time

def run(args, source):
    # Sleep for few seconds 
    time.sleep(10)
    # Create the object detection model
    base_options = core.BaseOptions(file_name=args.model, num_threads=args.numThreads)
    detection_options = processor.DetectionOptions(max_results=10, score_threshold=0.5)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)
    
    # Define the video loader
    dataset = LoadVideos(source, img_size=(args.frameHeight, args.frameWidth), sample_stride=args.stride, batchsize=args.batchsize)
    
    # define the tracker
    tracker = OCSort(det_thresh=0.45, iou_threshold=0.2, use_byte=False)
    vid_path = None
    # Initialize the item level arrays and track-item info dictionary
    levels = []
    track_dict = {}

    for batch_idx, (path, imgs, vid_cap, s) in enumerate(dataset):
        for frame_idx, img in enumerate(imgs):
            levels.append(localize(img))
            annotator = Annotator(img, line_width=2)
            input_tensor = vision.TensorImage.create_from_array(img)
            # Run object detection estimation using the model.
            detection_result = detector.detect(input_tensor)
            if len(detection_result.detections) > 0:
                # Get the detection results
                xyxy = detection2xyxy(detection_result)
                confs = detection2confs(detection_result)
                clss = detection2clss(detection_result)
                names = detection2names(detection_result)
                # pass the detections to the OCsort
                outputs = tracker.update(xyxy, confs, clss, img)
                if len(outputs) > 0:
                    for (output, conf, name) in zip(outputs, confs, names):
                        bbox = output[0:4]
                        id = int(output[4])
                        cls = int(output[5])
                        label = f'{int(id)} {name} {conf:.2f}'
                        annotator.mask_label(bbox, label, color=tuple(COLORS[int(id)]))
                        # Fill the tack-item info dictionary
                        center_x = (bbox[0] + bbox[2]) / 2
                        center_y = (bbox[1] + bbox[3]) / 2
                        if not id in track_dict:
                            track_dict[id] = {}
                            track_dict[id]["start_point"] = (center_x, center_y)
                            track_dict[id]["start_frame"] = batch_idx * args.batchsize + frame_idx
                            track_dict[id]["class_counter"] = {}
                            track_dict[id]["total_frame"] = 0
                        track_dict[id]["total_frame"] += 1
                        track_dict[id]["end_point"] = (center_x, center_y)
                        track_dict[id]["end_frame"] = batch_idx * args.batchsize + frame_idx
                        if not name in track_dict[id]["class_counter"]:
                            track_dict[id]["class_counter"][name] = 1
                        else:
                            track_dict[id]["class_counter"][name] += 1
            else:
                pass
                # print('No detections')
            # Write to the video
            im0 = annotator.result()
            if vid_path is None:  # new video
                num_videos = len(glob.glob(args.output_folder+'/*.mp4'))
                vid_path = args.output_folder + f"/output{num_videos+1}.mp4"
                if vid_cap:  # video
                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                    w = im0.shape[1]
                    h = im0.shape[0]
                else:  # stream
                    fps, w, h = 30, im0.shape[1], im0.shape[0]
                vid_writer = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
            im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
            vid_writer.write(im0)

    # Aggregate the information
    print(track_dict)
    track_result = []
    for track in track_dict:
        # Decide whether this is a moving item
        change_x = abs(track_dict[track]["start_point"][0] - track_dict[track]["end_point"][0])
        change_y = abs(track_dict[track]["start_point"][1] - track_dict[track]["end_point"][1])
        if (change_x / args.frameWidth < 0.1 and change_y / args.frameHeight < 0.1) or track_dict[track]["total_frame"] <= 4:
            continue # stationary objects
        # Obtain the object class name
        counter = 0
        class_name = None
        for c in track_dict[track]["class_counter"]:
            if track_dict[track]["class_counter"][c] > counter:
                counter = track_dict[track]["class_counter"][c]
                class_name = c
        # Decide the moving direction
        horizontal = "right" if track_dict[track]["end_point"][0] - track_dict[track]["start_point"][0] >= 0 else "left"
        vertical = "down" if track_dict[track]["end_point"][1] - track_dict[track]["start_point"][1] >= 0 else "up"
        # Decide the floor level
        floor_counter = {}
        for i in range(track_dict[track]["start_frame"], track_dict[track]["end_frame"]+1):
            if not levels[i] in floor_counter:
                floor_counter[levels[i]] = 1
            else:
                floor_counter[levels[i]] += 1
        counter = 0
        item_level = None
        for lvl in floor_counter:
            if floor_counter[lvl] > counter:
                counter = floor_counter[lvl]
                item_level = lvl
        track_result.append((class_name, (horizontal, vertical, item_level)))
    print(track_result)
    os.remove(source)
    change_items(track_result)
    return track_result
    