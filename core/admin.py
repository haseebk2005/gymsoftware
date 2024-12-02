from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import GymMember, Payment, Attendance

class GymMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'fname', 'membership_id', 'phone_number', 'date_of_birth', 'gender', 
                    'profile_picture_display', 'membership_type', 'active_status', 'weight', 
                    'height', 'fitness_goal', 'address', 'emergency_contact_relation', 
                    'joined_date', 'last_visit_date', 'activation_date', 'additional_notes')
    
    search_fields = ('name', 'membership_id', 'phone_number')
    list_filter = ('active_status', 'membership_type', 'activation_date')  # Added activation_date to filters
    
    fields = ('name', 'fname', 'phone_number', 'date_of_birth', 'gender', 'profile_picture', 
              'membership_id', 'membership_type', 'active_status', 'weight', 'height', 
              'fitness_goal', 'address', 'emergency_contact_relation', 'last_visit_date', 
              'activation_date', 'additional_notes')

    readonly_fields = ('joined_date', 'profile_picture_display')  # Added profile_picture_display as readonly

    def profile_picture_display(self, obj):
        """Display the profile picture if available."""
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="150" height="150" style="object-fit:cover;" />')
        return "No image available"
    profile_picture_display.short_description = "Profile Picture Preview"

    class Media:
        js = ('admin/js/capture_camera.js',)  # Include custom JavaScript for camera functionality
        css = {
            'all': ('admin/css/admin.css',)  # Optional: Include custom styles
        }

admin.site.register(GymMember, GymMemberAdmin)
admin.site.register(Payment)
admin.site.register(Attendance)
