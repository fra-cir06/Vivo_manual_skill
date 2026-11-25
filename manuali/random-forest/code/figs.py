import numpy as np, warnings
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
NAVY="#1F3A5F"; TEAL="#1B8A8A"; BLUE="#2A6FDB"; RED="#E0533D"; AMBER="#E3A21A"; PURPLE="#6B4FBB"; GRAY="#8A8F98"
plt.rcParams.update({"font.family":"TeX Gyre Pagella","mathtext.fontset":"custom",
  "mathtext.rm":"TeX Gyre Pagella","mathtext.it":"TeX Gyre Pagella:italic","mathtext.bf":"TeX Gyre Pagella:bold",
  "font.size":10.5,"axes.edgecolor":"#9AA3AF","axes.spines.top":False,"axes.spines.right":False,
  "axes.titleweight":"bold","axes.titlecolor":NAVY,"legend.frameon":False,"savefig.bbox":"tight",
  "axes.formatter.useoffset":False})
F="../figs/"
from es4_da_zero import gini

# 1) split giocattolo -------------------------------------------------
x=np.arange(1,11); y=np.array([0,0,0,0,0,1,0,1,1,1])
ts=(x[:-1]+x[1:])/2; G=[]
for t in ts:
    s=x<=t; G.append((s.sum()*gini(y[s])+(~s).sum()*gini(y[~s]))/10)
fig,ax=plt.subplots(1,2,figsize=(9,2.9),gridspec_kw={"width_ratios":[1.1,1]})
ax[0].scatter(x,np.zeros(10),c=[TEAL if v==0 else RED for v in y],s=140,zorder=3,edgecolor="white")
for xi,v in zip(x,y): ax[0].text(xi,0.13,str(v),ha="center",color=NAVY,fontsize=10)
ax[0].axvline(5.5,color=AMBER,lw=2,ls="--"); ax[0].text(5.5,-0.22,"$t^*=5.5$",ha="center",color=AMBER,fontweight="bold")
ax[0].set_ylim(-.35,.35); ax[0].set_yticks([]); ax[0].spines["left"].set_visible(False)
ax[0].set_xticks(x); ax[0].set_xlabel("ore di studio $x$"); ax[0].set_title("Dati: 0 = bocciato, 1 = promosso")
ax[1].plot(ts,G,"o-",color=NAVY); i=int(np.argmin(G))
ax[1].plot(ts[i],G[i],"o",ms=11,color=AMBER,zorder=4)
ax[1].axhline(gini(y),color=GRAY,ls=":"); ax[1].text(9.4,gini(y)+.012,"$H$(radice) = 0.48",ha="right",color=GRAY,fontsize=9)
ax[1].set_xticks(ts); ax[1].set_xlabel("soglia $t$"); ax[1].set_ylabel("$G(t)$"); ax[1].set_title("Impurità pesata dopo lo split")
fig.savefig(F+"split.pdf"); plt.close()
print("G:",np.round(G,4))

# 2) bootstrap 63.2% --------------------------------------------------
n=np.arange(1,61); f=1-(1-1/n)**n
rng=np.random.default_rng(0); sim=[np.mean([len(np.unique(rng.integers(0,k,k)))/k for _ in range(400)]) for k in n]
fig,ax=plt.subplots(figsize=(6.4,2.8))
ax.plot(n,f,color=NAVY,lw=2,label="formula $1-(1-1/n)^n$")
ax.plot(n,sim,".",color=AMBER,label="simulazione (400 bootstrap)")
ax.axhline(1-1/np.e,color=RED,ls="--",lw=1); ax.text(60,1-1/np.e+.015,"$1-1/e\\approx 0.632$",ha="right",color=RED)
ax.set_xlabel("dimensione del dataset $n$"); ax.set_ylabel("frazione di campioni distinti"); ax.set_ylim(.55,1.02); ax.legend(loc="upper right")
fig.savefig(F+"bootstrap.pdf"); plt.close()

# 3) varianza della media -------------------------------------------
B=np.arange(1,201)
fig,ax=plt.subplots(figsize=(6.4,3))
for rho,c in [(0,TEAL),(0.1,BLUE),(0.3,PURPLE),(0.6,RED)]:
    ax.plot(B,rho+(1-rho)/B,color=c,lw=2,label=f"$\\rho={rho}$"); ax.axhline(rho,color=c,ls=":",lw=.8)
ax.set_xscale("log"); ax.set_xlabel("numero di alberi $B$ (scala log)"); ax.set_ylabel("Var(media) / $\\sigma^2$")
ax.legend(ncol=4,loc="upper right"); ax.set_ylim(0,1.05)
fig.savefig(F+"varianza.pdf"); plt.close()

