import os
import cv2

VIDEO_FOLDER = "storage/videos"
VIDEO_PHOTO_FOLDER = "storage/videophotos"


def getVideoPhoto(filename, outputDir):
    video = VIDEO_FOLDER + '/' + filename
    videoCapture = cv2.VideoCapture(video)
    success, image = videoCapture.read()
    splittedFilename = filename.split(".")
    del splittedFilename[len(splittedFilename) - 1]
    imageName = '.'.join([str(element) for element in splittedFilename])
    cv2.imwrite(os.path.join(outputDir, '%s.png') % imageName, image)

    cv2.destroyAllWindows()
    videoCapture.release()
