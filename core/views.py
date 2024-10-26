import pdfplumber
from django.shortcuts import render, redirect
from .models import PDF
from io import BytesIO
from unidecode import unidecode
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string


def import_success(request):
    return render(request, 'import_success.html')


def procesar_lista(contenido):
    # Dividir el contenido en párrafos
    parrafos = contenido.split('\n\n')

    # Iniciar el contenido HTML
    html_contenido = ''

    # Recorrer los párrafos y agregarlos al contenido HTML
    for parrafo in parrafos:
        # Dividir el párrafo en elementos de la lista
        items = parrafo.split('-')

        # Si el delimitador "-" no funcionó, intentar con ""
        if len(items) == 1:
            items = parrafo.split("")
        # Iniciar la lista HTML para el párrafo
        lista_html = '<ul>'

        # Recorrer los elementos y agregarlos a la lista HTML
        for item in items:
            # Eliminar espacios en blanco al inicio y final de cada elemento
            item = item.strip()
            # Si el elemento no está vacío, agregarlo a la lista HTML
            if item:
                lista_html += f'<li>{item}</li>'

        # Cerrar la lista HTML para el párrafo
        lista_html += '</ul>'

        # Agregar la lista HTML al contenido HTML
        html_contenido += lista_html

    return html_contenido


def procesar_contenido(contenido):
    lineas = contenido.splitlines()
    resultado = []
    current_line = {'texto': '', 'nivel': 3}  # Inicializar con nivel 3

    for linea in lineas:
        if linea.strip():
            linea_limpia = linea.strip()
            resultado.append(current_line)
            current_line = {'texto': linea_limpia, 'nivel': 1 if linea_limpia.isupper() else 2}

    resultado.append(current_line)
    return resultado[1:]  # Eliminar el primer elemento inicializado vacío


def pdf_to_html(request):
    pdf_ids = request.GET.getlist('pdf_id')
    print(pdf_ids)  # Obtener lista de IDs de PDF
    if pdf_ids:
        identificaciones = []
        for pdf_id in pdf_ids:
            try:
                # Obtener el objeto PDF correspondiente a la ID proporcionada
                pdf_instance = PDF.objects.get(id=pdf_id)

                # Obtener el texto de evaluación si existe
                evaluacion_texto = ""
                if pdf_instance.evaluacion:
                    evaluacion_texto = pdf_instance.evaluacion.descripcion.replace('\n', '<br>')

                identificacion = {
                    'nombre': pdf_instance.nombre,
                    'materia': pdf_instance.materia,
                    'codigo': pdf_instance.codigo,
                    'condicion': pdf_instance.condicion,
                    'carrera': pdf_instance.carrera,
                    'curso': pdf_instance.curso.nombre if pdf_instance.curso else "",
                    'semestre': pdf_instance.semestre.nombre if pdf_instance.semestre else "",
                    'requisitos': pdf_instance.requisitos,
                    'cargaSemanal': pdf_instance.cargaSemanal,
                    'cargaSemestral': pdf_instance.cargaSemestral,
                }
                secciones = {
                    'II.FUNDAMENTACIÓN.': pdf_instance.fundamentacion,
                    'III.OBJETIVOS.': procesar_lista(pdf_instance.objetivos),
                    'IV.CONTENIDO.': procesar_contenido(pdf_instance.contenido),
                    'V.METODOLOGÍA.': procesar_lista(pdf_instance.metodologia),
                    'VI.EVALUACIÓN': evaluacion_texto,
                    'VII.BIBLIOGRAFÍA.': procesar_lista(pdf_instance.bibliografia),
                }
                identificaciones.append({'identificacion': identificacion, 'secciones': secciones})
                print("Nombre: ", pdf_instance.nombre)
                print("Materia: ", pdf_instance.materia)
            except PDF.DoesNotExist:
                pass  # Manejar la situación en la que el PDF no existe

        # Ordenar identificaciones por el campo 'codigo'
        identificaciones.sort(key=lambda x: x['identificacion']['codigo'])

        if identificaciones:
            html_content = render_to_string('pdf_to_html_template.html', {'identificaciones': identificaciones})
            return HttpResponse(html_content)
        else:
            return HttpResponse("No se encontraron PDFs con las IDs proporcionadas.")
    else:
        return HttpResponse("No se proporcionaron IDs de PDF.")


