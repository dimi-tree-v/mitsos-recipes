"""Configure the admin interface for the recipes app."""

from django.contrib import admin
from .models import Ingredient, Recipe, Author, Step


class StepInline(admin.TabularInline):
    """Step inline to enble CRUD of recipe steps for a given recipe."""

    model = Step
    extra = 0


class Ingredientsline(admin.TabularInline):
    """Step inline to enble CRUD of recipe ingredients for a given recipe."""

    model = Ingredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for the Recipe model."""

    list_display = (
        "title",
        "author",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "author__first_name", "author__last_name")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [Ingredientsline, StepInline]


class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for the Author model."""

    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Author, AuthorAdmin)
