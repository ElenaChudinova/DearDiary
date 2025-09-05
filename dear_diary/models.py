from django.db import models


class Note(models.Model):
    id = models.AutoField(
        auto_created=True, primary_key=True, verbose_name="ID Записи пользователя"
    )
    subject_note = models.CharField(
        max_length=100,
        verbose_name="Тема запись",
        help_text="Введите тему",
        null=True,
        blank=True,
    )
    text_note = models.TextField(
        max_length=10000,
        verbose_name="Текст записи",
        help_text="Введите текст",
        null=True,
        blank=True,
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        default=0,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="user",
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите автора записи",
    )
    public = models.BooleanField(
        verbose_name="Признак публичности записи", default=False
    )
    date_publication = models.DateField(
        blank=False,
        null=False,
        auto_now_add=True,
        verbose_name="Дата публикации записи",
    )
    avatar = models.ImageField(
        upload_to="photos",
        verbose_name="Аватар",
        null=True,
        blank=True,
        help_text="Загрузите изображение",
    )

    def __str__(self):
        return f"{self.subject_note} {self.text_note}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = [
            "subject_note",
            "text_note",
        ]
        permissions = [
            ("can_edit_subject_note", "Can edit subject_note"),
            ("can_edit_text_note", "Can edit text_note"),
        ]
