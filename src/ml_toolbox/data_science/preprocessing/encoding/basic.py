# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

from typing import Any, Literal

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


class BasicEncoding:
    """
    Méthodes d'encodage de base.

    Ces méthodes permettent de transformer les variables
    catégorielles en variables numériques.

    Toutes les méthodes retournent :

        (
            X_train_encodé,
            X_test_encodé,
            y_train,
            y_test,
            encoder,
        )

    L'encodeur retourné doit être réutilisé pour transformer
    les données de validation, de test et de production.
    """

    @staticmethod
    def one_hot(
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: Any,
        y_test: Any,
        columns: list[str],
        drop: str | None = None,
        handle_unknown: Literal[
                        "error",
                        "ignore",
                        "infrequent_if_exist",
                        ] = "ignore",
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        Any,
        Any,
        OneHotEncoder,
    ]:
        """
        Encodage One-Hot.

        Une colonne est créée pour chaque modalité.

        À utiliser lorsque :
        - les variables sont nominales
        - il n'existe pas d'ordre entre les catégories

        Avantages :
        - très largement utilisé
        - évite d'introduire un ordre artificiel
        - compatible avec la plupart des modèles

        Inconvénients :
        - peut créer un grand nombre de colonnes
        """

        encoder = OneHotEncoder(
            drop=drop,
            handle_unknown=handle_unknown,
            sparse_output=False,
        )

        train_encoded = encoder.fit_transform(
            X_train[columns]
        )

        test_encoded = encoder.transform(
            X_test[columns]
        )

        encoded_columns = encoder.get_feature_names_out(
            columns
        )

        train_encoded = pd.DataFrame(
            np.asarray(train_encoded),
            columns=encoded_columns,
            index=X_train.index,
        )

        test_encoded = pd.DataFrame(
            np.asarray(test_encoded),
            columns=encoded_columns,
            index=X_test.index,
        )

        X_train = pd.concat(
            [
                X_train.drop(columns=columns),
                train_encoded,
            ],
            axis=1,
        )

        X_test = pd.concat(
            [
                X_test.drop(columns=columns),
                test_encoded,
            ],
            axis=1,
        )

        return (
            X_train,
            X_test,
            y_train,
            y_test,
            encoder,
        )
        
    @staticmethod
    def ordinal(
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: Any,
        y_test: Any,
        columns: list[str],
        handle_unknown: Literal[
                            "error",
                            "use_encoded_value",
                        ] = "use_encoded_value",
        unknown_value: int = -1,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        Any,
        Any,
        OrdinalEncoder,
    ]:
        """
        Encodage ordinal.

        Chaque catégorie est remplacée par un entier.

        À utiliser lorsque :
        - les variables possèdent un ordre naturel
        (faible < moyen < élevé)
        - certains modèles nécessitent des données numériques

        Avantages :
        - très simple
        - ne crée pas de nouvelles colonnes
        - peu coûteux en mémoire

        Inconvénients :
        - introduit un ordre numérique
        - à éviter sur les variables nominales
        """

        encoder = OrdinalEncoder(
            handle_unknown=handle_unknown,
            unknown_value=unknown_value,
        )

        X_train = X_train.copy()
        X_test = X_test.copy()

        X_train.loc[:, columns] = encoder.fit_transform(
            X_train[columns]
        )

        X_test.loc[:, columns] = encoder.transform(
            X_test[columns]
        )

        return (
            X_train,
            X_test,
            y_train,
            y_test,
            encoder,
        )