from django.contrib.auth.models import BaseUserManager

class ManejadorUsuario(BaseUserManager):

    def create_user(self, usuario, password=None):
        if not usuario:
            raise ValueError('El usuario debe ser valido')

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_staffuser(self, usuario, password=None):
        usuario = self.create_user(usuario, password)
        usuario.staff = True
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, usuario, password=None):
        usuario = self.create_user(usuario, password)
        usuario.staff = True
        usuario.amin = True
        usuario.save(using=self._db)
        return usuario