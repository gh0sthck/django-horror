from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name="Имя")
    description = models.TextField(max_length=512, verbose_name="Описание товара", null=True, blank=True)
    price = models.IntegerField(verbose_name="Цена", default=0)
    image = models.ImageField(verbose_name="Изображение", upload_to="products", null=True, blank=True)

    def __repr__(self):
        return f"<Product: {self.name}>"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"