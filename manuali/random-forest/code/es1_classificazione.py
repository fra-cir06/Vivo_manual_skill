# ============================================================
# Esempio 1 - Classificazione con RandomForestClassifier
# Dataset: Breast Cancer Wisconsin (incluso in scikit-learn)
# ============================================================

# 1) IMPORT -----------------------------------------------------
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

RANDOM_STATE = 42                      # seme per risultati riproducibili

# 2) DATI -------------------------------------------------------
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
print(X.shape)                         # (campioni, feature)
print(y.value_counts())                # 1 = benigno, 0 = maligno

# 3) SUDDIVISIONE TRAIN / TEST ----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE)

# 4) MODELLO ----------------------------------------------------
rf = RandomForestClassifier(
    n_estimators=300,        # numero di alberi
    max_features="sqrt",     # feature candidate a ogni split
    oob_score=True,          # stima out-of-bag dell'accuratezza
    n_jobs=-1,               # usa tutti i core
    random_state=RANDOM_STATE)
rf.fit(X_train, y_train)

# 5) VALUTAZIONE ------------------------------------------------
y_pred = rf.predict(X_test)
print(f"OOB score     : {rf.oob_score_:.3f}")
print(f"Accuracy test : {accuracy_score(y_test, y_pred):.3f}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["maligno", "benigno"], digits=3))

# 6) PROBABILITA' PER UN NUOVO CAMPIONE ------------------------
nuovo = X_test.iloc[[0]]
print(rf.predict_proba(nuovo).round(3))   # [P(maligno), P(benigno)]
print(len(rf.estimators_))                # gli alberi addestrati
