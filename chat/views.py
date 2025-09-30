from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MessageThread, Message
from ads.models import Ad
from .forms import MessageForm


class StartThreadView(LoginRequiredMixin, View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, pk=ad_id)
        thread, created = MessageThread.objects.get_or_create(
            ad=ad,
            buyer=request.user,
            seller=ad.seller
        )
        return redirect('chat:thread_detail', thread_id=thread.id)


class ThreadDetailView(LoginRequiredMixin, View):
    template_name = 'chat/thread_detail.html'

    def get(self, request, thread_id):
        thread = get_object_or_404(MessageThread, id=thread_id)
        form = MessageForm()
        messages = thread.messages.all().order_by('created_at')
        return render(request, self.template_name, {
            'thread': thread,
            'messages': messages,
            'form': form
        })

    def post(self, request, thread_id):
        thread = get_object_or_404(MessageThread, id=thread_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            return redirect('chat:thread_detail', thread_id=thread.id)

        messages = thread.messages.all().order_by('created_at')
        return render(request, self.template_name, {
            'thread': thread,
            'messages': messages,
            'form': form
        })
