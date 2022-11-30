import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_bounding_box(img, threshold=20):
    '''
    get_bounding_box:
		Given the image captured from the camera, return the wide bounding boxes for the three level landmarks.
    Input:
        img         np.ndarray          Image captured from the camera
    Outputs: 
        bbox        ((x1, y1),(x2, y2)) Coordinates of the upper-left and lower-right corners of the bounding boxes
        center      (xc, yc) Center of the bounding box
    '''
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_width = img_gray.shape[1]
    cv2.normalize(img_gray, img_gray, 0, 50, cv2.NORM_MINMAX, cv2.CV_8U)
#     img_gray = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY_INV)[1]
    img_gray = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Return all wide bounding boxes
    bbox, center = [], []
    if len(contours) > 0:
        boxes = [cv2.boundingRect(c) for c in contours]
        for box in boxes:
            x, y, w, h = box
            if w > 0.5 * img_width:
                bbox.append(((int(x), int(y)), (int(x+w), int(y+h))))
                center.append((int(x+w/2), int(y+h/2)))
    return bbox, center


def localize(img):
	return 1


# Test code for finding suitable threshold
vid_capture = cv2.VideoCapture(0)
while(vid_capture.isOpened()):
	ret, frame = vid_capture.read()
	bbox, center = get_bounding_box(frame, threshold=20)
	for box in bbox:
		frame = cv2.rectangle(frame, box[0], box[1], (0, 0, 255), 5)
		cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
vid_capture.release()
cv2.destroyAllWindows()
