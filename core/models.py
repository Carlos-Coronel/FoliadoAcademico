from django.db import models


class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'carrera'


class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'curso'


class Semestre(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'semestre'


class Evaluacion(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion[:50]  # Muestra los primeros 50 caracteres

    class Meta:
        db_table = 'evaluacion'


class PDF(models.Model):
    id_carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    materia = models.CharField(max_length=100, null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, blank=True)
    condicion = models.CharField(max_length=100, null=True, blank=True)
    carrera = models.CharField(max_length=100, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.SET_NULL, null=True, blank=True)
    requisitos = models.TextField(null=True, blank=True)
    cargaSemanal = models.CharField(max_length=100, null=True, blank=True)
    cargaSemestral = models.CharField(max_length=100, null=True, blank=True)
    fundamentacion = models.TextField(null=True, blank=True)
    objetivos = models.TextField(null=True, blank=True)
    contenido = models.TextField(null=True, blank=True)
    metodologia = models.TextField(null=True, blank=True)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.SET_NULL, null=True, blank=True)
    bibliografia = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
