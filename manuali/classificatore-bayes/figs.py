import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, FancyArrowPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa
import os

OUT = os.path.join(os.path.dirname(__file__), "figs")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1F3A5F"; TEAL = "#1B8A8A"; BLUE = "#2A6FDB"; RED = "#E0533D"
AMBER = "#E3A21A"; PURPLE = "#6B4FBB"; GRAY = "#8A8F98"; LIGHT = "#E9EDF3"; GREEN = "#2E9E5B"

plt.rcParams.update({
    "font.family": "TeX Gyre Pagella",
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Pagella",
    "mathtext.it": "TeX Gyre Pagella:italic",
    "mathtext.bf": "TeX Gyre Pagella:bold",
    "font.size": 10.5,
    "axes.edgecolor": "#9AA3AF",
    "axes.labelcolor": "#2B2F36",
    "xtick.color": "#5A6170",
    "ytick.color": "#5A6170",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 11.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": NAVY,
    "legend.frameon": False,
    "savefig.bbox": "tight",
    "axes.formatter.useoffset": False,
})

def G(x, m, s):
    return np.exp(-(x - m) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))

def G2(X, Y, m, S):
    Si = np.linalg.inv(S); d0 = X - m[0]; d1 = Y - m[1]
    r2 = Si[0, 0] * d0 ** 2 + 2 * Si[0, 1] * d0 * d1 + Si[1, 1] * d1 ** 2
    return np.exp(-r2 / 2) / (2 * np.pi * np.sqrt(np.linalg.det(S))), r2

def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"))
    plt.close(fig)

def cov_ellipse(ax, m, S, r, **kw):
    w, v = np.linalg.eigh(S)
    ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
    e = Ellipse(m, 2 * r * np.sqrt(w[1]), 2 * r * np.sqrt(w[0]), angle=ang, fill=False, **kw)
    ax.add_patch(e)

# ---------- Sez 1: Venn ----------
def fig_venn():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.9))
    titles = ["Eventi disgiunti: $A\\cap B=\\emptyset$", "Eventi sovrapposti: $A\\cap B\\neq\\emptyset$", "Condizionare: $B$ diventa l'universo"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off"); ax.set_aspect("equal")
        ax.add_patch(Rectangle((0.2, 0.2), 9.6, 6.6, fc="#F6F8FB", ec="#9AA3AF", lw=1))
        ax.text(0.55, 6.15, "$\\Omega$", fontsize=13, color=NAVY)
        ax.set_title(t, fontsize=10.5)
    a = axs[0]
    a.add_patch(Circle((3, 3.5), 1.8, fc=BLUE, alpha=.25, ec=BLUE, lw=1.5)); a.text(3, 3.4, "$A$", ha="center", fontsize=14, color=BLUE)
    a.add_patch(Circle((7, 3.5), 1.8, fc=RED, alpha=.25, ec=RED, lw=1.5)); a.text(7, 3.4, "$B$", ha="center", fontsize=14, color=RED)
    a.text(5, 0.7, "$P(A\\cup B)=P(A)+P(B)$", ha="center", fontsize=10.5, color=NAVY)
    b = axs[1]
    b.add_patch(Circle((4, 3.6), 2.1, fc=BLUE, alpha=.22, ec=BLUE, lw=1.5)); b.text(3.0, 3.5, "$A$", ha="center", fontsize=14, color=BLUE)
    b.add_patch(Circle((6, 3.6), 2.1, fc=RED, alpha=.22, ec=RED, lw=1.5)); b.text(7.0, 3.5, "$B$", ha="center", fontsize=14, color=RED)
    b.text(5, 3.5, "$A\\cap B$", ha="center", fontsize=9.5, color=PURPLE)
    b.text(5, 0.7, "$P(A\\cup B)=P(A)+P(B)-P(A\\cap B)$", ha="center", fontsize=10, color=NAVY)
    c = axs[2]
    c.add_patch(Circle((4, 3.6), 2.1, fc="none", ec=BLUE, lw=1.2, ls="--")); c.text(2.7, 3.5, "$A$", ha="center", fontsize=14, color=BLUE, alpha=.6)
    c.add_patch(Circle((6, 3.6), 2.1, fc=RED, alpha=.12, ec=RED, lw=2.2)); c.text(7.2, 3.5, "$B$", ha="center", fontsize=14, color=RED)
    from matplotlib.patches import Wedge
    # intersection highlight via clip
    circ = Circle((6, 3.6), 2.1, transform=c.transData)
    p = c.add_patch(Circle((4, 3.6), 2.1, fc=PURPLE, alpha=.45, ec="none")); p.set_clip_path(circ)
    c.text(5, 0.7, "$P(A|B)=P(A\\cap B)\\,/\\,P(B)$", ha="center", fontsize=10.5, color=NAVY)
    save(fig, "venn")

# ---------- Sez 2: prior x likelihood ----------
def fig_prior_like():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.9))
    cls = ["$w_1$\nmalato", "$w_2$\nsano"]; col = [RED, BLUE]
    data = [([0.1, 0.9], "Prior  $P(w_i)$"), ([0.5, 0.1], "Likelihood  $p(\\mathbf{x}|w_i)$"), ([0.05 / 0.14, 0.09 / 0.14], "Posterior  $P(w_i|\\mathbf{x})$")]
    for ax, (v, t) in zip(axs, data):
        bars = ax.bar(cls, v, color=col, width=.55, alpha=.85)
        ax.set_ylim(0, 1.05); ax.set_title(t)
        for b_, val in zip(bars, v):
            ax.text(b_.get_x() + b_.get_width() / 2, val + .03, f"{val:.2f}", ha="center", fontsize=10.5, color="#2B2F36")
    axs[1].annotate("favorisce $w_1$", xy=(0, .5), xytext=(.55, .8), color=RED, fontsize=10, arrowprops=dict(arrowstyle="->", color=RED))
    axs[2].annotate("vince $w_2$", xy=(1, .64), xytext=(.05, .85), color=BLUE, fontsize=10, arrowprops=dict(arrowstyle="->", color=BLUE))
    fig.text(.355, .5, "$\\times$", fontsize=22, color=NAVY, ha="center")
    fig.text(.675, .5, "$\\Rightarrow$", fontsize=20, color=NAVY, ha="center")
    fig.tight_layout(w_pad=3)
    save(fig, "prior_like")

