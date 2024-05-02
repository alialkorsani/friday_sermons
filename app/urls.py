from django.urls import path

from app.views import News, Lectures, FridaySermons, Login, NewEdit, NewAdd, NewDelete, LectureAdd, LectureEdit, \
    LectureDelete, FridaySermonAdd, FridaySermonEdit, FridaySermonDelete, NewsSearch, FridaySermonsSearch, \
    LecturesSearch, Images, Statuses, Books, BooksLast, BooksSearch, Live, Helps, HelpsSearch, AidsCharts, AddView, \
    StatsAdd, StatsEdit, StatsDelete, Stats

urlpatterns = [
    path("login", Login),

    path("news", News),
    path("news_search", NewsSearch),
    # path("new_edit", NewEdit),
    # path("new_add", NewAdd),
    # path("new_delete", NewDelete),

    path("helps", Helps),
    path("helps_search", HelpsSearch),

    path("lectures", Lectures),
    path("lectures_search", LecturesSearch),
    # path("lecture_add", LectureAdd),
    # path("lecture_edit", LectureEdit),
    # path("lecture_delete", LectureDelete),

    path("friday_sermons", FridaySermons),
    path("friday_sermons_search", FridaySermonsSearch),
    # path("friday_sermon_add", FridaySermonAdd),
    # path("friday_sermon_edit", FridaySermonEdit),
    # path("friday_sermon_delete", FridaySermonDelete),

    path("images", Images),

    path("statuses", Statuses),

    path("books", Books),
    path("books_last", BooksLast),
    path("books_search", BooksSearch),

    path("live", Live),
    path("aids_charts", AidsCharts),
    path("add_view", AddView),

    path("stats", Stats),

]
