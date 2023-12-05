from django.contrib import admin

import feedback.models

__all__ = []


class PersonalDataInline(admin.TabularInline):
    model = feedback.models.PersonalData
    readonly_fields = ("mail", "name")
    can_delete = False


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            old_status = feedback.models.Feedback.objects.get(
                id=obj.id,
            ).get_status_display()
            new_status = obj.get_status_display()
            if old_status != new_status:
                feedback.models.StatusLog.objects.create(
                    user=request.user,
                    feedback=obj,
                    from_status=old_status,
                    to=new_status,
                )
        super().save_model(request, obj, form, change)

    list_display = (feedback.models.Feedback.status.field.name,)

    readonly_fields = [
        feedback.models.Feedback.text.field.name,
    ]

    inlines = [
        PersonalDataInline,
    ]