# ---------- Sez 3: errore ----------
def fig_errore():
    fig, ax = plt.subplots(figsize=(8.4, 3.5))
    x = np.linspace(-3.5, 6.5, 1500)
    p1, p2 = .5, .5
    a = G(x, 0, 1) * p1; b = G(x, 3, 1.2) * p2
    xs = 2.25
    idx = np.argmin(np.abs(a - b)[(x > 0) & (x < 3)]); xb = x[(x > 0) & (x < 3)][idx]
    ax.fill_between(x, 0, np.minimum(a, b), where=x < xs, color=RED, alpha=.28, lw=0, label="errore in $\\Re_1$ (era $w_2$)")
    ax.fill_between(x, 0, np.minimum(a, b), where=x >= xs, color=BLUE, alpha=.28, lw=0, label="errore in $\\Re_2$ (era $w_1$)")
    m = (x >= xb) & (x < xs)
    ax.fill_between(x[m], a[m], b[m], color=AMBER, alpha=.85, lw=0, label="errore riducibile")
    ax.plot(x, a, color=RED, lw=2.2); ax.plot(x, b, color=BLUE, lw=2.2)
    ax.text(-0.3, a.max() + .012, "$p(x|w_1)P(w_1)$", color=RED, ha="center")
    ax.text(3.4, b.max() + .012, "$p(x|w_2)P(w_2)$", color=BLUE, ha="center")
    for v, l in [(xb, "$x_B$"), (xs, "$x^*$")]:
        ax.axvline(v, color="#4A5160", ls="--", lw=1)
        ax.text(v, -0.025, l, ha="center", va="top", fontsize=12)
    ax.annotate("", xy=(-3.4, -0.06), xytext=(xs, -0.06), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.3), annotation_clip=False)
    ax.annotate("", xy=(xs, -0.06), xytext=(6.4, -0.06), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.3), annotation_clip=False)
    ax.text(-0.6, -0.083, "$\\Re_1$: decido $w_1$", color=RED, ha="center", fontsize=10)
    ax.text(4.3, -0.083, "$\\Re_2$: decido $w_2$", color=BLUE, ha="center", fontsize=10)
    ax.set_ylim(0, .23); ax.set_yticks([]); ax.set_xticks([]); ax.spines["left"].set_visible(False)
    ax.legend(loc="upper right", fontsize=9.5)
    save(fig, "errore_bayes")

