#models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal

class GymMember(models.Model):
    # Basic Information
    name = models.CharField(max_length=50)
    fname = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Gym Membership Details
    membership_id = models.CharField(max_length=20, unique=True)
    membership_type = models.CharField(max_length=50, choices=[
        ('single time', 'single time'),
        ('single time with electric machine', 'single time with electric machine'),
        ('double time', 'double time'),
        ('double time with electric machine', 'double time with electric machine')
    ])
    active_status = models.BooleanField(default=True)
    activation_date = models.DateField(null=True, blank=True)  # Editable activation date

    # Health and Fitness Information
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    fitness_goal = models.CharField(max_length=100, blank=True, null=True)

    # Contact Information
    address = models.TextField(blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)

    # Additional Details
    joined_date = models.DateField(auto_now_add=True)
    last_visit_date = models.DateField(null=True, blank=True)
    additional_notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Only set activation_date to today's date if it's not provided by the user and the member is active
        if self.active_status and not self.activation_date:
            self.activation_date = timezone.now().date()
        elif not self.active_status:
            # Optionally reset activation_date if member is deactivated
            self.activation_date = None
        super(GymMember, self).save(*args, **kwargs)



    def activate(self):
        self.active_status = True
        self.activation_date = timezone.now().date()  # Set activation date to today’s date
        self.save()

    @property
    def attendance_today(self):
        today = timezone.now().date()
        return Attendance.objects.filter(member=self, check_in_time__date=today).exists()

    @property
    def pending_fee(self):
        payments_made = Payment.objects.filter(member=self).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
        return self.total_membership_cost() - payments_made

    def total_membership_cost(self):
        cost = {
            'single time': 2000,
            'single time with electric machine': 3000,
            'double time': 4000,
            'double time with electric machine': 5000
        }
        return cost.get(self.membership_type, 0)

    def __str__(self):
        return f"{self.name} - {self.membership_id}"

class Attendance(models.Model):
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.check_in_time.date()}"

class Payment(models.Model):
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    remaining_balance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    overpayment = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=Decimal('0'))

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.member.total_membership_cost()
        
        # Calculate remaining balance based on all payments to date
        previous_payments = Payment.objects.filter(member=self.member).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
        calculated_remaining = self.total_amount - previous_payments - self.amount

        if calculated_remaining < 0:
            # If overpayment, set remaining balance to zero and record overpayment
            self.remaining_balance = Decimal('0')
            self.overpayment = abs(calculated_remaining)
        else:
            # Normal remaining balance without overpayment
            self.remaining_balance = calculated_remaining
            self.overpayment = Decimal('0')

        super().save(*args, **kwargs)
