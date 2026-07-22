"""
src/data_loader.py
Funciones de carga e inspección de datos.
Sesión 6: Pandas I — Python Intermedio para Análisis de Datos · DIAN 2026
"""

import pandas as pd


def cargar_declaraciones(ruta, columnas=None):
    """
    Carga un archivo CSV de declaraciones tributarias.

    Args:
        ruta (str): Ruta al archivo CSV.
        columnas (list, optional): Lista de columnas a cargar.
            Si es None, carga todas las columnas.

    Returns:
        pd.DataFrame: DataFrame con las declaraciones cargadas.

    Ejemplos:
        cargar_declaraciones("datos/declaraciones_iva_2025.csv")
        cargar_declaraciones("datos/declaraciones_iva_2025.csv", columnas=["nit", "valor_declarado"])
    """
    dtype = {}
    if columnas is None or "nit" in columnas:
        dtype["nit"] = str
    if columnas is None or "codigo_municipio" in columnas:
        dtype["codigo_municipio"] = str

    df = pd.read_csv(ruta, usecols=columnas, dtype=dtype or None)
    return df


def inspeccionar_datos(df):
    """
    Imprime un reporte de inspección del DataFrame.

    Muestra dimensiones, tipos de dato, conteo de valores faltantes
    por columna y total de filas duplicadas.

    Args:
        df (pd.DataFrame): DataFrame a inspeccionar.

    Returns:
        None
    """
    print("=== Dimensiones ===")
    print(df.shape)
    print("\n=== Tipos de dato ===")
    print(df.dtypes)
    print("\n=== Nulos por columna ===")
    print(df.isnull().sum())
    print("\n=== Total celdas vacías ===")
    print(df.isnull().sum().sum())
    print("\n=== Filas duplicadas ===")
    print(df.duplicated().sum())
    print("\n=== Columnas de texto ===")
    for col in df.select_dtypes(include="object").columns:
        n = df[col].nunique()
        print(f"{col}: {n} valores únicos")
        if n < 20:
            print(df[col].value_counts())

def validar_nulos(df, columnas_criticas):
    for columna in columnas_criticas:
        nulos = df[columna].isnull().sum()
        if nulos > 0:
            print(f"⚠️  {columna}: {nulos} nulos")
        else:
            print(f"✓ {columna}: sin nulos")
    
    """
    Revisa que las columnas críticas no tengan valores faltantes.

    Si alguna columna tiene nulos, imprime el nombre de la columna
    y la cantidad. No detiene la ejecución.

    Args:
        df (pd.DataFrame): DataFrame a validar.
        columnas_criticas (list): Columnas que no deben tener nulos.

    Returns:
        None

    Ejemplos:
        validar_nulos(df, ["nit", "valor_declarado", "estado"])
    """
    for columna in columnas_criticas:
        if columna not in df.columns:
            print(f"Columna no encontrada: {columna}")
            continue

        nulos = df[columna].isnull().sum()
        if nulos > 0:
            print(f"{columna}: {nulos} nulos")


# =============================================================================
# BLOQUE DE PRUEBA
# Se ejecuta solo cuando corres este archivo directamente:
#   python src/data_loader.py
# No se ejecuta cuando main.py importa las funciones.
# Actualiza las llamadas a medida que implementas cada función.
# =============================================================================
def probar_atributo_shape():
    df = pd.read_csv("data/inputs/declaraciones_iva_2025.csv")
    print(df.shape)

probar_atributo_shape()
if __name__ == "__main__":
    df = cargar_declaraciones("data/inputs/declaraciones_iva_2025.csv")
    inspeccionar_datos(df)
    validar_nulos(df, ["nit", "valor_declarado", "estado"])