def fig_sequenziale():
    # test medico: prior .02, sens .9, fp .1 ; sequenza di positivi
    p = .02; seq = [p]
    for _ in range(4):
        p = .9 * p / (.9 * p + .1 * (1 - p)); seq.append(p)
    fig, ax = plt.subplots(figsize=(6.4, 2.7))
    xs = np.arange(len(seq))
    ax.plot(xs, seq, "-o", color=PURPLE, lw=2.2, ms=7, mec="white", mew=1.5)
    for i, v in enumerate(seq):
        ax.text(i, v + .07, f"{100*v:.1f}%", ha="center", fontsize=10, color=NAVY)
    ax.set_xticks(xs, ["prior\niniziale"] + [f"dopo test\n{i} positivo" for i in range(1, 5)], fontsize=9)
    ax.set_ylim(0, 1.12); ax.set_ylabel("$P(\\mathrm{malato}\\,|\\,\\mathrm{dati})$")
    ax.set_title("La posteriori di oggi diventa il prior di domani", fontsize=10.5)
    save(fig, "sequenziale")

# ---------- Sez 4 / 11: dataset ----------
W1 = np.array([[72,173],[54,159],[65,172],[58,170],[62,165],[72,176],[60,173],[64,179]], float)
W2 = np.array([[55,166],[46,158],[52,158],[47,160],[55,167],[54,166],[55,164],[49,157],[51,165],[51,162]], float)
XQ = np.array([57, 168.])

def fig_conteggio():
    fig, ax = plt.subplots(figsize=(5.6, 4.1))
    ax.scatter(*W1.T, s=55, color=BLUE, ec="white", lw=1, zorder=3, label="$w_1$ maschi (8)")
    ax.scatter(*W2.T, s=55, color=RED, ec="white", lw=1, zorder=3, label="$w_2$ femmine (10)")
    ax.add_patch(Circle(XQ, 3.0, fc=AMBER, alpha=.12, ec=AMBER, lw=1.8, zorder=2))
    ax.scatter(*XQ, s=90, color="#6B7280", marker="o", ec="black", zorder=4)
    ax.text(XQ[0] + .4, XQ[1] - 1.4, "$\\mathbf{x}$", fontsize=14)
    ax.text(XQ[0] - 3.2, XQ[1] + 3.6, "intorno: 1 blu, 2 rossi", fontsize=9.5, color="#8A5A00")
    ax.set_xlabel("Peso [kg]"); ax.set_ylabel("Altezza [cm]"); ax.set_aspect("equal")
    ax.set_xlim(43, 76); ax.set_ylim(154, 182)
    ax.legend(loc="lower right", fontsize=9.5)
    save(fig, "conteggio")

# ---------- Sez 5 ----------
def fig_param_nonparam():
    rng = np.random.default_rng(3)
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.0))
    x = np.linspace(-4.5, 4.5, 600)
    cases = [("Dati gaussiani, $n=10$", "g", 10), ("Dati bimodali, $n=300$", "b", 300)]
    for ax, (t, mode, n) in zip(axs, cases):
        if mode == "g":
            pts = rng.normal(0, 1, n); truth = G(x, 0, 1)
        else:
            pts = np.where(rng.random(n) < .5, -1.6, 1.6) + .55 * rng.normal(size=n); truth = .5 * G(x, -1.6, .55) + .5 * G(x, 1.6, .55)
        mu, sd = pts.mean(), pts.std()
        h = .25
        kde = np.mean([G(x, p, h) for p in pts], axis=0)
        ax.plot(x, truth, color=GRAY, ls="--", lw=1.8, label="densità vera")
        ax.plot(x, G(x, mu, sd), color=BLUE, lw=2.2, label="parametrico (gaussiana MLE)")
        ax.plot(x, kde, color=AMBER, lw=2, ls=(0, (2, 1.5)), label="non parametrico (finestre)")
        ax.plot(pts, np.full_like(pts, -0.02), "|", color="#3B4250", ms=8, alpha=.6)
        ax.set_title(t); ax.set_yticks([]); ax.set_ylim(-.04, .85 if mode == "g" else .55)
    axs[0].text(0, .62, "picchi = overfitting", ha="center", color="#8A5A00", fontsize=10)
    axs[1].text(0, .47, "gaussiana sbagliata = underfitting", ha="center", color=BLUE, fontsize=10)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(.5, -.08), fontsize=9.5)
    save(fig, "param_nonparam")

