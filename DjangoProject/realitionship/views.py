from venv import create

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from .forms import Anketa as form_anketa
from .models import Anketa,Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        try:
            _=request.user.profile.anketa
        # BUG: can not load relationship
        except Exception:
            messages.warning(request, "Заполните анкету!")
    return render(request,"realitionship/index.html")


@login_required
def recomendation_search(request):
    try:
        current_anketa = request.user.profile.anketa
    except Exception:
        messages.warning(request, "Заполните анкету!")
        return redirect("rl:anketa")

    anketes = Anketa.objects.filter(
        age__gte=current_anketa.age - 2,
        age__lte=current_anketa.age + 2,
    )

    if current_anketa.find_gender != "both":
        anketes = anketes.filter(gender=current_anketa.find_gender)

    anketes = list(anketes)
    # try:
    #     del anketes[anketes.index(request.user.profile.anketa)]
    # except Exception:
    #     pass

    anketes_count = len(anketes)
    limit = int(request.GET.get("limit", 2))
    current_page = int(request.GET.get("page", 0))
    offset = limit * current_page
    end = limit + offset
    pages = [page for page in range(round(anketes_count / limit))]
    next_page = current_page + 1
    prev_page = current_page - 1
    anketes = anketes[offset:end]
    if len(pages) > 0:
        show_next_btn = True if next_page <= pages[-1] else False
        show_prev_btn = True if prev_page >= 0 else False
    else:
        show_next_btn = False
        show_prev_btn = False

    return render(request, "realitionship/index.html", context={
        "anketes": anketes,
        "current_page": current_page,
        "pages": pages,
        "next_page": next_page,
        "prev_page": prev_page,
        "show_next_btn": show_next_btn,
        "show_prev_btn": show_prev_btn
    })


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
    try:
        anketa = request.user.profile.anketa
    except Exception:
        anketa = None

    if request.method == "POST":
        form = form_anketa(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                anketa = request.user.profile.anketa
                anketa.gender=form_data.get("gender")
                anketa.age = form_data.get("age")
                print(anketa.age,type(anketa.age))
                if anketa.age <= 0:
                    messages.error(request,"Возраст не может быть отрицательным!")
                    return redirect("rl:anketa")
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
        #POST
        initial = {}
        if anketa:
            initial = {
                "gender": anketa.gender,
                "age": anketa.age,
                "find_gender": anketa.find_gender,
            }
        form = form_anketa(initial=initial)
        return render(request,"realitionship/anketa.html", context={"form":form})


@login_required
def view_profile(request):
    if request.method == "GET":
        username = request.GET.get("username",None)

        if not username:
            profile = request.user.profile
            try:
                anketa = request.user.profile.anketa
            except Exception as e:
                messages.warning(request, "Заполните анкету!")
        else:
            profile = Profile.objects.filter(user__username=username).first()
            if not profile:
                return HttpResponse("Создайте профиль!")

        return render(
            request, "realitionship/profile.html", context=
            {
            "likes_count":profile.liked.count(),
            "dislikes_count":profile.disliked.count(),
            "annotation": profile.annotation,
            "age": profile.anketa.age if profile.anketa else None,
            "user_icon": profile.user_icon,
            "username": profile.user.username,
            "is_user":True if request.user.username == username or username is None else False,
            "show_marked_items":profile.show_marked_items
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
