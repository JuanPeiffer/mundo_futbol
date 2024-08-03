from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    # Crear o obtener grupos
    user_group, _ = Group.objects.get_or_create(name='Usuario')
    creator_group, _ = Group.objects.get_or_create(name='Creador')
    staff_group, _ = Group.objects.get_or_create(name='Staff')

    # Intentar obtener permisos y asignarlos solo si existen
    try:
        add_noticia = Permission.objects.get(codename='add_noticia')
        change_noticia = Permission.objects.get(codename='change_noticia')
        delete_noticia = Permission.objects.get(codename='delete_noticia')

        # Asignar permisos al grupo Creador
        creator_group.permissions.set([add_noticia, change_noticia, delete_noticia])

        # Asignar permisos al grupo Staff
        staff_group.permissions.set([add_noticia, change_noticia, delete_noticia])

        # Eliminar permisos de grupo Usuario
        user_group.permissions.clear()

    except Permission.DoesNotExist:
        print("Algunos permisos no existen aún. Ejecute las migraciones nuevamente después de crear los modelos.")
