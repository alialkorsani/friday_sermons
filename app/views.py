import random
import string

from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum
from .helpers import getDataWithFiles, getData, getError, addDataWithImages, editDataWithImages, \
    deleteDataWithImages, addDataWithImageAndVideo, editDataWithImageAndVideo, deleteDataWithImageAndVideo, \
    addDataWithImageAndTwoVideos, editDataWithImageAndTwoVideos, deleteDataWithImageAndTwoVideos, searchInDataWithFiles, \
    getImages, getDataWithFilesHasDeleted, getLastDataWithFiles
from .models import New, Lecture, FridaySermon, Token, NewImage, LectureVideo, FridaySermonVideo, Image, Status, Book, \
    Live as LiveModel, Help, HELPS_TYPES, Views, Stat
from .tools import isLogin


def Login(request):
    """
    URL: http://127.0.0.1:8000/api/login
    desc: login to get admin previlage
    params:
        username: String=> admin username
        password: String=> admin password
    """
    username = request.GET.get("username")
    password = request.GET.get("password")
    user = User.objects.get(username=username)
    user.check_password(password)
    if  user.check_password(password):
        return JsonResponse(getError("not authenticated"), status=401)

    try:
        auth = user.auth
    except:
        auth = Token(
            token=''.join(random.choices(string.digits + string.ascii_letters, k=100)),
            user_id=user
        )
        auth.save()

    return JsonResponse(getData(auth.token))


def News(request):
    """
    URL: http://127.0.0.1:8000/api/news
    desc: getting all news
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    return JsonResponse(getDataWithFiles(New, request))


def NewsSearch(request):
    """
    URL: http://127.0.0.1:8000/api/news_search
    desc: search in news
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    search_text = request.GET.get("search_text")
    if search_text is None or search_text == "":
        return JsonResponse(getDataWithFiles(New, request))
    return JsonResponse(
        searchInDataWithFiles(
            New,
            request,
            Q(**{'title__icontains': search_text}) | Q(**{'desc__icontains': search_text})
        )
    )


def NewEdit(request):
    """
    URL: http://127.0.0.1:8000/api/new_edit
    desc: edit news
    note: only post working
    form data:
        token:! String=> to be authurized
        id:! Number=> id of new
        title:! String=> Title of new
        desc:! String=> Description of new
        edit_image_id_Index: Intger=> id of image, Index=> number start from 1 represent to number of edited image
        edit_image_Id: File=> replaced image file, Id=> id of image want to replace
        new_image_Index: File=> new image file, Index=> number start from 1 represent to number of newed image
    """
    return JsonResponse(
        **editDataWithImages(
            New, NewImage, request, r_id=request.POST.get("id"), r_title=request.POST.get("title"),
            r_desc=request.POST.get("desc"), token=request.POST.get("token")
        )
    )


def NewAdd(request):
    """
    URL: http://127.0.0.1:8000/api/new_add
    desc: edit news
    note: only post working
    form data:
        token:! String=> to be authurized
        title:! String=> Title of new
        desc:! String=> Description of new
        image_Index: File=> new image file, Index=> number start from 1 represent to number of newed image
    """
    return JsonResponse(
        **addDataWithImages(
            New, NewImage, request, r_title=request.POST.get("title"),
            r_desc=request.POST.get("desc"), token=request.POST.get("token")
        )
    )


def NewDelete(request):
    """
    URL: http://127.0.0.1:8000/api/new_delete
    desc: delete news
    note: only post working
    form data:
        token:! String=> to be authurized
        id:! Number=> id of new
    """
    return JsonResponse(
        **deleteDataWithImages(
            New, request
        )
    )


def Helps(request):
    """
    URL: http://127.0.0.1:8000/api/helps
    desc: getting all helps
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of helps per page
            default: 5
    """
    data = getDataWithFiles(Help, request)

    for item in data['data']:
        item['title'] = item['desc']
        item['files'] = [{'image': 'abdel-mahdi.jpg'}]
    return JsonResponse(data)


def HelpsSearch(request):
    """
    URL: http://127.0.0.1:8000/api/helps_search
    desc: search in helps
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of helps per page
            default: 5
    """
    search_text = request.GET.get("search_text")
    data = []
    if search_text is None or search_text == "":
        data = getDataWithFiles(Help, request)
    else:
        data = searchInDataWithFiles(
            Help,
            request,
            Q(**{'title__icontains': search_text}) | Q(**{'desc__icontains': search_text})
        )
    for item in data.data:
        item['title'] = item['desc']
        item['files'] = [{'image': 'abdel-mahdi.jpg'}]
    return JsonResponse(data)


