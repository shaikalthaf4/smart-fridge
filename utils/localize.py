import cv2
import argparse

def get_bounding_box(img, threshold=30):
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


def localize(img, threshold, levels):
    '''
    localize:
        Given the image of the fridge and food, determine the level of the food
    '''
    blocked = [True for i in range(len(levels))] # whether each level is blocked
    bbox, center = get_bounding_box(img, threshold)
    for box, c in zip(bbox, center):
        # Find the level that the current box corresponds to
        min_dist = float('inf')
        min_idx = -1
        for i, lvl in enumerate(levels):
            if abs(c[1]-lvl) < min_dist:
                min_dist = abs(c[1]-lvl)
                min_idx = i
        # Set the level to unblocked if the box width is large enough
        if (box[1][0]-box[0][0] >= 0.6*img.shape[1]):
            blocked[min_idx] = False
    for i in range(len(blocked)):
        if blocked[i] == True:
            return i
    return -1

# Test code for finding suitable threshold
if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--grey-thresh', help='Threshold for gray scale to do the landmark-based(LB)-localization', required=False, type=int, default=30)
    parser.add_argument('--level', type=int, help="number of levels of your fridge", required=False, default=3)
    args = parser.parse_args()
    vid_capture = cv2.VideoCapture(0)
    y_coord = [0 for _ in range(args.level)]
    y_count = [0 for _ in range(args.level)]
    while(vid_capture.isOpened()):
        ret, frame = vid_capture.read()
        if frame is None:
            break
        bbox, center = get_bounding_box(frame, threshold=args.grey_thresh)
        y_center = [center[i][1] for i in range(len(center))]
        y_center.sort()
        for i in range(len(y_center)):
            y_coord[i] += y_center[i]
            y_count[i] += 1
        for box in bbox:
            frame = cv2.rectangle(frame, box[0], box[1], (0, 0, 255), 5)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid_capture.release()
    cv2.destroyAllWindows()
    y = [int(y_coord[i]/y_count[i]) for i in range(args.level)]
    print(f'Suggested level values are {y}')
