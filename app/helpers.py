import os

from django.core.paginator import Paginator
from django.forms import model_to_dict

from app.tools import getData, getError, isLogin, isImage, isVideo
from friday_sermon.settings import BASE_DIR


def getDataWithFiles(model, request):
    """page number should add to the request as parameter (ex: page=1)"""
    page = request.GET.get("page")
    per_page = request.GET.get("per_page")
    items = model.objects.all().order_by('-created_at')
    if per_page is None:
        per_page = 5
    items = Paginator(items, per_page)
    if page is None:
        page = 1
    try:
        items = items.page(page)
    except:
        return getError("all list shown")
    data = []
    for i in range(0, len(items)):
        modelItem = model_to_dict(items[i])
        #modelItem["created_at"] = items[i].created_at.timestamp()
        # strftime("%Y/%m/%d %I:%M %p")
        data.append(modelItem)
        data[i]["files"] = list(items[i].files.all().values())
    return getData(data)


def getLastDataWithFiles(model, request):
    """page number should add to the request as parameter (ex: page=1)"""

    items = model.objects.all().order_by('-created_at')
    per_page = 7
    items = Paginator(items, per_page)
    page = 1
    try:
        items = items.page(page)
    except:
        return getError("all list shown")
    data = []
    for i in range(0, len(items)):
        modelItem = model_to_dict(items[i])
        modelItem["created_at"] = items[i].created_at.timestamp()
        # strftime("%Y/%m/%d %I:%M %p")
        data.append(modelItem)
        data[i]["files"] = list(items[i].files.all().values())
    return getData(data)


def getDataWithFilesHasDeleted(model, request):
    """page number should add to the request as parameter (ex: page=1)"""
    page = request.GET.get("page")
    per_page = request.GET.get("per_page")
    items = model.objects.filter(deleted=False).order_by('-created_at')
    if per_page is None:
        per_page = 5
    items = Paginator(items, per_page)
    if page is None:
        page = 1
    try:
        items = items.page(page)
    except:
        return getError("all list shown")
    data = []
    for i in range(0, len(items)):
        modelItem = model_to_dict(items[i])
        modelItem["created_at"] = items[i].created_at.timestamp()
        # strftime("%Y/%m/%d %I:%M %p")
        data.append(modelItem)
        data[i]["files"] = list(items[i].files.all().values())
    return getData(data)


def searchInDataWithFiles(model, request, query):
    """page number should add to the request as parameter (ex: page=1)"""
    page = request.GET.get("page")
    per_page = request.GET.get("per_page")
    items = model.objects.filter(query).order_by('-created_at')

    if per_page is None:
        per_page = 5
    items = Paginator(items, per_page)
    if page is None:
        page = 1
    try:
        items = items.page(page)
    except:
        return getError("all list shown")
    data = []
    for i in range(0, len(items)):
        modelItem = model_to_dict(items[i])
        modelItem["created_at"] = items[i].created_at.timestamp()
        # strftime("%Y/%m/%d %I:%M %p")
        data.append(modelItem)
        data[i]["files"] = list(items[i].files.all().values())
    return getData(data)


def editDataWithImages(model, ImageModel, request, **params):
    """
    Only Post Request Working
    You should add r_ in first of required params
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(params.get("token")):
        return {"data": getError("You should login first"), "status": 401}
    itemId = params.get("r_id")
    if itemId is None:
        return {"data": getError("id field is required"), "status": 400}
    try:
        item = model.objects.get(id=itemId).order_by('-created_at')
    except:
        return {"data": getError("Not found item"), "status": 400}

    for key, value in params.items():

        if "r_" in key and value is None:
            key = key.split("_")[1]
            return {"data": getError(key + " is required field"), "status": 400}
        if "r_" in key:
            key = key.split("_")[1]
        setattr(item, key, value)
    i = 1
    isLast = 0
    try:
        while True:
            imageId = request.POST.get("edit_image_id_" + str(i))
            if not imageId is None:
                file = item.files.get(id=imageId)
                try:
                    image = request.FILES["edit_image_" + str(imageId)]
                    if not isImage(image):
                        return {"data": getError("you should use image file in edit_image_Id field"), "status": 400}
                    path = BASE_DIR.joinpath("media\\" + file.image.name)
                    os.remove(path)
                    file.image = image
                    file.save()
                except:
                    file.delete()
            else:
                isLast += 1
            try:
                newImage = request.FILES["new_image_" + str(i)]
                if not isImage(newImage):
                    return {"data": getError("you should use image file in new_image_Index field"), "status": 400}

                if not newImage is None:
                    nImage = ImageModel(
                        image=newImage,
                        Item_id=item.pk
                    )
                    nImage.save()
                    item.files.add(nImage)
            except:
                isLast += 1
                pass
            if isLast >= 2:
                break
            i += 1

        item.save()
        return {"data": getData(None), "status": 200}
    except:
        return {"data": getError("error"), "status": 400}


def addDataWithImages(model, ImageModel, request, **params):
    """
    Only Post Request Working
    You should add r_ in first of required params
    ImageModel should contain image field and item field
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(params.get("token")):
        return {"data": getError("You should login first"), "status": 401}

    try:
        item = model.objects.create()
    except:
        return {"data": getError("Not found item"), "status": 400}

    for key, value in params.items():

        if "r_" in key and value is None:
            key = key.split("_")[1]
            return {"data": getError(key + " is required field"), "status": 400}
        if "r_" in key:
            key = key.split("_")[1]
        setattr(item, key, value)
    i = 1
    try:
        while True:
            try:
                newImage = request.FILES["image_" + str(i)]
                if not isImage(newImage):
                    return {"data": getError("you should use image file in image field"), "status": 400}
                if not newImage is None:
                    nImage = ImageModel(
                        image=newImage,
                        item_id=item.pk
                    )
                    nImage.save()
                    print("nImage")
                    print(nImage)
                    item.files.add(nImage)
            except:
                break
            i += 1

        item.save()
        return {"data": getData({"id": item.id}), "status": 200}
    except:
        return {"data": getError("error"), "status": 400}


