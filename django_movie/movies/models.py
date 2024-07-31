from datetime import datetime
from django.db import models

class Category(models.Model):
    """ Категории """

    name = models.CharField(
        "Категория",
        max_length=150,
    )
    description = models.TextField(
        "Описание",
    )
    url = models.SlugField(
        max_length=160,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name
    

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """ Актеры и режиссёры """

    name = models.CharField(
        "Имя",
        max_length=100,
    )
    age = models.PositiveSmallIntegerField(
        "Возраст",
        default=0
    )
    description = models.TextField(
        "Описание"
    )
    image = models.ImageField(
        "Изображение",
        upload_to="actors/",
    )

    def __str__(self) -> str:
        return self.name
    

    class Meta:
        verbose_name = "Актеры и режиссёры"
        verbose_name_plural = "Актеры и режиссёры"


class Genre(models.Model):
    """ Жанры """

    name = models.CharField(
        "Имя",
        max_length=100
    )
    description = models.TextField("Описание")
    url = models.SlugField(
        max_length=160,
        unique=True
    )

    def __str__(self) -> str:
        return self.name
    

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """ Фильмы """

    title = models.CharField(
        "Название",
        max_length=100
    )
    tagline = models.CharField(
        "Слоган",
        max_length=100,
        default=""
    )
    description = models.TextField("Описание")
    poster = models.ImageField(
        "Постер",
        upload_to="movies/",
    )
    year = models.PositiveSmallIntegerField(
        "Год выпуска",
        default=2024
    )
    country = models.CharField(
        "Страна",
        max_length=100,
        default="Россия"
    )
    directors = models.ManyToManyField(
        Actor,
        verbose_name="Режиссёры",
        related_name="film_directors",
    )
    actors = models.ManyToManyField(
        Actor,
        verbose_name="Актеры",
        related_name="film_actors",
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name="Жанры",
        related_name="film_genres",
    )
    world_premiere = models.DateField(
        "Премьера в мире",
        default=datetime.today,
    )
    budget = models.PositiveIntegerField(
        "Бюджет",
        default=0,
        help_text="В миллионах долларов"
    )
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США",
        default=0,
        help_text="В миллионах долларов"
    )
    fees_in_world = models.PositiveIntegerField(
        "Сборы в мире",
        default=0,
        help_text="В миллионах долларов"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        related_name="film_category",
    )
    url = models.SlugField(
        max_length=160,
        unique=True
    )
    draft = models.BooleanField(
        "Черновик",
        default=False
    )

    def __str__(self) -> str:
        return self.title
    

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """ Кадры из фильма """

    title = models.CharField(
        "Заголовок",
        max_length=100
    )
    description = models.TextField("Описание")
    image = models.ImageField(
        "Изображение",
        upload_to="movie_shots/",
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name="Фильм",
        on_delete=models.CASCADE,
        related_name="movie_shots",
    )

    def __str__(self) -> str:
        return self.title
    

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(
        "Значение",
        default=0
        
        # choices=[
        #     (1, "1"),
        #     (2, "2"),
        #     (3, "3"),
        #     (4, "4"),
        #     (5, "5"),
        # ]
    )

    def __str__(self) -> str:
        return self.value

    class Meta:
        verbose_name = "Звезда"
        verbose_name_plural = "Звезды"


class Rating(models.Model):
    """ Рейтинги фильмов """

    ip = models.CharField(
        "IP адрес",
        max_length=15,
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name="Звезда",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="Фильм",
    )

    def __str__(self) -> str:
        return f"{self.star.value} - {self.movie.title}"
    

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """ Отзывы """

    email = models.EmailField("E-mail")
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Текст отзыва", max_length=5000)
    parent = models.ForeignKey(
        "self",
        verbose_name="Родительский отзыв",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name="Фильм",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.movie.title}"
    

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
