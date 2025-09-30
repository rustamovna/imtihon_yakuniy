from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Ad, AdImage, Favorite, Category
from .forms import AdForm, ComplaintForm


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 20

    def get_queryset(self):
        return Ad.objects.filter(status='active').order_by('-created_at')


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        ad.views_count += 1
        ad.save(update_fields=['views_count'])
        context['is_fav'] = False
        if self.request.user.is_authenticated:
            context['is_fav'] = Favorite.objects.filter(user=self.request.user, ad=ad).exists()
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for idx, img in enumerate(images):
            AdImage.objects.create(ad=self.object, image=img, order=idx)
        messages.success(self.request, "E'lon yaratildi")
        return response

    def get_success_url(self):
        return reverse('ads:detail', kwargs={'pk': self.object.pk})


class AdEditView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for idx, img in enumerate(images):
            AdImage.objects.create(ad=self.object, image=img, order=idx)
        messages.success(self.request, "E'lon yangilandi")
        return response

    def get_success_url(self):
        return reverse('ads:detail', kwargs={'pk': self.object.pk})


class ToggleFavoriteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        fav, created = Favorite.objects.get_or_create(user=request.user, ad=ad)
        if not created:
            fav.delete()
            messages.info(request, "Sevimlidan o‘chirildi ❌")
        else:
            messages.success(request, "Sevimlilarga qo‘shildi ❤️")
        return redirect('ads:detail', pk=pk)

class SearchView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        qs = Ad.objects.filter(status='active').filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).order_by('-created_at')
        paginator = Paginator(qs, 20)
        ads = paginator.get_page(request.GET.get('page'))
        return render(request, 'ads/search_results.html', {'ads': ads, 'q': q})


class AdsByCategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        ads = Ad.objects.filter(category=category, status='active').order_by('-created_at')
        return render(request, 'ads/ads_by_category.html', {
            'category': category,
            'ads': ads
        })


class FavoritesView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/favorites.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.filter(favorited_by__user=self.request.user, status='active').order_by('-created_at')


class AddComplaintView(LoginRequiredMixin, View):
    template_name = 'ads/add_complaint.html'

    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        complaints = ad.complaints.all().order_by('-created_at')
        form = ComplaintForm()
        return render(request, self.template_name, {
            'form': form, 'ad': ad, 'complaints': complaints
        })

    def post(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        complaints = ad.complaints.all().order_by('-created_at')
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.ad = ad
            complaint.user = request.user
            complaint.save()
            messages.success(request, "✅ Shikoyatingiz yuborildi!")
            return redirect('ads:detail', pk=ad.id)
        return render(request, self.template_name, {
            'form': form, 'ad': ad, 'complaints': complaints
        })
