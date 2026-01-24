#!/usr/bin/env python3
import re
import sys
import os
from collections import Counter
from datetime import datetime

# ----------------- CONFIGURACIÓN -----------------

# Primera capa: dominios a excluir siempre (lista base)
DOMINIOS_EXCLUIR_PRIMARIOS = {
    "hotmail.com",
    "gmail.com",
    "live.com.mx",
    "live.com",
    "outlook.com",
    "yahoo.com",
    "yahoo.com.mx",
    "hotmail.com.mx",
    "icloud.com",
    "icloud.com.mx",
    "outlook.com.mx",
    "prodigy.net.mx",
    "msn.com",
    "terra.com.mx",
    "gmail.com.mx",
    "gmail.mx",
    "outlook.es",
    "hotmail.es",
    "yopmail.com",
    "gmbol.cem",
    "aol.com",
    "mail.com",
    "hotmail.co.uk",
    "me.com",
    "aol.co.uk",
    "yahoo.es",
    "gmail.co.uk",
    "gamil.com",
    "gmx.de",
    "blueyonder.co.uk",
    "qq.com",
    "protonmail.com",
    "email.com",
    "yahoo.com.br",
    "gmial.com",
    "fastweb.it",
    "gmail.co",
    "rocketmail.com",
    "t-online.de",
    "googlemail.com",
    "deped.gov.ph",
    "neuf.fr",
    "live.com.ar",
    "live.co.uk",
    "wp.pl",
    "outlook.nl",
    "gmil.com",
    "tin.it",
    "mailinator.com",
    "hotmail.nl",
    "gmal.com",
    "otmail.com",
    "bluewin.ch"
    "xs4all.nl",
    "bbox.fr",
    "yahoo.de",
    "hotmail.at"
    "tele2.nl"
    "hushmail.com"
    "wanadoo.es",
    "vodafone.de"
    "cathayhotel.com.tw",
    "live.co",
    "yandex.com",
    "yahoo.it",
    "mailbox92.biz",
    "kpnmail.nl",
    "o2.pl",
    "inbox.ru",
    "live.de",
    "anom.xyz",
    "gmaio.com",
    "hotnail.com",
    "yahoo.ca",
    "outlook.com.ar",
    "twocowmail.net",
}

# Segunda capa: top mundiales + otros free populares/temporales
DOMINIOS_FREE_EXTRA = {
    # Top globales y variantes comunes (free / ISP / públicos)
    "gmail.com", "gmail.com.mx", "gmail.com.br", "gmail.co", "gmail.es",
    "yahoo.com", "yahoo.com.mx", "yahoo.com.br", "yahoo.es", "yahoo.fr",
    "yahoo.co.uk", "yahoo.com.ar", "yahoo.it", "yahoo.de", "yahoo.ca",
    "hotmail.com", "hotmail.com.mx", "hotmail.es", "hotmail.fr", "hotmail.it",
    "hotmail.co.uk", "hotmail.de",
    "outlook.com", "outlook.com.mx", "outlook.es",
    "live.com", "live.com.mx", "live.fr", "live.co.uk", "live.it",
    "aol.com", "aol.co.uk",
    "icloud.com", "icloud.com.mx", "me.com", "mac.com",
    "mail.com",
    "gmx.de", "gmx.com", "gmx.net", "gmx.es",
    "proton.me", "protonmail.com",
    "zoho.com", "zohomail.com",
    "mail.ru", "yandex.com", "yandex.ru",
    "uol.com.br", "bol.com.br",
    "web.de",
    "libero.it", "virgilio.it", "tiscali.it",
    "wanadoo.fr", "orange.fr", "orange.es",
    "comcast.net", "verizon.net", "sbcglobal.net", "bellsouth.net",
    "charter.net", "shaw.ca", "bigpond.com", "bigpond.net.au",
    "rocketmail.com", "ymail.com",
    "qq.com",
    "free.fr",
    "laposte.net",
    "cox.net",
    "blueyonder.co.uk", "bluewin.ch",
    "sky.com",
    "ntlworld.com",
    # Temporales / desechables muy comunes
    "yopmail.com", "yopmail.net",
    "mailinator.com",
    "temp-mail.org", "guerrillamail.com", "10minutemail.com",
    "trashmail.com", "maildrop.cc", "getnada.com", "spambox.me",
    # Otras variantes vistas / typo-squats típicos
    "gmail.con", "gamil.com", "gmai.com", "gmial.com", "gmal.com",
    "gmaii.com", "gmaio.com", "gmaill.com", "gmail.net",
    "hotmail.con", "hotmal.com", "hotmaill.com", "hotmial.com",
    "hotmial.co.uk", "hotmailc.om", "hotmail.com.com", "hotmail.co",
    "outlook.de", "outlook.pt", "outlook.nl",
}

# Unión de ambas listas para limpieza profunda
DOMINIOS_EXCLUIR_DEEP = DOMINIOS_EXCLUIR_PRIMARIOS | DOMINIOS_FREE_EXTRA

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

# ----------------- TEXTOS IDIOMA -----------------

TEXTOS = {
    "es": {
        "descripcion": (
            "Este script limpia archivos de combos email:password,\n"
            "eliminando dominios gratuitos conocidos y líneas inválidas,\n"
            "para conservar principalmente correos corporativos.\n"
            "Creado por @BlackHat_RedCat.\n"
        ),
        "uso": "Uso: python corporatizarv2.py <archivo_o_carpeta> [es|en]",
        "sin_archivo": "Debes especificar un archivo o carpeta de entrada.",
        "idioma_no_valido": "Idioma no válido, se usará español por defecto.",
        "inicio": "Iniciando análisis y limpieza...",
        "fin": "Análisis terminado. Archivo resultante:",
        "fin_lote": "Procesamiento de carpeta terminado.",
        "estadisticas": "ESTADÍSTICAS DE LIMPIEZA",
        "total_lineas": "Líneas totales leídas",
        "validas_emailpass": "Líneas válidas email:password",
        "removidas_formato": "Líneas removidas por formato inválido",
        "removidas_dominios": "Líneas removidas por dominios excluidos",
        "final_corporativo": "Líneas finales (posible correo corporativo)",
        "por_dominios": "Distribución por dominio en el resultado",
        "fecha": "Fecha de análisis",
        "header_archivo": (
            "Este archivo es el resultado de la limpieza de combos "
            "email:password para excluir dominios gratuitos conocidos "
            "y resaltar posibles correos corporativos.\n"
            "Creado por @BlackHat_RedCat.\n"
        ),
        "porcentaje": "Porcentaje",
    },
    "en": {
        "descripcion": (
            "This script cleans email:password combo files,\n"
            "removing known free mail domains and invalid lines,\n"
            "keeping mostly corporate emails.\n"
            "Created by @BlackHat_RedCat.\n"
        ),
        "uso": "Usage: python corporatizarv2.py <file_or_folder> [es|en]",
        "sin_archivo": "You must specify an input file or folder.",
        "idioma_no_valido": "Invalid language, defaulting to Spanish.",
        "inicio": "Starting analysis and cleaning...",
        "fin": "Analysis completed. Output file:",
        "fin_lote": "Folder processing completed.",
        "estadisticas": "CLEANING STATISTICS",
        "total_lineas": "Total lines read",
        "validas_emailpass": "Valid email:password lines",
        "removidas_formato": "Lines removed due to invalid format",
        "removidas_dominios": "Lines removed due to excluded domains",
        "final_corporativo": "Final lines (possible corporate emails)",
        "por_dominios": "Domain distribution in the result",
        "fecha": "Analysis date",
        "header_archivo": (
            "This file is the result of cleaning email:password combos "
            "to exclude known free-mail domains and highlight possible "
            "corporate emails.\n"
            "Created by @BlackHat_RedCat.\n"
        ),
        "porcentaje": "Percentage",
    },
}

