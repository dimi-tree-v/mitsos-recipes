from django.db import models


UNITS_OF_MEASUREMENT = [
    # Volume
    ("CUPS", "cups"),
    ("TEASPOONS", "tsps"),
    ("TABLESPOONS", "tbsps"),
    ("MILLILITERS", "ml"),
    ("LITERS", "l"),
    ("FLUID_OUNCES", "fl oz"),
    ("PINTS", "pt"),
    ("QUARTS", "qt"),
    ("GALLONS", "gal"),
    # Weight
    ("GRAMS", "g"),
    ("KILOGRAMS", "kg"),
    ("OUNCES", "oz"),
    ("POUNDS", "lb"),
    # Count / Misc
    ("UNITS", "units"),  # generic: "2 units", "1 unit"
    ("PIECES", "pcs"),  # e.g., "3 pieces of chicken"
    ("SLICES", "slices"),
    ("CLOVES", "cloves"),  # garlic
    ("CAN", "can"),  # canned goods
    ("BUNCH", "bunch"),  # herbs
    ("PINCH", "pinch"),  # small amounts
    ("DASH", "dash"),  # even smaller
]


class Author(models.Model):
    """
    Class defining the author model, the creator of recipes.

    The author is a non-user model in the MVP and articles/ recipes can only
    be added by the admin.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Recipe(models.Model):
    """
    The recipe model defines all ingredients and steps required to
    cook a scrumptious meal or dessert!
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    def __str__(self):
        return f"{self.author}'s {self.title}"


class Step(models.Model):
    """Ordered steps to instruct creation of meal."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField(db_index=True)
    body = models.TextField(max_length=500)

    class Meta:
        ordering = ["order"]
        unique_together = ("recipe", "order")

    def __str__(self):
        return f"Step {self.order} of {self.recipe}"


class Ingredient(models.Model):
    """Food ingredient and quantity required for recipe."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit_of_measurement = models.CharField(
        choices=UNITS_OF_MEASUREMENT,
        max_length=15,
    )
