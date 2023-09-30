import optuna
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import re
import pickle


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
        "metric": "mse",
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

    return mae, r2


def run_optuna(df, n_trials=50):
    study = optuna.create_study(directions=["minimize", "maximize"])
    study.optimize(lambda trial: objective(trial, df), n_trials=n_trials)
    return study.best_trials


if __name__ == "__main__":
    quarterly_data = pd.read_csv("clean_data/quarterly_data.csv")
    dataframes_slctn_cluster = [None] * 4
    # Select all columns except cluster and slctn_number by specific value of cluster AND slctn_number
    cluster_vals = range(4)
    slctn_number_vals = range(4)

    # Get the columns to keep
    columns_to_keep = quarterly_data.columns.difference(
        ["cluster", "slctn_nmbr", "prev_npo_sum"]
    )

    for cluster_val in cluster_vals:
        dataframes_slctn_cluster[cluster_val] = [None] * 4
        for slctn_number_val in slctn_number_vals:
            filtered_df = quarterly_data[
                (quarterly_data["cluster"] == cluster_val)
                & (quarterly_data["slctn_nmbr"] == slctn_number_val)
            ]
            res = filtered_df[columns_to_keep]
            res["prev_npo_sum"] = res["npo_sum"].shift(
                1, fill_value=res.iloc[0]["npo_sum"]
            )
            res = res.rename(columns=lambda x: re.sub("[^A-Za-z0-9_]+", "", x))
            dataframes_slctn_cluster[cluster_val][slctn_number_val] = res

    slctn = 0
    cluster = 3

    best_trials = run_optuna(dataframes_slctn_cluster[slctn][cluster])
    for i, trial in enumerate(best_trials):
        print(i, trial.values)
    with open("model/placeholder.pkl", "wb") as f:
        pickle.dump(best_trials[0].params, f)