# ----------------- FUNCIONES -----------------


def validar_email(email: str) -> bool:
    return EMAIL_REGEX.fullmatch(email) is not None


def extraer_email_password(linea: str):
    linea = linea.strip()
    if not linea:
        return None, None
    # Normaliza separadores
    linea = linea.replace(",", ":").replace("|", ":").replace(" ", "")
    partes = linea.split(":")
    if len(partes) != 2:
        return None, None
    email, password = partes
    email = email.strip()
    password = password.strip()
    if not email or not password:
        return None, None
    if not validar_email(email):
        return None, None
    return email, password


def obtener_dominio(email: str) -> str:
    partes = email.split("@", 1)
    if len(partes) != 2:
        return ""
    return partes[1].lower()


def es_dominio_excluido_deep(dominio: str) -> bool:
    return dominio in DOMINIOS_EXCLUIR_DEEP


def construir_nombre_salida(ruta_archivo: str) -> str:
    base_dir = os.path.dirname(ruta_archivo) or "."
    base_name = os.path.basename(ruta_archivo)
    nombre, ext = os.path.splitext(base_name)
    nuevo_nombre = f"{nombre}_corporatizado{ext or '.txt'}"
    return os.path.join(base_dir, nuevo_nombre)


def limpiar_archivo(ruta_archivo: str, lang: str = "es"):
    txt = TEXTOS[lang]

    total_lineas = 0
    validas_emailpass = 0
    removidas_formato = 0
    removidas_dominios = 0

    lineas_finales = []
    contador_dominios = Counter()

    with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            total_lineas += 1
            email, password = extraer_email_password(linea)

            if email is None:
                removidas_formato += 1
                continue

            validas_emailpass += 1
            dominio = obtener_dominio(email)

            # Limpieza profunda: excluye primarios + top free + temporales
            if es_dominio_excluido_deep(dominio):
                removidas_dominios += 1
                continue

            registro = f"{email}:{password}"
            lineas_finales.append(registro)
            if dominio:
                contador_dominios[dominio] += 1

    ruta_salida = construir_nombre_salida(ruta_archivo)
    fecha_analisis = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_final = len(lineas_finales)

    with open(ruta_salida, "w", encoding="utf-8") as out:
        # Descripción y fecha
        out.write(txt["header_archivo"])
        out.write("\n")
        out.write(f"{txt['fecha']}: {fecha_analisis}\n")
        out.write("\n")
        out.write(f"{txt['estadisticas']}\n")
        out.write("-" * 60 + "\n")
        out.write(f"{txt['total_lineas']}: {total_lineas}\n")
        out.write(f"{txt['validas_emailpass']}: {validas_emailpass}\n")
        out.write(f"{txt['removidas_formato']}: {removidas_formato}\n")
        out.write(f"{txt['removidas_dominios']}: {removidas_dominios}\n")
        out.write(f"{txt['final_corporativo']}: {total_final}\n")
        out.write("\n")
        out.write(f"{txt['por_dominios']}:\n")

        if total_final > 0:
            for dominio, count in sorted(
                contador_dominios.items(), key=lambda x: x[1], reverse=True
            ):
                porcentaje = (count / total_final) * 100
                out.write(
                    f"  {dominio}: {count} "
                    f"({porcentaje:.2f}% {txt['porcentaje']})\n"
                )
        else:
            out.write("  (sin datos)\n")

        out.write("\n")
        out.write("-" * 60 + "\n")
        out.write("\n")

        # Combos finales
        for registro in lineas_finales:
            out.write(registro + "\n")

    return ruta_salida


