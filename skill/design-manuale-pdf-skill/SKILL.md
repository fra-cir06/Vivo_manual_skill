---
name: "design-manuale-pdf-skill"
description: "Usala quando l'utente chiede un PDF descritto come manuale, dispensa, guida o appunti, da documenti forniti o solo da un argomento: contenuti verificati su fonti ufficiali, impaginazione LaTeX in stile «dispensa» adattata al tema."
---

# Design manuale PDF

Skill per produrre manuali, dispense e guide in PDF con uno **schema fisso** e uno **stile adattato all'argomento**. La base grafica è quella della *Dispensa sul Classificatore di Bayes* e del *Manuale d'uso Kathará (lab basic-ipv4)*. Il PDF si costruisce in **LaTeX (XeLaTeX)** a partire dal template completo in fondo a questo file. Vale per qualunque argomento: teoria con formule, software e comandi, oppure un oggetto da usare (elettrodomestico, strumento, attrezzatura) senza alcuna formula né codice.

**Principio guida: la leggibilità viene prima del numero di pagine.** Un PDF con qualche pagina in più ma pulito è sempre meglio di uno compatto con blocchi spezzati, righe isolate o codice che va a capo male.

## Quando usarla

- L'utente chiede un **PDF** e dice che è un **manuale** (o dispensa, guida, guida d'uso, appunti di studio), allegando del materiale **oppure indicando solo l'argomento** (manuale da zero).
- Se chiede un manuale ma in un altro formato (Word, Google Docs, slide), segui quel formato e non questa skill.

## 1. Fonti: contenuti chiari e precisi

I casi possibili sono due. **Le regole di qualità valgono sempre**, cambia solo da dove si parte.

**Caso A: l'utente fornisce documentazione** (PDF, slide, testi, immagini allegati o presenti nella conversazione o nel progetto).
- Il suo materiale è la **base**: struttura, argomenti, esempi e terminologia seguono quel materiale. Leggilo tutto, comprese le immagini delle pagine (per i PDF: `pdftotext -layout` e lo strumento Read sulle pagine).
- Le fonti ufficiali e autorevoli del web servono a **verificare, precisare e completare**.

**Caso B: l'utente dà solo l'argomento** (manuale «da zero»).
- Le fonti ufficiali e autorevoli sono **l'unica base**. Fai una ricerca ampia: più ricerche distinte, una per ogni sottotema, e apri le pagine principali, non solo gli estratti.
- Definisci tu l'**indice del manuale** a partire da come l'argomento è organizzato nelle fonti di riferimento: documentazione ufficiale, programmi di corso, libri di testo, manuale del produttore. Copri prima le basi, poi gli aspetti avanzati, poi l'uso pratico.
- **Controllo di completezza**: prima di scrivere, confronta il tuo indice con quello di almeno due fonti di riferimento e annota gli argomenti che mancano. Includili o dichiara nella pagina «Come usare questo manuale» che restano fuori.
- Se l'argomento è ampio o ambiguo (pubblico, livello, modello di prodotto, versione), fai **una sola domanda** prima di iniziare. Se l'utente non risponde o non è presente, scegli l'interpretazione più ragionevole e scrivila nella pagina «Come usare questo manuale».

**Che cosa conta come fonte**
- **Ufficiale**: manuali e man page del produttore o del progetto, documentazione del software, schede tecniche e manuali del costruttore, standard (RFC, ISO, IEEE), normative, siti istituzionali.
- **Autorevole**: libri di testo di riferimento, dispense universitarie, enciclopedie e documentazioni riconosciute del settore.
- **Da evitare**: forum, blog anonimi, siti SEO. Si usano solo per un dettaglio pratico che non si trova altrove, e in quel caso lo si segnala.

