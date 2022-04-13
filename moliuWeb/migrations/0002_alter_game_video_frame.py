# Generated by Django 4.0.2 on 2022-04-13 16:42

from django.db import migrations, models
import django.db.models.deletion
import moliuWeb.models


class Migration(migrations.Migration):

    dependencies = [
        ("moliuWeb", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="video",
            field=models.FileField(upload_to=moliuWeb.models.videoUploadPath),
        ),
        migrations.CreateModel(
            name="Frame",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        choices=[
                            (-1, "Non Scored"),
                            (0, "Very Bad"),
                            (25, "Bad"),
                            (50, "Regular"),
                            (75, "Good"),
                            (100, "Very Good"),
                        ],
                        default=-1,
                    ),
                ),
                ("frameImage", models.CharField(max_length=250)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="moliuWeb.game"
                    ),
                ),
            ],
        ),
    ]