# ---------- Sez 6 ----------
def fig_gauss_regola():
    fig, ax = plt.subplots(figsize=(7.4, 3.0))
    x = np.linspace(-4, 4, 800); y = G(x, 0, 1)
    for k, c, a in [(3, TEAL, .15), (2, TEAL, .25), (1, TEAL, .4)]:
        m = np.abs(x) <= k; ax.fill_between(x[m], 0, y[m], color=c, alpha=a, lw=0)
    ax.plot(x, y, color=NAVY, lw=2.2)
    for k, t, yy in [(1, "68.3%", .19), (2, "95.4%", .07), (3, "99.7%", .012)]:
        ax.annotate("", xy=(-k, yy), xytext=(k, yy), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1))
        ax.text(0, yy + .012, t, ha="center", fontsize=10, color=NAVY, bbox=dict(fc="white", ec="none", pad=.5))
    ax.set_xticks(range(-3, 4), ["$\\mu-3\\sigma$", "$\\mu-2\\sigma$", "$\\mu-\\sigma$", "$\\mu$", "$\\mu+\\sigma$", "$\\mu+2\\sigma$", "$\\mu+3\\sigma$"])
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    save(fig, "gauss_regola")

DATA1 = np.array([3, 7, 9, -2, 15, 54, -11, 0, 23, -8], float)

def fig_mle1d():
    mu, sd = DATA1.mean(), DATA1.std()
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.1), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axs[0]
    x = np.linspace(-50, 70, 800)
    ax.plot(x, G(x, mu, sd), color=BLUE, lw=2.2)
    ax.plot(DATA1, np.zeros_like(DATA1), "s", color=NAVY, ms=6, clip_on=False, zorder=4)
    ax.plot([54], [0], "s", color=RED, ms=7, clip_on=False, zorder=5)
    ax.text(54, .0022, "outlier", color=RED, ha="center", fontsize=9.5)
    ax.vlines(mu, 0, G(mu, mu, sd), color=RED, lw=1.2)
    p25 = G(25, mu, sd)
    ax.vlines(25, 0, p25, color=PURPLE, lw=1.2, ls="--"); ax.hlines(p25, -50, 25, color=PURPLE, lw=1.2, ls="--")
    ax.plot(25, p25, "o", color=PURPLE, ms=6)
    ax.text(-48, p25 + .0008, "$p(25)\\approx 0.01495$", color=PURPLE, fontsize=10)
    ax.text(mu + 1, G(mu, mu, sd) + .0005, "$\\hat\\mu=9$", color=RED, fontsize=10.5)
    ax.set_title("Gaussiana stimata: $\\hat\\mu=9$, $\\hat\\sigma\\approx 17.86$"); ax.set_ylim(0, .026)
    ax2 = axs[1]
    ms = np.linspace(-10, 28, 300)
    ll = [np.sum(np.log(G(DATA1, m, sd))) for m in ms]
    ax2.plot(ms, ll, color=TEAL, lw=2.2)
    ax2.axvline(mu, color=RED, ls="--", lw=1.2); ax2.plot(mu, max(ll), "o", color=RED)
    ax2.text(mu + 1, max(ll) - .25, "massimo in\n$\\mu=\\bar{x}=9$", color=RED, fontsize=10)
    ax2.set_xlabel("$\\mu$ (con $\\sigma$ fissata)"); ax2.set_ylabel("$\\ln L(\\mu)$")
    ax2.set_title("Log-verosimiglianza")
    fig.tight_layout(w_pad=2)
    save(fig, "mle1d")

