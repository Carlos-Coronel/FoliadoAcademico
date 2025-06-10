from django.db import models


class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    cod_carrera = models.CharField(max_length=45)
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'core_carrera'


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


class Materia(models.Model):
    codigo = models.CharField(primary_key=True, max_length=100)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'materia'


class PDF(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.OneToOneField(Materia, models.DO_NOTHING, db_column='codigo')
    condicion = models.CharField(max_length=100, blank=True, null=True)
    requisitos = models.TextField(blank=True, null=True)
    cargasemanal = models.CharField(db_column='cargaSemanal', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    cargasemestral = models.CharField(db_column='cargaSemestral', max_length=100, blank=True,
                                      null=True)  # Field name made lowercase.
    fundamentacion = models.TextField(blank=True, null=True)
    objetivos = models.TextField(blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    metodologia = models.TextField(blank=True, null=True)
    bibliografia = models.TextField(blank=True, null=True)
    id_carrera = models.ForeignKey(Carrera, models.DO_NOTHING, blank=True, null=True)
    curso = models.ForeignKey(Curso, models.DO_NOTHING, blank=True, null=True)
    semestre = models.ForeignKey(Semestre, models.DO_NOTHING, blank=True, null=True)
    evaluacion = models.ForeignKey(Evaluacion, models.DO_NOTHING, blank=True, null=True)


    def __str__(self):
        return self.nombre
