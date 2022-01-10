"""
    1. Customer Suport Model
    2. Customer Suport messages Model
"""
from django.db import models
from django.contrib.auth.models import User
from checkout.models import Order, OrderLine


class CustomerSuport(models.Model):
    """
    Customer Suport Model. Order status choices
    order, order_line, user_profile Foreign keys
    """
    SUBMITTED = 'Submitted'
    REVIEW = 'In Review'
    RESOLVED = 'Resolved'
    SELECT = 'Select'
    ORDER = 'Order'
    PRODUCT = 'Product'
    ACCOUNT = 'Account'

    ISSUE_CHOICES = [
        (SELECT, 'Select'),
        (ORDER, 'Order'),
        (PRODUCT, 'Product'),
        (ACCOUNT, 'Account'),
    ]

    STATUS_CHOICES = [
        (SUBMITTED, 'Submitted'),
        (REVIEW, 'In Review'),
        (RESOLVED, 'Resolved'),
    ]

    status = models.CharField(
        max_length=60, default=SUBMITTED,
        choices=STATUS_CHOICES)
    user_profile = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_support')
    issue = models.CharField(
        max_length=60, default=SELECT,
        choices=ISSUE_CHOICES)
    message = models.TextField(max_length=500)
    order_line = models.ForeignKey(
        OrderLine, on_delete=models.CASCADE,
        related_name='orderline_support', null=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_support', null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket #{self.id}. {self.issue} Issue. In {self.order}'


class Message(models.Model):
    """
    Customer Suport Model messages
    thread, user, Foreign keys
    Boolean field read unread messags
    """
    thread = models.ForeignKey(
        CustomerSuport, null=False, blank=False,
        on_delete=models.CASCADE, related_name='messages_thread')
    user = models.ForeignKey(
        User, null=False, blank=False,
        on_delete=models.CASCADE, related_name="sender")
    message = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __str__(self):
        return f'From {self.user} issue: {self.thread}'