**Regole valide in entrambi i casi**
- Verifica sul web **ogni** comando, opzione, versione, specifica tecnica, procedura di sicurezza o dato che può cambiare nel tempo, anche se pensi di conoscerlo.
- Ogni concetto importante deve poggiare su almeno una fonte ufficiale o autorevole. Per dati critici (sicurezza, dosi, limiti, valori tecnici) servono, se possibile, **due fonti concordi**.
- Fonti in disaccordo (tra il materiale dell'utente e il web, oppure tra due fonti web): non scegliere in silenzio. Riporta le versioni in un box «Attenzione» con le rispettive fonti; quando la scelta è chiara, privilegia la fonte ufficiale più recente.
- Dichiara nel testo le parti **ricostruite o dedotte**, cioè non presenti in alcuna fonte.
- Ricalcola in Python ogni numero degli esempi. **Anche i conteggi citati nel testo** («18 combinazioni», «90 addestramenti più il refit finale», «143 pazienti nel test») si ricavano dal codice o da un calcolo, mai a mente.
- Per software e librerie dichiara le **versioni** usate (nella pagina «Come usare questo manuale» e nelle fonti).
- In fondo al manuale c'è sempre la pagina **«Fonti e approfondimenti»**: prima l'eventuale materiale dell'utente, poi le fonti ufficiali e autorevoli consultate, con titolo e indirizzo.
- Nessun copia-incolla lungo dalle fonti: riformula con parole tue. Le immagini protette **non si copiano: si ridisegnano**.

## 2. Rigore didattico e metodologico

**Progressione didattica.** Ogni concetto segue lo stesso percorso: **intuizione o esempio semplice → formalizzazione → applicazione pratica → come leggere il risultato**. Nei passaggi in cui c'è una scelta (un parametro, una soglia, una metrica), spiega *perché* si sceglie così e quali alternative esistono. Dopo ogni output o grafico, spiega come interpretarlo.

**Gli esempi rispettano le regole che il manuale insegna.** Un esempio non deve mai violare una regola enunciata nel testo. Se il manuale dice «separa subito il test set», ogni esempio lo fa; se dice «preprocessing dentro la pipeline», ogni esempio lo fa. Se un esempio semplifica di proposito, lo dichiara.

**Conclusioni proporzionate ai risultati.**
- Per ogni metrica di' **cosa misura** e **su quali dati** è calcolata (training, validazione, test, out-of-bag).
- Quando confronti metodi, usa lo **stesso protocollo** per tutti e includi un **riferimento semplice** (baseline) quando ha senso.
- Distingui ciò che vale **in quell'esempio** da ciò che vale **in generale** («su questo dataset la regressione lineare vince di poco» non è «la regressione lineare è migliore»).
- Riporta l'incertezza quando c'è (deviazione standard tra fold, ripetizioni).

**Valutazione corretta (manuali di statistica, ML, analisi dati).**
- Scegli la suddivisione dei dati tenendo conto di **duplicati, gruppi** (più righe dello stesso paziente, utente, macchina) **e ordine temporale**: `GroupKFold`, `TimeSeriesSplit`, deduplicazione prima dello split.
- Trasformazioni e iperparametri si stimano **solo** su training e validazione. Il test serve una volta sola, alla fine.
- **Niente dati sintetici con righe duplicate** (per esempio `lista * 10`) prima di una validazione incrociata o di una ricerca degli iperparametri: le copie finiscono sia in training sia in validazione e gonfiano i risultati. Genera i dati con rumore (`numpy.random.default_rng(seed)`) o con le funzioni `make_*` di scikit-learn.
- Le misure di interpretabilità calcolate sul test (es. `permutation_importance`) vanno accompagnate da una nota: sono lecite **solo come analisi finale**, mai per selezionare feature e riaddestrare.

**Implementazioni didattiche «da zero».**
- Dichiara in un box quali input sono supportati e quali **semplificazioni** sono state fatte (velocità, tipi di dato, casi limite).
- Non assumere forme comode dei dati: per esempio usa la mappatura reale delle etichette (`self.classes_` con `np.unique(y, return_inverse=True)`) in **tutti** i metodi (`fit`, `predict`, `predict_proba`, punteggi), senza presupporre classi `0, 1, …, K−1`.
- Verifica il codice su **almeno un caso diverso** da quello illustrato (altre etichette, altro dataset) e confrontalo con un'implementazione di riferimento, se esiste.

## 3. Schema fisso del documento

Ogni manuale ha sempre questa struttura:

1. **Copertina**: fascia superiore colorata con linea d'accento, titolo grande in Fira Sans ExtraBold, sottotitolo, motivo decorativo **legato al tema**, box con l'elemento simbolo (una formula, un comando, una frase chiave o un pittogramma), autore (`\autore`), anno o versione, pillole della legenda. Imposta anche `\titolopdf` e `\autore`: finiscono nei **metadati del PDF**.
2. **«Come usare questo manuale»**: come è organizzato, a chi è rivolto, versioni del software usate e legenda **dei soli box usati davvero** nel documento.
3. **Indice**.
4. **Capitoli**. Ognuno contiene:
   - il banner `\sezione{n}{Titolo}{sottotitolo o slide}`;
   - in apertura, se utile, un box `inbreve`;
   - spiegazione a due livelli: prima l'**idea semplice** (box Intuizione), poi i **dettagli precisi** (box Tecnica, oppure passi numerati per le procedure);
   - esempi concreti, avvertenze e almeno una figura quando aiuta;
   - facoltativo ma consigliato nei manuali di studio: un box `esercizi` (2–4 esercizi), con le soluzioni nell'appendice finale;
   - in chiusura il box `appunti` (riepilogo del capitolo o appunti divisi per slide con `\pag{n}`).
5. **Pagine finali**: pagina riassuntiva adatta al tipo di manuale (vedi tabella sotto); se ci sono esercizi, **«Soluzioni degli esercizi»**; facoltativo un **glossario**; sempre **«Fonti e approfondimenti»**.

## 4. Adattare il manuale al tipo di argomento

Formule e codice **non sono obbligatori**: usa solo gli elementi che servono all'argomento.

| Tipo di manuale | Elementi principali | Figure tipiche | Pagina finale |
|---|---|---|---|
| **Teorico/scientifico** (es. ML, statistica) | Intuizione, Tecnica, `formula`/`formulat`, Esempio con calcoli, Esercizi | grafici matplotlib, diagrammi | Formulario |
| **Tecnico/software** (es. Kathará, CLI, configurazioni) | `scheda` comando, `terminale`, `filecfg`, `\codicefile`, `\outputfile`, Esempio, Attenzione | schemi TikZ di architettura e reti, diagrammi temporali, finestre ricostruite | Scheda riassuntiva dei comandi + checklist dei problemi |
| **D'uso di un oggetto/prodotto** (es. elettrodomestico, strumento, attrezzatura) | `passi` numerati, `consiglio`, `attenzione` (titolo «Sicurezza»), tabelle «problema → causa → soluzione», box `inbreve` | disegni TikZ dell'oggetto con parti numerate ed etichette, sequenze illustrate dei passi, icone e pittogrammi, tabelle di manutenzione | Scheda rapida (operazioni frequenti, manutenzione, risoluzione problemi) |
| **Procedurale/organizzativo** (es. guide, regolamenti, processi) | `passi`, `inbreve`, tabelle, `consiglio` | diagrammi di flusso, timeline, checklist | Checklist riassuntiva |

**Nei manuali senza formule o codice**: niente box Tecnica pieni di simboli. La precisione si ottiene con **dati e specifiche** (misure, tempi, valori, modelli) presi dalla documentazione ufficiale, con passi chiari e verificabili e con avvertenze di sicurezza esplicite. Il linguaggio è semplice e diretto, all'imperativo nei passi («Premi», «Collega»).

**Checklist di completezza per manuali di ML supervisionato.** Oltre a teoria, iperparametri, flusso di lavoro e limiti del modello (es. gli alberi non estrapolano), verifica che ci sia almeno un box (Attenzione o Approfondimento) su ciascuno di questi punti:
- **Baseline**: confronto onesto con un modello semplice, sulla stessa validazione incrociata.
- **Metrica e validazione**: quale metrica, su quali dati, con quale schema di split (gruppi, tempo, duplicati).
- **Soglia e calibrazione**: come si comporta `predict_proba` del modello, come scegliere una soglia diversa da 0,5 sui dati di validazione, e quando servono probabilità calibrate (`CalibratedClassifierCV`, curva di calibrazione).
- **Classi sbilanciate**: `class_weight`, e quando affiancare o preferire la **PR-AUC** (*average precision*) alla ROC-AUC.
- **Feature categoriche ad alta cardinalità**: `OneHotEncoder` contro alternative adatte al modello (`OrdinalEncoder` o `TargetEncoder` per i modelli ad alberi).
- **Interpretazione**: misure di importanza, loro limiti, importanza ≠ causalità.
- **Limiti strutturali** del modello e quando non usarlo.

## 5. Stile: base fissa + scelte creative per argomento

**Fissi (identità del manuale)**: font, impaginazione, struttura, forma dei box, banner dei capitoli, intestazione e piè di pagina, tabelle con intestazione colorata.

**Da adattare ogni volta**, con giudizio, per rendere l'argomento più chiaro:
- **Palette d'accento**: navy resta il colore principale; teal (accento) e ambra (secondario) si possono ridefinire in `preamble.tex` per evocare il tema. Mantieni contrasto e leggibilità, al massimo 2 colori d'accento nuovi. Esempi:

| Tema | teal → | ambra → |
|---|---|---|
| tecnologia, reti, ML (default) | `1B8A8A` | `D9940F` |
| natura, salute, sport | verde `2E8B57` | lime `8DB600` |
| cucina, casa, artigianato | terracotta `C8553D` | ocra `D9A441` |
| elettronica, energia | ciano `0F7FB5` | giallo `E6B800` |
| storia, diritto, umanistiche | bordeaux `8C2F39` | oro `B8860B` |

- **Copertina**: motivo decorativo disegnato in TikZ e coerente con il tema (curve gaussiane per la statistica, nodi e collegamenti per le reti, alberi stilizzati per i modelli ad alberi, la sagoma dell'oggetto per un manuale d'uso, una timeline per la storia).
- **Titoli dei box** (argomento opzionale): «Sicurezza», «Lo sapevi?», «Manutenzione», «Errore comune», «Nel mondo reale»…
- **Figure su misura**: inventa la visualizzazione che spiega meglio (sezioni esplose, schemi con parti numerate, confronti prima/dopo, diagrammi temporali, mappe, alberi, flussi).
- **Icone e simboli**: disegnati in TikZ o presi da `pifont` (`\ding{51}` ✓, `\ding{55}` ✗, `\ding{43}` ☛, `\ding{46}` ✎, `\ding{72}` ★).

**Accessibilità**: ogni box deve restare riconoscibile **anche senza colore** (stampa in bianco e nero, daltonismo): icona + titolo scritto sono obbligatori, il colore è solo un aiuto. Nei grafici distingui le serie anche con tipo di linea o marcatore, non solo con il colore. Codice e output devono avere contrasto sufficiente alla dimensione di lettura.

Prima di scrivere, decidi in due righe palette, motivo di copertina e tipi di figura, e applicali in modo **coerente in tutto il documento**. La creatività serve alla chiarezza: niente decorazioni che distraggono.

## 6. Codice ed esempi eseguibili (manuali con codice)

**Codice e output non si copiano mai a mano nel `.tex`.** Si includono dai file veri, così testo e programma non possono divergere.

**Organizzazione della cartella**
```
manuale/
├── main.tex, preamble.tex, c01.tex …
├── code/        script didattici consegnati all'utente (es1_….py, es2_….py)
├── output/      output reali salvati da controlla_codice.py (es1_….txt)
├── figs/        figure in PDF vettoriale
└── servizio/    script NON didattici: figure, tabelle, CSV (es. build_figures.py)
```
- Gli script di `code/` contengono **solo** il codice didattico: niente righe di servizio (esportazione di CSV, salvataggio di figure per il manuale). Quello va in `servizio/`.
- Nel PDF il codice entra con `\codicefile{file.py}{prima}{ultima}` (righe reali, numerate come nel file) e l'output con `\outputfile{output/file.txt}{titolo}`. Nel testo le righe si richiamano con `\rr{36}` o `\rr{36}[41]` (→ «r. 36–41»). Prima di scrivere i richiami, stampa il file numerato (`cat -n`) e usa quei numeri.
- Il blocco `codice` scritto a mano nel `.tex` è ammesso solo per frammenti brevi che non esistono come file (2–6 righe); anche questi vanno eseguiti almeno una volta.

**Regole per gli script didattici**
- Righe di **al massimo 78 caratteri**. Spezza a mano le chiamate lunghe, con un argomento per riga e rientro allineato. I listati non vanno mai a capo da soli (nel template `breaklines=false`): una riga troppo lunga si vede subito come errore.
- **Tutti gli `import` in testa** al file, nessun import inutilizzato o duplicato.
- **Stessi nomi in tutti gli script** dello stesso manuale (es. sempre `RANDOM_STATE`, sempre `X_train`/`X_test`), stesso ordine delle sezioni, commenti in italiano.
- Seme casuale fissato ovunque serva; dati inclusi nella libreria o generati nel codice, così chiunque può rieseguire.
- Ogni script gira **senza errori né warning non voluti**.
- Il controllo si fa con lo script `controlla_codice.py` (in fondo a questo file): verifica lunghezza delle righe, posizione e uso degli import, esecuzione senza warning, e salva l'output in `output/`. Se è disponibile `ruff`, lancia anche `ruff check --select E,F,W code/`.
- Gli script consegnati all'utente devono coincidere **esattamente** con quelli inclusi nel PDF.

## 7. Impaginazione e tipografia

**Blocchi che non si spezzano (keep-together).**
- I box didattici (Intuizione, Tecnica, Esempio, Attenzione, Consiglio, Approfondimento, Esercizi, Riepilogo), le tabelle brevi, le figure con la loro didascalia e i blocchi di codice **fino a ~25 righe** restano interi: se non entrano nello spazio rimasto, slittano in blocco alla pagina dopo. Nel template i box sono già `unbreakable` e `\figura` tiene unite figura e didascalia.
- Un box più lungo di mezza pagina si rende spezzabile con il secondo argomento opzionale (`\begin{tecnica}[Titolo][breakable]`), oppure si divide in due box. Un listato più lungo di ~25 righe si divide in più `\codicefile` con intervalli di righe che seguono la struttura del codice (funzione, classe, blocco logico), oppure si passa `[breakable]`.
- Mai parentesi di chiusura (`)`, `]`, `}`) o una sola riga di codice isolate in cima a una pagina.

**Righe isolate e pagine quasi vuote.**
- Nel template: penalità massime per righe vedove e orfane; `\Needspace` prima di ogni sottosezione, così un titolo non resta mai da solo in fondo alla pagina.
- Una pagina quasi vuota è accettabile **solo** se è la conseguenza di un blocco intero slittato. Se capita spesso, riordina il contenuto (sposta un box breve prima di una tabella grande, dividi una tabella lunga in due) invece di spezzare i blocchi.

**Tipografia.**
- Scrivi i caratteri Unicode veri, mai sequenze LaTeX: trattino medio **–** per intervalli e anni (`r. 10–16`, `A.A. 2026–2027`, `3,4–3,5 %`), lineetta **—** per gli incisi, segno meno **−** nei numeri del testo. Le sequenze `--` diventano trattini doppi in ogni testo a spaziatura fissa (titoli dei listati, `\texttt`, alberi di cartelle).
- Virgolette coerenti in tutto il documento: «…» (e “…” solo dentro a «…»).
- Negli alberi di cartelle usa i caratteri `├──`, `└──`, `│`, non `|--`.

## 8. Figure

- Matplotlib: crea le figure con `constrained_layout=True` (o `fig.tight_layout()`) e salva con `bbox_inches="tight"` in PDF vettoriale.
- **Niente etichette sovrapposte**: con linee verticali o orizzontali vicine (es. media e valore vero), metti le etichette su lati opposti (`ha="right"` e `ha="left"`), sfalsale in altezza o spostale nella legenda fuori dall'area dei dati.
- Assi, legende e numeri devono essere leggibili **alla dimensione di stampa** (testo ≥ 8 pt nel PDF finale).
- Ogni grafico ha una didascalia che dice cosa guardare; tienilo vicino al testo che lo spiega (`\figura`).
- Distingui le serie anche con stile di linea o marcatore (accessibilità).

## 9. Procedura operativa

1. **Fonti** (sezione 1). Caso A: leggi il materiale dell'utente, poi cerca le fonti ufficiali e annota le differenze. Caso B: ricerca ampia, poi costruisci l'indice e fai il controllo di completezza.
2. **Tipo e stile** (sezioni 4–5). Dividi in capitoli; per i manuali di ML spunta la checklist di completezza.
3. **Cartella di lavoro** (sezione 6): `preamble.tex` (template), `main.tex` e un file per capitolo; personalizza `\titolobreve`, `\titolopdf`, `\autore`, `\etichettasezione` ed eventualmente i colori d'accento.
4. **Codice prima del testo** (se c'è codice): scrivi gli script in `code/`, eseguili con `controlla_codice.py` finché non ci sono problemi, genera le figure con gli script di `servizio/`. Solo dopo scrivi le spiegazioni, partendo dai numeri di riga reali e dagli output salvati.
5. **Scrivi i capitoli** (sezioni 2–3), applicando la progressione didattica e le regole di rigore.
6. **Compila due volte**: `xelatex -interaction=nonstopmode main.tex`. Controlla `grep "^!" main.log` e `grep Overfull main.log`: zero errori, zero overfull.
7. **Controllo del PDF**: `python3 controlla_pdf.py main.pdf`. Correggi tutti gli errori (✗) e valuta gli avvisi (⚠). Poi **guarda tutti i fogli di anteprima** in `qa/` e, per le pagine con codice, grafici o cambi di pagina delicati, rendi la singola pagina a 80–100 dpi e controllala da vicino. Ricompila e ripeti finché il quality gate (sezione 10) è superato.
8. **Consegna**: copia il PDF in `/mnt/user-data/outputs/<Nome_Descrittivo>.pdf` e, se ci sono, gli script di `code/` (identici a quelli del PDF); inviali con SendUserFile. Nel messaggio riassumi la struttura, le scelte di stile, le fonti principali, le versioni del software e le parti ricostruite o i limiti.

## 10. Quality gate finale (prima di ogni consegna)

Consegna solo se **tutti** i punti sono veri:
1. Ogni script didattico gira senza errori né warning non voluti, ha gli import in testa e nessun import inutilizzato (`controlla_codice.py` termina con «OK»).
2. Nessuna riga di codice supera i 78 caratteri e nessun listato va a capo da solo.
3. Codice e output nel PDF vengono dai file (`\codicefile`, `\outputfile`) e gli script consegnati coincidono con quelli inclusi; i richiami `\rr{…}` puntano alle righe giuste.
4. Ogni numero e conteggio citato nel testo è stato ricalcolato.
5. Nessun box, tabella breve, figura con didascalia o blocco di codice fino a ~25 righe è spezzato tra due pagine; nessun frammento isolato in cima a una pagina.
6. Nessun grafico ha etichette sovrapposte o tagliate; tutto è leggibile alla dimensione di stampa.
7. Nessun `--` letterale, comando LaTeX grezzo o `??` nel testo (`controlla_pdf.py` senza errori).
8. Ogni esempio rispetta le regole che il manuale insegna; le conclusioni dicono su quali dati sono calcolate.
9. La pagina «Fonti e approfondimenti» elenca le fonti e le parti ricostruite; le versioni del software sono dichiarate; i metadati del PDF (titolo, autore) sono impostati.

## 11. Riferimento del sistema di design

**Font**
- Testo: TeX Gyre Pagella (Palatino), 11 pt.
- Matematica (se c'è): `mathpazo`, con vettori in grassetto; **sempre notazione matematica**, mai informatica.
- Titoli, box, tabelle, didascalie: Fira Sans (SemiBold, Light, ExtraBold).
- Codice (se c'è): DejaVu Sans Mono.

**Palette base (HEX)**: navy `1F3A5F`, teal `1B8A8A`, blu `2A6FDB`, rosso `E0533D`, ambra `D9940F`, viola `6B4FBB`, verde `2E9E5B`, grigio `5A6170`, chiaro `EEF2F7`, testo `22262D`.

**Impaginazione**: A4, margini 2.3 cm; testo `\raggedright` (manca la sillabazione italiana); intestazione con `\titolobreve` a sinistra e il titolo del capitolo a destra; numero di pagina in un cerchio navy.

| Elemento | Comando | Uso |
|---|---|---|
| Metadati | `\titolopdf`, `\autore` (in `preamble.tex`) | titolo e autore del PDF e della copertina |
| Banner capitolo | `\sezione{n}{Titolo}{sottotitolo}` | nuova pagina, numero grande |
| Sottosezione | `\subsection{…}` | numero in riquadro teal chiaro; non resta mai sola in fondo alla pagina |
| In breve | `\begin{inbreve}` | sintesi di apertura del capitolo |
| Intuizione | `\begin{intuizione}[titolo][opzioni]` | idea semplice, analogie |
| Tecnica | `\begin{tecnica}[titolo][opzioni]` | dettagli precisi, definizioni, formule |
| Esempio | `\begin{esempio}[titolo][opzioni]` | casi concreti, calcoli verificati |
| Attenzione / Sicurezza | `\begin{attenzione}[Sicurezza][opzioni]` | errori, rischi, precisazioni sulle fonti |
| Consiglio | `\begin{consiglio}[titolo][opzioni]` | suggerimenti pratici, buone abitudini |
| Approfondimento | `\begin{mlbox}[titolo][opzioni]` | collegamenti, curiosità, uso reale |
| Esercizi / Soluzioni | `\begin{esercizi}[titolo][opzioni]`, `\soluzione{n.m}{testo}` | fine capitolo / appendice |
| Passi numerati | `\begin{passi} \item …` | procedure e istruzioni d'uso |
| Formula | `formula` / `formulat{Titolo}` | solo se ci sono formule |
| Codice da file | `\codicefile[opzioni]{file.py}{da}{a}`, `\codicefileintero{file.py}` | righe reali numerate da `code/` |
| Output da file | `\outputfile[opzioni]{output/file.txt}{titolo}` | output salvato dall'esecuzione |
| Richiamo righe | `\rr{36}`, `\rr{36}[41]` | etichetta «r. 36–41» nel testo |
| Parole evidenziate | `\paroleevidenziate{Classe1,funzione2}` | nomi chiave in teal nei listati |
| Codice breve | `\begin{codice}{nome.py}` | solo frammenti che non esistono come file |
| Terminale / File / Scheda comando | `terminale{titolo}`, `filecfg{file}`, `scheda{cmd}` + `\campo` + `\sint` | manuali tecnici; delimitatori `§…§` prompt/chiave, `¤…¤` evidenziato, `°…°` commento |
| Tabelle | `tabularx`, `\rowcolor{navy}\thd{…}`, `\rowcolors{2}{chiaro}{white}`, colonna `Y` | |
| Figura | `\figura[.9\linewidth]{file.pdf}{didascalia}` | figura e didascalia sempre insieme |
| Evidenziazioni | `\hl{…}`, `\key{…}`, `\inl{…}` | |
| Appunti | `\begin{appunti}{Riepilogo}` + `\pag{n}` | chiusura di ogni capitolo |
| Stili TikZ | `dev`, `host`, `rtr`, `cd`, `lnk`, `lab`, `ipl`, `macl`, `netl` | schemi di reti e dispositivi |

**Grafici matplotlib (stesso stile)**
```python
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")
NAVY = "#1F3A5F"; TEAL = "#1B8A8A"; BLUE = "#2A6FDB"; RED = "#E0533D"
AMBER = "#E3A21A"; PURPLE = "#6B4FBB"; GRAY = "#8A8F98"
plt.rcParams.update({
    "font.family": "TeX Gyre Pagella", "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Pagella",
    "mathtext.it": "TeX Gyre Pagella:italic",
    "mathtext.bf": "TeX Gyre Pagella:bold",
    "font.size": 10.5, "axes.edgecolor": "#9AA3AF",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlecolor": NAVY,
    "legend.frameon": False, "savefig.bbox": "tight",
    "axes.formatter.useoffset": False,
    "figure.constrained_layout.use": True})
# salva sempre in PDF vettoriale:
# fig.savefig("figs/nome.pdf", bbox_inches="tight")
```
(Se cambi i colori d'accento, usa gli stessi HEX anche nei grafici. In mathtext niente `\begin{pmatrix}`.)

## 12. Insidie note (già risolte nel template)

- Compila con **XeLaTeX**: LuaLaTeX qui non trova i font.
- `babel` non ha l'opzione `italian`: usa `\babelprovide[import,main]{italian}`. Testo `\raggedright` (non `\RaggedRight`, non giustificato).
- Nei tcolorbox usa `halign=flush center` / `flush left` (già impostato con `every box`).
- Nelle colonne `p{}` metti `\leavevmode` prima di `\color`. Se in una tabella le colonne risultano disallineate in verticale, usa colonne `m{}` e, dentro il gruppo della tabella, `\renewcommand\tabularxcolumn[1]{m{#1}}`; nelle colonne `X` di testo aggiungi `>{\raggedright\arraybackslash}`.
- I box dentro `tcbraster` sono già `unbreakable`.
- I box hanno due argomenti opzionali: `[titolo][opzioni tcolorbox]`. Per un titolo con parentesi quadre racchiudilo tra graffe.
- `\inl{}` non va a capo: per le sintassi lunghe usa `\sint{}`.
- Nei listing: delimitatori `§`, `¤`, `°`. Niente `#` nel titolo di `terminale`. I titoli di `codice`, `filecfg`, `terminale` e `\outputfile` accettano `_` (sono già protetti con `\detokenize`).
- I listati hanno `breaklines=false`: una riga troppo lunga esce dal box ed è visibile come overfull. Si corregge accorciando la riga nel `.py`, non riattivando l'a-capo.
- Formule lunghe con più casi (regressione/classificazione) vanno in `align*` su più righe, non affiancate con `\qquad`.
- Usa `\thd` per le intestazioni di tabella (`\th` è già definito).
- Nei `\foreach` di TikZ niente virgole nei testi.
- La copertina usa `remember picture`: due compilazioni.
- Verifica i font con `fc-list : family`. Se ne manca uno, usa il sostituto più simile e dillo all'utente.
- Una tabella lunga che non entra sotto il banner del capitolo lascia la pagina quasi vuota: dividila in due tabelle con la stessa intestazione, o metti prima i box brevi.
- `\figura` tiene unite solo le immagini da file. Un disegno TikZ con la sua didascalia va racchiuso in `\par\noindent\begin{minipage}{\linewidth} … \didascalia{…}\end{minipage}\par`, altrimenti la didascalia può finire nella pagina dopo.
- Nei `\foreach` di TikZ i valori con virgole (es. le cardinalità `(0,N)`) vanno tra graffe: `{(0,N)}`.

## Template: preamble.tex

```latex
\documentclass[11pt,a4paper]{article}
% >>> PERSONALIZZA <<<
\newcommand{\titolobreve}{Titolo \,·\, Sottotitolo breve}  % testo dell'intestazione
\newcommand{\etichettasezione}{Capitolo}                  % oppure: Sezione
\newcommand{\titolopdf}{Titolo completo del manuale}       % metadati PDF + copertina
\newcommand{\autore}{Nome Cognome}                         % metadati PDF + copertina

% ---------------- Matematica (Palatino, stile manuale scientifico) ----------------
\usepackage{amsmath,amssymb,mathtools}
\usepackage[sc]{mathpazo}
\usepackage{bm}
\linespread{1.06}

% ---------------- Font del testo ----------------
\usepackage[no-math]{fontspec}
\setmainfont{TeX Gyre Pagella}
\setsansfont{Fira Sans}[BoldFont={Fira Sans SemiBold},ItalicFont={Fira Sans Italic},BoldItalicFont={Fira Sans SemiBold Italic}]
\newfontfamily\headfont{Fira Sans}[BoldFont={Fira Sans SemiBold},ItalicFont={Fira Sans Italic}]
\newfontfamily\headlight{Fira Sans Light}
\newfontfamily\headblack{Fira Sans ExtraBold}

\usepackage{babel}
\babelprovide[import,main]{italian}

% ---------------- Pagina ----------------
\usepackage[a4paper,top=2.5cm,bottom=2.4cm,left=2.3cm,right=2.3cm,headheight=15pt,headsep=0.9cm]{geometry}
\usepackage[table]{xcolor}
\usepackage{graphicx,tikz,booktabs,array,tabularx,enumitem,ragged2e,pifont,microtype}
\usetikzlibrary{calc,positioning,shapes.geometric,arrows.meta,shadows}
\usepackage[most]{tcolorbox}
\usepackage{titlesec,fancyhdr,tocloft}
\usepackage[hidelinks]{hyperref}
\usepackage{needspace,etoolbox}
\AtBeginDocument{\hypersetup{pdftitle={\titolopdf},pdfauthor={\autore},pdfsubject={\titolobreve}}}

\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt}
\raggedright
\setlength{\RaggedRightParindent}{0pt}
\emergencystretch=2em
\widowpenalty=10000 \clubpenalty=10000 \displaywidowpenalty=10000

% ---------------- Palette ----------------
\definecolor{navy}{HTML}{1F3A5F}
\definecolor{teal}{HTML}{1B8A8A}
\definecolor{blu}{HTML}{2A6FDB}
\definecolor{rosso}{HTML}{E0533D}
\definecolor{ambra}{HTML}{D9940F}
\definecolor{viola}{HTML}{6B4FBB}
\definecolor{verde}{HTML}{2E9E5B}
\definecolor{grigio}{HTML}{5A6170}
\definecolor{chiaro}{HTML}{EEF2F7}
\definecolor{testo}{HTML}{22262D}
\color{testo}

% vettori in grassetto
\newcommand{\x}{\mathbf{x}}
\newcommand{\vv}{\mathbf{v}}
\newcommand{\mmu}{\bm{\mu}}
\newcommand{\SSigma}{\bm{\Sigma}}
\newcommand{\argmax}{\operatorname*{arg\,max}}
\newcommand{\T}{^{\mathsf{t}}}
\newcommand{\hl}[1]{{\color{navy}\bfseries #1}}
\newcommand{\key}[1]{\textcolor{teal}{\textbf{#1}}}
\newcommand{\slide}[1]{{\headfont\footnotesize\color{grigio}\,[slide #1]}}

% ---------------- Liste ----------------
\setlist{itemsep=2pt,topsep=3pt,parsep=0pt}
\setlist[itemize,1]{label={\color{teal}\small$\blacktriangleright$},leftmargin=1.3em}
\setlist[itemize,2]{label={\color{ambra}\footnotesize$\bullet$},leftmargin=1.2em}
\setlist[enumerate,1]{label={\headfont\bfseries\color{navy}\arabic*.},leftmargin=1.6em}

% ---------------- Icone (tikz) ----------------
\newcommand{\iconbulb}{\tikz[baseline=-0.6ex,scale=.85]{\fill[white](0,.06)circle(.13);\fill[white](-.07,-.15)rectangle(.07,-.06);\draw[white,line width=.4pt](-.06,-.19)--(.06,-.19);}}
\newcommand{\iconwarn}{\tikz[baseline=-0.6ex]{\node[regular polygon,regular polygon sides=3,fill=white,inner sep=1.1pt,minimum size=11pt]{}; \node[font=\headblack\tiny,text=rosso] at (0,-.02){!};}}
\newcommand{\iconml}{\tikz[baseline=-0.6ex,scale=.8]{\foreach \y in {-.16,.16}{\fill[white](-.2,\y)circle(.05);} \foreach \y in {-.2,0,.2}{\fill[white](.2,\y)circle(.05);\draw[white,line width=.35pt](-.2,.16)--(.2,\y);\draw[white,line width=.35pt](-.2,-.16)--(.2,\y);}}}

% ---------------- Box ----------------
\tcbset{every box/.style={halign=flush left}}
\tcbset{
  base/.style={enhanced,unbreakable,arc=3pt,boxrule=0pt,left=11pt,right=11pt,top=9pt,bottom=8pt,
    before skip=12pt,after skip=12pt,fonttitle=\headfont\bfseries\small,
    attach boxed title to top left={xshift=10pt,yshift=-9pt},
    boxed title style={arc=2.5pt,boxrule=0pt,left=6pt,right=6pt,top=2pt,bottom=2pt},
    overlay unbroken and first={}},
}
\DeclareTColorBox{intuizione}{ O{Intuizione} O{} }{base,colback=teal!6,colbacktitle=teal,coltitle=white,
  borderline west={3pt}{0pt}{teal},title={\iconbulb\ \ #1},top=13pt,#2}
\DeclareTColorBox{tecnica}{ O{In termini tecnici} O{} }{base,colback=navy!5,colbacktitle=navy,coltitle=white,
  borderline west={3pt}{0pt}{navy},title={$\Sigma$\ \ #1},top=13pt,#2}
\DeclareTColorBox{esempio}{ O{Esempio} O{} }{base,colback=ambra!7,colbacktitle=ambra,coltitle=white,
  borderline west={3pt}{0pt}{ambra},title={\ding{46}\ \ #1},top=13pt,#2}
\DeclareTColorBox{attenzione}{ O{Attenzione} O{} }{base,colback=rosso!6,colbacktitle=rosso,coltitle=white,
  borderline west={3pt}{0pt}{rosso},title={\iconwarn\ \ #1},top=13pt,#2}
\DeclareTColorBox{mlbox}{ O{Approfondimento} O{} }{base,colback=viola!6,colbacktitle=viola,coltitle=white,
  borderline west={3pt}{0pt}{viola},title={\iconml\ \ #1},top=13pt,#2}
\newtcolorbox{formula}[1][]{enhanced,arc=5pt,boxrule=0.9pt,colframe=navy!55,colback=white,
  left=8pt,right=8pt,top=6pt,bottom=6pt,before skip=10pt,after skip=10pt,halign=flush center,
  #1}
\newtcolorbox{formulat}[1]{enhanced,arc=5pt,boxrule=0.9pt,colframe=navy!55,colback=white,
  left=8pt,right=8pt,top=10pt,bottom=6pt,before skip=14pt,after skip=10pt,halign=flush center,
  attach boxed title to top center={yshift=-8pt},boxed title style={colback=navy!55,arc=2pt,boxrule=0pt,top=1pt,bottom=1pt},
  fonttitle=\headfont\bfseries\footnotesize,coltitle=white,title={#1}}
\newtcolorbox{appunti}[1]{enhanced,unbreakable,arc=4pt,boxrule=.8pt,colframe=grigio!60,colback=chiaro,
  left=12pt,right=12pt,top=12pt,bottom=10pt,before skip=16pt,after skip=8pt,
  fonttitle=\headfont\bfseries\small,coltitle=white,colbacktitle=grigio,
  attach boxed title to top left={xshift=10pt,yshift=-9pt},boxed title style={arc=2.5pt,boxrule=0pt,left=6pt,right=6pt},
  title={\ding{43}\ \ #1},fontupper=\small}
\newcommand{\pag}[1]{\par\vspace{4pt}{\headfont\bfseries\scriptsize\setlength{\fboxsep}{1.5pt}\colorbox{teal}{\color{white}\,p.\,#1\,}}\enspace}

% ---------------- Titoli ----------------
\newcounter{sez}
\newcommand{\sezione}[3]{% num titolo slide
  \clearpage
  \refstepcounter{section}
  \addcontentsline{toc}{section}{\protect\numberline{\thesection}#2}
  \markboth{#2}{#2}
  \begin{tikzpicture}
    \fill[navy,rounded corners=8pt] (0,0) rectangle (\textwidth,2.6cm);
    \fill[teal,rounded corners=8pt] (0,0) rectangle (2.6cm,2.6cm);
    \fill[teal] (1.6cm,0) rectangle (2.6cm,2.6cm);
    \node[font=\headblack\fontsize{40}{40}\selectfont,text=white] at (1.3cm,1.3cm) {\thesection};
    \node[anchor=south west,font=\headfont\bfseries\fontsize{19}{22}\selectfont,text=white,text width=\textwidth-3.6cm,align=left] at (3.0cm,.85cm) {#2};
    \node[anchor=west,font=\headlight\small,text=white!80!teal] at (3.1cm,.48cm) {\etichettasezione\ #1 \quad·\quad #3};
  \end{tikzpicture}
  \par\vspace{6pt}
}
\titleformat{\subsection}{\headfont\bfseries\large\color{navy}}{\colorbox{teal!15}{\color{teal}\thesubsection}}{0.6em}{}
\titlespacing*{\subsection}{0pt}{16pt}{6pt}
% un titolo non resta mai da solo in fondo alla pagina
\pretocmd{\subsection}{\Needspace{9\baselineskip}}{}{}
\pretocmd{\subsubsection}{\Needspace{6\baselineskip}}{}{}
\titleformat{\subsubsection}{\headfont\bfseries\normalsize\color{teal}}{}{0em}{}
\titlespacing*{\subsubsection}{0pt}{10pt}{3pt}

% ---------------- Header / footer ----------------
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyhead[L]{\headfont\footnotesize\color{grigio}\titolobreve}
\fancyhead[R]{\headfont\footnotesize\color{teal}\leftmark}
\fancyfoot[C]{\tikz{\node[circle,fill=navy,text=white,font=\headfont\bfseries\footnotesize,minimum size=17pt,inner sep=0pt]{\thepage};}}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\tikz{\node[circle,fill=navy,text=white,font=\headfont\bfseries\footnotesize,minimum size=17pt,inner sep=0pt]{\thepage};}}}

% ---------------- Indice ----------------
\renewcommand{\cfttoctitlefont}{\headfont\bfseries\Huge\color{navy}}
\renewcommand{\cftsecfont}{\headfont\bfseries\color{navy}}
\renewcommand{\cftsecpagefont}{\headfont\bfseries\color{teal}}
\renewcommand{\cftsecleader}{\color{grigio!50}\cftdotfill{\cftdotsep}}
\renewcommand{\cftsubsecfont}{\headfont\small\color{grigio}}
\renewcommand{\cftsubsecpagefont}{\headfont\small\color{grigio}}
\setlength{\cftbeforesecskip}{7pt}
\setcounter{tocdepth}{1}

% tabelle
\newcommand{\thd}[1]{{\headfont\bfseries\small\color{white}#1}}
\renewcommand{\arraystretch}{1.25}
\renewcommand{\tabularxcolumn}[1]{m{#1}}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcommand{\fig}[2][\linewidth]{\begin{center}\includegraphics[width=#1]{figs/#2}\end{center}}
% figura + didascalia sempre sulla stessa pagina: \figura[larghezza]{file.pdf}{didascalia}
\newcommand{\figura}[3][\linewidth]{\par\noindent\begin{minipage}{\linewidth}\fig[#1]{#2}\didascalia{#3}\end{minipage}\par}
\newcommand{\didascalia}[1]{\vspace{-8pt}\begin{center}\begin{minipage}{.9\linewidth}\centering\headfont\footnotesize\color{grigio}#1\end{minipage}\end{center}\vspace{-2pt}}


% ---------------- Codice e terminali ----------------
\setmonofont{DejaVu Sans Mono}[Scale=0.84]
\usepackage{listings}
\definecolor{termbg}{HTML}{14202E}
\definecolor{termfg}{HTML}{E4E9F0}
\definecolor{termprompt}{HTML}{5FD3B4}
\definecolor{termhl}{HTML}{F5C04A}
\definecolor{termdim}{HTML}{8A97A8}
\lstdefinestyle{term}{basicstyle=\ttfamily\small\color{termfg},columns=fullflexible,keepspaces=true,
  breaklines=false,
  showstringspaces=false,upquote=true,
  moredelim=[is][\color{termprompt}\bfseries]{§}{§},
  moredelim=[is][\color{termhl}\bfseries]{¤}{¤},
  moredelim=[is][\color{termdim}\itshape]{°}{°},
  literate={à}{{\`a}}1 {è}{{\`e}}1 {é}{{\'e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1}
\lstdefinestyle{file}{basicstyle=\ttfamily\small\color{testo},columns=fullflexible,keepspaces=true,breaklines=false,
  upquote=true,showstringspaces=false,
  moredelim=[is][\color{teal}\bfseries]{§}{§},
  moredelim=[is][\color{rosso}\bfseries]{¤}{¤},
  moredelim=[is][\color{grigio}\itshape]{°}{°},
  literate={à}{{\`a}}1 {è}{{\`e}}1 {é}{{\'e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1}
\tcbuselibrary{listings}
% terminale: argomento = titolo della finestra
\newtcblisting{terminale}[1]{enhanced,listing only,breakable,colback=termbg,colframe=termbg,arc=5pt,boxrule=0pt,
  left=9pt,right=9pt,top=4pt,bottom=4pt,before skip=9pt,after skip=9pt,
  listing options={style=term},
  title={\tikz[baseline=-.6ex]{\foreach \c [count=\i] in {rosso,ambra,verde}{\fill[\c](\i*.32,0)circle(.09);}}\hfill{\ttfamily\footnotesize\color{termdim}\detokenize{#1}}\hfill\phantom{\tikz{\fill(0,0)circle(.09);\fill(.64,0)circle(.09);}}},
  colbacktitle=termbg!80!white,coltitle=white,toptitle=3pt,bottomtitle=3pt,titlerule=0pt}
% file di configurazione: argomento = nome del file
\newtcblisting{filecfg}[1]{enhanced,listing only,breakable,colback=white,colframe=navy!40,arc=4pt,boxrule=.7pt,
  left=9pt,right=9pt,top=4pt,bottom=4pt,before skip=9pt,after skip=9pt,listing options={style=file},
  attach boxed title to top left={xshift=8pt,yshift=-8pt},boxed title style={colback=navy!70,arc=2pt,boxrule=0pt},
  fonttitle=\ttfamily\footnotesize\bfseries,coltitle=white,title={\detokenize{#1}},top=10pt}
\newcommand{\cmd}[1]{\texttt{\color{navy}#1}}
\newcommand{\inl}[1]{{\setlength{\fboxsep}{1.2pt}\colorbox{chiaro}{\ttfamily\small\color{navy}#1}}}
% scheda comando
\newtcolorbox{scheda}[2][]{enhanced,breakable,arc=4pt,boxrule=0pt,colback=white,
  borderline={.8pt}{0pt}{teal!60},left=11pt,right=11pt,top=10pt,bottom=8pt,before skip=14pt,after skip=12pt,
  title={\ttfamily\bfseries\normalsize #2},fonttitle=\color{white},colbacktitle=teal,
  toptitle=4pt,bottomtitle=4pt,#1}
\newcommand{\campo}[1]{\par\vspace{3pt}{\headfont\bfseries\footnotesize\color{teal}\MakeUppercase{#1}}\par\vspace{1pt}}
\tikzset{
  dev/.style={draw=navy,fill=white,line width=1pt,rounded corners=3pt,minimum width=1.25cm,minimum height=.75cm,font=\headfont\bfseries\small,text=navy},
  host/.style={dev,fill=blu!8,draw=blu},
  rtr/.style={circle,draw=teal,fill=teal!10,line width=1.1pt,minimum size=1.05cm,font=\headfont\bfseries\small,text=teal!70!black},
  cd/.style={draw=ambra,fill=ambra!15,line width=1pt,rounded corners=7pt,minimum width=1.0cm,minimum height=.62cm,font=\headfont\bfseries,text=ambra!60!black},
  lnk/.style={line width=1.2pt,color=grigio!80},
  lab/.style={font=\ttfamily\scriptsize,text=testo,fill=white,inner sep=1.2pt,rounded corners=1pt},
  ipl/.style={font=\ttfamily\scriptsize\bfseries,text=rosso!85!black,fill=white,inner sep=1.2pt},
  macl/.style={font=\ttfamily\scriptsize,text=viola,fill=viola!8,inner sep=1.5pt,rounded corners=1pt},
  netl/.style={font=\ttfamily\scriptsize\bfseries,text=verde!70!black,fill=verde!8,draw=verde!50,rounded corners=2pt,inner sep=2pt},
}
\newcommand{\wsrow}[7]{\rowcolor{#7}#1 & #2 & #3 & #4 & #5 & #6\\}

\newcommand{\sint}[1]{{\ttfamily\small\color{navy}\raggedright #1\par}}


% ---------------- Codice sincronizzato con i file (manuali con codice) ----------------
% Regola: il codice e l'output NON si copiano a mano nel .tex: si includono dai file veri.
\definecolor{pykw}{HTML}{1F3A5F}
\definecolor{pystr}{HTML}{2E7D4F}
\definecolor{pycom}{HTML}{6B7280}
\definecolor{pybg}{HTML}{F7F9FC}
\lstdefinestyle{py}{language=Python,basicstyle=\ttfamily\small\color{testo},columns=fullflexible,keepspaces=true,
  breaklines=false,upquote=true,showstringspaces=false,
  keywordstyle=\color{pykw}\bfseries,stringstyle=\color{pystr},commentstyle=\color{pycom}\itshape,
  morekeywords={as,with,None,True,False,self},emphstyle=\color{teal}\bfseries,
  numbers=left,numberstyle=\tiny\color{grigio},numbersep=7pt,xleftmargin=12pt,
  literate={à}{{\`a}}1 {è}{{\`e}}1 {é}{{\'e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1}
% parole da evidenziare in teal nei listati (classi/funzioni chiave dell'argomento)
\newcommand{\paroleevidenziate}[1]{\lstset{emph={#1}}}
\tcbset{codicestyle/.style={enhanced,listing only,colback=pybg,colframe=teal!55,arc=4pt,boxrule=.7pt,
  left=4pt,right=8pt,top=10pt,bottom=4pt,before skip=12pt,after skip=10pt,
  attach boxed title to top left={xshift=8pt,yshift=-8pt},boxed title style={colback=teal,arc=2pt,boxrule=0pt},
  fonttitle=\ttfamily\footnotesize\bfseries,coltitle=white},
  outputstyle/.style={enhanced,listing only,colback=termbg,colframe=termbg,arc=5pt,boxrule=0pt,
  left=9pt,right=9pt,top=4pt,bottom=4pt,before skip=9pt,after skip=9pt,
  colbacktitle=termbg!80!white,coltitle=white,toptitle=3pt,bottomtitle=3pt,titlerule=0pt,
  fonttitle=\ttfamily\footnotesize}}
% \codicefile[opzioni]{file.py}{prima}{ultima}: righe reali del file, numerate come nel file.
%   Fino a ~25 righe il blocco resta unito; oltre, passa [breakable] oppure dividi in più blocchi.
\newcommand{\codicefile}[4][]{\tcbinputlisting{codicestyle,listing file=code/#2,
  listing options={style=py,firstline=#3,lastline=#4,firstnumber=#3},
  title={\ding{230}\ \detokenize{#2}\ \ (righe #3–#4)},#1}}
% \codicefileintero[opzioni]{file.py}: tutto il file
\newcommand{\codicefileintero}[2][]{\tcbinputlisting{codicestyle,listing file=code/#2,
  listing options={style=py},title={\ding{230}\ \detokenize{#2}},#1}}
% \outputfile[opzioni]{output/file.txt}{titolo}: output salvato dall'esecuzione reale
\newcommand{\outputfile}[3][]{\tcbinputlisting{outputstyle,listing file=#2,listing options={style=term},
  title={\tikz[baseline=-.6ex]{\foreach \c [count=\i] in {rosso,ambra,verde}{\fill[\c](\i*.32,0)circle(.09);}}\hfill{\ttfamily\footnotesize\color{termdim}\detokenize{#3}}\hfill\phantom{\tikz{\fill(0,0)circle(.09);\fill(.64,0)circle(.09);}}},#1}}
% codice scritto direttamente nel .tex (solo frammenti brevi che non esistono come file)
\newtcblisting{codice}[1]{codicestyle,listing options={style=py},title={\ding{230}\ \detokenize{#1}}}
% richiamo di righe nel testo: \rr{36} oppure \rr{36}[41]  ->  r. 36–41
\NewDocumentCommand{\rr}{m o}{{\headfont\bfseries\scriptsize\setlength{\fboxsep}{1.4pt}%
  \colorbox{teal!15}{\color{teal!70!black}r.\,#1\IfValueT{#2}{–#2}}}}

% ---------------- Esercizi e soluzioni ----------------
\DeclareTColorBox{esercizi}{ O{Esercizi} O{} }{base,colback=blu!5,colbacktitle=blu,coltitle=white,
  borderline west={3pt}{0pt}{blu},title={\ding{45}\ \ #1},top=13pt,#2}
% nelle soluzioni (appendice): \soluzione{1.2}{testo}
\newcommand{\soluzione}[2]{\par\vspace{4pt}{\headfont\bfseries\small\color{blu}Esercizio #1.}\enspace #2\par}

% ---------------- Elementi per manuali senza formule/codice ----------------
\DeclareTColorBox{consiglio}{ O{Consiglio} O{} }{base,colback=verde!6,colbacktitle=verde,coltitle=white,
  borderline west={3pt}{0pt}{verde},title={\ding{51}\ \ #1},top=13pt,#2}
% passi numerati con cerchi (procedure, istruzioni d'uso)
\newlist{passi}{enumerate}{1}
\setlist[passi]{label={\protect\tikz[baseline=(n.base)]\protect\node[circle,fill=teal,text=white,font=\headfont\bfseries\footnotesize,inner sep=0pt,minimum size=1.35em](n){\arabic*};},leftmargin=2.1em,itemsep=6pt,topsep=6pt}
% box «In breve» per riassunti di poche righe in apertura di capitolo
\newtcolorbox{inbreve}{enhanced,arc=4pt,boxrule=0pt,colback=chiaro,left=12pt,right=12pt,top=8pt,bottom=8pt,
  borderline north={2pt}{0pt}{teal},fontupper=\small,before skip=6pt,after skip=10pt}
```

## Template: main.tex di esempio (copertina, «Come usare», indice, capitolo tecnico, capitolo senza formule, capitolo con codice, soluzioni)

Per provarlo: `code/demo.py` (tre righe che stampano una media), `output/demo.txt` prodotto da `controlla_codice.py` e `figs/grafico.pdf`.

```latex
\input{preamble}
\begin{document}
% ================= COPERTINA =================
\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  \fill[navy] (current page.north west) rectangle ([yshift=-15.5cm]current page.north east);
  \fill[teal] ([yshift=-15.5cm]current page.north west) rectangle ([yshift=-16.1cm]current page.north east);
  \node[anchor=north west,font=\headfont\small\bfseries,text=ambra] at ([xshift=2.3cm,yshift=-2.2cm]current page.north west) {CORSO \,·\, ARGOMENTO};
  \node[anchor=north west,font=\headblack\fontsize{44}{48}\selectfont,text=white,align=left] at ([xshift=2.2cm,yshift=-3.0cm]current page.north west) {Titolo del\\[2pt]manuale};
  \node[anchor=north west,font=\headlight\Large,text=white!85!teal,align=left] at ([xshift=2.3cm,yshift=-6.9cm]current page.north west) {Sottotitolo descrittivo su una o due righe};
  % motivo decorativo (sostituibile con un disegno legato al tema)
  \begin{scope}[shift={([xshift=3cm,yshift=-12.8cm]current page.north west)}]
    \foreach \x/\h in {0/2.2,1.6/3.4,3.2/1.6,4.8/4.0,6.4/2.8,8.0/3.6,9.6/2.0,11.2/3.0,12.8/1.4}{
      \fill[white,opacity=.10,rounded corners=3pt] (\x,0) rectangle ++(1.1,\h);}
    \draw[ambra,line width=1.4pt] plot[smooth] coordinates {(0.55,2.6) (2.15,3.8) (3.75,2.0) (5.35,4.4) (6.95,3.2) (8.55,4.0) (10.15,2.4) (11.75,3.4) (13.35,1.8)};
  \end{scope}
\end{tikzpicture}
\vspace*{15.2cm}
\begin{center}
\begin{tcolorbox}[enhanced,width=.8\linewidth,colback=white,colframe=navy!35,arc=6pt,boxrule=.8pt,halign=flush center,top=8pt,bottom=8pt]
\large Formula, comando o frase chiave dell'argomento
\end{tcolorbox}
\vspace{1cm}
{\headfont\large\color{navy}\bfseries Dispensa / Manuale di studio\par}
\vspace{2pt}
{\headfont\color{grigio}\autore \,·\, breve descrizione \,·\, A.A. 2026–2027 o versione\par}
\vspace{1cm}
\begin{tikzpicture}
  \foreach \c/\t [count=\i] in {teal/Intuizione,navy/Tecnica,ambra/Esempi,rosso/Attenzione,viola/Approfondimento}{
    \node[fill=\c,text=white,font=\headfont\bfseries\footnotesize,rounded corners=3pt,minimum width=2.5cm,minimum height=.6cm] at (\i*2.85,0) {\t};}
\end{tikzpicture}
\end{center}
% ================= COME USARE + INDICE =================
\clearpage\thispagestyle{plain}
{\headfont\bfseries\Huge\color{navy}Come usare questo manuale\par}
\vspace{4pt}{\color{teal}\rule{3cm}{2.5pt}}\vspace{8pt}

Spiega in poche righe come è organizzato il documento e il significato dei riquadri.
\begin{intuizione}L'idea di fondo, senza formule.\end{intuizione}
\begin{tecnica}Definizioni, formule e passaggi.\end{tecnica}
\begin{esempio}Esempi svolti passo per passo.\end{esempio}
\begin{attenzione}Errori tipici e precisazioni.\end{attenzione}
\begin{mlbox}Collegamenti e approfondimenti.\end{mlbox}
\begin{formulat}{Formula chiave}Le formule da ricordare.\end{formulat}
\begin{esercizi}Esercizi di fine capitolo, con soluzioni in appendice.\end{esercizi}
% nella legenda metti SOLO i box usati davvero nel documento
\clearpage\thispagestyle{plain}
\tableofcontents
% ================= CAPITOLO =================
\sezione{1}{Titolo del capitolo}{slide 3–12 / sottotitolo}
\subsection{Primo paragrafo}
Testo normale con \hl{evidenziazione navy} e \key{parola chiave teal}.
\begin{formula}$\displaystyle P(A|B)=\frac{P(A\cap B)}{P(B)}$\end{formula}
\begin{terminale}{pc1}
§root@pc1:/#§ ip address
inet ¤195.11.14.5/24¤ scope global eth0   °# commento°
\end{terminale}
\begin{filecfg}{lab.conf}
§pc1[0]§="A/00:00:00:00:00:01"
\end{filecfg}
\begin{scheda}{comando}
\campo{Sintassi}\sint{comando [opzioni] ARGOMENTO}
\campo{Cosa fa}Descrizione.
\end{scheda}
\begin{center}
\rowcolors{2}{chiaro}{white}
\begin{tabularx}{\linewidth}{l Y}
\rowcolor{navy}\thd{Colonna} & \thd{Descrizione}\\
a & b\\ c & d\\
\end{tabularx}
\end{center}
\begin{appunti}{— Capitolo 1}
\pag{3} Appunto breve per la slide 3.
\pag{4} Appunto breve per la slide 4.
\end{appunti}
\sezione{2}{Capitolo senza formule}{istruzioni d'uso}
\begin{inbreve}In questo capitolo: come accendere l'apparecchio e fare il primo utilizzo.\end{inbreve}
\begin{passi}
  \item Collega il cavo di alimentazione.
  \item Tieni premuto il tasto di accensione per 3 secondi.
  \item Attendi che la spia diventi verde.
\end{passi}
\begin{consiglio}Pulisci il filtro una volta al mese: la macchina dura di più.\end{consiglio}
\begin{attenzione}[Sicurezza]Non aprire il coperchio con l'apparecchio acceso.\end{attenzione}
\begin{appunti}{Riepilogo del capitolo}Punti chiave.\end{appunti}
% ================= CAPITOLO CON CODICE (manuali tecnici) =================
\sezione{3}{Capitolo con codice}{codice e output presi dai file veri}
\paroleevidenziate{mean}
\codicefile{demo.py}{1}{5}
In \rr{4} si definiscono i dati; in \rr{4}[5] si calcola e si stampa la media.
\outputfile{output/demo.txt}{python demo.py}
\figura[.8\linewidth]{grafico.pdf}{Didascalia: resta sulla stessa pagina della figura.}
\begin{tecnica}[Box lungo][breakable]Solo i box più lunghi di mezza pagina possono spezzarsi.\end{tecnica}
\begin{esercizi}
\begin{passi}\item Calcola la mediana degli stessi valori.\end{passi}
\end{esercizi}
\begin{appunti}{Riepilogo del capitolo}Punti chiave.\end{appunti}
% ================= APPENDICE: SOLUZIONI =================
\clearpage
\phantomsection\addcontentsline{toc}{section}{Soluzioni degli esercizi}
{\headfont\bfseries\Huge\color{navy}Soluzioni degli esercizi\par}
\vspace{4pt}{\color{teal}\rule{3cm}{2.5pt}}\vspace{8pt}
\soluzione{3.1}{La mediana di $\{3,5,8\}$ è 5.}
\end{document}
```

## Strumento: controlla_codice.py

Salvalo nella cartella del manuale ed eseguilo con `python3 controlla_codice.py code/*.py`.

```python
#!/usr/bin/env python3
"""Controlla gli script didattici prima di includerli nel manuale.

Uso:  python3 controlla_codice.py code/*.py   (dalla cartella del manuale)
- righe al massimo di 78 caratteri;
- import tutti in testa al file e nessun import inutilizzato;
- lo script gira senza errori né warning; l'output viene salvato in
  output/<nome>.txt per essere incluso con \\outputfile.
Esce con codice 1 se trova problemi.
"""
import ast
import pathlib
import subprocess
import sys

MAX = 78
problemi = 0


def segnala(f, msg):
    global problemi
    problemi += 1
    print(f"  ✗ {f}: {msg}")


for nome in sys.argv[1:]:
    f = pathlib.Path(nome)
    testo = f.read_text(encoding="utf-8")
    print(f"• {f.name}")
    for i, riga in enumerate(testo.splitlines(), 1):
        if len(riga) > MAX:
            segnala(f.name, f"riga {i} lunga {len(riga)} caratteri (max {MAX})")
    albero = ast.parse(testo)
    importati, fine_testa = {}, True
    for nodo in albero.body:
        e_import = isinstance(nodo, (ast.Import, ast.ImportFrom))
        e_doc = (isinstance(nodo, ast.Expr)
                 and isinstance(nodo.value, ast.Constant))
        if e_import and not fine_testa:
            segnala(f.name, f"import non in testa (riga {nodo.lineno})")
        if not (e_import or e_doc):
            fine_testa = False
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.Import, ast.ImportFrom)):
            for a in nodo.names:
                nome_locale = (a.asname or a.name).split(".")[0]
                importati[nome_locale] = nodo.lineno
    usati = {n.id for n in ast.walk(albero) if isinstance(n, ast.Name)}
    usati |= {n.value.id for n in ast.walk(albero)
              if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    for n, riga in importati.items():
        if n not in usati:
            segnala(f.name, f"import inutilizzato '{n}' (riga {riga})")
    r = subprocess.run([sys.executable, "-W", "always", f.name],
                       cwd=f.parent, capture_output=True, text=True)
    if r.returncode != 0:
        segnala(f.name, "errore in esecuzione:\n" + r.stderr[-800:])
    elif "Warning" in r.stderr:
        segnala(f.name, "warning in esecuzione:\n" + r.stderr[-800:])
    out = f.parent.parent / "output" / (f.stem + ".txt")
    out.parent.mkdir(exist_ok=True)
    out.write_text(r.stdout, encoding="utf-8")
    for i, riga in enumerate(r.stdout.splitlines(), 1):
        if len(riga) > 90:
            segnala(f.name, f"riga {i} dell'output lunga {len(riga)} caratteri")

print("OK: nessun problema" if problemi == 0 else f"{problemi} problemi")
sys.exit(1 if problemi else 0)
```

## Strumento: controlla_pdf.py

Eseguilo dopo la seconda compilazione: `python3 controlla_pdf.py main.pdf`.

```python
#!/usr/bin/env python3
"""Controllo di qualità del PDF compilato.

Uso:  python3 controlla_pdf.py main.pdf
- trova «--» letterali e altri resti di markup nel testo estratto;
- segnala pagine quasi vuote e frammenti isolati in cima alla pagina;
- crea i fogli di anteprima qa/foglio-N.png (12 pagine ciascuno) da guardare.
Esce con codice 1 se trova problemi certi (markup grezzo).
"""
import glob
import pathlib
import re
import subprocess
import sys

from PIL import Image

pdf = pathlib.Path(sys.argv[1])
qa = pdf.parent / "qa"
qa.mkdir(exist_ok=True)
for vecchio in qa.glob("*.png"):
    vecchio.unlink()

n = int(re.search(r"Pages:\s+(\d+)",
                  subprocess.run(["pdfinfo", pdf], capture_output=True,
                                 text=True).stdout).group(1))
errori, avvisi = [], []
RESTI = [(r"(?<![-\w])--(?!-)", "«--» letterale (usa –)"),
         (r"\\[a-zA-Z]+\{", "comando LaTeX non interpretato"),
         (r"\?\?", "riferimento non risolto (??)"),
         (r"¤", "delimitatore dei listing rimasto nel testo")]

for p in range(1, n + 1):
    testo = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l",
                            str(p), pdf, "-"], capture_output=True,
                           text=True).stdout
    for regex, msg in RESTI:
        for m in re.finditer(regex, testo):
            riga = testo[:m.start()].count("\n")
            frammento = testo.splitlines()[riga].strip()[:70]
            errori.append(f"p. {p}: {msg} → «{frammento}»")
    righe = [r.strip() for r in testo.splitlines() if r.strip()]
    if p > 2 and len(righe) > 2:
        prima = righe[1]          # righe[0] è l'intestazione
        solo_chiusura = re.fullmatch(r"[\)\]\}\s,;:.]+", prima)
        fine_frase = len(prima.split()) <= 3 and prima.endswith((".", ";", ":"))
        if solo_chiusura or fine_frase:
            avvisi.append(f"p. {p}: frammento isolato in cima → «{prima}»")

subprocess.run(["pdftoppm", "-r", "45", "-png", pdf, qa / "p"], check=True)
pagine = sorted(glob.glob(str(qa / "p-*.png")))
for i, f in enumerate(pagine, 1):
    im = Image.open(f).convert("L")
    w, h = im.size
    corpo = im.crop((0, int(h * .07), w, int(h * .90)))   # senza testata/piede
    bbox = corpo.point(lambda v: 255 if v < 200 else 0).getbbox()
    riemp = bbox[3] / corpo.size[1] if bbox else 0
    if 2 < i < len(pagine) and riemp < 0.40:
        avvisi.append(f"p. {i}: pagina piena solo al {riemp:.0%} "
                      "(accettabile solo se un blocco intero è slittato)")
for k in range(0, len(pagine), 12):
    ims = [Image.open(f) for f in pagine[k:k + 12]]
    w, h = ims[0].size
    foglio = Image.new("RGB", (w * 6, h * 2), "white")
    for j, im in enumerate(ims):
        foglio.paste(im, ((j % 6) * w, (j // 6) * h))
    foglio.save(qa / f"foglio-{k // 12 + 1}.png")
for f in pagine:
    pathlib.Path(f).unlink()

print(f"{n} pagine controllate")
for e in errori:
    print("  ✗", e)
for a in avvisi:
    print("  ⚠", a)
print(f"Fogli di anteprima in {qa}/ — guardali tutti prima di consegnare.")
sys.exit(1 if errori else 0)
```
