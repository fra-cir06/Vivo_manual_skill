# ============================================================
# Esempio 4 - Random Forest "da zero" con NumPy
# Scopo didattico: vedere ogni ingrediente dell'algoritmo.
# ============================================================
import numpy as np

def gini(y):
    """Impurità di Gini: H = sum_k p_k (1 - p_k) = 1 - sum_k p_k^2."""
    _, conteggi = np.unique(y, return_counts=True)
    p = conteggi / len(y)
    return 1.0 - np.sum(p ** 2)

def miglior_split(X, y, feature_candidate):
    """Cerca (feature j, soglia t) che minimizza l'impurità pesata G."""
    n = len(y)
    best = (None, None, gini(y))               # (j, t, G) - nessuno split
    for j in feature_candidate:
        valori = np.unique(X[:, j])
        soglie = (valori[:-1] + valori[1:]) / 2  # punti medi
        for t in soglie:
            sx = X[:, j] <= t
            G = (sx.sum() * gini(y[sx]) + (~sx).sum() * gini(y[~sx])) / n
            if G < best[2]:
                best = (j, t, G)
    return best

class Albero:
    def __init__(self, max_features, min_samples_leaf=1, rng=None):
        self.m, self.min_leaf, self.rng = max_features, min_samples_leaf, rng

    def fit(self, X, y, n_classi):
        self.n_classi = n_classi
        self.radice = self._cresci(X, y)
        return self

    def _foglia(self, y):                       # frequenze di classe
        return {"proba": np.bincount(y, minlength=self.n_classi) / len(y)}

    def _cresci(self, X, y):
        if len(np.unique(y)) == 1 or len(y) < 2 * self.min_leaf:
            return self._foglia(y)
        # >>> la differenza rispetto a un albero CART: m feature a caso <<<
        cand = self.rng.choice(X.shape[1], self.m, replace=False)
        j, t, _ = miglior_split(X, y, cand)
        if j is None:
            return self._foglia(y)
        sx = X[:, j] <= t
        if sx.sum() < self.min_leaf or (~sx).sum() < self.min_leaf:
            return self._foglia(y)
        return {"j": j, "t": t,
                "sx": self._cresci(X[sx], y[sx]),
                "dx": self._cresci(X[~sx], y[~sx])}

    def predict_proba(self, X):
        out = []
        for x in X:
            nodo = self.radice
            while "proba" not in nodo:
                nodo = nodo["sx"] if x[nodo["j"]] <= nodo["t"] else nodo["dx"]
            out.append(nodo["proba"])
        return np.array(out)

class RandomForestDaZero:
    def __init__(self, n_estimators=100, max_features="sqrt", random_state=0):
        self.B, self.max_features = n_estimators, max_features
        self.rng = np.random.default_rng(random_state)

    def fit(self, X, y):
        n, p = X.shape
        m = max(1, int(np.sqrt(p))) if self.max_features == "sqrt" else self.max_features
        self.classi = np.unique(y)
        self.alberi, self.oob_mask = [], []
        for _ in range(self.B):
            idx = self.rng.integers(0, n, n)          # 1) campione bootstrap
            oob = np.ones(n, bool); oob[idx] = False  #    chi è rimasto fuori
            t = Albero(m, rng=self.rng).fit(X[idx], y[idx], len(self.classi))
            self.alberi.append(t); self.oob_mask.append(oob)
        self._X, self._y = X, y
        return self

    def predict_proba(self, X):                      # 2) media delle probabilità
        return np.mean([t.predict_proba(X) for t in self.alberi], axis=0)

    def predict(self, X):
        return self.classi[np.argmax(self.predict_proba(X), axis=1)]

    def oob_score(self):                             # 3) stima out-of-bag
        n = len(self._y); somma = np.zeros((n, len(self.classi))); cont = np.zeros(n)
        for t, oob in zip(self.alberi, self.oob_mask):
            somma[oob] += t.predict_proba(self._X[oob]); cont[oob] += 1
        ok = cont > 0
        pred = np.argmax(somma[ok], axis=1)
        return np.mean(pred == self._y[ok])

if __name__ == "__main__":
    import time
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    X, y = load_breast_cancer(return_X_y=True)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

    t0 = time.time()
    mio = RandomForestDaZero(n_estimators=50, random_state=0).fit(X_tr, y_tr)
    t_mio = time.time() - t0
    t0 = time.time()
    sk = RandomForestClassifier(n_estimators=50, random_state=0).fit(X_tr, y_tr)
    t_sk = time.time() - t0
    print(f"Da zero : acc test = {np.mean(mio.predict(X_te) == y_te):.3f}  OOB = {mio.oob_score():.3f}  tempo = {t_mio:.1f} s")
    print(f"sklearn : acc test = {sk.score(X_te, y_te):.3f}  tempo = {t_sk:.2f} s")
    print(f"accordo tra le predizioni: {np.mean(mio.predict(X_te) == sk.predict(X_te)):.3f}")
