# Pipelines for demo on next Monday
# (1) Load a Video
# (2) Run detection on it
# (3) Pass the detection to the tracker
import cv2
import numpy as np
import argparse
from utils.plot import Annotator
from utils.dataloader import LoadVideos
from utils.general import detection2xyxy,detection2confs, detection2clss, detection2names
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
from track.ocsort import OCSort
COLORS = np.random.randint(0, 255, size=(100, 3), dtype="uint8")


def run(args):
    # define the video loader
    dataset = LoadVideos(args.source, img_size=(args.frameHeight, args.frameWidth), sample_stride=args.stride)
    # define the tracker
    tracker = OCSort(
        det_thresh=0.45,
        iou_threshold=0.2,
        use_byte=False 
    )
    for frame_idx, (path, imgs, vid_cap, s) in enumerate(dataset):
        for img in imgs:
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
                        id = output[4]
                        cls = output[5]
                        label = f'{int(id)} {name} {conf:.2f}'
                        annotator.mask_label(bbox, label, color=tuple(COLORS[int(id)]))
            else:
                print('No detections')
            
            # Write to the video
            im0 = annotator.result()
            if vid_path is None:  # new video
                vid_path = args.save_path
                if vid_cap:  # video
                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                    w = im0.shape[1]
                    h = im0.shape[0]
                else:  # stream
                    fps, w, h = 30, im0.shape[1], im0.shape[0]
                vid_writer = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
            im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
            vid_writer.write(im0)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--source',
        help='Source to a sample video for testing',
        required=False,
        default='TBF'
    )
    parser.add_argument(
        '--model',
        help='Path of the object detection model.',
        required=False,
        default='efficientdet_lite0.tflite')
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, type=int, default=0)
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480)
    parser.add_argument(
        '--numThreads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4)
    parser.add_argument(
        '--enableEdgeTPU',
        help='Whether to run the model on EdgeTPU.',
        action='store_true',
        required=False,
        default=False)
    parser.add_argument(
        '--stride',
        help='Stride when processing the video',
        required=False,
        type=int,
        default=1
    )
    parser.add_argument(
        '--batchsize',
        help='Batchsize when processing the video',
        required=False,
        type=int,
        default=8
    )
    parser.add_argument(
        '--save-path',
        help='Path to save the video',
        required=False,
        default='output.mp4'
    )
    args = parser.parse_args()
    run(args)


if __name__ == '__main__':
    main()

 