# ---------- Sez 7 ----------
def fig_autovettori():
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0))
    t = np.linspace(0, 2 * np.pi, 300)
    for ax, A, title in [(axs[0], np.array([[2, 0], [0, 1.]]), "$A=$ diag$(2,\\,1)$"), (axs[1], np.array([[4, 2], [2, 3.]]), "$A=[[4,\\,2],\\,[2,\\,3]]$")]:
        C = np.vstack([np.cos(t), np.sin(t)]); E = A @ C
        ax.plot(*C, color=GRAY, ls="--", lw=1.5, label="cerchio unitario")
        ax.plot(*E, color=BLUE, lw=2.2, label="immagine $A\\mathbf{v}$")
        w, v = np.linalg.eigh(A)
        for lam, vec, c in zip(w[::-1], v.T[::-1], [AMBER, GREEN]):
            vec = vec * np.sign(vec[0] if abs(vec[0]) > 1e-9 else vec[1])
            ax.annotate("", xy=vec * lam, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.4, mutation_scale=16))
            ax.text(*(vec * lam * 1.08 + np.array([.1, .25])), f"$\\lambda={lam:.2f}$", color=c, fontsize=10.5)
        if A[0, 1] == 0:
            w_ = np.array([1, 1.]); Aw = A @ w_
            ax.annotate("", xy=w_, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.6))
            ax.annotate("", xy=Aw, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.6, ls="--"))
            ax.text(.55, 1.05, "$\\mathbf{w}$", color=PURPLE); ax.text(2.05, 1.0, "$A\\mathbf{w}$", color=PURPLE)
        lim = 6.2 if A[0, 1] else 2.8
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim * .8, lim * .8); ax.set_aspect("equal")
        ax.axhline(0, color="#C7CDD6", lw=.8); ax.axvline(0, color="#C7CDD6", lw=.8)
        ax.set_title(title)
    axs[0].legend(loc="lower left", fontsize=9)
    save(fig, "autovettori")

# ---------- Sez 8 ----------
def fig_multinormali():
    fig, axs = plt.subplots(1, 3, figsize=(9.8, 3.3))
    rng = np.random.default_rng(1)
    X, Y = np.meshgrid(np.linspace(-4, 4, 300), np.linspace(-4, 4, 300))
    for ax, s12, t in zip(axs, [1.2, 0, -1.2], ["$\\sigma^{12}>0$: correlazione positiva", "$\\sigma^{12}=0$: assi paralleli (Naive Bayes)", "$\\sigma^{12}<0$: correlazione negativa"]):
        S = np.array([[2.0, s12], [s12, 1.2]]) if s12 else np.array([[2.0, 0], [0, .7]])
        Z, _ = G2(X, Y, (0, 0), S)
        ax.contourf(X, Y, Z, levels=12, cmap="Blues", alpha=.85)
        pts = rng.multivariate_normal((0, 0), S, 120)
        ax.scatter(*pts.T, s=5, color=NAVY, alpha=.6)
        w, v = np.linalg.eigh(S)
        for lam, vec in zip(w, v.T):
            ax.plot([-2.2 * np.sqrt(lam) * vec[0], 2.2 * np.sqrt(lam) * vec[0]], [-2.2 * np.sqrt(lam) * vec[1], 2.2 * np.sqrt(lam) * vec[1]], color=AMBER, lw=1.6)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(t, fontsize=9.8)
        ax.set_xlabel("$x^1$"); ax.set_ylabel("$x^2$")
    save(fig, "multinormali")

def fig_mahalanobis():
    S = np.array([[4.0, 2.4], [2.4, 2.0]]); m = np.zeros(2)
    fig, ax = plt.subplots(figsize=(5.4, 4.4))
    rng = np.random.default_rng(5)
    pts = rng.multivariate_normal(m, S, 220)
    ax.scatter(*pts.T, s=6, color=GRAY, alpha=.6)
    for r, a in zip([1, 2, 3], [.9, .6, .4]):
        cov_ellipse(ax, m, S, r, ec=BLUE, lw=1.8, alpha=a)
        ax.text(*(np.array([.9, .45]) * r * 1.65), f"$r={r}$", color=BLUE, fontsize=10)
    ax.add_patch(Circle(m, 2.5, fill=False, ec=GRAY, ls="--", lw=1.2))
    A = np.array([2.0, 1.5]); B = np.array([-1.0, 2.29])
    B = B / np.linalg.norm(B) * 2.5; A = A / np.linalg.norm(A) * 2.5
    Si = np.linalg.inv(S)
    for P, c, l in [(A, GREEN, "A"), (B, RED, "B")]:
        rM = np.sqrt(P @ Si @ P)
        ax.plot(*P, "o", color=c, ms=9, mec="white", mew=1.5, zorder=5)
        ax.plot([0, P[0]], [0, P[1]], color=c, lw=1.3, ls=":")
        off = (.35, -1.1) if l == "A" else (-4.6, .3)
        ax.text(P[0] + off[0], P[1] + off[1], f"{l}: euclidea 2.5\nMahalanobis {rM:.2f}", color=c, fontsize=9.5, bbox=dict(fc="white", ec="none", alpha=.85, pad=1))
    ax.plot(0, 0, "o", color=NAVY, ms=6); ax.text(.1, -.45, "$\\boldsymbol{\\mu}$", fontsize=12)
    ax.set_aspect("equal"); ax.set_xlim(-6, 6.5); ax.set_ylim(-4.6, 4.8); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Stessa distanza euclidea, diversa Mahalanobis", fontsize=10.5)
    save(fig, "mahalanobis")

