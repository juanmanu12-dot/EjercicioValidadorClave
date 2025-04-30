from abc import ABC, abstractmethod

from validadorclave.modelo.errores import (
    NoCumpleLongitudMinimaError,
    NoTieneCaracterEspecialError,
    NoTieneLetraMayusculaError,
    NoTieneLetraMinusculaError,
    NoTieneNumeroError,
    NoTienePalabraSecretaError
)


class ReglaValidacion(ABC):

    def __init__(self, _longitud_esperada: int) -> None:
        self._longitud_esperada: int = _longitud_esperada

    def _validar_longitud(self, clave: str) -> bool:
        return len(clave) > self._longitud_esperada

    def _contiene_mayuscula(self, clave: str) -> bool:
        return any(char.isupper() for char in clave)

    def _contiene_minuscula(self, clave: str) -> bool:
        return any(char.islower() for char in clave)

    def _contiene_numero(self, clave: str) -> bool:
        return any(char.isdigit() for char in clave)

    @abstractmethod
    def es_valida(self, clave: str) -> bool:
        ...


class ReglaValidacionGanimedes(ReglaValidacion):

    def __init__(self) -> None:
        super().__init__(_longitud_esperada=8)

    def contiene_caracter_especial(self, clave: str) -> bool:
        especiales = "@_#$%"
        return any(char in especiales for char in clave)

    def es_valida(self, clave: str) -> bool:
        validation_dict = {
            "length": self._validar_longitud(clave),
            "upper": self._contiene_mayuscula(clave),
            "lower": self._contiene_minuscula(clave),
            "digit": self._contiene_numero(clave),
            "esp_char": self.contiene_caracter_especial(clave)
        }

        keys = list(validation_dict.keys())
        values = list(validation_dict.values())

        if False in values:
            position = values.index(False)
            error = keys[position]

            if error == "length":
                raise NoCumpleLongitudMinimaError(f"La clave debe tener una longitud de más de {self._longitud_esperada} caracteres")
            elif error == "upper":
                raise NoTieneLetraMayusculaError("La clave no contiene al menos una letra mayúscula")
            elif error == "lower":
                raise NoTieneLetraMinusculaError("La clave no contiene al menos una letra minúscula")
            elif error == "digit":
                raise NoTieneNumeroError("La clave no contiene al menos un número")
            elif error == "esp_char":
                raise NoTieneCaracterEspecialError("La clave debe contener al menos un carácter especial: @_#$%")

        return True


class ReglaValidacionCalisto(ReglaValidacion):

    def __init__(self) -> None:
        super().__init__(_longitud_esperada=6)

    def contiene_calisto(self, clave: str) -> bool:
        palabra = "calisto"
        if palabra.lower() in clave.lower():
            indice = clave.lower().index(palabra.lower())
            original = clave[indice:indice + len(palabra)]
            mayusculas = sum(1 for c in original if c.isupper())
            if 2 <= mayusculas < len(palabra):
                return True
        return False

    def es_valida(self, clave: str) -> bool:
        validation_dict = {
            "length": self._validar_longitud(clave),
            "upper": self._contiene_mayuscula(clave),
            "lower": self._contiene_minuscula(clave),
            "digit": self._contiene_numero(clave),
            "calisto": self.contiene_calisto(clave)
        }

        keys = list(validation_dict.keys())
        values = list(validation_dict.values())

        if False in values:
            position = values.index(False)
            error = keys[position]

            if error == "length":
                raise NoCumpleLongitudMinimaError(f"La clave debe tener una longitud de más de {self._longitud_esperada} caracteres")
            elif error == "upper":
                raise NoTieneLetraMayusculaError("La clave no contiene al menos una letra mayúscula")
            elif error == "lower":
                raise NoTieneLetraMinusculaError("La clave no contiene al menos una letra minúscula")
            elif error == "digit":
                raise NoTieneNumeroError("La clave no contiene al menos un número")
            elif error == "calisto":
                raise NoTienePalabraSecretaError("La palabra 'calisto' debe estar escrita con al menos dos letras en mayúscula")

        return True


class Validador:
    def __init__(self, regla: ReglaValidacion) -> None:
        self.regla = regla

    def es_valida(self, clave: str) -> bool:
        return self.regla.es_valida(clave)
