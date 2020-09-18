
from django.contrib import admin

from school.models import Person, Course, Grade
from django import forms
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    def clean_first_name(self):
        if self.cleaned_data["first_name"] == "Spike":
            raise forms.ValidationError("No Vampires")

        return self.cleaned_data["first_name"]
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    fields = ("first_name", "last_name", "courses")
    search_fields = ("last_name__startswith", )
    list_display = ("last_name", "first_name", "show_average")
    pass
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["first_name"].label = "First Name (Humans only!):"
        return form

    def show_average(self, obj):
        from django.db.models import Avg
        result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
        return result["grade__avg"]

    class Meta:
        ordering = ("last_name", "first_name")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
     list_display = ("name", "year", "view_students_link")
     list_filter = ("year", )
     def view_students_link(self, obj):
         count = obj.person_set.count()
         url = (
             reverse("admin:school_person_changelist")
             + "?"
             + urlencode({"courses__id": f"{obj.id}"})
         )
         return format_html('<a href="{}">{} Students</a>', url, count)

     view_students_link.short_description = "Students"
    
pass 

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass

