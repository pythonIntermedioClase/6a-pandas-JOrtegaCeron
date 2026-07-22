"""
main.py
Flujo ETL: carga, inspección, clasificación y exportación de declaraciones IVA.
Sesión 6: Pandas I — Python Intermedio para Análisis de Datos · DIAN 2026
"""

# =============================================================================
# IMPORTS
# Todos los imports van aquí, al inicio del archivo, antes de cualquier otra
# línea de código. Nunca dentro de funciones ni distribuidos a lo largo del
# código. A medida que implementas cada módulo, descomenta el import
# correspondiente.
import numpy as np
import pandas as pd
from datetime import date

# Sección 3:
# from src.data_loader import cargar_declaraciones
#
# Sección 4 — agrega las dos funciones nuevas al import de data_loader:
from src.data_loader import cargar_declaraciones, inspeccionar_datos, validar_nulos
#
# Sección 5:
from src.data_transformer import clasificar_por_valor, agregar_identificador_periodo, preparar_columnas_salida
#
# Sección 6:
from src.data_exporter import exportar_csv, exportar_excel_por_categoria
# =============================================================================


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

RUTA_DATOS = "data/inputs/declaraciones_iva_2025.csv"
CARPETA_RESULTADOS = "data/outputs"
COLUMNAS_CRITICAS = ["nit", "valor_declarado", "estado"]
COLUMNAS_SALIDA = [
    "identificador_periodo",
    "nit",
    "razon_social",
    "municipio",
    "periodo",
    "valor_declarado",
    "nivel_riesgo",
    "estado",
]


# =============================================================================
# MENÚ
# Esta función ya está implementada. Ejecútala, lee el código y úsala como
# referencia para entender el ciclo del programa.
# =============================================================================

def mostrar_menu():
    """Muestra el menú principal y retorna la opción elegida por el usuario."""
    print("\n" + "=" * 45)
    print("  Pipeline — Declaraciones IVA 2025")
    print("=" * 45)
    print("  1. Cargar datos")
    print("  2. Inspeccionar datos")
    print("  3. Transformar datos")
    print("  4. Exportar resultados")
    print("  5. Ejecutar pipeline completo")
    print("  0. Salir")
    print("=" * 45)
    return input("  Opción: ").strip()


# =============================================================================
# PIPELINE
# __main__ solo llama a main(). La lógica vive en funciones, no a nivel de
# módulo: así puedes importar main.py desde otros scripts sin efectos.
# =============================================================================

