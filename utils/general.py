import numpy as np
def detection2xyxy(detection_result):
    xywhs = []
    for detection in detection_result.detections:
        bbox = detection.bounding_box
        xywhs.append([bbox.origin_x, bbox.origin_y, bbox.width+bbox.origin_x, bbox.height+bbox.origin_y])
    return np.array(xywhs)

def detection2confs(detection_result):
    confs = []
    for detection in detection_result.detections:
        category = detection.categories[0]
        confs.append(category.score)
    return np.array(confs)

def detection2clss(detection_result):
    clss = []
    for detection in detection_result.detections:
        category = detection.categories[0]
        clss.append(category.index)
    return np.array(clss)

def detection2names(detection_result):
    names = []
    for detection in detection_result.detections:
        category = detection.categories[0]
        names.append(category.category_name)
    return np.array(names)