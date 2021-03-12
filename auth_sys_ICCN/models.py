from django.db import models


# Create your models here.
class GestionServeur(models.Model):
    password = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100,default="")

    class Meta:
        verbose_name = "gestion serveur"
        ordering = ['id']

    def __str__(self):
         return ' '.join([
        self.password,
        self.ip_address,
    ])

class GestionUtilisateur(models.Model):
    username = models.CharField(max_length=100)
    userpassword = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)

    class Meta:
        verbose_name = "gestion utilisateur"
        ordering = ['id']

    def __str__(self):
         return ' '.join([
         self.username,
         self.userpassword,
         self.ip_address,
    ])
