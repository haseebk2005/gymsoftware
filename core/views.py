from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import *
from .forms import GymMemberForm
from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
import os
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count


def dashboard(request):
    # Get the current date and time in the local time zone
    today = timezone.localtime(timezone.now()).date()  # Get today's date with time zone awareness
    last_30_days = today - timedelta(days=29)  # Start from 30 days ago (inclusive of today)

    # Filter attendance data for the last 30 days (including today)
    attendance_data = Attendance.objects.filter(check_in_time__gte=timezone.make_aware(datetime.combine(last_30_days, datetime.min.time())))

    # Prepare labels and data for the graph
    labels, data = [], []
    for i in range(30):
        day = last_30_days + timedelta(days=i)
        labels.append(day.strftime('%Y-%m-%d'))
        daily_attendance = attendance_data.filter(check_in_time__date=day).count()
        data.append(daily_attendance)

    # Get the total attendance for today
    total_attendance_today = attendance_data.filter(check_in_time__date=today).count()

    # Get the total number of active members
    total_active_members = GymMember.objects.filter(active_status=True).count()

    # Pass context to the template
    context = {
        'labels': labels,
        'data': data,
        'total_attendance_today': total_attendance_today,
        'total_active_members': total_active_members
    }

    return render(request, 'index.html', context)


from django.utils.timezone import now  # Import the now function to get the current date

from django.utils import timezone
from django.db.models import Q
from .models import GymMember

def member_list(request):
    active_status = request.GET.get('active', 'all')
    search_query = request.GET.get('search', '')

    # Start with all members
    members = GymMember.objects.all()

    # Filter by active status
    if active_status == "True":
        members = members.filter(active_status=True)
    elif active_status == "False":
        members = members.filter(active_status=False)

    # Search filtering
    if search_query:
        members = members.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(membership_id__icontains=search_query)
        )

    # Order members by membership_id and name
    members = members.order_by('membership_id')

    # Get the current date (without time)
    now = timezone.localdate()  # Use localdate() for just the date

    # Pass data to the template
    return render(request, 'totalmembers.html', {
        'members': members,
        'active_status': active_status,
        'search_query': search_query,
        'now': now,  # Pass only the date, no time
    })

def member_detail(request, id):
    member = get_object_or_404(GymMember, id=id)
    form = GymMemberForm(instance=member)  # Pass form to template

    last_30_days = [(datetime.now().date() - timedelta(days=i)) for i in range(30)]
    attendance_data = [
        {
            "date": day,
            "status": Attendance.objects.filter(member=member, check_in_time__date=day).exists()
        }
        for day in last_30_days
    ]

    pending_fee = member.pending_fee

    return render(request, 'member_detail.html', {
        "member": member,
        "attendance_data": attendance_data,
        "pending_fee": pending_fee,
        "form": form,
    })


from django.http import JsonResponse

def mark_attendance(request, member_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            member = GymMember.objects.get(id=member_id)
            with transaction.atomic():
                Attendance.objects.create(member=member, check_in_time=timezone.now())
            return JsonResponse({'success': True, 'message': 'Attendance marked successfully.'})
        except GymMember.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Member not found.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)



def activate_member(request, member_id):
    member = GymMember.objects.get(id=member_id)
    member.active_status = True
    member.activation_date = timezone.now().date()
    member.save()
    return redirect('member_list')

from django.http import HttpResponse

def deactivate_member(request, member_id):
    print("Deactivate member function called")
    member = get_object_or_404(GymMember, id=member_id)
    print(f"Found member: {member}")
    
    if request.method == "POST":
        member.active_status = False
        member.save()
        print(f"Deactivated member {member_id}")
        return redirect('member_list')
    return HttpResponse("Invalid request method", status=405)


def print_receipt(request, member_id):
    member = get_object_or_404(GymMember, id=member_id)

    # Get payments for the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_payments = Payment.objects.filter(
        member=member,
        payment_date__year=current_year,
        payment_date__month=current_month
    )

    total_paid = monthly_payments.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'print_receipt.html', {
        'member': member,
        'monthly_payments': monthly_payments,
        'total_paid': total_paid,
        'current_date': datetime.now(),
    })


def register_member(request):
    if request.method == 'POST':
        form = GymMemberForm(request.POST, request.FILES)
        if form.is_valid():
            new_member = form.save()
            # Remove registration fee logic
            return redirect('member_list')
    else:
        form = GymMemberForm()
    return render(request, 'register_member.html', {'form': form})

from django.db import transaction
from django.contrib import messages
def fee_reset(request):
    with transaction.atomic():
        # Loop through all payments to find the total unpaid fees for each member
        for payment in Payment.objects.all():
            # If the member has a remaining balance, add it to the remaining balance of all members
            if payment.remaining_balance > 0:
                total_remaining_balance = payment.remaining_balance  # Calculate the unpaid balance
                
                # Add the unpaid balance to all other members' remaining balances
                for other_payment in Payment.objects.all():
                    if other_payment.member != payment.member:  # Avoid adding to the same member's balance
                        other_payment.remaining_balance += total_remaining_balance
                        other_payment.save()
                
                # Now reset the fee for the current payment
                payment.total_amount += payment.remaining_balance  # Add remaining balance to total amount
                payment.remaining_balance = payment.total_amount  # Reset remaining balance to updated total amount
            else:
                # If the fee is already paid in full, reset the payment and balance as usual
                payment.remaining_balance = payment.total_amount  # Reset remaining balance to total amount
            payment.amount = 0  # Reset the payment amount to 0
            payment.overpayment = Decimal('0')  # Reset any overpayment
            payment.save()

    messages.success(request, 'All fees have been reset successfully.')
    return redirect('member_list')

def pay_fee(request, member_id):
    member = get_object_or_404(GymMember, id=member_id)

    if request.method == 'POST':
        # Get the payment amount from the form input
        amount = Decimal(request.POST['amount'])  # Ensure amount is a Decimal
        
        # Create a new payment record
        Payment.objects.create(
            member=member,
            amount=amount,
            total_amount=member.total_membership_cost(),
            remaining_balance=0  # or calculate dynamically if needed
        )

        # After payment creation, recalculate the pending fee
        payments_made = Payment.objects.filter(member=member).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        pending_fee = member.total_membership_cost() - payments_made  # Calculate pending fee

        return redirect('/totalmembers/?active=True')

    # Calculate pending fee for the template if needed
    payments_made = Payment.objects.filter(member=member).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    pending_fee = member.total_membership_cost() - payments_made

    return render(request, 'pay_fee.html', {'member': member, 'pending_fee': pending_fee})
def fee(request):

    collected_fee = Payment.objects.aggregate(total_collected=Sum('amount'))['total_collected'] or 0
    context={
        'collected_fee':collected_fee
    }
    return render(request,'fee.html',context)
