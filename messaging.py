from struct import unpack_from

import pint


ureg = pint.UnitRegistry()


def parse_inverter_message(message):
    return {
        "numeroSerial":           message[32:48].decode("ascii").rstrip(),
        "voltajeDC":                   0.1 * unpack_from("<H", message, 50)[0],
        "corrienteDC":                       0.1 * unpack_from("<H", message, 54)[0],
        "corrienteGrid":                 round(0.1 * unpack_from("<H", message, 62)[0], 2),
        "voltajeGrid":                 0.1 * unpack_from("<H", message, 68)[0],
        "consumoDiario":          0.01 * unpack_from("<H", message, 76)[0],
        "potenciaInstantanea":             float(unpack_from("<I", message, 116)[0]),
        "consumoMensualActual":          float(unpack_from("<I", message, 120)[0]),
        "consumoMensualAnterior":          float(unpack_from("<I", message, 124)[0]), 
        "consumoAyer":             round(0.1 * unpack_from("<H", message, 128)[0], 2),
        "potenciaAparente":  float(unpack_from("<I", message, 142)[0]),
    }