from django.db import models

from users.models import User


class Category(models.Model):

    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):

        return self.title


class Genre(models.Model):

    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):

        return self.title


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(blank=True, null=True)
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

    def __str__(self):
        return self.text


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
