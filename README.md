# Supaprastintos blokų grandinės (blockchain) kūrimas

Šios užduoties tikslas – sukurti supaprastintą blokų grandinę (angl. blockchain), kurios duomenų sluoksnio struktūra pavaizduota žemiau:
![image](https://raw.githubusercontent.com/IgnasTamosaitis/simplifiedBlockchain/refs/heads/main/images/struktura.png)

Sistema imituoja supaprastintą blokų grandinės veikimą – generuoja vartotojus, kuria transakcijas, formuoja blokus, skaičiuoja Merkle medį, atlieka *Proof-of-Work*  ir užtikrina vientisumą pasitelkiant *hash*.

---

### Pagrindinės Funkcijos

1. **Blokų generavimas**  
   Sistema surenka transakcijas ir suformuoja naują bloką.  
   Kiekvienas blokas turi:
   - ankstesnio bloko hash,
   - savo hash,
   - Merkle Root (visų transakcijų ID sujungtas į vieną maišą),
   - nonce (naudojamas PoW).

2. **Transakcijų tikrinimas**  
   Prieš įtraukiant transakciją į bloką, tikrinama:
   - ar siuntėjas egzistuoja,
   - ar gavėjas egzistuoja,
   - ar siuntėjas turi pakankamai balanso,
   - ar transakcijos hash sutampa su perskaičiuotu (vientisumo tikrinimas).

3. **Proof-of-Work (PoW)**  
   Blokas laikomas iškastu tik tada, kai jo hash prasideda nurodytu kiekiu nulių (sitam projekte → `"000"`).  
   Nonce didinamas tol, kol randamas tinkamas hash, taip užtikrinama apsauga nuo klastojimo.

4. **Merkle Root hash**  
   Iš visų bloko transakcijų ID sudaromas Merkle Tree ir apskaičiuojama jo šaknis.  
   Pasikeitus bent vienai transakcijai → keičiasi Merkle Root → keičiasi bloko hash → iškart matyti klastojimas.

5. **Decentralizuoto kasimo imitacija (konkurencija)**  
   Sistema sukuria kelis „kandidatinius blokus“, kurie vienu metu bando rasti tinkamą hash.  
   - Jei per limitą niekas neranda – didinamos ribos,
   - Jei vis tiek nesiseka – priimamas kandidatas su mažiausiu hash (fallback mechanizmas).  
   Tai imituoja konkurencinį kasimą kaip realiame blockchain tinkle.

---
### Projekto struktūra

```
simplified_blockchain/
│
├── models/
│   ├── __init__.py           # Paketo inicializacija
│   ├── blockchain.py         # Pagrindinė blockchain logika
│   ├── block.py              # Block ir BlockHeader klasės
│   ├── transaction.py        # Transaction klasė su verifikacija
│   ├── user.py               # User klasė balansų valdymui
│   ├── merkle_tree.py        # Merkle Tree implementacija (v0.2)
│   └── mining_pool.py        # Lygiagretaus kasimo imitacija (v0.2)
│
├── hash_utils.py             # Pasirinktinė maišos funkcija
├── main.py                   # Programos paleidimo failas
└── README.md                 # Projekto aprašymas ir instrukcijos
```

### Paleidimas

Reikalavimai:
- **Python 3.8+**
- Papildomų bibliotekų nereikia (naudojama tik standartinė biblioteka)

Paleidimas:
```bash
python main.py
```
---

## Veikimo esmė: v0.1 → v0.2

Ši sistema imituoja supaprastintą blockchain veikimą: sukuriami vartotojai, formuojamos transakcijos, jos tikrinamos, blokuojamos į blokus, skaičiuojamas Merkle Root ir vykdomas Proof-of-Work kasimas. Pabaigoje gaunama nuosekli blokų grandinė, kurioje kiekvienas blokas priklausomas nuo ankstesnio.

---

### v0.1 – bazinis veikimas (vienas kasėjas, PoW)

**Procesas:**
1. Sugeneruojami vartotojai.
2. Sukuriamos transakcijos tarp jų.
3. Surinkus tam tikrą kiekį transakcijų – formuojamas blokas.
4. Blokas kasamas kol jo hash prasideda `000`.
5. Blokas pridedamas prie grandinės.

**Pagrindinis pavyzdys:**
```python
from models.blockchain import Blockchain

# Pradinė sistema
bc = Blockchain(difficulty_target="000")

# Duomenų generavimas
bc.generate_users(n=200)
bc.generate_transactions(m=1500)

# Kasimas po 50 transakcijų į bloką
bc.mine_until_done(block_tx_count=50)

print(bc.summary())

```

Kas svarbiausia v0.1:

* Nonce didinamas kol hash atitinka 000….
* Hash skaičiuojamas iš Block Header, todėl pakeitus bet ką bloko antraštėje, keičiasi visas hash.
* Kiekvienas blokas saugo ankstesnio bloko hash → grandinė negali būti pakeista tyliai.


Tipinė v0.1 blokų išvestis:

```python
============================================================
BLOCK #3
============================================================
Hash:              000c7f...a81
Previous Hash:     0004b9...f3a
Merkle Root:       28f15fcd26275f85...
Timestamp:         1762281717
Difficulty Target: 000
Nonce:             30000
Transactions:      50
============================================================

```

### v0.2 – patobulinta versija (Merkle Tree + tikrinimas + konkurencinis kasimas)

* Tikras Merkle Tree, o ne tik sujungtas hash
* Transakcijų validacija (balansas, hash, siuntėjo/gavėjo egzistavimas)
* Konkurencinė kasyba su 5 kandidatais
* Laiko ir bandymų limitai
* Fallback mechanizmas – jei niekas neranda teisingo hash, priimamas geriausias (mažiausias) hash

Pagrindinis veikimas:

```python
from models.blockchain import Blockchain

blockchain = Blockchain(difficulty_target="000")

# Sugeneruojami duomenys
blockchain.generate_users(n=1000)
blockchain.generate_transactions(m=10000)

# Konkurencinis kasimas: 5 kandidatai, 100 txn per bloką
blockchain.mine_until_done(block_tx_count=100)

print(blockchain.summary())

```

O kas vyksta konkurencinio kasimo metu:

```python
candidates = mining_pool.create_candidates(
    all_transactions=pending,
    prev_block_hash=prev_hash,
    index=len(chain),
    version=1,
    difficulty_target="000",
    tx_per_block=100,
)

winner = mining_pool.mine_competitively(
    candidates=candidates,
    time_limit=3.0,
    max_attempts_per_round=150000,
)

```

- Sukuriami 5 skirtingi blokai su skirtingomis transakcijomis
- Visi vienu metu bando rasti hash, prasidedantį 000
- Jei nepavyksta — didinami limitai
- Jei vis tiek nepavyksta — priimamas mažiausias hash (fallback), kad grandinė nestovėtų


Realus v0.2 rezultatas: 

```yaml

============================================================
🧱 BLOCK #96
============================================================
Hash:              c018a09e3825865b3e4344f882aed21008f9af8c2a501433da8b7d39ac0b7c1d
Previous Hash:     b0fcf2ac16292bf7d09cedb7fe2c7a28...
Merkle Root:       28f15fcd26275f85316896510da0ad456ce926964fb85639b924b681e3c4b8c2
Timestamp:         1762281717
Difficulty Target: 000
Nonce:             30000
Transactions:      5
============================================================

📜 TRANSACTIONS (showing first 3 of 5):
------------------------------------------------------------
Tx #1: 0daccfbe-090d-46...
  From:   User_a07ad7 → 1994
  To:     User_4baeb2
  Hash:   9dc73ce39509146162f2adeb25d54ec9...

Tx #2: da493848-29e6-44...
  From:   User_7ab952 → 3794
  To:     User_170a6f
  Hash:   4ccb6abdc4aa28c3122601237bd45b3c...

Tx #3: 1bdca732-541d-43...
  From:   User_9d821a → 3727
  To:     User_0a340c
  Hash:   ac2f100dc0e561830a6d36556199a5a5...
------------------------------------------------------------

✅ Liko neapdorotų transakcijų: 0

============================================================
🎉 BLOCKCHAIN SUMMARY
============================================================
📊 Blokų skaičius:          97
👥 Vartotojų skaičius:      1000
📝 Apdorotų transakcijų:    9505
⏱️  Genesis timestamp:       1762281292
⏱️  Last block timestamp:    1762281717
🔗 Genesis hash:            6ec090a47d2789bd73dec592bed2db86...
🔗 Last block hash:         c018a09e3825865b3e4344f882aed210...
🌳 Last Merkle root:        28f15fcd26275f85316896510da0ad45...
============================================================


```


















## Versijos

### v0.2 (2025-11-05) ✅
**Naujos funkcijos:**
- ✅ **Merkle Tree implementacija** - Pilnas binarinis Merkle medis su tikru Merkle root hash
- ✅ **Transakcijų verifikacija:**
  - Balanso tikrinimas (siuntėjas negali siųsti daugiau, nei turi)
  - Transakcijos ID maišos reikšmės tikrinimas
  - Siuntėjo/gavėjo egzistavimo patikrinimas
- ✅ **Patobulintas kasimo procesas:**
  - 5 kandidatiniai blokai (~100 transakcijų kiekviename)
  - Konkurencinis kasimas su laiko limitu (5-10 sekundžių)
  - Automatinis bandymų skaičiaus didinimas, jei nepavyksta
  - Decentralizuoto kasimo simuliacija

**Techniniai patobulinimai:**
- Tikras Merkle root skaičiavimas blokų antraštėse
- Transakcijų validacija prieš pridedant į fondą
- Patobulintas konsolės išvedimas su kasimo progresu
- Optimizuota maišos funkcija (DJB2 algoritmo variantas)

### v0.1 (2025-10-29) ✅
**Pagrindinės funkcijos:**
- ✅ **Centralizuota blokų grandinė** - Pilna blockchain struktūra su susietu blokų sąrašu
- ✅ **Pasirinktinė maišos funkcija** - Custom hash algoritmas be išorinių bibliotekų
- ✅ **Transakcijų sistema:**
  - Transakcijų kūrimas tarp vartotojų
  - Unikalūs transakcijų ID (UUID)
  - Laiko žymos (timestamps)
  - Transakcijų maišos skaičiavimas
- ✅ **Blokų struktūra:**
  - BlockHeader su metadata (version, index, prev_hash, merkle_root, timestamp, difficulty, nonce)
  - Block su transakcijų sąrašu
  - Blokų hash skaičiavimas
- ✅ **Proof-of-Work kasimas:**
  - Nonce paieška
  - Konfigūruojamas difficulty target
  - Hash validacija
- ✅ **Konsolės išvedimas:**
  - Vizualus transakcijų kūrimo procesas
  - Detalus blokų kasimo procesas
  - Blockchain būsenos atnaujinimai
- ✅ **OOP praktikos:**
  - Enkapsuliacija (private metodai su _)
  - Konstruktoriai su parametrų validacija
  - Aiški klasių struktūra (User, Transaction, Block, BlockHeader, Blockchain)
  - RAII principai (resource management konstruktoriuose)

## Aprašymas
Šis projektas įgyvendina supaprastintą **blokų grandinės (Blockchain)** modelį su Merkle Tree ir konkurenciniu kasimu, skirtą edukaciniams tikslams.

Sistema imituoja:
- Vartotojų valdymą su balansais
- Transakcijų generavimą ir validaciją
- Merkle Tree struktūrų kūrimą
- Decentralizuotą kasimą su keliais kandidatais
- Proof-of-Work algoritmą

## Projekto struktūra

```
simplified_blockchain/
│
├── models/
│   ├── __init__.py           # Paketo inicializacija
│   ├── blockchain.py         # Pagrindinė blockchain logika
│   ├── block.py              # Block ir BlockHeader klasės
│   ├── transaction.py        # Transaction klasė su verifikacija
│   ├── user.py               # User klasė balansų valdymui
│   ├── merkle_tree.py        # Merkle Tree implementacija (v0.2)
│   └── mining_pool.py        # Konkurencinis kasimas (v0.2)
│
├── hash_utils.py             # Pasirinktinė maišos funkcija
├── main.py                   # Programos įėjimo taškas
└── README.md                 # Šis failas
```


## Naudojimas

### Reikalavimai
- **Python 3.8+**
- Nereikia papildomų bibliotekų (naudojama tik standartinė biblioteka)

### Paleidimas
```bash
python main.py
```

### Parametrų keitimas

Galite modifikuoti parametrus `main.py` faile:

```python
# Pakeisti sunkumo lygį (daugiau nulių = sunkiau)
blockchain = Blockchain(difficulty_target="0")

# Pakeisti vartotojų skaičių
blockchain.generate_users(n=100)

# Pakeisti transakcijų skaičių
blockchain.generate_transactions(m=500)

# Pakeisti transakcijų skaičių bloke
blockchain.mine_until_done(block_tx_count=50)
```

## Ekranvaizdžiai / Screenshots

### Genesis Block Creation
```
[INIT] Kuriamas GENESIS blokas...
[INIT] Difficulty target: '0'
[MINING] Mining block #0...
[MINING] Target: hash must start with '0'
[MINING] Success! Nonce: 3, Attempts: 3
[OK] Genesis blokas sukurtas!
     Hash: 0a1b2c3d4e5f...
     Merkle Root: 0000000000000000...
     Nonce: 3
```

### Transaction Generation (v0.1 feature)
```
============================================================
📝 TRANSAKCIJŲ GENERAVIMAS
============================================================
Generuojama transakcijų: 200

Transaction #1 ✅ VALID
  ID:       f47ac10b-58cc...
  From:     User_a3f7e2 (12345678...)
  To:       User_9b2d41 (87654321...)
  Amount:   1500
  Balance:  50000
  Hash:     3a5f9c2d1e8b7a4f6c...
  Time:     1730745600

Transaction #2 ✅ VALID
  ID:       e39bd087-92ff...
  From:     User_d8c4b1 (abcdef12...)
  To:       User_5e7a93 (fedcba98...)
  Amount:   2300
  Balance:  75000
  Hash:     8f2c4a1d9e3b5c7a2f...
  Time:     1730745601

============================================================
📊 TRANSAKCIJŲ STATISTIKA
============================================================
✅ Validžios transakcijos:  190
❌ Atmestos transakcijos:   10
📦 Transakcijų fonde:       190
============================================================
```

### Block Mining (v0.2 competitive mining)
```
[POOL] Kuriami kandidatiniai blokai (5 vnt)...
[CANDIDATE #0] ✓ 20 txs, Merkle: a7f3c9d2...
[CANDIDATE #1] ✓ 20 txs, Merkle: b8e4d0f1...
[CANDIDATE #2] ✓ 20 txs, Merkle: c9f5e1a2...
[CANDIDATE #3] ✓ 20 txs, Merkle: d0a6f2b3...
[CANDIDATE #4] ✓ 20 txs, Merkle: e1b7a3c4...

[MINING] Pradedamas konkurencinis kasimas...
[CANDIDATE #0] ⛏️  100000 attempts in 0.52s - continuing...
[CANDIDATE #1] ⛏️  100000 attempts in 0.51s - continuing...

🎉 WINNER FOUND!
[WINNER] Candidate #2
[WINNER] Hash: 0abc123def456...
[WINNER] Nonce: 15732
[WINNER] Total attempts: 215,732
[WINNER] Mining time: 1.0821s
```

### Block Information (Bitcoin Block Explorer style - v0.1 feature)
```
============================================================
🧱 BLOCK #1
============================================================
Hash:              0abc123def4567890abcdef1234567890abcdef...
Previous Hash:     0123456789abcdef0123456789abcdef...
Merkle Root:       c9f5e1a2b3d4c5a6f7e8d9c0a1b2c3d4...
Timestamp:         1730745650
Difficulty Target: 0
Nonce:             15732
Transactions:      20
============================================================

📜 TRANSACTIONS (showing first 3 of 20):
------------------------------------------------------------

Tx #1: f47ac10b-58cc...
  From:   User_a3f7e2 → 1500
  To:     User_9b2d41
  Hash:   3a5f9c2d1e8b7a4f6c...

Tx #2: e39bd087-92ff...
  From:   User_d8c4b1 → 2300
  To:     User_5e7a93
  Hash:   8f2c4a1d9e3b5c7a2f...

Tx #3: a12cd789-45ab...
  From:   User_3f8e12 → 890
  To:     User_7d2a4c
  Hash:   2b8e9f1a3c5d7e9b4a...

------------------------------------------------------------
```

### Final Summary
```
============================================================
🎉 BLOCKCHAIN SUMMARY
============================================================
📊 Blokų skaičius:          11
👥 Vartotojų skaičius:      50
📝 Apdorotų transakcijų:    200
⏱️  Genesis timestamp:       1730745500
⏱️  Last block timestamp:    1730745750
🔗 Genesis hash:            0a1b2c3d4e5f6789...
🔗 Last block hash:         0f9e8d7c6b5a4321...
🌳 Last Merkle root:        e1b7a3c4d5f6a7b8...
============================================================
```

## Techniniai detaliai

### Maišos funkcija
Pasirinktinė DJB2 algoritmo varianto implementacija:
- Naudoja bitų postūmius (`<<`) greičiui
- Generuoja 64 simbolių šešioliktainį hash (256 bitų atitikmuo)
- Vienas praėjimas per duomenis
- Optimizuota sparta

### Kasimo algoritmas
Proof-of-Work su konfigūruojamu sunkumu:
- Inkrementinis nonce paieška
- Hash prefikso atitikimas
- Konkurencinis daugelio kandidatų metodas

### Merkle Tree
Binarinė medžio konstrukcija:
- Iš apačios į viršų statymas iš transakcijų ID
- Porų maišymas
- Nelyginio skaičiaus apdorojimas per dubliavimą

### OOP praktikos (v0.1 requirement)

**1. Enkapsuliacija:**
```python
class Blockchain:
    def __init__(self):
        self.users: Dict[str, User] = {}          # Private data
        self.pending_transactions: List = []       # Private data
        self.chain: List[Block] = []               # Private data
        self._create_genesis_block()               # Private method
    
    def _create_genesis_block(self):               # Private method (underscore prefix)
        # Implementation...
```

**2. Konstruktoriai su validacija:**
```python
class Transaction:
    def __init__(self, sender_key: str, receiver_key: str, amount: int):
        self.tx_id = str(uuid.uuid4())             # Auto-generated
        self.sender_key = sender_key
        self.receiver_key = receiver_key
        self.amount = amount
        self.timestamp = int(time.time())          # Auto timestamp
        self._hash = self._calculate_hash()        # Immediate calculation
```

**3. RAII (Resource Acquisition Is Initialization):**
```python
class Block:
    def __init__(self, header: BlockHeader, transactions: List[Transaction]):
        self.header = header
        self.transactions = transactions
        self.index = header.index
        self.merkle_tree = self._build_merkle_tree()  # Resource created in constructor
```

**4. Aiški klasių struktūra:**
- `User` - Vartotojo duomenys ir balansų valdymas
- `Transaction` - Transakcijos duomenys ir hash skaičiavimas
- `BlockHeader` - Bloko metadata
- `Block` - Blokas su transakcijomis ir Merkle tree
- `MerkleTree` - Merkle medžio struktūra
- `MiningPool` - Konkurencinio kasimo valdymas
- `Blockchain` - Pagrindinė sistema, koordinuojanti viską

---

## AI pagalbos panaudojimas

### Kur buvo naudojama AI pagalba (GitHub Copilot / ChatGPT)

#### 1. **Kodo struktūros projektavimas**
- Klasių hierarchijos pasiūlymai
- OOP geriausių praktikų rekomendacijos
- Modulių organizavimas

#### 2. **Algoritmų implementacija**
- **Merkle Tree** binarinio medžio logika
- **Konkurencinis kasimas** round-robin algoritmas
- **Transakcijų validacija** srautų projektavimas

#### 3. **Kodo dokumentacija**
- Docstring generavimas visoms funkcijoms
- README.md struktūros ir turinio kūrimas
- Komentarų rašymas

#### 4. **Debugging pagalba**
- Import klaidų sprendimas (sys.path pataisymai)
- Logikos klaidų identifikavimas
- Merkle Tree tuščių transakcijų apdorojimas
- Kasimo proceso optimizavimas

#### 5. **Konsolės išvedimo formatavimas**
- Vizualių progreso indikatorių kūrimas
- Struktūrizuotų žurnalų pranešimų dizainas
- Santraukų statistikos formatavimas

#### 6. **Optimizavimas**
- Maišos funkcijos greičio pagerinimas (DJB2 algoritmas)
- Kasimo parametrų derinimas
- Didelių duomenų rinkinių apdorojimo optimizavimas

### Kas NEBUVO generuota AI

- Pagrindinis blockchain konceptas ir reikalavimai
- Pasirinktinės maišos funkcijos algoritmo idėja
- Bendrų projekto architektūros sprendimai
- Testavimas ir verifikacija
- Galutinių parametrų derinimas
- Versijų valdymo sprendimai

### AI įrankių apibūdinimas

**AI buvo naudojama kaip:**
- Kodo rašymo pagalbininkas
- Dokumentacijos generatorius
- Debugging partneris
- Algoritminių sprendimų patarėjas

**AI NEBUVO naudojama kaip:**
- Pagrindinis projekto kūrėjas
- Automatinis kodo generatorius "iš nieko"
- Sprendimų priėmimo sistema

---

