from django.db import models

from random import choice


class Config(models.Model):

    key = models.CharField(max_length=128)
    active = models.BooleanField(default=True)


class Command(models.Model):

    title = models.CharField(max_length=128, null=False, blank=False)
    command = models.CharField(max_length=1024, default='sudo ', unique=True, null=False, blank=False)
    short_code = models.SlugField(null=False, blank=False, unique=True,
                                  help_text='specify a short code for this command')
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Button(models.Model):

    COLOR_CHOICES = (
        ('random', 'Random'),
        ('#FFC312', 'Sunflower'),
        ('#C4E538', 'Energos'),
        ('#12CBC4', 'Blue Martina'),
        ('#FDA7DF', 'Lavender Rose'),
        ('#ED4C67', 'Bara Red'),
        ('#F79F1F', 'Radiant Yellow'),
        ('#A3CB38', 'Android Green'),
        ('#1289A7', 'Mediterranean Sea'),
        ('#D980FA', 'Lavender Tea'),
        ('#B53471', 'Very Berry'),
        ('#EE5A24', 'Puffins Bill'),
        ('#009432', 'Pixelated Grass'),
        ('#0652DD', 'Merchant Marine Blue'),
        ('#9980FA', 'Forgotten Purple'),
        ('#833471', 'Hollyhock'),
        ('#EA2027', 'Red Pigment'),
        ('#006266', 'Turkish Aqua'),
        ('#1B1464', '20K Leagues Under The Sea'),
        ('#5758BB', 'Circumorbital Ring'),
        ('#6F1E51', 'Magenta Purple'),
    )

    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='buttons')
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='random', null=False, blank=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.command} [ {self.color} ]"

    def save(self, *args, **kwargs):
        if self.color == 'random':
            self.color = choice(
                list(map(lambda c: c[0], self.COLOR_CHOICES[1:]))
            )

        super().save(*args, **kwargs)
