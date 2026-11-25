# ============================================================
# Esempio 3 - Regressione con RandomForestRegressor
# Dataset: Diabetes (442 pazienti, 10 feature, target continuo)
# ============================================================
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

RS = 0
X, y = load_diabetes(return_X_y=True, as_frame=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=RS)

modelli = {
    "Regressione lineare": LinearRegression(),
    "Albero singolo":      DecisionTreeRegressor(random_state=RS),
    "Random Forest":       RandomForestRegressor(n_estimators=500, max_features=1/3,
                                                 min_samples_leaf=5, oob_score=True,
                                                 n_jobs=-1, random_state=RS),
}
for nome, m in modelli.items():
    m.fit(X_tr, y_tr)
    p = m.predict(X_te)
    print(f"{nome:20s} MAE={mean_absolute_error(y_te,p):6.2f}  "
          f"RMSE={root_mean_squared_error(y_te,p):6.2f}  R2={r2_score(y_te,p):.3f}")

rf = modelli["Random Forest"]
print(f"R2 out-of-bag: {rf.oob_score_:.3f}")

# Predizione = media delle predizioni dei singoli alberi
x0 = X_te.iloc[[0]]
per_albero = np.array([t.predict(x0.values)[0] for t in rf.estimators_])
print(f"media alberi = {per_albero.mean():.3f}   rf.predict = {rf.predict(x0)[0]:.3f}")
print(f"dispersione tra alberi (dev. std) = {per_albero.std():.2f}")

# Confronto più robusto: validazione incrociata ripetuta (5 fold x 3)
from sklearn.model_selection import RepeatedKFold, cross_val_score
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=RS)
for nome, m in modelli.items():
    s = cross_val_score(m, X, y, cv=cv, scoring="r2", n_jobs=-1)
    print(f"{nome:20s} R2 CV = {s.mean():.3f} +/- {s.std():.3f}")