def Lectures(request):
    """
    URL: http://127.0.0.1:8000/api/lectures
    desc: getting all lectures
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    return JsonResponse(getDataWithFiles(Lecture, request))


def LecturesSearch(request):
    """
    URL: http://127.0.0.1:8000/api/lectures_search
    desc: search in lectures
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    search_text = request.GET.get("search_text")
    if search_text is None or search_text == "":
        return JsonResponse(getDataWithFiles(Lecture, request))
    return JsonResponse(
        searchInDataWithFiles(
            Lecture,
            request,
            Q(**{'title__icontains': search_text}) | Q(**{'desc__icontains': search_text})
        )
    )


def LectureAdd(request):
    """
    URL: http://127.0.0.1:8000/api/lecture_add
    desc: edit lectures
    note: only post working
    form data:
        token:! String=> to be authurized
        title:! String=> Title of new
        desc:! String=> Description of new
        image: File=> new image file
        video: File=> new video file
    """
    return JsonResponse(
        **addDataWithImageAndVideo(
            Lecture, LectureVideo, request, r_title=request.POST.get("title"),
            r_desc=request.POST.get("desc"), token=request.POST.get("token")
        )
    )


def LectureEdit(request):
    """
    URL: http://127.0.0.1:8000/api/lecture_edit
    desc: edit lectures
    note: only post working
    form data:
        id:! Number=> id of lecture
        token:! String=> to be authurized
        title:! String=> Title of new
        desc:! String=> Description of new
        image: File=> new image file
        video: File=> new video file
    """
    return JsonResponse(
        **editDataWithImageAndVideo(
            Lecture, request, r_id=request.POST.get("id"), r_title=request.POST.get("title"),
            r_desc=request.POST.get("desc"), token=request.POST.get("token"),
        )
    )


def LectureDelete(request):
    """
    URL: http://127.0.0.1:8000/api/lecture_delete
    desc: delete lecture
    note: only post working
    form data:
        token:! String=> to be authurized
        id:! Number=> id of new
    """
    return JsonResponse(
        **deleteDataWithImageAndVideo(
            Lecture, request
        )
    )


def FridaySermons(request):
    """
    URL: http://127.0.0.1:8000/api/friday_sermons
    desc: search in friday sermons
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    return JsonResponse(getDataWithFiles(FridaySermon, request))


def FridaySermonsSearch(request):
    """
    URL: http://127.0.0.1:8000/api/friday_sermons_search
    desc: search in friday sermons
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    search_text = request.GET.get("search_text")
    if search_text is None or search_text == "":
        return JsonResponse(getDataWithFiles(FridaySermon, request))
    return JsonResponse(
        searchInDataWithFiles(
            FridaySermon,
            request,
            Q(**{'title__icontains': search_text}) | Q(**{'desc__icontains': search_text}) |
            Q(**{'title_1__icontains': search_text}) | Q(**{'title_2__icontains': search_text}) |
            Q(**{'desc_1__icontains': search_text}) | Q(**{'desc_2__icontains': search_text})
        )
    )


def FridaySermonAdd(request):
    """
    URL: http://127.0.0.1:8000/api/friday_sermon_add
    desc: edit lectures
    note: only post working
    form data:
        token:! String=> to be authurized
        title_1:! String=> Title of first sermon
        title_2:! String=> Title of second sermon
        desc_1:! String=> Description of first sermon
        desc_2:! String=> Description of second sermon
        image: File=> sermon image file
        video_1: File=> new video file of first sermon
        video_2: File=> new video file of second sermon
    """
    return JsonResponse(
        **addDataWithImageAndTwoVideos(
            FridaySermon, FridaySermonVideo, request, r_title_1=request.POST.get("title_1"),
            r_title=request.POST.get("title"), r_desc=request.POST.get("desc"),
            r_title_2=request.POST.get("title_2"), r_desc_1=request.POST.get("desc_1"),
            r_desc_2=request.POST.get("desc_2"), token=request.POST.get("token")
        )
    )


def FridaySermonEdit(request):
    """
    URL: http://127.0.0.1:8000/api/friday_sermon_edit
    desc: edit lectures
    note: only post working
    form data:
        token:! String=> to be authurized
        id:! Intger=> id of sermon
        title_1:! String=> Title of first sermon
        title_2:! String=> Title of second sermon
        desc_1:! String=> Description of first sermon
        desc_2:! String=> Description of second sermon
        image: File=> sermon image file
        video_1: File=> new video file of first sermon
        video_2: File=> new video file of second sermon
    """
    return JsonResponse(
        **editDataWithImageAndTwoVideos(
            FridaySermon, FridaySermonVideo, request, r_title_1=request.POST.get("title_1"),
            r_title=request.POST.get("title"), r_desc=request.POST.get("desc"),
            r_title_2=request.POST.get("title_2"), r_desc_1=request.POST.get("desc_1"),
            r_desc_2=request.POST.get("desc_2"), token=request.POST.get("token")
        )
    )


