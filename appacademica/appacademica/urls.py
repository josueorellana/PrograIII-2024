"""
URL configuration for appacademica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from academica.views import hola_mundo, saludo, edad, index, vista, consultar_alumnos, guardar_alumno, consultar_docentes, guardar_docente, consultar_materias, guardar_materia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/', hola_mundo),
    path('saludo/<str:nombre>/', saludo),
    path('edad/<int:edad>/', edad),
    path('', index),
    path('vista/<str:form>/', vista),
    path('consultar_alumnos/', consultar_alumnos),
    path('guardar_alumno/', guardar_alumno),
    path('consultar_docentes/', consultar_docentes),
    path('guardar_docente/', guardar_docente),
    path('consultar_materias/', consultar_materias),
    path('guardar_materia/', guardar_materia),
]
