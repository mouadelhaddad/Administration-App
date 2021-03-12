from django import forms
from auth_sys_ICCN.models import GestionServeur
from auth_sys_ICCN.models import GestionUtilisateur

class GestionServeurForm(forms.ModelForm):
    class Meta:
        model = GestionServeur
        fields = "__all__"

class GestionUtilisateurForm(forms.ModelForm):
    class Meta:
        model = GestionUtilisateur
        fields = "__all__"