# ---------- Sez 9 ----------
X5 = np.array([[3, 7], [4.5, 12], [13, 7.2], [1, 4], [23, 15.8]])

def fig_stima2d():
    mu = X5.mean(0); S = (X5 - mu).T @ (X5 - mu) / 5
    fig = plt.figure(figsize=(10, 4.0))
    ax = fig.add_subplot(1, 2, 1)
    Xg, Yg = np.meshgrid(np.linspace(-15, 33, 300), np.linspace(-3, 21, 300))
    Z, _ = G2(Xg, Yg, mu, S)
    ax.contourf(Xg, Yg, Z, levels=14, cmap="YlGnBu")
    ax.scatter(*X5.T, color=NAVY, s=40, ec="white", zorder=4, label="pattern")
    ax.scatter(*mu, color=RED, s=60, marker="D", ec="white", zorder=5, label="$\\boldsymbol{\\mu}=(8.9,\\,9.2)$")
    w, v = np.linalg.eigh(S)
    for lam, vec, c in zip(w, v.T, [GREEN, AMBER]):
        ax.annotate("", xy=mu + 2 * np.sqrt(lam) * vec * np.sign(vec[0]), xytext=mu, arrowprops=dict(arrowstyle="-|>", color=c, lw=2))
    ax.text(mu[0] + 13, mu[1] + 6.2, "$\\lambda_1\\approx77.2$", color="#8A5A00", fontsize=10)
    ax.text(mu[0] - 3.5, mu[1] - 6.2, "$\\lambda_2\\approx6.7$", color=GREEN, fontsize=10)
    ax.set_title("Vista dall'alto: curve di livello"); ax.legend(loc="upper left", fontsize=9)
    ax.set_xlabel("$x^1$"); ax.set_ylabel("$x^2$")
    ax3 = fig.add_subplot(1, 2, 2, projection="3d")
    Xg, Yg = np.meshgrid(np.linspace(-15, 33, 80), np.linspace(-3, 21, 80))
    Z, _ = G2(Xg, Yg, mu, S)
    ax3.plot_surface(Xg, Yg, Z, cmap="YlGnBu", lw=0, antialiased=True, rstride=1, cstride=1)
    ax3.set_title("Vista laterale: la 'campana' 2D"); ax3.set_xlabel("$x^1$"); ax3.set_ylabel("$x^2$")
    ax3.set_zticks([]); ax3.view_init(28, -60)
    ax3.xaxis.pane.fill = False; ax3.yaxis.pane.fill = False; ax3.zaxis.pane.fill = False
    save(fig, "stima2d")

# ---------- Sez 10 ----------
def post_map(ax, ms, Ss, ps, xr, yr, cols, title, n=400):
    X, Y = np.meshgrid(np.linspace(*xr, n), np.linspace(*yr, n))
    D = [G2(X, Y, m, S)[0] * p for m, S, p in zip(ms, Ss, ps)]
    P1 = D[0] / (D[0] + D[1])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("rb", [cols[1], "#FFFFFF", cols[0]])
    ax.contourf(X, Y, P1, levels=np.linspace(0, 1, 21), cmap=cmap, alpha=.55)
    ax.contour(X, Y, P1, levels=[.5], colors=[NAVY], linewidths=2.2)
    for m, S, c in zip(ms, Ss, cols):
        for r in [1, 2]:
            cov_ellipse(ax, m, S, r, ec=c, lw=1.4)
    ax.set_title(title, fontsize=10); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])