def escribir_resumen_global(ruta_salida_global, lang, registros, contador_dominios):
    txt = TEXTOS[lang]
    fecha_analisis = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_final = len(registros)
    total_lineas = total_final  # ya son líneas limpias
    validas_emailpass = total_final

    with open(ruta_salida_global, "w", encoding="utf-8") as out:
        out.write(txt["header_archivo"])
        out.write("\n")
        out.write(f"{txt['fecha']}: {fecha_analisis}\n")
        out.write("\n")
        out.write(f"{txt['estadisticas']} (GLOBAL)\n")
        out.write("-" * 60 + "\n")
        out.write(f"{txt['total_lineas']}: {total_lineas}\n")
        out.write(f"{txt['validas_emailpass']}: {validas_emailpass}\n")
        out.write(f"{txt['removidas_formato']}: 0\n")
        out.write(f"{txt['removidas_dominios']}: 0\n")
        out.write(f"{txt['final_corporativo']}: {total_final}\n")
        out.write("\n")
        out.write(f"{txt['por_dominios']}:\n")

        if total_final > 0:
            for dominio, count in sorted(
                contador_dominios.items(), key=lambda x: x[1], reverse=True
            ):
                porcentaje = (count / total_final) * 100
                out.write(
                    f"  {dominio}: {count} "
                    f"({porcentaje:.2f}% {txt['porcentaje']})\n"
                )
        else:
            out.write("  (sin datos)\n")

        out.write("\n")
        out.write("-" * 60 + "\n")
        out.write("\n")

        for registro in sorted(registros):
            out.write(registro + "\n")


def seleccionar_idioma(argv):
    if len(argv) >= 3:
        lang = argv[2].lower()
        if lang not in ("es", "en"):
            print(TEXTOS["es"]["idioma_no_valido"])
            return "es"
        return lang
    return "es"


def procesar_entrada(ruta: str, lang: str = "es"):
    txt = TEXTOS[lang]

    # Acumuladores globales
    global_registros = set()
    global_dominios = Counter()

    if os.path.isdir(ruta):
        print(txt["inicio"])
        for nombre in os.listdir(ruta):
            ruta_completa = os.path.join(ruta, nombre)
            if not os.path.isfile(ruta_completa):
                continue
            if not nombre.lower().endswith(".txt"):
                continue

            print(f"[+] Limpiando archivo: {ruta_completa}")
            salida = limpiar_archivo(ruta_completa, lang=lang)
            print(f"    -> {txt['fin']} {salida}")

            # Leer el archivo ya corporatizado para acumular al global
            with open(salida, "r", encoding="utf-8", errors="ignore") as f:
                cuerpo = False
                for linea in f:
                    linea = linea.rstrip("\n")
                    if not cuerpo:
                        # cuando llegamos a la línea de separación "---"
                        if linea.strip().startswith("---"):
                            cuerpo = True
                        continue
                    if not linea:
                        continue
                    if ":" not in linea:
                        continue

                    email, pwd = linea.split(":", 1)
                    email = email.strip()
                    pwd = pwd.strip()
                    if not EMAIL_REGEX.fullmatch(email):
                        continue

                    dominio = obtener_dominio(email)
                    if not dominio:
                        continue

                    registro = f"{email}:{pwd}"
                    if registro not in global_registros:
                        global_registros.add(registro)
                        global_dominios[dominio] += 1

        # escribir archivo global en la misma carpeta
        ruta_salida_global = os.path.join(ruta, "global_corporatizado.txt")
        escribir_resumen_global(
            ruta_salida_global, lang, global_registros, global_dominios
        )
        print(f"[+] Archivo global: {ruta_salida_global}")
        print(txt["fin_lote"])

    else:
        print(txt["inicio"])
        salida = limpiar_archivo(ruta, lang=lang)
        print(f"{txt['fin']} {salida}")


def main():
    if len(sys.argv) < 2:
        print(TEXTOS["es"]["sin_archivo"])
        print(TEXTOS["es"]["uso"])
        sys.exit(1)

    ruta_entrada = sys.argv[1]
    lang = seleccionar_idioma(sys.argv)
    txt = TEXTOS[lang]

    print(txt["descripcion"])
    procesar_entrada(ruta_entrada, lang=lang)


if __name__ == "__main__":
    main()
