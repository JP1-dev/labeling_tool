import cv2 as cv


def rescale(path, scale=0.9):
    frame= cv.imread(path)
    height= int(frame.shape[0] * scale)
    width= int(frame.shape[1] * scale)
    dimensions= (width, height)
    frame= cv.resize(frame, dimensions, interpolation= cv.INTER_AREA)
    cv.imwrite(path, frame)
    return True


