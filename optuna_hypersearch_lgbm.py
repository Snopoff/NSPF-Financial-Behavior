import optuna
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import re


def train_test_split(df):
    train_size = int(len(df) * 0.8)
    train_data, test_data = df.iloc[:train_size, :], df.iloc[train_size:, :]
    X_train = train_data.loc[:, df.columns != "npo_sum"]
    y_train = train_data.loc[:, "npo_sum"]
    X_test = test_data.loc[:, df.columns != "npo_sum"]
    y_test = test_data.loc[:, "npo_sum"]
    return X_train, y_train, X_test, y_test


def objective(trial, df):
    X_train, y_train, X_test, y_test = train_test_split(df)
    param = {
        "verbose": -1,
        "metric": "mae",
        "random_state": 48,
        "n_estimators": 20000,
        "reg_alpha": trial.suggest_loguniform("reg_alpha", 1e-3, 10.0),
        "reg_lambda": trial.suggest_loguniform("reg_lambda", 1e-3, 10.0),
        "colsample_bytree": trial.suggest_categorical(
            "colsample_bytree", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        ),
        "subsample": trial.suggest_categorical(
            "subsample", [0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
        ),
        "learning_rate": trial.suggest_categorical(
            "learning_rate", [0.006, 0.008, 0.01, 0.014, 0.017, 0.02]
        ),
        "max_depth": trial.suggest_categorical("max_depth", [10, 20, 100]),
        "num_leaves": trial.suggest_int("num_leaves", 1, 1000),
        "min_child_samples": trial.suggest_int("min_child_samples", 1, 300),
        "cat_smooth": trial.suggest_int("min_data_per_groups", 1, 100),
    }
    model = LGBMRegressor(**param)

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
    )

    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    return r2
    return mae, r2


quarterly_data = pd.read_csv("clean_data/quarterly_data.csv")
qdata_0 = quarterly_data.loc[
    quarterly_data.cluster == 0, quarterly_data.columns != "cluster"
]
qdata_0 = qdata_0.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
qdata_1 = quarterly_data.loc[
    quarterly_data.cluster == 1, quarterly_data.columns != "cluster"
]
qdata_1 = qdata_1.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
qdata_2 = quarterly_data.loc[
    quarterly_data.cluster == 2, quarterly_data.columns != "cluster"
]
qdata_2 = qdata_2.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
qdata_3 = quarterly_data.loc[
    quarterly_data.cluster == 3, quarterly_data.columns != "cluster"
]
qdata_3 = qdata_3.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))


def run_optuna(df):
    study = optuna.create_study(
        directions=["maximize"]
    )  # optuna.create_study(directions=["minimize", "maximize"])
    study.optimize(lambda trial: objective(trial, df), n_trials=25)
    return study.best_trial


if __name__ == "__main__":
    quarterly_data = pd.read_csv("clean_data/quarterly_data.csv")
    qdata_0 = quarterly_data.loc[
        quarterly_data.cluster == 0, quarterly_data.columns != "cluster"
    ]
    qdata_0 = qdata_0.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
    qdata_1 = quarterly_data.loc[
        quarterly_data.cluster == 1, quarterly_data.columns != "cluster"
    ]
    qdata_1 = qdata_1.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
    qdata_2 = quarterly_data.loc[
        quarterly_data.cluster == 2, quarterly_data.columns != "cluster"
    ]
    qdata_2 = qdata_2.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
    qdata_3 = quarterly_data.loc[
        quarterly_data.cluster == 3, quarterly_data.columns != "cluster"
    ]
    qdata_3 = qdata_3.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
    num_of_trials, best_trials = run_optuna(qdata_0)
