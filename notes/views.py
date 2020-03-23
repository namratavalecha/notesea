from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework import serializers
from django.forms.models import modelformset_factory, inlineformset_factory
from .models import *
from rest_framework.generics import ListAPIView
from .serializers import NoteSerializer
from .forms import SignUpForm, NoteForm
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponse, Http404
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q



def home_view(request):
    return render(request, 'home.html')

def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('notes:home')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            print(user.profile.email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            context = {'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                }
            subject = 'Please Activate Your Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.profile.email]
            plain_text_content = render_to_string('activation_request.html', context)
            print(plain_text_content)
            # mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, plain_text_content= plain_text_content)
            try:
		send_mail(subject, plain_text_content, from_email, to_email)
            	# sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            	# response = sg.send(mail)
            	# print(response.status_code)
            	# print(response.body)
            	# print(response.headers)
            except Exception as e:
            	print(e.message)
            return redirect('notes:activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



class NoteList(ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return(Note.objects.filter(user = user_id))




class NewNoteView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        user = request.user
        user_ = User.objects.filter(id = user.id)
        if user_.exists():
            query = ""
            query = request.GET.get('q')
            if query:
                notes = get_note_queryset(user, str(query))
            else:
                notes = Note.objects.filter(user = user).order_by('-pinned', '-created')
            # print(notes)
            noteForm = NoteForm()
            return render(request, 'new_note.html', {'notes': notes, 'form': noteForm})
        else:
            return render(request, 'base.html')


    def post(self, request):
        noteForm = NoteForm(request.POST)

        if noteForm.is_valid():
            note_form = noteForm.save(commit=False)
            note_form.user = request.user
            note_form.save()
            return HttpResponseRedirect(reverse('notes:create-note'))

        else:
            print(noteForm.errors)
        return render(request, 'new_note.html', {'form': noteForm})



@api_view(['POST'])
def change_pinned(request, id):
    print(request.POST)
    note_id = request.POST.get('id')
    note_obj = Note.objects.filter(id=id)
    if note_obj.exists():
        if note_obj[0].pinned == True:
            Note.objects.filter(id=id).update(pinned = False)
        else:
            Note.objects.filter(id=id).update(pinned = True)
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'pinned changed'})
    else:
        return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'no note found'})


class NoteDelete(APIView):
    def get_object(self, id):
        try:
            return Note.objects.get(id=id)
        except Note.DoesNotExist:
            raise Http404


    def delete(self, request, id, format=None):
        note = self.get_object(id)
        note.delete()
        return Response({'status':status.HTTP_204_NO_CONTENT, 'message':'note deleted'})


@login_required
def detail_view(request, id):
    user = request.user
    user_ = User.objects.filter(id = user.id)
    if user_.exists():
        query = ""
        query = request.GET.get('q')
        if query:
            notes = get_note_queryset(user, str(query))
        else:
            notes = Note.objects.filter(user = user).order_by('-pinned', '-created')
        # notes = Note.objects.filter(user = user).order_by('-pinned', '-created')
        current_note = Note.objects.filter(id=id)
        if current_note.exists():
            return render(request, 'detail.html', {'notes': notes, 'current_note': current_note[0]})
        else:
            return HttpResponseRedirect(reverse('notes:create-note'))
    else:
        return render(request, 'base.html')


@login_required
def edit_view(request, id):
    user = request.user
    user_ = User.objects.filter(id = user.id)
    if user_.exists():
        query = ""
        query = request.GET.get('q')
        if query:
            notes = get_note_queryset(user, str(query))
        else:
            notes = Note.objects.filter(user = user).order_by('-pinned', '-created')
        # notes = Note.objects.filter(user = user).order_by('-pinned', '-created')
        current_note = Note.objects.filter(id=id)
        if current_note.exists():
            instance = get_object_or_404(Note, id=id)
            form = NoteForm(request.POST or None, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('notes:edit', id=id)
        else:
            return HttpResponseRedirect(reverse('notes:create-note'))
    return render(request, 'edit_note.html', {'form': form, 'notes': notes, 'current_id':id}) 


def get_note_queryset(user, query = None):
    # print(query)
    queryset = []
    queries = query.split(" ")
    # print(queries)
    for q in queries:
        notes = Note.objects.filter(user=user).filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
            ).distinct().order_by('-pinned', '-created')
#         for note in notes:
#             queryset.append(note)
#     return list(set(queryset))
    return notes
