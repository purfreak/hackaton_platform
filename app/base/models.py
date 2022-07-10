from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Hackathon(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    test_py = models.FileField(null=True, blank=True)
    train_py = models.FileField(null=True, blank=True)
    labels_csv = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Team(models.Model):
    name = models.CharField(max_length=50)
    hackathon = models.ForeignKey(
        'Hackathon',
        on_delete=models.CASCADE
    )
    score = models.IntegerField(default=0)
    url = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f'{self.name}'


class HackathonParticipant(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    hackathon = models.ForeignKey(
        'Hackathon',
        on_delete=models.CASCADE
    )


class TeamParticipant(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    class RoleEnum(models.TextChoices):
        CAPTAIN = 'C', _('Captain')
        TEAMMATE = 'T', _('Teammate')
        INVITED = 'I', _('Invited')
        DECLINED = 'D', _('Declined')

    role = models.CharField(
        max_length=1,
        choices=RoleEnum.choices,
        default=RoleEnum.INVITED,
    )
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name="participants"
    )


class Leaderboard(models.Model):
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE
    )
    score = models.IntegerField(default=0)
