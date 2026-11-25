# Dati misti (numerici + categorici) con ColumnTransformer
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

df = pd.DataFrame({
    "eta":     [23, 45, 31, 52, 38, 29, 61, 44, 35, 50] * 10,
    "reddito": [18, 52, 30, 61, 40, 22, 75, 48, 33, 58] * 10,
    "citta":   ["MI", "RM", "NA", "MI", "TO", "RM", "MI", "NA", "TO", "RM"] * 10,
    "compra":  [0, 1, 0, 1, 1, 0, 1, 1, 0, 1] * 10,
})
X, y = df.drop(columns="compra"), df["compra"]

prep = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["citta"]),   # testo -> colonne 0/1
], remainder="passthrough")                                      # numeriche invariate

modello = Pipeline([("prep", prep),
                    ("rf", RandomForestClassifier(random_state=0))])

ricerca = RandomizedSearchCV(
    modello,
    param_distributions={"rf__n_estimators": randint(100, 500),
                         "rf__min_samples_leaf": randint(1, 10)},
    n_iter=10, cv=5, random_state=0)
ricerca.fit(X, y)
print(ricerca.best_params_)
print(ricerca.predict(pd.DataFrame({"eta": [40], "reddito": [45], "citta": ["BO"]})))
