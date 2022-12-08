from base64 import b64encode
from PIL import Image
from typing import Optional

from routes.routeutil.FileUtils import videoAllowedFile


class GImage:

    @staticmethod
    def decodeBase64FromPathWithExtension(imageName: Optional[str]):
        photoPath = "photos"
        splittedImageName = imageName.split(".")
        if videoAllowedFile(imageName):
            photoPath = "videophotos"
            splittedImageName[len(splittedImageName) - 1] = "png"

        imageName = '.'.join([str(element) for element in splittedImageName])

        with open(f"storage/{photoPath}/{imageName}", "rb") as imageFile:
            return {"extension": splittedImageName[len(splittedImageName) - 1], "src": b64encode(imageFile.read()).decode()}

    @staticmethod
    def decodeBase64FromPath(imageName):
        with open(f"storage/photos/{imageName}", "rb") as imageFile:
            return b64encode(imageFile.read()).decode()
