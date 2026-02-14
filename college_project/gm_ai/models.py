from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# =========================
# CUSTOM USER (XARIDOR)
# =========================
class CustomUser(AbstractUser):

    full_name = models.CharField("To‘liq ism", max_length=255)

    # Nullable qoldiramiz migratsiya muammosi chiqmasligi uchun
    city = models.CharField(
        "Shahar",
        max_length=100,
        null=True,
        blank=True
    )

    passport_id = models.CharField(
        "Passport ID",
        max_length=20,
        unique=True
    )

    phone = models.CharField(
        "Telefon",
        max_length=20
    )

    permanent_address = models.TextField(
        "Doimiy manzil"
    )

    def __str__(self):
        return f"{self.username} - {self.full_name}"


# =========================
# AUTOSALON (DILER)
# =========================
class Autosalon(models.Model):

    name = models.CharField(
        "Avtosalon nomi",
        max_length=255
    )

    city = models.CharField(
        "Shahar",
        max_length=100
    )

    address = models.TextField(
        "Manzil"
    )

    phone = models.CharField(
        "Telefon",
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Avtosalon"
        verbose_name_plural = "Avtosalonlar"
        ordering = ["city", "name"]

    def __str__(self):
        return f"{self.name} ({self.city})"


# =========================
# CONTRACT (SHARTNOMA)
# =========================
class Contract(models.Model):

    MODEL_CHOICES = [
        ("Captiva", "Chevrolet Captiva"),
        ("Tracker", "Chevrolet Tracker"),
        ("Onix", "Chevrolet Onix"),
    ]

    MODIFICATION_CHOICES = [
        ("lt2", "LT 2"),
        ("premier", "Premier"),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="contracts"
    )

    autosalon = models.ForeignKey(
        Autosalon,
        on_delete=models.CASCADE,
        related_name="contracts"
    )

    model = models.CharField(
        max_length=50,
        choices=MODEL_CHOICES,
        db_index=True
    )

    modification = models.CharField(
        max_length=50,
        choices=MODIFICATION_CHOICES
    )

    color = models.CharField(
        max_length=50
    )

    contract_number = models.CharField(
        max_length=50,
        unique=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Shartnoma"
        verbose_name_plural = "Shartnomalar"

    def save(self, *args, **kwargs):
        """
        Agar contract_number bo‘lmasa avtomatik generatsiya qiladi:
        UZM-2026-0001
        """
        if not self.contract_number:
            year = timezone.now().year
            last_contract = Contract.objects.filter(
                created_at__year=year
            ).order_by("-id").first()

            if last_contract and last_contract.contract_number:
                last_number = int(last_contract.contract_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.contract_number = f"UZM-{year}-{str(new_number).zfill(4)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.contract_number} | {self.user.username}"
