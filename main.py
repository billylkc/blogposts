import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_trend(slope, intercept, group, size=1000):
    """ Generate dummy trend data with slope and intercept with a gaussian noise """

    idx = np.arange(start=1, stop=size + 1, step=1)
    y = [slope * x + intercept for x in idx]
    noise = generate_noise(0, 3, size)

    dict = {
        "x": idx,
        "y": np.add(y, noise),
        "group": group,
    }
    df = pd.DataFrame(dict)

    return df


def generate_noise(mu, sigma, size):
    """ Gaussian noise """
    return np.random.normal(mu, sigma, size)


def build_super_model(dd):
    """
    Super Model

    Args:
      dd (Dataframe): Grouped Dataframe

    Return:
      result (Dataframe): Linear Model coefficient with Test set evlauation metrics (e.g. rmse, mape, etc..)
    """
    # TODO: add cross validation
    # Split training and testing set
    X = np.array(dd.x).reshape((-1, 1))
    y = dd.y
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Fit model with train set
    lm = LinearRegression()
    lm.fit(X_train, y_train)

    # Predict on test set
    y_pred = lm.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    result = pd.DataFrame.from_dict(
        {
            "coef": lm.coef_,
            "intercept": lm.intercept_,
            "rmse": rmse,
            "mape": mape,
        }
    )

    return result


def main():

    slopes = [1, 0.4, 0.8]
    intercepts = [3, 4, 5]
    groups = ["a", "b", "c"]

    dfs = map(
        generate_trend,
        slopes,
        intercepts,
        groups,
    )
    df = pd.concat(dfs, 0)

    result = df.groupby("group").apply(lambda x: build_super_model(x))
    result = result.droplevel(1)
    result.reset_index(drop=False, inplace=True)

    # Print result
    print("------------------")
    print("Raw Data \n")
    print(df.head())
    print(df.shape)

    print("------------------")
    print("Predicted \n")
    print(result)

    print("------------------")
    print("Actual \n")
    dict = {
        "group": groups,
        "coef": slopes,
        "intercepte": intercepts,
    }
    print(pd.DataFrame.from_dict(dict))
    print("------------------")


if __name__ == "__main__":
    main()
