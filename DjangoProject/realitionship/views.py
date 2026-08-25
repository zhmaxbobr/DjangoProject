from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from .forms import Anketa as form_anketa
from .models import Anketa
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    try:
        _=request.user.profile.anketa
    except Exception as e:
        messages.warning(request, "Заполните анкету!")
    return render(request,"realitionship/index.html")

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("rl:index")
    else:
        form = UserCreationForm()
    return render(request, "registration/sign_up.html", context={"form": form})


@login_required
def anketa(request):
    if request.method == "POST":
        form = form_anketa(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                anketa = request.user.profile.anketa
                anketa.gender=form_data.get("gender")
                anketa.age = form_data.get("age")
                anketa.find_gender = form_data.get("find_gender")
                anketa.save()
            except Exception as e:
                Anketa.objects.create(
                    gender=form_data.get("gender"),
                    age = form_data.get("age"),
                    find_gender = form_data.get("find_gender"),
                    profile=request.user.profile
                )
        return redirect("rl:profile")
    else:
        form = form_anketa()
        return render(request,"realitionship/anketa.html", context={"form":form})

@login_required
def view_profile(request):
    if request.method == "GET":
        try:
            _ = request.user.profile.anketa
        except Exception as e:
            messages.warning(request, "Заполните анкету!")
        likes_count = request.user.profile.liked.count()
        dislikes_count = request.user.profile.disliked.count()
        annotation = request.user.profile.annotation
        # = request.user.profile.anketa
        #if anketa:
        #age = request.user.profile.anketa.age or -1
        user_icon = request.user.profile.user_icon
        username = request.user.username
        return render(
            request,"realitionship/profile.html", context=
        {
            "likes_count":likes_count,
            "dislikes_count":dislikes_count,
            "annotation":annotation,
           # "age":age,
            "user_icon":user_icon,
            "username":username
        }
                      )

def view_liked(request):
    liked_count = request.user.profile.liked.count()
    limit = int(request.GET.get("limit",2))
    current_page = int(request.GET.get("page",0))
    offset = limit*current_page
    end = limit+offset
    pages = [page for page in range(round(liked_count/limit))]
    next_page = current_page+1
    prev_page = current_page-1
    liked = request.user.profile.liked.all()[offset:end]
    if len(pages) > 0:
        show_next_btn = True if next_page <= pages[-1] else False
        show_prev_btn = True if prev_page >= 0 else False
    else:
        show_next_btn = False
        show_prev_btn = False

    return render(request,"realitionship/marked/liked.html",context={
                                                                     "liked":liked,
                                                                     "current_page":current_page,
                                                                     "pages":pages,
                                                                     "next_page":next_page,
                                                                     "prev_page":prev_page,
                                                                     "show_next_btn":show_next_btn,
                                                                     "show_prev_btn":show_prev_btn
                                                                     })

def view_disliked(request):
    disliked_count = request.user.profile.disliked.count()
    limit = int(request.GET.get("limit", 2))
    current_page = int(request.GET.get("page", 0))
    offset = limit * current_page
    end = limit + offset
    pages = [page for page in range(round(disliked_count / limit))]
    next_page = current_page + 1
    prev_page = current_page - 1
    disliked = request.user.profile.disliked.all()[offset:end]
    if len(pages) > 0:
        show_next_btn = True if next_page <= pages[-1] else False
        show_prev_btn = True if prev_page >= 0 else False
    else:
        show_next_btn = False
        show_prev_btn = False

    return render(request, "realitionship/marked/disliked.html", context={
        "disliked": disliked,
        "current_page": current_page,
        "pages": pages,
        "next_page": next_page,
        "prev_page": prev_page,
        "show_next_btn": show_next_btn,
        "show_prev_btn": show_prev_btn
    })