#!/usr/bin/env python3
"""Command-line FASTA sequence analyzer.

This script reads DNA sequences from a FASTA file, calculates basic statistics
for each sequence, applies optional filters, and writes the results to a TSV file.

Usage:
    uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv
    uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv --min-len 50
"""

import argparse
import sys
from pathlib import Path


def parsear_argumentos():
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Analiza secuencias de ADN en formato FASTA."
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Ruta del archivo FASTA de entrada.",
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Ruta del archivo TSV de salida.",
    )

    parser.add_argument(
        "--min-len",
        type=int,
        default=None,
        help="Longitud mínima permitida.",
    )

    parser.add_argument(
        "--max-len",
        type=int,
        default=None,
        help="Longitud máxima permitida.",
    )

    parser.add_argument(
        "--min-gc",
        type=float,
        default=None,
        help="Contenido GC mínimo permitido, entre 0.0 y 1.0.",
    )

    parser.add_argument(
        "--max-gc",
        type=float,
        default=None,
        help="Contenido GC máximo permitido, entre 0.0 y 1.0.",
    )

    args = parser.parse_args()
    validar_argumentos(args, parser)

    return args


def validar_argumentos(args, parser):
    """Validate command-line filter arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        parser (argparse.ArgumentParser): Parser used to show clear errors.

    Raises:
        SystemExit: If any argument has an invalid value.
    """
    if args.min_len is not None and args.min_len < 0:
        parser.error("--min-len debe ser mayor o igual a 0.")

    if args.max_len is not None and args.max_len < 0:
        parser.error("--max-len debe ser mayor o igual a 0.")

    if (
        args.min_len is not None
        and args.max_len is not None
        and args.min_len > args.max_len
    ):
        parser.error("--min-len no puede ser mayor que --max-len.")

    if args.min_gc is not None and not 0 <= args.min_gc <= 1:
        parser.error("--min-gc debe estar entre 0.0 y 1.0.")

    if args.max_gc is not None and not 0 <= args.max_gc <= 1:
        parser.error("--max-gc debe estar entre 0.0 y 1.0.")

    if (
        args.min_gc is not None
        and args.max_gc is not None
        and args.min_gc > args.max_gc
    ):
        parser.error("--min-gc no puede ser mayor que --max-gc.")


def leer_fasta(ruta):
    """Read sequences from a FASTA file.

    Args:
        ruta (str): Path to the FASTA input file.

    Returns:
        list[tuple[str, str]]: A list of tuples with header and sequence.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    ruta_fasta = Path(ruta)

    if not ruta_fasta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    secuencias = []
    encabezado_actual = None
    fragmentos_secuencia = []

    with ruta_fasta.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            if linea.startswith(">"):
                if encabezado_actual is not None:
                    secuencia_completa = "".join(fragmentos_secuencia)
                    secuencias.append((encabezado_actual, secuencia_completa))

                encabezado_actual = linea[1:].strip()
                fragmentos_secuencia = []
            else:
                fragmentos_secuencia.append(linea.upper())

    if encabezado_actual is not None:
        secuencia_completa = "".join(fragmentos_secuencia)
        secuencias.append((encabezado_actual, secuencia_completa))

    return secuencias


def calcular_gc(secuencia):
    """Calculate GC content for a DNA sequence.

    Args:
        secuencia (str): DNA sequence.

    Returns:
        float: GC content between 0 and 1.
    """
    if len(secuencia) == 0:
        return 0.0

    cantidad_gc = secuencia.count("G") + secuencia.count("C")

    return cantidad_gc / len(secuencia)


def calcular_estadisticas(encabezado, secuencia):
    """Calculate basic statistics for a sequence.

    Args:
        encabezado (str): FASTA sequence header.
        secuencia (str): DNA sequence.

    Returns:
        dict: Sequence statistics with header, length, and GC content.
    """
    return {
        "encabezado": encabezado,
        "longitud": len(secuencia),
        "contenido_gc": calcular_gc(secuencia),
    }


def pasa_filtros(stats, args):
    """Check whether sequence statistics pass the selected filters.

    Args:
        stats (dict): Sequence statistics.
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        bool: True if the sequence passes all filters, False otherwise.
    """
    longitud = stats["longitud"]
    contenido_gc = stats["contenido_gc"]

    if args.min_len is not None and longitud < args.min_len:
        return False

    if args.max_len is not None and longitud > args.max_len:
        return False

    if args.min_gc is not None and contenido_gc < args.min_gc:
        return False

    if args.max_gc is not None and contenido_gc > args.max_gc:
        return False

    return True


def escribir_resultados(stats, ruta):
    """Write filtered sequence statistics to a TSV file.

    Args:
        stats (list[dict]): Filtered sequence statistics.
        ruta (str): Path to the output TSV file.
    """
    ruta_salida = Path(ruta)

    with ruta_salida.open("w", encoding="utf-8") as archivo:
        archivo.write("encabezado\tlongitud\tcontenido_gc\n")

        for item in stats:
            archivo.write(
                f"{item['encabezado']}\t"
                f"{item['longitud']}\t"
                f"{item['contenido_gc']:.4f}\n"
            )


def main():
    """Run the FASTA analyzer command-line workflow."""
    args = parsear_argumentos()

    try:
        print(f"Leyendo archivo: {args.input}")
        secuencias = leer_fasta(args.input)

        resultados = []

        for encabezado, secuencia in secuencias:
            stats = calcular_estadisticas(encabezado, secuencia)

            if pasa_filtros(stats, args):
                resultados.append(stats)

        escribir_resultados(resultados, args.output)

        print(f"{len(secuencias)} secuencias encontradas")
        print(f"{len(resultados)} secuencias pasan los filtros")
        print(f"Resultados escritos en: {args.output}")

    except FileNotFoundError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()