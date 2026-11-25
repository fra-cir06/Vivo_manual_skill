# ============================================================
# Esempio 2 - Pipeline completa: preprocessing, CV, tuning,
#             importanza delle feature, salvataggio del modello
# ============================================================
import numpy as np
import pandas as pd
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import (train_test_split, StratifiedKFold,
                                     cross_val_score, GridSearchCV)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score

RS = 42
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=RS)

# --- 1. Pipeline: ogni passo ha un nome -------------------------
pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),     # gestisce eventuali NaN
    ("rf", RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=RS)),
])

# --- 2. Validazione incrociata ----------------------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RS)
scores = cross_val_score(pipe, X_tr, y_tr, cv=cv, scoring="roc_auc")
print("AUC per fold:", scores.round(4))
print(f"AUC media   : {scores.mean():.4f} +/- {scores.std():.4f}")

# --- 3. Ricerca degli iperparametri -----------------------------
griglia = {
    "rf__max_features": ["sqrt", 0.3, 0.6],
    "rf__min_samples_leaf": [1, 3, 5],
    "rf__max_depth": [None, 8],
}
gs = GridSearchCV(pipe, griglia, cv=cv, scoring="roc_auc", n_jobs=-1)
gs.fit(X_tr, y_tr)
print("Migliori parametri:", gs.best_params_)
print(f"AUC CV migliore   : {gs.best_score_:.4f}")
print("Combinazioni provate:", len(gs.cv_results_["params"]))

best = gs.best_estimator_
proba = best.predict_proba(X_te)[:, 1]
print(f"AUC sul test      : {roc_auc_score(y_te, proba):.4f}")

# --- 4. Importanza delle feature: MDI vs permutazione -----------
rf = best.named_steps["rf"]
mdi = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
perm = permutation_importance(best, X_te, y_te, n_repeats=20,
                              random_state=RS, scoring="roc_auc", n_jobs=-1)
perm_s = pd.Series(perm.importances_mean, index=X.columns).sort_values(ascending=False)
print("Top 5 MDI:\n", mdi.head(5).round(4))
print("Top 5 permutazione:\n", perm_s.head(5).round(4))

# --- 5. Salvataggio e ricaricamento -----------------------------
joblib.dump(best, "rf_breast_cancer.joblib")
ricaricato = joblib.load("rf_breast_cancer.joblib")
print("Stesse predizioni:", np.array_equal(ricaricato.predict(X_te), best.predict(X_te)))

mdi.to_csv("mdi.csv"); perm_s.to_csv("perm.csv")
pd.DataFrame({"mean": perm.importances_mean, "std": perm.importances_std}, index=X.columns).to_csv("perm_full.csv")
