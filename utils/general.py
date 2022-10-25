
def detection2xyxy(detection_result):
    xywhs = []
    for detection in detection_result.detections:
        bbox = detection.bounding_box
        xywhs.append([bbox.origin_x, bbox.origin_y, bbox.width+bbox.origin_x, bbox.height+bbox.origin_y])
    return xywhs

def detection2confs(detection_result):
    confs = []
    for detection in detection_result.detections:
        category = detection.categories[0]
        confs.append(category.score)
    return confs

def detection2clss(detection_result):
    clss = []
    for detection in detection_result.detections:
        category = detection.categories[0]
        print(category)
        pass
    return clss

def detection2names(detection_result):
    names = []
    for detection in detection_result.detections:
        category = detection.categories[0]
        names.append(category.category_name)
    return names