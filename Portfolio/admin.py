from django.contrib import admin
from .models import Skill, Use, Project, CMessage, Info, Certificate, SocialMedia

# Register your models here.

admin.site.register(Skill)
admin.site.register(Use)
admin.site.register(CMessage)
admin.site.register(Project)
admin.site.register(Info)
admin.site.register(SocialMedia)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'issuer', 'aspect_ratio', 'date_issued']
    list_filter = ['category', 'issuer', 'date_issued']
    search_fields = ['title', 'description', 'issuer']
    readonly_fields = ['aspect_ratio']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'issuer', 'date_issued')
        }),
        ('Content', {
            'fields': ('image', 'description')
        }),
        ('Metadata', {
            'fields': ('aspect_ratio',),
            'classes': ('collapse',)
        }),
    )