def fig_superfici():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6))
    S = np.array([[1, .3], [.3, .8]])
    post_map(axs[0], [(-1, 0), (1.5, .6)], [S, S], [.5, .5], (-4, 4.5), (-3.2, 3.8), [BLUE, RED], "$\\Sigma_1=\\Sigma_2$, $P(w_1)=P(w_2)=0.5$\nconfine: retta (iperpiano)")
    post_map(axs[1], [(-1, 0), (1.5, .6)], [S, S], [.8, .2], (-4, 4.5), (-3.2, 3.8), [BLUE, RED], "$\\Sigma_1=\\Sigma_2$, $P(w_1)=0.8$\nla retta si sposta verso $w_2$")
    post_map(axs[2], [(0, 0), (1.6, .3)], [np.array([[3, 0], [0, 2.4]]), np.array([[.25, 0], [0, .3]])], [.5, .5], (-4.5, 5), (-3.6, 4), [BLUE, RED], "$\\Sigma_1\\neq\\Sigma_2$\nconfine: curva quadratica")
    save(fig, "superfici")

def fig_regioni_disgiunte():
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    post_map(ax, [(0, 0), (0, 0.0)], [np.array([[0.5, 0], [0, 1.2]]), np.array([[4, 0], [0, .2]])], [.5, .5], (-5, 5), (-3, 3), [BLUE, RED], "")
    ax.text(0, .2, "$\\Re_1$", color=NAVY, fontsize=13, ha="center")
    ax.text(-3.7, 0, "$\\Re_2$", color="#9B2C1C", fontsize=13, ha="center"); ax.text(3.7, 0, "$\\Re_2$", color="#9B2C1C", fontsize=13, ha="center")
    ax.set_title("$\\Re_2$ formata da due pezzi separati", fontsize=10)
    save(fig, "regioni_disgiunte")

# ---------- Sez 11 ----------
def fig_maschi_femmine_param():
    m1, m2 = W1.mean(0), W2.mean(0)
    S1 = np.cov(W1.T, bias=True); S2 = np.cov(W2.T, bias=True)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
    ax = axs[0]
    for m, S, c in [(m1, S1, BLUE), (m2, S2, RED)]:
        for r in [1, 2]:
            cov_ellipse(ax, m, S, r, ec=c, lw=1.6, alpha=1 if r == 1 else .55)
        ax.plot(*m, "+", color=c, ms=12, mew=2)
    ax.scatter(*W1.T, s=40, color=BLUE, ec="white", zorder=3); ax.scatter(*W2.T, s=40, color=RED, ec="white", zorder=3)
    ax.scatter(*XQ, s=80, color="#6B7280", ec="black", zorder=4); ax.text(XQ[0] + .6, XQ[1] - 1.8, "$\\mathbf{x}$", fontsize=13)
    ax.set_title("Gaussiane stimate (ellissi a $r=1$ e $r=2$)", fontsize=10.5)
    ax.set_xlabel("Peso [kg]"); ax.set_ylabel("Altezza [cm]"); ax.set_aspect("equal"); ax.set_xlim(38, 82); ax.set_ylim(150, 186)
    ax = axs[1]
    X, Y = np.meshgrid(np.linspace(38, 82, 400), np.linspace(150, 186, 400))
    d1 = G2(X, Y, m1, S1)[0] * 8 / 18; d2 = G2(X, Y, m2, S2)[0] * 10 / 18
    P1 = d1 / (d1 + d2)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("rb", [RED, "#FFFFFF", BLUE])
    cf = ax.contourf(X, Y, P1, levels=np.linspace(0, 1, 21), cmap=cmap, alpha=.6)
    ax.contour(X, Y, P1, levels=[.5], colors=[NAVY], linewidths=2)
    ax.scatter(*W1.T, s=40, color=BLUE, ec="white", zorder=3); ax.scatter(*W2.T, s=40, color=RED, ec="white", zorder=3)
    ax.scatter(*XQ, s=80, color="#6B7280", ec="black", zorder=4)
    ax.text(XQ[0] + .8, XQ[1] + .6, "$P(w_2|\\mathbf{x})\\approx0.64$", fontsize=10, color="#7A1F12")
    cb = fig.colorbar(cf, ax=ax, fraction=.046, pad=.03); cb.set_label("$P(w_1|\\mathbf{x})$"); cb.set_ticks([0, .5, 1])
    ax.set_title("Posteriori e confine di decisione ($P=0.5$)", fontsize=10.5)
    ax.set_xlabel("Peso [kg]"); ax.set_aspect("equal")
    fig.tight_layout(w_pad=2)
    save(fig, "mf_param")

