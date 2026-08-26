# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from datetime import datetime


class DateTimeUtils:
    """
    Classe utilitaire pour la gestion et le formatage des dates.
    """

    _FORMATS = {
        "timestamp": "%Y%m%d%H%M%S",
        "filename": "%Y%m%d_%H%M%S",
        "date": "%Y-%m-%d",
        "time": "%H:%M:%S",
        "datetime": "%Y-%m-%d %H:%M:%S",
        "iso": "%Y-%m-%dT%H:%M:%S",
    }

    @classmethod
    def now(cls, format_id: str) -> str:
        """
        Retourne la date et l'heure actuelles au format souhaité.

        Parameters
        ----------
        format_id : str, default="timestamp"
            Identifiant du format de sortie.

            Formats prédéfinis disponibles :
            - "timestamp" : YYYYMMDDHHMMSS
            - "filename"  : YYYYMMDD_HHMMSS
            - "date"      : YYYY-MM-DD
            - "time"      : HH:MM:SS
            - "datetime"  : YYYY-MM-DD HH:MM:SS
            - "iso"       : YYYY-MM-DDTHH:MM:SS

            Si le format n'est pas reconnu, il est interprété comme un
            format compatible avec datetime.strftime().

        Returns
        -------
        str
            Date formatée.
        """
        return datetime.now().strftime(cls._FORMATS.get(format_id, format_id))

    @classmethod
    def format_date(
        cls,
        value: str | datetime,
        format_id: str = "datetime",
        input_format: str | None = None,
    ) -> str:
        """
        Formate une date existante.

        Parameters
        ----------
        value : str | datetime
            Date à formater.
            Si une chaîne est fournie, le format d'entrée doit être
            précisé avec `input_format`.

        format_id : str, default="datetime"
            Identifiant du format de sortie.

            Formats prédéfinis disponibles :
            - "timestamp" : YYYYMMDDHHMMSS
            - "filename"  : YYYYMMDD_HHMMSS
            - "date"      : YYYY-MM-DD
            - "time"      : HH:MM:SS
            - "datetime"  : YYYY-MM-DD HH:MM:SS
            - "iso"       : YYYY-MM-DDTHH:MM:SS

            Si le format n'est pas reconnu, il est interprété comme un
            format compatible avec datetime.strftime().

        input_format : str, optional
            Format de la chaîne d'entrée si `value` est une chaîne.

        Returns
        -------
        str
            Date formatée.

        Raises
        ------
        ValueError
            Si `value` est une chaîne et que `input_format` n'est pas fourni.
        """

        if isinstance(value, str):
            if input_format is None:
                raise ValueError(
                    "Le paramètre 'input_format' est obligatoire lorsque 'value' est une chaîne."
                )
            value = datetime.strptime(value, input_format)

        return value.strftime(cls._FORMATS.get(format_id, format_id))