from django import forms
from .models import GymMember

class GymMemberForm(forms.ModelForm):
    class Meta:
        model = GymMember
        fields = [
            'name', 'fname', 'phone_number', 'date_of_birth', 'gender', 
            'profile_picture', 'membership_id', 'membership_type', 
            'active_status', 'activation_date',  # Added activation_date
            'weight', 'height', 'bmi', 
            'fitness_goal', 'address', 'emergency_contact_relation', 
            'last_visit_date', 'additional_notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_visit_date': forms.DateInput(attrs={'type': 'date'}),
            'activation_date': forms.DateInput(attrs={'type': 'date'}),  # Date picker for activation_date
            'profile_picture': forms.ClearableFileInput(),
            'active_status': forms.CheckboxInput(),  # Adding checkbox for active status
        }
    
    def __init__(self, *args, **kwargs):
        super(GymMemberForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Placeholder texts
        self.fields['name'].widget.attrs.update({'placeholder': 'Full Name'})
        self.fields['fname'].widget.attrs.update({'placeholder': 'Father Name'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Phone Number'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Full Address'})
        self.fields['emergency_contact_relation'].widget.attrs.update({'placeholder': 'Emergency Contact Relation'})
