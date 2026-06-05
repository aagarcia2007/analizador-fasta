# Requisitos del Analizador de Secuencias FASTA

## Descripción del problema

En bioinformática, el formato FASTA se usa para almacenar secuencias biológicas.
Cada secuencia tiene un encabezado que inicia con `>` y una o más líneas con la
secuencia de ADN.

El problema consiste en crear un programa de línea de comandos que lea un archivo
FASTA, calcule estadísticas básicas de cada secuencia y permita filtrar resultados.

## Objetivo

Construir un programa en Python que procese archivos FASTA y genere un reporte
en formato TSV con estadísticas de longitud y contenido GC.

## Requisitos funcionales

1. El programa debe recibir la ruta del archivo FASTA de entrada.
2. El programa debe recibir la ruta del archivo TSV de salida.
3. El programa debe calcular la longitud de cada secuencia.
4. El programa debe calcular el contenido GC de cada secuencia.
5. El programa debe permitir filtros opcionales:
   - Longitud mínima con `--min-len`
   - Longitud máxima con `--max-len`
   - Contenido GC mínimo con `--min-gc`
   - Contenido GC máximo con `--max-gc`
6. El programa debe escribir los resultados en un archivo TSV.
7. El programa debe mostrar un mensaje claro si el archivo no existe.
8. El programa debe poder ejecutarse con y sin filtros.

## Entrada esperada

Ejemplo sin filtros:

```bash
uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv

Ejemplo con filtros:

uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv --min-len 50 --min-gc 0.4

Salida esperada

En consola:

Leyendo archivo: data/ejemplo.fasta
4 secuencias encontradas
2 secuencias pasan los filtros
Resultados escritos en: resultados.tsv

Archivo resultados.tsv:

encabezado	longitud	contenido_gc
seq1 Homo sapiens BRCA1	78	0.4872
seq3 Homo sapiens TP53	130	0.5538

Casos de prueba funcionales
Caso	Entrada	Acción esperada	Salida esperada
1	data/ejemplo.fasta sin filtros	Analizar todas las secuencias	TSV con todas las secuencias
2	--min-len 50	Filtrar por longitud mínima	TSV solo con secuencias >= 50
3	--min-gc 0.4 --max-gc 0.6	Filtrar por GC	TSV solo con secuencias dentro del rango
4	Archivo inexistente	Mostrar error claro	Mensaje de error sin traceback feo