from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year
from users.models import User


class Category(models.Model):

    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):

        return self.title


class Genre(models.Model):

    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):

        return self.title


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        blank=True,
        null=True,
        validators=(validate_year,),
    )
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name="titles",
        verbose_name="Категория",
        help_text="Категория, к которой будет относиться произведение",
        on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.text


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message="оценка должна быть не меньше 1",
            ),
            MaxValueValidator(
                10,
                message="оценка должна быть не больше 10",
            ),
        )
    )
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

        constraints = [
            models.UniqueConstraint(fields=["title", "author"], name="unique_review")
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
