from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render


class CustomAdminSite(AdminSite):
    site_header = "Doctor Appointment System Administration"
    site_title = "Doctor Appointment Admin"
    index_title = "Welcome to Doctor Appointment System Administration"

    def index(self, request, extra_context=None):
        """
        Display the main admin index page.
        """
        context = {
            'title': self.index_title,
            'app_list': self.get_app_list(request),
            'has_permission': self.has_permission(request),
        }
        context.update(extra_context or {})
        return render(request, 'admin/index.html', context)


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')
