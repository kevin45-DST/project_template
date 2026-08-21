# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

class NumericsUtils:
    """Utilitaires liés aux valeurs numériques."""

    @staticmethod    
    def parse_file_size(value: str | int) -> int:
        """Convertit une taille exprimée en octets ou avec une unité."""

        if isinstance(value, int):
            return value

        value = value.strip().upper()

        units = {
            "KB": 1024,
            "MB": 1024 ** 2,
            "GB": 1024 ** 3,
        }

        for unit, multiplier in units.items():
            if value.endswith(unit):
                number = float(value[:-len(unit)])
                return int(number * multiplier)

        return int(value)