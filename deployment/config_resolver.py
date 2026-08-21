# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import argparse
from ctypes import ArgumentError
import re
from pathlib import Path
from typing import Any

import yaml


class TokenResolver:
    """Résout les tokens de configuration pour un environnement donné."""

    TOKEN_PATTERN = re.compile(r"\{\{(\??)([A-Z0-9_]+)\}\}")
    _MISSING = object()

    CONFIG_DIRECTORY = Path("deployment/config")
    VARIABLES_DIRECTORY = Path("deployment/variables")
    OUTPUT_DIRECTORY = Path("config")

    @classmethod
    def resolve(cls, environment: str) -> None:
        """
        Résout les fichiers de configuration pour un environnement.

        Args:
            environment: Nom de l'environnement à utiliser.
        """
        variables = cls._load_variables(environment)

        variables = cls._resolve_value(
            variables,
            variables,
        )

        cls.OUTPUT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        for config_file in cls.CONFIG_DIRECTORY.glob("*.yaml"):
            cls._resolve_file(
                config_file=config_file,
                variables=variables,
            )

    @classmethod
    def _load_variables(
        cls,
        environment: str,
    ) -> dict[str, Any]:
        """Charge les variables associées à un environnement."""
        variables_file = (
            cls.VARIABLES_DIRECTORY
            / f"{environment}/variables.yaml"
        )
        
        if not variables_file.exists():
            raise FileNotFoundError(
                f"Environnement inconnu : '{environment}'"
            )

        with variables_file.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    @classmethod
    def _resolve_file(
        cls,
        config_file: Path,
        variables: dict[str, Any],
    ) -> None:
        """Résout un fichier de configuration."""
        with config_file.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        resolved_config = cls._resolve_value(
            config,
            variables,
        )

        output_file = cls.OUTPUT_DIRECTORY / config_file.name

        with output_file.open("w", encoding="utf-8") as file:
            yaml.safe_dump(
                resolved_config,
                file,
                allow_unicode=True,
                sort_keys=False,
            )

    @classmethod
    def _resolve_value(
        cls,
        value: Any,
        variables: dict[str, Any],
    ) -> Any:
        """Résout récursivement les tokens présents dans une valeur."""

        if isinstance(value, dict):
            resolved = {}

            for key, item in value.items():
                resolved_value = cls._resolve_value(
                    item,
                    variables,
                )

                if resolved_value is not cls._MISSING:
                    resolved[key] = resolved_value

            return resolved

        if isinstance(value, list):
            resolved = []

            for item in value:
                resolved_value = cls._resolve_value(
                    item,
                    variables,
                )

                if resolved_value is not cls._MISSING:
                    resolved.append(resolved_value)

            return resolved

        if isinstance(value, str):
            return cls._resolve_string(
                value,
                variables,
            )

        return value

    @classmethod
    def _resolve_string(
        cls,
        value: str,
        variables: dict[str, Any],
    ) -> Any:
        """Résout récursivement les tokens présents dans une chaîne."""

        matches = list(cls.TOKEN_PATTERN.finditer(value))

        if not matches:
            return value

        if (
            len(matches) == 1
            and matches[0].group(0) == value
        ):
            optional = matches[0].group(1) == "?"
            token = matches[0].group(2)

            if token not in variables:
                if optional:
                    return cls._MISSING

                raise KeyError(
                    f"Token de configuration inconnu : '{token}'"
                )

            resolved_value = variables[token]

            if isinstance(resolved_value, str):
                return cls._resolve_string(
                    resolved_value,
                    variables,
                )

            return resolved_value

        def replace(match: re.Match) -> str:
            optional = match.group(1) == "?"
            token = match.group(2)

            if token not in variables:
                if optional:
                    return ""

                raise KeyError(
                    f"Token de configuration inconnu : '{token}'"
                )

            return str(variables[token])

        resolved_value = cls.TOKEN_PATTERN.sub(
            replace,
            value,
        )

        return cls._resolve_string(
            resolved_value,
            variables,
        )

    @staticmethod
    def _get_variable(
        token: str,
        variables: dict[str, Any],
    ) -> Any:
        """Retourne la valeur associée à un token."""
        if token not in variables:
            raise KeyError(
                f"Token de configuration inconnu : '{token}'"
            )

        return variables[token]
    
def main() -> None:
    """Résout la configuration pour l'environnement demandé."""
    parser = argparse.ArgumentParser(
        description="Résout la configuration pour un environnement."
    )

    parser.add_argument(
        "--environment",
        required=True,
        help="Environnement cible.",
    )

    args = parser.parse_args()

    if args:
        TokenResolver.resolve(args.environment)
    else:
        raise ArgumentError("Arguments non renseignées")


if __name__ == "__main__":
    main()