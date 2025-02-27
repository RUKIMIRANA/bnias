from .models import (
    Colline,
    Profile,
    Commune,
    Citizen,
    Service,
    Province,
    Publication,
    Notification,
    RegisteredIdCard,
    LostIdCardReport,
    RegisteredIdCardApplication,
)
from django.db.models import Q, Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as login_me_in, logout as log_me_out


# Create your views here.
class ServiceList(ListView):
    paginate_by = 48
    queryset = Service.objects.order_by("-id")
    template_name = "service/index.html"


class ServiceDetail(DetailView):
    model = Service
    paginate_by = 48
    template_name = "service/show.html"


class PublicationList(ListView):
    paginate_by = 48
    queryset = Publication.objects.order_by("-id")
    template_name = "publication/index.html"


class PublicationDetail(DetailView):
    model = Publication
    paginate_by = 48
    template_name = "publication/show.html"


@login_required(login_url="/login")
@require_http_methods(["GET", "POST"])
def dashboard(request):
    citizen_count = Citizen.objects.count()
    service_count = Service.objects.count()
    lost_count = LostIdCardReport.objects.count()
    applicant_count = RegisteredIdCardApplication.objects.count()
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()
    regions = (
        RegisteredIdCardApplication.objects.values("province_id", "province__name")
        .annotate(count=Count("province_id"))
        .order_by("province_id")
    )
    return render(
        request,
        "dashboard/index.html",
        {
            "profile": profile,
            "regions": regions,
            "lost_count": lost_count,
            "service_count": service_count,
            "citizen_count": citizen_count,
            "applicant_count": applicant_count,
        },
    )


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        return render(request, "auth/register.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == "" or password != confirm_password:
            messages.info(request, "Password do not match")
            return redirect("register")

        if email == "" or User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect("register")

        if username == "" or User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("register")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        user_login = authenticate(username=username, password=password)
        login_me_in(request, user_login)

        return redirect("dashboard")


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        return render(request, "auth/login.html")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("login")

        login_me_in(request, user)
        return redirect("dashboard")


@login_required(login_url="login")
def logout(request):
    log_me_out(request)
    return redirect("home")


@require_http_methods(["GET", "POST"])
def apply(request):
    if request.method == "GET":
        communes = Commune.objects.all()
        collines = Colline.objects.all()
        provinces = Province.objects.all()
        return render(
            request,
            "apply.html",
            {"provinces": provinces, "collines": collines, "communes": communes},
        )

    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        gender = request.POST["gender"]
        birth_date = request.POST["birthdate"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        province = request.POST["province"]
        commune = request.POST["commune"]
        colline = request.POST["colline"]

        if RegisteredIdCardApplication.objects.filter(
            Q(email=email) | Q(phone=phone)
        ).exists():
            messages.info(request, "Application already sent")

        else:
            applicant = RegisteredIdCardApplication(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_date=birth_date,
                phone=phone[:10],
                email=email,
                province_id=province,
                commune_id=commune,
                colline_id=colline,
            )

            if request.FILES.get("picture") is not None:
                applicant.image = request.FILES.get("applicant")

            applicant.save()
            messages.info(request, "Thank you for applying, we'll be in touch soon")

        return redirect("apply")


@login_required(login_url="/login")
@require_http_methods(["GET", "POST"])
def lost(request):
    if request.method == "GET":
        communes = Commune.objects.all()
        collines = Colline.objects.all()
        provinces = Province.objects.all()
        profile = Profile.objects.filter(profile_user_id=request.user.id).first()
        return render(
            request,
            "dashboard/lost.html",
            {
                "provinces": provinces,
                "collines": collines,
                "communes": communes,
                "profile": profile,
            },
        )

    if request.method == "POST":
        card_id = request.POST["nid"]
        date = request.POST["date"]
        report = request.POST["report"]
        province = request.POST["province"]
        commune = request.POST["commune"]
        colline = request.POST["colline"]

        if LostIdCardReport.objects.filter(Q(card_id=card_id) | Q(date=date)).exists():
            messages.info(request, "Lost report already sent")

        else:
            lost = LostIdCardReport(
                card_id=card_id,
                date=date,
                report=report,
                province_id=province,
                commune_id=commune,
                colline_id=colline,
            )

            lost.save()
            messages.info(
                request,
                "Thank you for reporting the lost ID card, we'll be in touch soon",
            )

        return redirect("lost")


@require_http_methods(["GET"])
@login_required(login_url="/login")
def approve(request, id):
    applicant = get_object_or_404(RegisteredIdCardApplication, pk=id)
    applicant.is_approved = True

    if not Citizen.objects.filter(
        first_name=applicant.first_name, last_name=applicant.last_name
    ).exists():
        citizen = Citizen(
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            phone=applicant.phone,
            birth_date=applicant.birth_date,
            user_id=request.user.id,
        )
        citizen.save()

    applicant.save()
    return redirect("citizen")


@require_http_methods(["GET"])
@login_required(login_url="/login")
def deny(request, id):
    applicant = get_object_or_404(RegisteredIdCardApplication, pk=id)
    applicant.delete()
    return redirect("applicant")


@require_http_methods(["GET"])
@login_required(login_url="/login")
def my_card(request):
    # citizen = Citizen.objects.get(user=request.user)
    # card = citizen.card if citizen.card else "No card available"
    return render(request, "dashboard/my-card.html")


@require_http_methods(["GET"])
@login_required(login_url="/login")
def citizen(request):
    rows = Citizen.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/citizen.html",
        {"page_object": page_object, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def colline(request):
    rows = Colline.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/colline.html",
        {"page_object": page_object, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def card(request):
    rows = RegisteredIdCard.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request, "dashboard/card.html", {"page_object": page_object, "profile": profile}
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def commune(request):
    rows = Commune.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/commune.html",
        {"page_object": page_object, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def province(request):
    rows = Province.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/province.html",
        {"page_object": page_object, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def applicant(request):
    rows = RegisteredIdCardApplication.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/applicant/index.html",
        {"page_object": page_object, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def applicant_show(request, id):
    applicant = get_object_or_404(RegisteredIdCardApplication, pk=id)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/applicant/show.html",
        {"applicant": applicant, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def notification(request):
    rows = Notification.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/notification.html",
        {"page_object": page_object, "profile": profile},
    )


@require_http_methods(["GET"])
@login_required(login_url="/login")
def lost_cards(request):
    rows = LostIdCardReport.objects.order_by("-id")
    paginator = Paginator(rows, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    profile = Profile.objects.filter(profile_user_id=request.user.id).first()

    return render(
        request,
        "dashboard/lost-cards.html",
        {"page_object": page_object, "profile": profile},
    )


@login_required(login_url="signin")  # type: ignore
@require_http_methods(["GET", "POST"])
def settings(request):
    if request.method == "GET":
        profile = Profile.objects.filter(profile_user_id=request.user.id).first()
        return render(request, "settings.html", {"profile": profile})


@require_http_methods(["GET"])
def profile(request, id):
    me = request.user.id
    user = get_object_or_404(User, pk=id)

    if not Profile.objects.filter(profile_user_id=id).exists():
        profile = Profile.objects.create(user=user, profile_user_id=user.id)  # type: ignore
        profile.save()
    else:
        profile = Profile.objects.filter(profile_user_id=id).get()

    return render(request, "profile.html", {"profile": profile, "user": user, "me": me})


@require_http_methods(["POST"])
@login_required(login_url="signin")
def profile_update(request, id):
    user = get_object_or_404(User, pk=request.user.id)

    if not Profile.objects.filter(profile_user_id=id).exists():
        profile = Profile.objects.create(user=user, profile_user_id=user.id)  # type: ignore
        profile.save()
    else:
        profile = Profile.objects.filter(profile_user_id=id).get()

    user.last_name = request.POST["last_name"]
    user.first_name = request.POST["first_name"]
    user.username = request.POST["username"]
    user.email = request.POST["email"]
    profile.bio = request.POST["bio"]

    if request.FILES.get("image") != None:
        profile.image = request.FILES.get("image")

    user.save()
    profile.save()
    messages.info(request, "Settings updated")

    return redirect(request.META.get("HTTP_REFERER"))