# ---------- Sez 12 ----------
def fig_confidenza():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.7))
    ms = [(-1.5, 0), (1.5, 0.4)]; S = [np.array([[1, .3], [.3, .7]]), np.array([[.8, -.2], [-.2, .9]])]
    X, Y = np.meshgrid(np.linspace(-5, 5, 400), np.linspace(-3.5, 3.5, 400))
    d = [G2(X, Y, m, s)[0] * .5 for m, s in zip(ms, S)]
    P1 = d[0] / (d[0] + d[1]); px = d[0] + d[1]
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("rb", [RED, "#FFFFFF", BLUE])
    ax = axs[0]
    cf = ax.contourf(X, Y, P1, levels=np.linspace(0, 1, 21), cmap=cmap, alpha=.65)
    ax.contour(X, Y, np.maximum(P1, 1 - P1), levels=[.8], colors=[AMBER], linewidths=1.8, linestyles="--")
    ax.contour(X, Y, P1, levels=[.5], colors=[NAVY], linewidths=1.8)
    ax.text(0, 2.9, "fascia ambigua: $\\max_i P(w_i|\\mathbf{x})<0.8$", ha="center", color="#8A5A00", fontsize=9.5)
    ax.set_title("Confidenza = posteriori (sfumatura)", fontsize=10.5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax = axs[1]
    ax.contourf(X, Y, P1, levels=np.linspace(0, 1, 21), cmap=cmap, alpha=.65)
    thr = 0.01
    ax.contourf(X, Y, px, levels=[0, thr], colors=["#D9DDE3"], alpha=.95)
    ax.contour(X, Y, px, levels=[thr], colors=["#4A5160"], linewidths=1.4)
    ax.plot(3.8, -2.6, "*", color="black", ms=13); ax.text(3.6, -2.2, "pattern\nscartato", fontsize=9.5, ha="center")
    ax.set_title("Open-set: rifiuto se $p(\\mathbf{x})$ è troppo bassa", fontsize=10.5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    save(fig, "confidenza")

def fig_normalita():
    rng = np.random.default_rng(2)
    fig, axs = plt.subplots(1, 3, figsize=(10, 2.9))
    a = rng.normal(170, 7, 300); b = np.concatenate([rng.normal(160, 4, 150), rng.normal(180, 4, 150)])
    for ax, d, t, c in [(axs[0], a, "Istogramma: dati normali", TEAL), (axs[1], b, "Istogramma: dati bimodali", RED)]:
        ax.hist(d, bins=24, density=True, color=c, alpha=.45, ec="white")
        x = np.linspace(d.min() - 5, d.max() + 5, 300)
        ax.plot(x, G(x, d.mean(), d.std()), color=NAVY, lw=2, label="gaussiana stimata")
        ax.set_title(t, fontsize=10.5); ax.set_yticks([])
    axs[0].legend(fontsize=9, loc="upper left")
    ax = axs[2]
    from math import erf, sqrt
    from scipy.stats import norm  # noqa
    q = norm.ppf((np.arange(1, 301) - .5) / 300)
    ax.plot(q, np.sort((a - a.mean()) / a.std()), ".", color=TEAL, ms=3.5, label="normali")
    ax.plot(q, np.sort((b - b.mean()) / b.std()), ".", color=RED, ms=3.5, label="bimodali")
    ax.plot([-3, 3], [-3, 3], color=NAVY, lw=1.2, ls="--")
    ax.set_title("Q-Q plot: punti sulla retta = normalità", fontsize=10.5); ax.set_xlabel("quantili teorici"); ax.set_ylabel("quantili osservati")
    ax.legend(fontsize=9)
    save(fig, "normalita")

if __name__ == "__main__":
    for f in [fig_venn, fig_prior_like, fig_errore, fig_sequenziale, fig_conteggio, fig_param_nonparam, fig_gauss_regola,
              fig_mle1d, fig_autovettori, fig_multinormali, fig_mahalanobis, fig_stima2d, fig_superfici, fig_regioni_disgiunte,
              fig_maschi_femmine_param, fig_confidenza, fig_normalita]:
        f(); print("ok", f.__name__)
