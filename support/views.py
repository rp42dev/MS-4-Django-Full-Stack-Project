from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from checkout.models import Order, OrderLine
from .models import CustomerSuport, Message
from .forms import SupportForm, MessageForm, IssueStatusForm



@login_required
def support(request):
    """
    A view to return the shop suport page
    """
    return render(request, 'support/support.html')


@login_required
def submit(request, order_number):

    order = get_object_or_404(Order, order_number=order_number)
    order_line = OrderLine.objects.filter(order__order_number=order_number)
    issues = CustomerSuport.objects.all()
    profile = request.user

    if not order.user_profile == profile:
        messages.error(request, 'Sorry no order could be found')
        return redirect(reverse('order_history', args=[order_number]))

    if request.POST:
        form = SupportForm(request.POST)
        if form.is_valid():
            product = request.POST['product']
            if not product:
                order_line_item = None
            else:
                order_line_item = order_line.get(product_id=product)

            support_post = CustomerSuport(
                status='Submitted',
                user_profile=profile,
                issue=request.POST['support-issue'],
                message=request.POST['support-message'],
                order=order,
                order_line=order_line_item,
            )
            support_post.save()
            issue = issues.get(order__order_number=order_number)
            issue_id = issue.id 

            inital_message = Message(
                thread=issue,
                user=profile,
                message=issue.message,
            )
            inital_message.save()

            messages.success(request, 'Successfuly added rieview')
            return redirect(reverse('messages_view', args=[issue_id]))

        else:
            messages.error(request, 'Error with form')
            return redirect(reverse('order_history', args=[order_number]))

    form = SupportForm()

    context = {
        'form': form,
        'order': order,
        'order_line': order_line,
    }

    return render(request, 'support/support.html', context)


@login_required
def messages_view(request, issue_id):
    issue = get_object_or_404(CustomerSuport, pk=issue_id)
    profile = request.user
    if not profile.is_superuser:
        status_form = None
        if not issue.user_profile == profile:
            messages.error(request, 'Error loading support ticket')
            return redirect(reverse('home'))
    else:
        status_form = IssueStatusForm(instance=issue)
        if 'issue_status-status' in request.POST:
            if status_form.is_valid:
                status = request.POST['issue_status-status']
                issue.status = status
                issue.save()
                messages.success(request, f'Issue status was changed to {status}')
                return redirect(reverse('messages_view', args=[issue_id]))

    all_messages = Message.objects.all()
    thread_messages = all_messages.filter(thread=issue)

    if 'mesage-message' in request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                thread=issue,
                user=profile,
                message=request.POST['mesage-message'],
            )
        message.save()
        messages.success(request, 'Your message was sent successfuly')
        return redirect(reverse('messages_view', args=[issue_id]))
    if 'unread' in request.GET:
        for m in thread_messages:
            m.unread = request.GET['unread']
            m.save()
    form = MessageForm()
    context = {
        'thread_messages': thread_messages,
        'status_form': status_form,
        'issue': issue,
        'form': form,
    }
    return render(request, 'messages/messages.html', context)
