from pymediainfo import MediaInfo

from app.models import Token


def getData(data):
    return {
        "message": "done",
        "data": data,
        "status": 1
    }


def getError(msg):
    return {
        "message": msg,
        "data": [],
        "status": 0
    }


def isLogin(token):
    try:
        tokenModel = Token.objects.get(token=token)
        if len(tokenModel.token) == 100:
            return True
        else:
            return False
    except:
        return False


def isVideo(video):
    fileInfo = MediaInfo.parse(video)
    for track in fileInfo.tracks:
        if track.track_type == "Video":
            return True
    return False


def isImage(image):
    fileInfo = MediaInfo.parse(image)
    for track in fileInfo.tracks:
        if track.track_type == "Image":
            return True
    return False
