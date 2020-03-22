from django.urls import path, re_path
from django.conf.urls import include
from .views import home_view, signup_view, activate, activation_sent_view, NoteList, NewNoteView, change_pinned, NoteDelete, detail_view, edit_view
from django.conf.urls.static import static


app_name = 'notes'

urlpatterns = [
	path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('sent/', activation_sent_view, name="activation_sent"),
    re_path(r'^activate/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', activate, name='activate'),
    re_path(r'^note_list_api/(?P<user_id>.+)/$', NoteList.as_view(), name = 'note_list_api'),
    path('create/', NewNoteView.as_view(), name="create-note"),
	re_path(r'^change_pin/(?P<id>\d+)/$', change_pinned, name="change_pin"),
	re_path(r'^delete/(?P<id>\d+)/$', NoteDelete.as_view(), name="delete-note"),
    re_path(r'^detail/(?P<id>\d+)/$', detail_view, name="detail"),
    re_path(r'^edit/(?P<id>\d+)/$', edit_view, name="edit"),
	]