def FridaySermonDelete(request):
    """
    URL: http://127.0.0.1:8000/api/friday_sermon_delete
    desc: delete Sermon
    note: only post working
    form data:
        token:! String=> to be authurized
        id:! Number=> id of new
    """
    return JsonResponse(
        **deleteDataWithImageAndTwoVideos(
            FridaySermon, request
        )
    )


def Images(request):
    """
    URL: http://127.0.0.1:8000/api/images
    desc: getting all images
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    return JsonResponse(getImages(Image, request))


def Statuses(request):
    """
    URL: http://127.0.0.1:8000/api/statuses
    desc: getting all images
    note: when using status you should run command repeatedly to clear old statuses
    """
    return JsonResponse(getDataWithFilesHasDeleted(Status, request))


def Books(request):
    """
    URL: http://127.0.0.1:8000/api/books
    desc: getting all books
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    return JsonResponse(getDataWithFiles(Book, request))


def BooksLast(request):
    """
    URL: http://127.0.0.1:8000/api/books_last
    desc: getting last 7 books added
    """
    return JsonResponse(getLastDataWithFiles(Book, request))


def BooksSearch(request):
    """
    URL: http://127.0.0.1:8000/api/books_search
    desc: search in books
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    search_text = request.GET.get("search_text")
    if search_text is None or search_text == "":
        return JsonResponse(getDataWithFiles(Book, request))
    return JsonResponse(
        searchInDataWithFiles(
            Book,
            request,
            Q(**{'title__icontains': search_text}) | Q(**{'desc__icontains': search_text}) | Q(
                **{'author__icontains': search_text})
        )
    )


def Live(request):
    """
    URL: http://127.0.0.1:8000/api/live
    desc: getting Live stream
    """
    data = LiveModel.objects.last()
    if data is not None:
        data = model_to_dict(data)
    else:
        data = {}
    return JsonResponse(getData(data))


def AddView(request):
    """
    URL: http://127.0.0.1:8000/api/add_view
    desc: a model (help, news, etc) has viewed
    """
    view = Views(type=request.GET['type'], model_id=request.GET['id'])
    view.save()
    return JsonResponse(
        {"data": None, "status": 200}
    )


def Stats(request):
    """
    URL: http://127.0.0.1:8000/api/lectures
    desc: getting all lectures
    params:
        page: Number=> number of page
            default: 1
        per_page: Number=> number of news per page
            default: 5
    """
    data = Stat.objects.last()
    if data is not None:
        data = model_to_dict(data)
    else:
        data = {}
    return JsonResponse(getData(data))


def StatsAdd(request):
    """
    URL: http://127.0.0.1:8000/api/lecture_add
    desc: edit lectures
    note: only post working
    form data:
        token:! String=> to be authurized
        title:! String=> Title of new
        desc:! String=> Description of new
        image: File=> new image file
        video: File=> new video file
    """
    if request.method != 'POST':
        return JsonResponse({"data": getError("Only POST Working"), "status": 400})
    if not isLogin(request.POST.get("token")):
        return JsonResponse({"data": getError("You should login first"), "status": 401})
    try:
        item = Stat.objects.create()
    except:
        return JsonResponse({"data": getError("Not found item"), "status": 400})

    setattr(item, 'key', request.POST.get("key"))
    setattr(item, 'label', request.POST.get("label"))
    setattr(item, 'value', request.POST.get("value"))
    item.save()
    return JsonResponse(
        {"data": getData({"id": item.id}), "status": 200}
    )


def StatsEdit(request):
    """
    URL: http://127.0.0.1:8000/api/lecture_edit
    desc: edit lectures
    note: only post working
    form data:
        id:! Number=> id of lecture
        token:! String=> to be authurized
        title:! String=> Title of new
        desc:! String=> Description of new
        image: File=> new image file
        video: File=> new video file
    """
    itemId = request.POST.get("r_id")
    if itemId is None:
        return JsonResponse({"data": getError("id field is required"), "status": 400})
    try:
        item = Stat.objects.get(id=itemId)
    except:
        return JsonResponse({"data": getError("Not found item"), "status": 400})

    setattr(item, 'key', request.POST.get("key"))
    setattr(item, 'label', request.POST.get("label"))
    setattr(item, 'value', request.POST.get("value"))
    item.save()
    return JsonResponse(
        {"data": getData([]), "status": 200}
    )


def StatsDelete(request):
    """
    URL: http://127.0.0.1:8000/api/lecture_delete
    desc: delete lecture
    note: only post working
    form data:
        token:! String=> to be authurized
        id:! Number=> id of new
    """
    if request.method != 'POST':
        return JsonResponse({"data": getError("Only POST Working"), "status": 400})
    if not isLogin(request.POST.get("token")):
        return JsonResponse({"data": getError("You should login first"), "status": 401})
    itemId = request.POST.get("id")
    if itemId is None:
        return JsonResponse({"data": getError("id field is required"), "status": 400})
    try:
        item = Stat.objects.get(id=itemId)
    except:
        return JsonResponse({"data": getError("Not found item"), "status": 400})

    item.delete()
    return JsonResponse(
        {"data": getData(None), "status": 200}
    )


def AidsCharts(request):
    """
    URL: http://127.0.0.1:8000/api/aids_charts
    desc: getting Charts data
    params:
         days:! Intger=> period in days
         source:! String=> select help source
    """

    year = int(request.GET.get("year"))
    source = request.GET.get("source")

    items = Stat.objects.filter(source=source, year=year)

    data = []
    for i in range(0, len(items)):
        modelItem = model_to_dict(items[i])
        # modelItem["created_at"] = items[i].created_at.timestamp()
        # strftime("%Y/%m/%d %I:%M %p")
        data.append(modelItem)

    allC = {}
    allC["count"] = \
        Stat.objects.filter(source=source, year=year).aggregate(
            Sum('count'))[
            "count__sum"]
    allC["value"] = \
        Stat.objects.filter(source=source, year=year).aggregate(
            Sum('value'))[
            "value__sum"]

    return JsonResponse(getData({"allC": allC, "items": data}))
    helps = Stat.objects.all()
    days = 365
    if helps is None:
        return JsonResponse(getData({}))
    #days = int(request.GET.get("days"))
    source = request.GET.get("source")

    allC = {}
    allC["count"] = Help.objects.filter(source=source, created_at__gte=datetime.now() - timedelta(days=days)).count()
    allC["value"] = \
        Help.objects.filter(source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))[
            "value__sum"]
    MarriageC = {}
    MarriageC["count"] = Help.objects.filter(type="MG", source=source,
                                             created_at__gte=datetime.now() - timedelta(days=days)).count()
    MarriageC["value"] = \
        Help.objects.filter(type="MG", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]

    BuildingC = {}
    BuildingC["count"] = Help.objects.filter(type="B", source=source,
                                             created_at__gte=datetime.now() - timedelta(days=days)).count()
    BuildingC["value"] = \
        Help.objects.filter(type="B", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]

    DebtsC = {}
    DebtsC["count"] = Help.objects.filter(type="D", source=source,
                                          created_at__gte=datetime.now() - timedelta(days=days)).count()
    DebtsC["value"] = \
        Help.objects.filter(type="D", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]

    OtherC = {}
    OtherC["count"] = Help.objects.filter(type="O", source=source,
                                          created_at__gte=datetime.now() - timedelta(days=days)).count()
    OtherC["value"] = \
        Help.objects.filter(type="O", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]
    MedicalC = {}
    MedicalC["count"] = Help.objects.filter(type="MD", source=source,
                                            created_at__gte=datetime.now() - timedelta(days=days)).count()
    MedicalC["value"] = \
        Help.objects.filter(type="MD", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]
    ReductionC = {}
    ReductionC["count"] = Help.objects.filter(type="R", source=source,
                                              created_at__gte=datetime.now() - timedelta(days=days)).count()
    ReductionC["value"] = \
        Help.objects.filter(type="R", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]
    RentC = {}
    RentC["count"] = Help.objects.filter(type="P", source=source,
                                         created_at__gte=datetime.now() - timedelta(days=days)).count()
    RentC["value"] = \
        Help.objects.filter(type="P", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]

    FeedC = {}
    FeedC["count"] = Help.objects.filter(type="F", source=source,
                                         created_at__gte=datetime.now() - timedelta(days=days)).count()
    FeedC["value"] = \
        Help.objects.filter(type="F", source=source, created_at__gte=datetime.now() - timedelta(days=days)).aggregate(
            Sum('value'))["value__sum"]

    return JsonResponse(getData({
        "allC": allC,
        "MG": MarriageC,
        "B": BuildingC,
        "D": DebtsC,
        "O": OtherC,
        "MD": MedicalC,
        "R": ReductionC,
        "P": RentC,
        "F": FeedC
    }))
