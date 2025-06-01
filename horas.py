import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee ficText, normaliza expresiones horarias y escribe el resultado en ficNorm.
    Expresiones incorrectas se dejan tal cual.
    """
    def corrige_hora(match):
        h = int(match.group(1))
        m = int(match.group(2)) if match.group(2) else 0
        if 0 <= h < 24 and 0 <= m < 60:
            return f'{h:02}:{m:02}'
        else:
            return match.group(0)

    def corrige_hhmm(match):
        h = int(match.group(1))
        m = int(match.group(2))
        if 0 <= h < 24 and 0 <= m < 60:
            return f'{h:02}:{m:02}'
        else:
            return match.group(0)

    def corrige_en_punto(match):
        h = int(match.group(1))
        if 1 <= h <= 12:
            return f'{h % 12:02}:00'
        else:
            return match.group(0)

    def corrige_y_cuarto_media(match):
        h = int(match.group(1))
        sufijo = match.group(2)
        if 1 <= h <= 12:
            if "cuarto" in sufijo:
                return f'{h % 12:02}:15'
            elif "media" in sufijo:
                return f'{h % 12:02}:30'
        return match.group(0)

    def corrige_menos_cuarto(match):
        h = int(match.group(1))
        if 2 <= h <= 12:
            return f'{(h - 1) % 12:02}:45'
        return match.group(0)

    def corrige_con_periodo(match):
        h = int(match.group(1))
        m = 0
        periodo = match.group(2)
        if periodo == "de la mañana":
            if 4 <= h <= 12:
                return f'{h % 12:02}:{m:02}'
        elif periodo == "del mediodía":
            if 12 <= h <= 15:
                return f'{(h if h < 13 else h - 12) + 12:02}:{m:02}'
        elif periodo == "de la tarde":
            if 3 <= h <= 8:
                return f'{(h + 12) % 24:02}:{m:02}'
        elif periodo == "de la noche":
            if 8 <= h <= 11:
                return f'{h % 12:02}:{m:02}'
            elif h == 12:
                return f'00:{m:02}'
        elif periodo == "de la madrugada":
            if 1 <= h <= 6:
                return f'{h % 12:02}:{m:02}'
        return match.group(0)

    with open(ficText, encoding='utf-8') as fin, open(ficNorm, 'w', encoding='utf-8') as fout:
        for linea in fin:
            original = linea

            # HH:MM (hora estándar)
            linea = re.sub(r'\b(\d{1,2}):(\d{2})\b', corrige_hora, linea)

            # 8h27m, 7h, etc.
            linea = re.sub(r'\b(\d{1,2})h(\d{1,2})m\b', corrige_hhmm, linea)
            linea = re.sub(r'\b(\d{1,2})h\b', lambda m: f'{int(m.group(1)):02}:00' if 0 <= int(m.group(1)) < 24 else m.group(0), linea)

            # 8 en punto
            linea = re.sub(r'\b(\d{1,2}) en punto\b', corrige_en_punto, linea)

            # 8 y cuarto / 8 y media
            linea = re.sub(r'\b(\d{1,2}) y (cuarto|media)\b', corrige_y_cuarto_media, linea)

            # 8 menos cuarto
            linea = re.sub(r'\b(\d{1,2}) menos cuarto\b', corrige_menos_cuarto, linea)

            # 7 de la mañana / tarde / noche / madrugada
            linea = re.sub(r'\b(\d{1,2}) (de la mañana|de la noche|del mediodía|de la tarde|de la madrugada)\b', corrige_con_periodo, linea)

            fout.write(linea)

if __name__ == '__main__':
    normalizaHoras('horas.txt', 'horas_normalizadas.txt')