def eliminar_encabezados_pies_pagina(page):
    # Obtener el tamaño de la página
    width, height = page.width, page.height

    # Recortar la página para eliminar los encabezados
    page = page.within_bbox((0, 0, width, height))

    # Extraer el texto de la página
    page_text = page.extract_text()

    # Eliminar cualquier texto que contenga "Página [número]"
    page_text_lines = page_text.split('\n')
    page_text_filtered = []

    for line in page_text_lines:
        if not line.startswith("Página "):
            # Si la línea no comienza con "Página ", la agregamos sin modificaciones
            page_text_filtered.append(line)
        else:
            # Si la línea comienza con "Página ", la ignoramos
            continue

    # Eliminar la frase "Carrera de Ingeniería en Informática Facultad de Ciencias Tecnológicas – UNC@" si aparece
    # como una frase completa
    page_text_filtered = [
        line.replace("Carrera de Ingeniería en Informática Facultad de Ciencias Tecnológicas – UNC@", "") for line in
        page_text_filtered]

    # Unir las líneas con saltos de línea
    page_text_filtered = '\n'.join(page_text_filtered)

    return page_text_filtered


def importar_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')

        for pdf_file in pdf_files:
            file_data = BytesIO(pdf_file.read())
            pdf_document = pdfplumber.open(file_data)

            text = ""
            for page_number in range(len(pdf_document.pages)):
                page = pdf_document.pages[page_number]

                # Eliminar encabezados y pies de página
                page_text = eliminar_encabezados_pies_pagina(page)

                text += page_text
            if not text:
                continue  # Si el texto está vacío, se pasa al siguiente archivo

            # Utilizar pdfplumber para obtener los títulos del PDF
            titles = []
            for page in pdf_document.pages:
                title_parts = []
                title = ""
                upper_count = 0
                for obj in page.chars:
                    if "Bold" in obj["fontname"]:
                        title += obj["text"]
                        if obj["text"].isupper():
                            upper_count += 1
                    elif title:
                        title_parts.extend(title.split('.')) if '.' in title else title_parts.append(title.strip())
                        title = ""
                for part in title_parts:
                    if part and len(part.strip()) > 8 and sum(1 for c in part if c.isupper()) >= 5:
                        titles.append(part.strip())

            nombre_archivo = pdf_file.name
            del titles[:2]

            # print(titles)
            # Identificar las secciones basadas en los títulos y sus ubicaciones en el texto
            secciones = {}
            patrones_secciones = titles

            for i in range(len(patrones_secciones)):
                start_idx = text.find(patrones_secciones[i])
                end_idx = text.find(patrones_secciones[i + 1]) if i + 1 < len(patrones_secciones) else len(text)
                secciones[patrones_secciones[i]] = text[start_idx:end_idx].strip()

            # Crear una nueva instancia
            pdf_instance = PDF(nombre=nombre_archivo)

            for titulo, texto in secciones.items():
                titulo_normalized = unidecode(titulo)  # Normalizar los caracteres
                if 'IDENTIFICACION' in titulo_normalized:
                    extraer_datos_identificacion(pdf_instance, texto)
                elif 'FUNDAMENTACION' in titulo_normalized:
                    partes_texto = texto.split('.')
                    if len(partes_texto) > 1:
                        texto_fundamentacion = '.'.join(partes_texto[1:-2]).strip()
                    else:
                        texto_fundamentacion = ''
                    pdf_instance.fundamentacion = texto_fundamentacion
                elif 'OBJETIVOS' in titulo_normalized:
                    partes_texto = texto.split('.')
                    if len(partes_texto) > 1:
                        texto_objetivos = '.'.join(partes_texto[1:-2]).strip()
                        if not texto_objetivos:
                            partes_texto = texto.split('\n')
                            print(partes_texto)
                            texto_objetivos = '\n'.join(partes_texto[1:-2]).strip()
                    else:
                        texto_objetivos = ''
                    pdf_instance.objetivos = texto_objetivos
                elif 'CONTENIDO' in titulo_normalized:
                    partes_texto = texto.split('.')
                    if len(partes_texto) > 1:
                        texto_contenido = '.'.join(partes_texto[1:-2]).strip()
                    else:
                        texto_contenido = ''
                    pdf_instance.contenido = texto_contenido
                elif 'METODOLOGIA' in titulo_normalized:
                    partes_texto = texto.split('.')
                    if len(partes_texto) > 1:
                        texto_metodologia = '.'.join(partes_texto[1:-2]).strip()
                    else:
                        texto_metodologia = ''
                    pdf_instance.metodologia = texto_metodologia
                elif 'EVALUACION' in titulo_normalized:
                    partes_texto = texto.split('.')
                    if len(partes_texto) > 1:
                        texto_evaluacion = '.'.join(partes_texto[1:-2]).strip()
                    else:
                        texto_evaluacion = ''
                    pdf_instance.evaluacion = texto_evaluacion
                elif 'BIBLIOGRAFIA' in titulo_normalized:
                    partes_texto = texto.split('\n')
                    print(partes_texto)
                    if len(partes_texto) > 1:
                        texto_bibliografia = '\n'.join(partes_texto[1:]).strip()
                    else:
                        texto_bibliografia = ''
                    pdf_instance.bibliografia = texto_bibliografia
            # Guardar la instancia en la base de datos
            pdf_instance.save()

        return redirect('import_success')
    return render(request, 'import_pdf.html')