def main():
    """Ejecuta el pipeline interactivo de declaraciones IVA."""

    # df y df_salida se declaran aquí para que todas las opciones del menú
    # puedan leerlas y modificarlas. Arrancan en None hasta que se ejecute
    # la carga.
    df = None
    df_salida = None

    opcion = mostrar_menu()

    while opcion != "0":

        # -----------------------------------------------------------------
        # OPCIÓN 1: CARGA
        # El import ya está en el bloque de arriba, solo descoméntalo.
        # Completa los espacios marcados con ___ y ejecuta.
        # -----------------------------------------------------------------
        if opcion == "1":
            df = cargar_declaraciones(RUTA_DATOS)
            print(f"Filas cargadas: {len(df)}")
            

        # -----------------------------------------------------------------
        # OPCIÓN 2: INSPECCIÓN
        # Tienes los nombres de las funciones. Escribe las llamadas completas.
        # Antes de llamar a inspeccionar_datos(), verifica que df no sea None;
        # si lo es, muestra un mensaje y vuelve al menú.
        # Funciones disponibles: inspeccionar_datos(), validar_nulos()
        # -----------------------------------------------------------------
        elif opcion == "2":
            if df is None:
                print("Primero carga los datos con la opción 1.")
            else:
                inspeccionar_datos(df)
                validar_nulos(df, COLUMNAS_CRITICAS)

        # -----------------------------------------------------------------
        # OPCIÓN 3: TRANSFORMACIÓN
        # - Clasificar cada registro en nivel de riesgo (Alto / Medio / Bajo)
        #   con umbral_alto=10_000_000 y umbral_medio=5_000_000.
        # - Agregar la columna identificador_periodo.
        # - Guardar en df_salida solo las columnas de COLUMNAS_SALIDA.
        # Verifica que df no sea None antes de transformar.
        # -----------------------------------------------------------------
        elif opcion == "3":
            if df is None:
                print("Primero carga los datos con la opción 1.")
            else:
                df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
                df = agregar_identificador_periodo(df)
                df_salida = preparar_columnas_salida(df, COLUMNAS_SALIDA)
                print(df_salida.head())

        # -----------------------------------------------------------------
        # OPCIÓN 4: EXPORTACIÓN
        # Genera un CSV y un Excel en data/outputs/.
        # -----------------------------------------------------------------
        elif opcion == "4":
            if df_salida is None:
                print("Primero transforma los datos con la opción 3.")
            else:
                exportar_csv(df_salida, CARPETA_RESULTADOS, "declaraciones_clasificadas")
                exportar_excel_por_categoria(df_salida, CARPETA_RESULTADOS, "declaraciones", "nivel_riesgo")
                print("Archivos generados en", CARPETA_RESULTADOS)

        # -----------------------------------------------------------------
        # OPCIÓN 5: PIPELINE COMPLETO
        # Ejecuta las cuatro etapas anteriores en secuencia.
        # -----------------------------------------------------------------
        elif opcion == "5":
            # Cargar
            df = cargar_declaraciones(RUTA_DATOS)
            print(f"Filas cargadas: {len(df)}")
            # Inspeccionar
            inspeccionar_datos(df)
            validar_nulos(df, COLUMNAS_CRITICAS)
            # Transformar
            df = clasificar_por_valor(df, umbral_alto=10_000_000, umbral_medio=5_000_000)
            df = agregar_identificador_periodo(df)
            df_salida = preparar_columnas_salida(df, COLUMNAS_SALIDA)
            print(df_salida.head())
            # Exportar
            exportar_csv(df_salida, CARPETA_RESULTADOS, "declaraciones_clasificadas")
            exportar_excel_por_categoria(df_salida, CARPETA_RESULTADOS, "declaraciones", "nivel_riesgo")
            print("Pipeline completo. Archivos generados en", CARPETA_RESULTADOS)

        else:
            print("  Opción no válida. Intenta de nuevo.")

        opcion = mostrar_menu()

    print("  Hasta luego.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
def probar_acceso_diccionario():
    declaracion = {"nit": "800234567-0", "estado": "Pendiente","valor_declarado": 1_500_000}
    print(declaracion["valor_declarado"])

def revisar_declaracion(declaracion):
    for clave, valor in declaracion.items():
        print(f"{clave}: {valor}")
    declaracion["estado"] = "Revisada"
    print(f"\nEstado actualizado: {declaracion['estado']}")
def probar_np_where():
    df = pd.read_csv("data/inputs/declaraciones_iva_2025.csv")
    df["categoria"] = np.where(df["valor_declarado"] >= 5_000_000, "Alto", np.where(df["valor_declarado"] >= 1_000_000, "Medio", "Bajo"))
    print(df[["valor_declarado", "categoria"]].head())

#probar_np_where()

if __name__ == "__main__":
    declaracion = {
        "nit": "900123456-1",
        "razon_social": "Comercializadora Andina S.A.S",
        "valor_declarado": 4_500_000,
        "estado": "Presentada",
        "municipio": "Bogotá",
    }
    revisar_declaracion(declaracion)
    # main()

    #def probar_acceso_serie():
    #serie = pd.Series([100, 200, 300])
    #print(serie[5])

    def explorar_dataframe():
        datos = {
            "nit": ["900123456-1", "800234567-0", "700345678-9", "600456789-8"],
            "razon_social": ["Empresa A", "Empresa B", "Empresa C", "Empresa D"],
            "municipio": ["Bogotá", "Cali", "Medellín", "Barranquilla"],
            "valor_declarado": [4_500_000, 12_300_000, 2_100_000, 8_750_000],
            }
        df = pd.DataFrame(datos)
        print(df.index)
        print(df.columns)
        print(df.shape)
        df.to_excel("declaraciones.xlsx")


if __name__ == "__main__":
    explorar_dataframe()
    # main()

    def analizar_serie(nits, valores):
        serie = pd.Series(valores, index=nits)
        print(f"Media:        {serie.mean()}")
        print(f"Máximo:       {serie.max()}")
        print(f"Mínimo:       {serie.min()}")
        print(f"NIT con mayor valor: {serie.idxmax()}")


if __name__ == "__main__":
    nits    = ["900111222-0", "800333444-5", "700555666-1", "600777888-2", "500999000-3"]
    valores = [4_500_000, 12_300_000, 2_100_000, 8_750_000, 15_200_000]
    analizar_serie(nits, valores)
    # main()

    def construir_dataframe(lista_declaraciones):
        df = pd.DataFrame(lista_declaraciones)
        print(f"Elementos en la lista: {len(lista_declaraciones)}")
        print(f"Filas en el DataFrame: {len(df)}")
        return df

def probar_exportar_excel():
    df = pd.DataFrame({"a": [1, 2]})
    df.to_excel("data/outputs/prueba.xlsx", index=False)

probar_exportar_excel()

if __name__ == "__main__":
    declaraciones = [
        {"nit": "900111222-0", "razon_social": "Empresa A", "valor_declarado": 4_500_000},
        {"nit": "800333444-5", "razon_social": "Empresa B", "valor_declarado": 12_300_000},
        {"nit": "700555666-1", "razon_social": "Empresa C", "valor_declarado": 2_100_000},
    ]
    construir_dataframe(declaraciones)
    main()