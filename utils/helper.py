def erradicate_accents(s: str) -> str:
    return str(s).replace("á", "a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")

def format_str(s: str) -> str:
    return erradicate_accents(str(s).lower().strip())

dates = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
}