def extraer_datos_identificacion(pdf_instance, texto):
    lines = texto.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if 'nombre de la materia' in line.lower():
            pdf_instance.materia = extraer_valor(line, lines[i + 1])
        elif 'código' in line.lower():
            pdf_instance.codigo = extraer_valor(line, lines[i + 1])
        elif 'condición' in line.lower():
            pdf_instance.condicion = extraer_valor(line, lines[i + 1])
        elif 'carrera' in line.lower():
            pdf_instance.carrera = extraer_valor(line, lines[i + 1])
        elif 'curso' in line.lower():
            pdf_instance.curso = extraer_valor(line, lines[i + 1])
        elif 'semestre' in line.lower():
            pdf_instance.semestre = extraer_valor(line, lines[i + 1])
        elif 'requisitos' in line.lower():
            pdf_instance.requisitos = extraer_valor(line, lines[i + 1])
        elif 'semanal' in line.lower():
            pdf_instance.cargaSemanal = extraer_valor(line, lines[i + 1])
        elif 'semestral' in line.lower():
            pdf_instance.cargaSemestral = extraer_valor(line, lines[i + 1])


def extraer_valor(linea_actual, linea_siguiente):
    # Si la línea actual contiene un ':', lo dividimos y tomamos el segundo elemento
    if ':' in linea_actual:
        valor = linea_actual.split(':', 1)[1].strip()
        valor = valor.replace(':', '').strip()
        # Si el valor de la línea actual no está vacío después de eliminar los dos puntos, lo retornamos
        if valor:
            return valor

    # Si la línea siguiente no está vacía, la retornamos como valor
    if linea_siguiente.strip():
        valor_siguiente = linea_siguiente.replace(':', '').strip()
        if valor_siguiente:
            return valor_siguiente

    return None


def get_materiasf(request, codcarrera):
    print(codcarrera)
    materias = list(PDF.objects.filter(codigo__icontains=codcarrera).values())
    if len(materias) <= 0:
        data = {'message': "Not Found"}
    else:
        data = {'message': "Success", 'materias': materias}

    return JsonResponse(data)


def menu(request):
    return render(request, 'menu.html', )