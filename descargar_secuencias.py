#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para descargar secuencias desde NCBI
Taller PyLadies Cuernavaca - Entornos Virtuales

Compatible con: Windows, Mac, Linux

Uso:
    Windows (Anaconda Prompt):
        python descargar_secuencias.py --email TU_EMAIL@ejemplo.com
    
    Mac/Linux (Terminal):
        python descargar_secuencias.py --email TU_EMAIL@ejemplo.com
    
    O simplemente (si el script es ejecutable en Mac/Linux):
        ./descargar_secuencias.py --email TU_EMAIL@ejemplo.com
"""

import argparse
from Bio import Entrez, SeqIO
from pathlib import Path

def descargar_secuencia(accession, email, output_dir):
    """
    Descarga una secuencia desde NCBI y la guarda en formato FASTA
    
    Args:
        accession: ID de acceso (ej: NC_045512)
        email: Tu email para NCBI
        output_dir: Carpeta donde guardar
    """
    # Configurar email para NCBI (requisito de NCBI)
    Entrez.email = email
    
    # Crear carpeta si no existe
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Nombre del archivo de salida
    output_file = output_dir / f"{accession}.fasta"
    
    # Si ya existe, saltar
    if output_file.exists():
        print(f"  ✓ Ya descargado: {accession}")
        return True
    
    try:
        # Descargar secuencia desde NCBI
        print(f"  Descargando {accession}...", end=" ")
        
        handle = Entrez.efetch(
            db="nucleotide",     # Base de datos de nucleótidos
            id=accession,        # ID de la secuencia
            rettype="fasta",     # Formato FASTA
            retmode="text"       # Modo texto
        )
        
        # Leer la secuencia
        record = SeqIO.read(handle, "fasta")
        handle.close()
        
        # Guardar en archivo
        SeqIO.write(record, output_file, "fasta")
        
        # Mostrar información
        print(f"✓ ({len(record.seq)} nucleótidos)")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    # Configurar argumentos del script
    parser = argparse.ArgumentParser(
        description='Descargar secuencias desde NCBI usando Biopython'
    )
    
    parser.add_argument(
        '--email',
        required=True,
        help='Tu email (requerido por NCBI)'
    )
    
    parser.add_argument(
        '--input',
        default='secuencias.txt',
        help='Archivo con lista de IDs (default: secuencias.txt)'
    )
    
    parser.add_argument(
        '--output',
        default='secuencias_descargadas',
        help='Carpeta de salida (default: secuencias_descargadas)'
    )
    
    args = parser.parse_args()
    
    # Leer archivo con lista de IDs
    print("\n" + "="*60)
    print("DESCARGADOR DE SECUENCIAS NCBI - PYLADIES CUERNAVACA")
    print("="*60)
    
    with open(args.input) as f:
        accessions = [line.strip() for line in f if line.strip()]
    
    print(f"\nTotal de secuencias a descargar: {len(accessions)}")
    print(f"Guardando en: {args.output}/\n")
    
    # Descargar cada secuencia
    exitosas = 0
    fallidas = 0
    
    for i, accession in enumerate(accessions, 1):
        print(f"[{i}/{len(accessions)}] {accession}:", end=" ")
        
        if descargar_secuencia(accession, args.email, args.output):
            exitosas += 1
        else:
            fallidas += 1
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"✓ Exitosas: {exitosas}")
    print(f"✗ Fallidas:  {fallidas}")
    print(f"\nArchivos guardados en: {args.output}/")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
