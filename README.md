# Ticketing

Il progetto consiste nella creazione di un sistema di vendita ticket per eventi (cinema, concerti, convegni, etc..) e nella gestione dell'assegnazione dei posti all'utente dedito all'acquisto. Vengono gestiti anche i processi che portano alla scelta del provider per l'acquisto di uno o più biglietti.

Il sistema di biglietteria deve soddisfare i seguenti requisiti:

Richieste funzionali:

    - L'utente può prenotare i biglietti per uno spettacolo specifico.
    - L'utente può prenotare più di un biglietto contemporaneamente.
    - L'utente può prenotare posti specifici o, almeno, richiedere “N posti insieme”.
    - Una volta che l'utente ha selezionato il/i posto/i, gli viene concesso un periodo di tempo di 10 minuti per pagarlo.
    - Durante questo periodo di tempo, i posti sono considerati riservati per la sessione di questo utente.
    - Gli altri utenti dovrebbero vedere questi posti come temporaneamente non disponibili.
    - Possono comunque rientrare nel pool di posti disponibili se l'utente che li "detiene" decide di interrompere la transazione o se l'utente non paga i posti in tempo.
    - Il sistema di pagamento è esterno e utilizzato tramite API (es. Paypal)

Requisiti non funzionali

    - Consistenza
        - Ovviamente non vendere lo stesso posto due volte.
        - Riporta rapidamente i posti in piscina.
    - Reattività
        - La mappa dei posti dovrebbe riflettere in ogni momento la mappa dell'occupazione effettiva, con bassa latenza.
        - Tieni presente che il rapporto lettura-scrittura può essere piuttosto elevato.
    - Disponibilità
        - Il sistema dovrebbe servire correttamente le richieste degli utenti finali, anche se i singoli nodi, responsabili di quanto sopra, muoiono o si comportano male. Non perdere i dati dei biglietti già venduti, così come le sessioni di acquisto attualmente aperte.

# Gestione Entità

Le entità principali consisteranno in Utenti, Spettacoli, Posti, Prenotazioni, e Pagamenti.

User come entità esiste già.

Gli spettacoli saranno identificati con l'entità `Event`:
- `id`
- `name`
- `date`

I posti di ogni evento saranno identificati con l'entità `Seat`:
- `id`
- `event_id`
- `row`
- `column`
- `status`
- `price`
- `reservated_at`

Il campo `status` è un enum che può avere come valori `AVAILABLE`, `RESERVERD`, `SOLD`

Le prenotazioni sono i biglietti che saranno prenotati e saranno identificati con l'entità `Ticket`:
- `id`
- `user_id`
- `seat_id`
- `payment_id`
- `status`

Il campo `status` è un enum che può avere come valori `PENDING`, `PAID`, `CANCELLED`

Come anticipato dall'entita `Ticket` l'entità per gestire i pagamenti sarà `Payment`:
- `id`
- `user_id`
- `amount`
- `provider`
- `status`

Il campo `privder` è un enum che può avere come valori `PAYPAL`, `OTHER`
Il campo `status` è un enum che può avere come valori `PENDING`, `SUCCESS`, `FAILED`

# Gestione flusso prenotazione

## 1. Selezione posti e creazione ticket

Un utente può selezionare uno o piu posti, bisognerà quindi verificare che siano disponibili, se lo sono apro una transaction a db e aggiorno lo stato dei posti a reserved impostando anche il reserved_at cosi che rimanga bloccato per 10 minuti.
Per ogni posto prenotato creo un ticket inserendo come stato pending e chiudo la transaction.

## 2. Conferma prenotazione

Nei 10 minuti nella quale il posto è prenotato, l'utente può procedere con il pagamento del biglietto (o dei biglietti in caso di più posti prenotati a suo nome), viene creato quindi un ordine di pagamento con status pending che reindirizza l'utente al provider selezionato, ad esempio paypal.
Il pagamento verrà simulato e una volta concluso apro una transaction a db: lo status del pagamento verrà impostato a success, i ticket collegati a paid e i posti avranno status sold e si potrà fare a meno del reserved_at.