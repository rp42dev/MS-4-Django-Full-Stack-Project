"""
    1. A view to return the contact us page
    2. A view to return the shop suport page
    3. A view to submit support issue tickets
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings

from checkout.models import Order, OrderLine
from .models import CustomerSuport, Message
from .forms import SupportForm, MessageForm, IssueStatusForm


def contact_view(request):
    """
    A view to return the contact page
    Renders page with contact form
    Sends email message to the shop email
    """
    if request.POST:
        subject = request.POST.get('subject')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        body = render_to_string(
                'email/customer-message.txt',
                {'name': name, 'email': email, 'message': message})

        # Message from user
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]
        )

        body = render_to_string(
                'email/auto-response.txt',
                {'name': name, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        # Auto response
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

    return render(request, 'support/contact.html')


@login_required
def support(request):
    """
    A view to return the shop suport page
    """
    profile = request.user

    if request.POST:
        form = SupportForm(request.POST)
        if form.is_valid():
            support_post = CustomerSuport(
                status='Submitted',
                user_profile=profile,
                issue=request.POST['support-issue'],
                message=request.POST['support-message'],
                order=None,
                order_line=None,
            )

            support_post.save()

            issues = CustomerSuport.objects.filter(user_profile=profile)
            issue = issues.last()
            issue_id = issue.id

            inital_message = Message(
                thread=issue,
                user=profile,
                message=issue.message,
            )
            inital_message.save()

            messages.success(
                request, f'Your support ticket #{issue_id}\
                wil get back to you asap')
            return redirect(reverse('messages_view', args=[issue_id]))

        else:
            messages.error(request, 'Error with form')
            return redirect(reverse('home'))

    form = SupportForm()

    context = {
        'form': form,
    }

    return render(request, 'support/support.html', context)


@login_required
def submit(request, order_number):
    """
    A view to submit support issue tickets
    If order was created get order from the database
    Othervise User can submit issues without order
    User must have account and logged in
    """
    profile = request.user
    order = get_object_or_404(Order, order_number=order_number)
    order_line = OrderLine.objects.filter(order__order_number=order_number)
    issues = CustomerSuport.objects.all().filter(user_profile=profile)

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

    return render(request, 'support/submit.html', context)


@login_required
def messages_view(request, issue_id):
    """
    Rerurn a Support messages view
    Get costumer support ticket from database
    Check if user profile contains current ticket
    POST an messages regarding current issue to administrator
    If user is Superuser then return all the messages to admin
    Finaly save to database all the read messages as read
    """
    issue = get_object_or_404(CustomerSuport, pk=issue_id)
    profile = request.user
    if not profile.is_superuser:
        status_form = None
        if not issue.user_profile == profile:
            messages.error(request, 'Error loading support ticket')
            return redirect(reverse('home'))
    else:
        status_form = IssueStatusForm(
            instance=issue, data=request.POST or None)
        if 'issue_status-status' in request.POST:
            if status_form.is_valid():
                status = request.POST['issue_status-status']
                issue.status = status
                issue.save()
                messages.success(
                    request, f'Issue status changed to {status}')
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
        messages.success(request, 'Your message sent successfuly')
        return redirect(reverse('messages_view', args=[issue_id]))
    if 'unread' in request.GET:
        for message in thread_messages:
            message.unread = request.GET['unread']
            message.save()
    form = MessageForm()
    context = {
        'thread_messages': thread_messages,
        'status_form': status_form,
        'issue': issue,
        'form': form,
    }
    return render(request, 'messages/messages.html', context)
