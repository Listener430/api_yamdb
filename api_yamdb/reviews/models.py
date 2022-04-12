from django.db import models


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
        help_text="Категория, к которой будет относиться произведени",
    )
    genres = models.ManyToManyField(Genres, through="GenresTitle")

    def __str__(self):
        return self.text


class GenresTitle(models.Model):
    genres = models.ForeignKey(Genres)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genres} {self.title}"


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
    rating = models.IntegerField(choices=[i for i in range(10)])


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
