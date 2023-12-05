from django.contrib import admin

import rating.models

__all__ = []

admin.site.register(rating.models.Rating)
