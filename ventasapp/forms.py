from django.forms import ModelForm
from django import forms
import datetime

from .models.bodega import Bodega
from .models.color import Color
from .models.genero import Genero
from .models.motivo import Motivo
from .models.producto import Producto
from .models.silueta import Silueta
from .models.material import Material
from .models.diseno import Diseno
from .models.talla import Talla
from .models.venta_no_realizada import VentaNoRealizada
from .models.usuario_bodega import Usuario_Bodega

class BodegaCrearForm(ModelForm):
    class Meta:
        model = Bodega
        fields = ['codigo', 'descripcion']
    
    def __init__(self, *args, **kwargs): 
        super(BodegaCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False


class BodegaEditarForm(ModelForm):
    class Meta:
        model = Bodega
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(BodegaEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class ColorCrearForm(ModelForm):
    class Meta:
        model = Color
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(ColorCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class ColorEditarForm(ModelForm):
    class Meta:
        model = Color
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(ColorEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class GeneroCrearForm(ModelForm):
    class Meta:
        model = Genero
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(GeneroCrearForm, self).__init__(*args, **kwargs)                     
        self.fields['descripcion'].required = False
        
        instance = kwargs.get('instance')
        if instance:
            self.fields['codigo'].initial = instance.codigo
            self.fields['descripcion'].initial = instance.descripcion

class GeneroEditarForm(ModelForm):
    class Meta:
        model = Genero
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(GeneroEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class MotivoCrearForm(ModelForm):
    class Meta:
        model = Motivo
        fields = ['codigo', 'descripcion']
    
    def __init__(self, *args, **kwargs): 
        super(MotivoCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class MotivoEditarForm(ModelForm):
    class Meta:
        model = Motivo
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(MotivoEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class ProductoCrearForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(ProductoCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class ProductoEditarForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(ProductoEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class SiluetaCrearForm(ModelForm):
    class Meta:
        model = Silueta
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(SiluetaCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class SiluetaEditarForm(ModelForm):
    class Meta:
        model = Silueta
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(SiluetaEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class MaterialCrearForm(ModelForm):
    class Meta:
        model = Material
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(MaterialCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class MaterialEditarForm(ModelForm):
    class Meta:
        model = Material
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(MaterialEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class DisenoCrearForm(ModelForm):
    class Meta:
        model = Diseno
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(DisenoCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class DisenoEditarForm(ModelForm):
    class Meta:
        model = Diseno
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(DisenoEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class TallaCrearForm(ModelForm):
    class Meta:
        model = Talla
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(TallaCrearForm, self).__init__(*args, **kwargs)                       
        self.fields['descripcion'].required = False

class TallaEditarForm(ModelForm):
    class Meta:
        model = Talla
        fields = ['codigo', 'descripcion']

    def __init__(self, *args, **kwargs): 
        super(TallaEditarForm, self).__init__(*args, **kwargs)                       
        self.fields['codigo'].disabled = True
        self.fields['descripcion'].required = False

class DateInput(forms.DateInput):
    input_type = 'date'

class NumberInput(forms.TextInput):
    input_type = 'number'

class VentaNoRealizadaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genero']=forms.ModelChoiceField(queryset=Genero.objects.all().order_by('descripcion'),
                                                     widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['genero'].required = False
        self.fields['genero'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'


        self.fields['bodega'].required = False
        self.fields['bodega'].disabled = True

        self.fields['producto']=forms.ModelChoiceField(queryset=Producto.objects.all().order_by('descripcion'),
                                                        widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['producto'].required = False
        self.fields['producto'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'
        
        self.fields['color']=forms.ModelChoiceField(queryset=Color.objects.all().order_by('descripcion'),
                                                     widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['color'].required = False
        self.fields['color'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'

        self.fields['talla']=forms.ModelChoiceField(queryset=Talla.objects.all().order_by('descripcion'),
                                                     widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['talla'].required = False
        self.fields['talla'].label_from_instance = lambda obj: f'{obj.descripcion}'
        
        self.fields['silueta']=forms.ModelChoiceField(queryset=Silueta.objects.all().order_by('descripcion'),
                                                       widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['silueta'].required = False
        self.fields['silueta'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'

        self.fields['motivo']=forms.ModelChoiceField(queryset=Motivo.objects.all().order_by('descripcion'),
                                                      widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['motivo'].required = True
        self.fields['motivo'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'

        self.fields['diseno']=forms.ModelChoiceField(queryset=Diseno.objects.all().order_by('descripcion'),
                                                      widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['diseno'].required = False
        self.fields['diseno'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'

        self.fields['material']=forms.ModelChoiceField(queryset=Material.objects.all().order_by('descripcion'),
                                                        widget=forms.Select(attrs={'class':'form-control'}))
        self.fields['material'].required = False
        self.fields['material'].label_from_instance = lambda obj: f'{obj.codigo} - {obj.descripcion}'
        


    class Meta:
        model = VentaNoRealizada
        fields = '__all__'
        widgets = {
            'edad': NumberInput(attrs={'min': '0', 'max': '99', 'step': '1','class': 'form-control'},),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
                                
        }

