from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad, AdImage, Favorite, Category, Favorite
from .forms import AdForm, ComplaintForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
# Create your views here.

def ad_list(request):
    qs = Ad.objects.filter(status='active').order_by('-created_at')

    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {'ads': ads})
def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.views_count += 1
    ad.save(update_fields=['views_count'])
    is_fav = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, ad=ad).exists()
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'is_fav': is_fav})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            ad = form.save(commit=False)
            ad.seller = request.user
            ad.save()
            for idx, img in enumerate(images):
                AdImage.objects.create(ad=ad, image=img, order=idx)
            messages.success(request, "E'lon yaratildi")
            return redirect('ads:detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        images = request.FILES.getlist('images')
        if form.is_valid():
            ad = form.save()
            for idx, img in enumerate(images):
                AdImage.objects.create(ad=ad, image=img, order=idx)
            messages.success(request, "E'lon yangilandi")
            return redirect('ads:detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'ad': ad})

@login_required
def toggle_favorite(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, ad=ad)
    if not created:
        fav.delete()
        messages.info(request, "Sevimlidan o'chirildi")
    else:
        messages.success(request, "Sevimlilarga qo'shildi")
    return redirect('ads:detail', pk=pk)

def search(request):
    q = request.GET.get('q','')
    qs = Ad.objects.filter(status='active').filter(
        Q(title__icontains=q) |
        Q(description__icontains=q)
    ).order_by('-created_at')
    paginator = Paginator(qs, 20)
    ads = paginator.get_page(request.GET.get('page'))
    return render(request, 'ads/search_results.html', {'ads': ads, 'q': q})


def ads_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    ads = Ad.objects.filter(category=category, status='active').order_by('-created_at')
    return render(request, 'ads/ads_by_category.html', {
        'category': category,
        'ads': ads
    })
    


@login_required
def favorites(request):
    ads = Ad.objects.filter(favorited_by__user=request.user)
    return render(request, 'ads/favorites.html', {'ads': ads})


@login_required
def add_complaint(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    complaints = ad.complaints.all().order_by('-created_at')  

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.ad = ad
            complaint.user = request.user
            complaint.save()
            messages.success(request, "✅ Shikoyatingiz yuborildi!")
            return redirect('ads:detail', pk=ad.id)  
    else:
        form = ComplaintForm()

    return render(
        request,
        'ads/add_complaint.html',
        {'form': form, 'ad': ad, 'complaints': complaints}
    )