def deleteDataWithImages(model, request):
    """
    Only Post Request Working
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(request.POST.get("token")):
        return {"data": getError("You should login first"), "status": 401}
    itemId = request.POST.get("id")
    if itemId is None:
        return {"data": getError("id field is required"), "status": 400}
    try:
        item = model.objects.get(id=itemId)
    except:
        return {"data": getError("Not found item"), "status": 400}
    for rItem in item.files.all():
        path = BASE_DIR.joinpath("media\\" + rItem.image.name)
        os.remove(path)
    item.delete()
    return {"data": getData(None), "status": 200}


def addDataWithImageAndVideo(model, ImageVideoModel, request, **params):
    """
    Only Post Request Working
    You should add r_ in first of required params
    ImageVideoModel should contain image field and item field
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(params.get("token")):
        return {"data": getError("You should login first"), "status": 401}

    try:
        item = model.objects.create()
    except:
        return {"data": getError("Not found item"), "status": 400}

    for key, value in params.items():

        if "r_" in key and value is None:
            key = key.split("_")[1]
            return {"data": getError(key + " is required field"), "status": 400}
        if "r_" in key:
            key = key.split("_")[1]
        setattr(item, key, value)
    try:
        newImage = request.FILES["image"]
        newVideo = request.FILES["video"]
        if not isImage(newImage):
            return {"data": getError("you should use image file in image field"), "status": 400}
        if not isVideo(newVideo):
            return {"data": getError("you should use video file in video field"), "status": 400}
        if newImage is not None and newVideo is not None:
            nImage = ImageVideoModel(
                image=newImage,
                video=newVideo,
                item_id=item.pk
            )
            nImage.save()
            item.files.add(nImage)
    except:
        return {"data": getError("image field and video field is required"), "status": 400}
    item.save()

    return {"data": getData({"id": item.id}), "status": 200}


def editDataWithImageAndVideo(model, request, **params):
    """
    Only Post Request Working
    You should add r_ in first of required params
    ImageVideoModel should contain image field and item field
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(params.get("token")):
        return {"data": getError("You should login first"), "status": 401}

    itemId = params.get("r_id")
    if itemId is None:
        return {"data": getError("id field is required"), "status": 400}
    try:
        item = model.objects.get(id=itemId)
    except:
        return {"data": getError("Not found item"), "status": 400}

    for key, value in params.items():

        if "r_" in key and value is None:
            key = key.split("_")[1]
            return {"data": getError(key + " is required field"), "status": 400}
        if "r_" in key:
            key = key.split("_")[1]
        setattr(item, key, value)
    try:
        newImage = request.FILES["image"]
        newVideo = request.FILES["video"]
        if not isImage(newImage):
            return {"data": getError("you should use image file in image field"), "status": 400}
        if not isVideo(newVideo):
            return {"data": getError("you should use video file in video field"), "status": 400}
        if newImage is not None and newVideo is not None:
            nImage = item.files.first()
            path = BASE_DIR.joinpath("media\\" + nImage.image.name)
            os.remove(path)
            path = BASE_DIR.joinpath("media\\" + nImage.video.name)
            os.remove(path)
            nImage.image = newImage
            nImage.video = newVideo
            nImage.save()

    except:
        return {"data": getError("image field and video field is required"), "status": 400}
    item.save()

    return {"data": getData([]), "status": 200}


def deleteDataWithImageAndVideo(model, request):
    """
    Only Post Request Working
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(request.POST.get("token")):
        return {"data": getError("You should login first"), "status": 401}
    itemId = request.POST.get("id")
    if itemId is None:
        return {"data": getError("id field is required"), "status": 400}
    try:
        item = model.objects.get(id=itemId)
    except:
        return {"data": getError("Not found item"), "status": 400}
    for rItem in item.files.all():
        path = BASE_DIR.joinpath("media\\" + rItem.image.name)
        os.remove(path)
        path = BASE_DIR.joinpath("media\\" + rItem.video.name)
        os.remove(path)
    item.delete()
    return {"data": getData(None), "status": 200}


