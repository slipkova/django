from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


def attachment_path(instance, filename):
    return "film/" + str(instance.film.id) + "/attachments/" + filename


def poster_path(instance, filename):
    return "film/" + str(instance.id) + "/poster/" + filename


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Genre name",
                            help_text="Enter a film genre (e.g. sci-fi, comedy)")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    plot = models.TextField(blank=True, null=True, verbose_name="Plot")
    release_date = models.DateField(blank=True, null=True,
                                    help_text="Please use the following format: <em>YYYY-MM - DD < / em >.",
                                    verbose_name="Release date")
    runtime = models.IntegerField(blank=True, null=True,
                                  help_text="Please enter an integer value (minutes)",
                                  verbose_name="Runtime")
    rate = models.FloatField(default=5.0,
                             validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
                             null=True,
                             help_text="Please enter an float value (range 1.0 - 10.0)",
                             verbose_name="Rate")

    poster = models.ImageField(upload_to=poster_path, blank=True, null=True, verbose_name="Poster")
    genres = models.ManyToManyField(Genre, help_text='Select a genre for this film')

    class Meta:
        ordering = ["-release_date", "title"]

    def __str__(self):

        return f"{self.title}, year: {str(self.release_date.year)}, rate: {str(self.rate)}"

    def get_absolute_url(self):

        return reverse('film-detail', args=[str(self.id)])


class Attachment(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")

    # Časový údaj o poslední aktualizaci přílohy - automaticky se ukládá aktuální čas
    last_update = models.DateTimeField(auto_now=True)

    # Pole pro upload souboru
    # Parametr upload_to zajistí uložení souboru do složky specifikované v návratové hodnotě metody attachment_path
    file = models.FileField(upload_to=attachment_path, null=True, verbose_name="File")

    # Konstanta, v níž jsou ve formě n-tic (tuples) předdefinovány různé typy příloh
    TYPE_OF_ATTACHMENT = (
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('video', 'Video'),
        ('other', 'Other'),
    )

    # Pole s definovanými předvolbami pro uložení typu přílohy
    type = models.CharField(max_length=5, choices=TYPE_OF_ATTACHMENT, blank=True, default='image',
                            help_text='Select allowed attachment type', verbose_name="Attachment type")

    # Cizí klíč, který zajišťuje propojení přílohy s daným filmem (vztah N:1)
    # Parametr on_delete slouží k zajištění tzv. referenční integrity - v případě odstranění filmu
    # budou odstraněny i všechny jeho přílohy (models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    # Metadata
    class Meta:
        # Primární seřazeno podle poslední aktualizace souborů, sekundárně podle typu přílohy

        ordering = ["-last_update", "type"]

    # Methods
    def __str__(self):
        """ Textová reprezentace objektu """

        return f"{self.title}, ({self.type})"