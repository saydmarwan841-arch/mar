"""
Django Admin Configuration
===========================
Customized admin interface for managing quiz questions.

Provides an intuitive interface for creating, editing, and managing
quiz questions with full support for both Multiple Choice and True/False formats.
"""

from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Question Admin Interface
    ========================
    Custom admin configuration for the Question model.
    
    Features:
    - List view with key question details
    - Inline editing of display order
    - Advanced filtering by question type and creation date
    - Powerful search functionality
    - Organized fieldsets for better UX
    - Collapsible sections for optional fields
    
    Display Customizations:
    - Shows: Question text, type, correct answer, order, creation date
    - Editable: Order field inline in list view
    - Searchable: Question text
    - Filterable: By type and creation date
    """
    
    # Columns displayed in list view
    list_display = (
        'text',
        'question_type',
        'correct_answer',
        'order',
        'created_at'
    )
    
    # Filters available in right sidebar
    list_filter = (
        'question_type',
        'created_at',
    )
    
    # Fields searchable via search box
    search_fields = ('text',)
    
    # Fields editable directly in list view
    list_editable = ('order',)
    
    # Organized fieldsets for better form layout
    fieldsets = (
        ('📝 Question Details', {
            'fields': ('text', 'question_type', 'order'),
            'description': 'إدخال نص السؤال ونوعه وترتيب العرض'
        }),
        ('🔤 Multiple Choice Options (MCQ)', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d'),
            'classes': ('collapse',),  # Collapsible section
            'description': 'أضف الخيارات الأربعة للأسئلة متعددة الاختيار فقط'
        }),
        ('✅ Correct Answer', {
            'fields': ('correct_answer',),
            'description': 'الإجابة الصحيحة: A، B، C، D، True، أو False'
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Set readonly fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Pagination
    list_per_page = 20
    
    # Custom sorting in list view
    list_display_links = ('text',)
    
    # Actions dropdown customization
    actions_on_top = True
    actions_on_bottom = False
    
    def get_readonly_fields(self, request, obj=None):
        """
        Dynamically set readonly fields.
        
        Makes timestamps readonly when editing existing questions.
        
        Args:
            request (HttpRequest): The current request
            obj (Question): The object being edited (None if creating new)
            
        Returns:
            tuple: Tuple of readonly field names
        """
        if obj:  # Editing existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        """
        Custom save method with logging.
        
        Args:
            request (HttpRequest): The current request
            obj (Question): The question object
            form (ModelForm): The admin form
            change (bool): True if editing, False if creating
        """
        super().save_model(request, obj, form, change)
    
    class Media:
        """Additional CSS for better admin interface styling"""
        css = {
            'all': ('admin/css/admin_custom.css',)
        }