# 4) errore OOB vs numero di alberi ---------------------------------
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
X,yb=load_breast_cancer(return_X_y=True)
fig,ax=plt.subplots(figsize=(6.4,3))
for mf,c,lab in [("sqrt",TEAL,"max_features='sqrt'"),("log2",AMBER,"max_features='log2'"),(None,RED,"max_features=None (bagging)")]:
    rf=RandomForestClassifier(warm_start=True,oob_score=True,max_features=mf,random_state=1,n_jobs=-1)
    err=[]; Ns=list(range(15,401,10))
    for k in Ns:
        rf.set_params(n_estimators=k); rf.fit(X,yb); err.append(1-rf.oob_score_)
    ax.plot(Ns,err,color=c,lw=2,label=lab); print(lab, round(err[-1],4))
ax.set_xlabel("n_estimators"); ax.set_ylabel("errore OOB"); ax.legend()
fig.savefig(F+"oob.pdf"); plt.close()

# 5) confini di decisione: albero vs foresta ------------------------
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
Xm,ym=make_moons(n_samples=300,noise=0.3,random_state=0)
xx,yy=np.meshgrid(np.linspace(-2,3,300),np.linspace(-1.6,2.1,300))
cm=ListedColormap(["#CDE7E7","#F8D4CD"])
fig,axs=plt.subplots(1,3,figsize=(10,3.1))
mods=[("Un albero (profondità piena)",DecisionTreeClassifier(random_state=0)),
      ("Un albero su un bootstrap",None),
      ("Random Forest (300 alberi)",RandomForestClassifier(n_estimators=300,random_state=0))]
for a,(tit,m) in zip(axs,mods):
    if m is None:
        idx=np.random.default_rng(3).integers(0,300,300); m=DecisionTreeClassifier(random_state=1).fit(Xm[idx],ym[idx])
    else: m.fit(Xm,ym)
    if hasattr(m,"estimators_"):
        Z=m.predict_proba(np.c_[xx.ravel(),yy.ravel()])[:,1].reshape(xx.shape)
        a.contourf(xx,yy,Z,levels=20,cmap=matplotlib.colors.LinearSegmentedColormap.from_list("x",["#CDE7E7","white","#F8D4CD"]))
    else:
        Z=m.predict(np.c_[xx.ravel(),yy.ravel()]).reshape(xx.shape); a.contourf(xx,yy,Z,cmap=cm)
    a.scatter(Xm[:,0],Xm[:,1],c=[TEAL if v==0 else RED for v in ym],s=9,edgecolor="none")
    a.set_title(tit,fontsize=10); a.set_xticks([]); a.set_yticks([])
fig.savefig(F+"confini.pdf"); plt.close()

# 6) importanze -------------------------------------------------------
import pandas as pd
mdi=pd.read_csv("mdi.csv",index_col=0).iloc[:,0]; perm=pd.read_csv("perm_full.csv",index_col=0)
top=mdi.head(8).index[::-1]
fig,ax=plt.subplots(1,2,figsize=(10,3.2),sharey=True)
ax[0].barh(top,mdi[top],color=TEAL); ax[0].set_title("MDI (feature_importances_)"); ax[0].set_xlabel("diminuzione media di impurità")
ax[1].barh(top,perm.loc[top,"mean"],xerr=perm.loc[top,"std"],color=AMBER,ecolor=GRAY); ax[1].set_title("Permutazione sul test (AUC)"); ax[1].set_xlabel("calo medio di AUC")
fig.savefig(F+"importanze.pdf"); plt.close()

# 7) dispersione delle predizioni dei singoli alberi (regressione) ---
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
Xd,yd=load_diabetes(return_X_y=True)
a_,b_,c_,d_=train_test_split(Xd,yd,test_size=.25,random_state=0)
r=RandomForestRegressor(n_estimators=500,max_features=1/3,min_samples_leaf=5,random_state=0,n_jobs=-1).fit(a_,c_)
pt=np.array([t.predict(b_[[0]])[0] for t in r.estimators_])
fig,ax=plt.subplots(figsize=(6.4,2.8))
ax.hist(pt,bins=30,color=TEAL,alpha=.85,edgecolor="white")
ax.axvline(pt.mean(),color=AMBER,lw=2.5); ax.text(pt.mean()+3,ax.get_ylim()[1]*.88,f"media = {pt.mean():.1f}\n= predizione RF",color=AMBER,fontweight="bold")
ax.axvline(d_[0],color=RED,ls="--"); ax.text(d_[0]-3,ax.get_ylim()[1]*.88,f"valore vero = {d_[0]:.0f}",color=RED,ha="right")
ax.set_xlabel("predizione del singolo albero"); ax.set_ylabel("n. alberi")
fig.savefig(F+"dispersione.pdf"); plt.close()
print("vero",d_[0],"media",pt.mean())
