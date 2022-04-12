from django.db import models

from users.models import User


class Categories(models.Model):

    title = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):

        return self.title


class Genres(models.Model):

    title = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):

        return self.title


class Title(models.Model):
    text = models.TextField()
    categories = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        related_name="titles",
        verbose_name="Категория",
        help_text="Категория, к которой будет относиться произведение",
        on_delete=models.CASCADE,
    )
    genres = models.ManyToManyField(
        Genres, through="GenresTitle", related_name="titles"
    )

    def __str__(self):
        return self.text


class GenresTitle(models.Model):
    genres = models.ForeignKey(Genres, on_delete=models.PROTECT)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genres} {self.title}"


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
    rating = models.IntegerField()


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
