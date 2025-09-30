from django.shortcuts import render, get_object_or_404, redirect
from .models import MessageThread, Message
from ads.models import Ad
from django.contrib.auth.decorators import login_required
from .forms import MessageForm

@login_required
def start_thread(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    thread, created = MessageThread.objects.get_or_create(
        ad=ad, 
        buyer=request.user, 
        seller=ad.seller
        )
    return redirect('chat:thread_detail', thread_id=thread.id)  

@login_required
def thread_detail(request, thread_id):  
    thread = get_object_or_404(MessageThread, id=thread_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            return redirect('chat:thread_detail', thread_id=thread.id)
    else:
        form = MessageForm()

    messages = thread.messages.all().order_by('created_at')  

    return render(request, 'chat/thread_detail.html', {
        'thread': thread,
        'messages': messages,
        'form': form
    })