def addDataWithImageAndTwoVideos(model, ImageVideoModel, request, **params):
    """
    Only Post Request Working
    You should add r_ in first of required params
    ImageVideoModel should contain image field, item field, video_1 field and video_2 field
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(params.get("token")):
        return {"data": getError("You should login first"), "status": 401}

    try:
        item = model.objects.create()
    except:
        return {"data": getError("Not found item"), "status": 400}

    for key, value in params.items():

        if "r_" in key and value is None:
            try:
                key = key.split("_")[1] + "_" + key.split("_")[2]
            except:
                key = key.split("_")[1]
            return {"data": getError(key + " is required field"), "status": 400}
        if "r_" in key:
            try:
                key = key.split("_")[1] + "_" + key.split("_")[2]
            except:
                key = key.split("_")[1]
        setattr(item, key, value)
    try:
        newImage = request.FILES["image"]
        newVideo_1 = request.FILES["video_1"]
        newVideo_2 = request.FILES["video_2"]

        if not isImage(newImage):
            return {"data": getError("you should use image file in image field"), "status": 400}
        if not isVideo(newVideo_1):
            return {"data": getError("you should use video file in video_1 field"), "status": 400}
        if not isVideo(newVideo_2):
            return {"data": getError("you should use video file in video_2 field"), "status": 400}

        if newImage is not None and newVideo_1 is not None and newVideo_2 is not None:
            nImage = ImageVideoModel(
                image=newImage,
                video_1=newVideo_1,
                video_2=newVideo_2,
                item_id=item.pk
            )
            nImage.save()
            item.files.add(nImage)
    except:
        return {"data": getError("image field, video_1 field and video_2 field is required"), "status": 400}
    item.save()

    return {"data": getData({"id": item.id}), "status": 200}


def editDataWithImageAndTwoVideos(model, ImageVideoModel, request, **params):
    """
    Only Post Request Working
    You should add r_ in first of required params
    ImageVideoModel should contain image field, item field, video_1 field and video_2 field
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(params.get("token")):
        return {"data": getError("You should login first"), "status": 401}
    itemId = request.POST.get("id")
    if itemId is None:
        return {"data": getError("id field is required"), "status": 400}
    try:
        item = model.objects.get(id=itemId)
    except:
        return {"data": getError("Not found item"), "status": 400}

    for key, value in params.items():

        if "r_" in key and value is None:
            try:
                key = key.split("_")[1] + "_" + key.split("_")[2]
            except:
                key = key.split("_")[1]
            return {"data": getError(key + " is required field"), "status": 400}
        if "r_" in key:
            try:
                key = key.split("_")[1] + "_" + key.split("_")[2]
            except:
                key = key.split("_")[1]
        setattr(item, key, value)
    try:
        newImage = request.FILES["image"]
        newVideo_1 = request.FILES["video_1"]
        newVideo_2 = request.FILES["video_2"]

        if not isImage(newImage):
            return {"data": getError("you should use image file in image field"), "status": 400}
        if not isVideo(newVideo_1):
            return {"data": getError("you should use video file in video_1 field"), "status": 400}
        if not isVideo(newVideo_2):
            return {"data": getError("you should use video file in video_2 field"), "status": 400}

        if newImage is not None and newVideo_1 is not None and newVideo_2 is not None:
            nImage = ImageVideoModel(
                image=newImage,
                video_1=newVideo_1,
                video_2=newVideo_2,
                item_id=item.pk
            )
            nImage.save()
            item.files.add(nImage)
    except:
        return {"data": getError("image field, video_1 field and video_2 field is required"), "status": 400}
    item.save()

    return {"data": getData([]), "status": 200}


def deleteDataWithImageAndTwoVideos(model, request):
    """
    Only Post Request Working
    Related files should contain image field, item field, video_1 field and video_2 field
    """
    if request.method != 'POST':
        return {"data": getError("Only POST Working"), "status": 400}
    if not isLogin(request.POST.get("token")):
        return {"data": getError("You should login first"), "status": 401}
    itemId = request.POST.get("id")
    if itemId is None:
        return {"data": getError("id field is required"), "status": 400}
    try:
        item = model.objects.get(id=itemId)
    except:
        return {"data": getError("Not found item"), "status": 400}
    for rItem in item.files.all():
        path = BASE_DIR.joinpath("media\\" + rItem.image.name)
        os.remove(path)
        path = BASE_DIR.joinpath("media\\" + rItem.video_1.name)
        os.remove(path)
        path = BASE_DIR.joinpath("media\\" + rItem.video_2.name)
        os.remove(path)
    item.delete()
    return {"data": getData(None), "status": 200}


def getImages(model, request):
    """page number should add to the request as parameter (ex: page=1)"""
    page = request.GET.get("page")
    per_page = request.GET.get("per_page")
    items = model.objects.all().order_by('-created_at')
    if per_page is None:
        per_page = 5
    items = Paginator(items, per_page)
    if page is None:
        page = 1
    try:
        items = items.page(page)
    except:
        return getError("all list shown")
    data = []
    for i in range(0, len(items)):
        data.append({"title": items[i].title, "image": items[i].image.name})
    return getData(data)
