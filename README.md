
# Supaprastintos blokų grandinės (blockchain) kūrimas

Šios užduoties tikslas – sukurti supaprastintą blokų grandinę (angl. blockchain), kurios duomenų sluoksnio struktūra pavaizduota žemiau:
![image](https://raw.githubusercontent.com/IgnasTamosaitis/simplifiedBlockchain/refs/heads/main/images/struktura.png)

Sistema imituoja supaprastintą blokų grandinės veikimą – generuoja vartotojus, kuria transakcijas, formuoja blokus, skaičiuoja Merkle medį, atlieka *Proof-of-Work*  ir užtikrina vientisumą pasitelkiant *hash*.

### Pagrindinės Funkcijos

1. Blokų Generavimas: Blokai generuojami, kai surenkama pakankamai transakcijų. Kiekvienas blokas turi ankstesnio bloko hash, dabartinį hash ir Merkle Root Hash.
2. Transakcijų Tikrinimas: Prieš įtraukiant transakciją į bloką, tikrinama, ar siuntėjo balansui pakanka lėšų ir ar transakcijos maišos kodas sutampa su nurodytu.
3. Proof-of-Work (PoW): Siekiant užtikrinti blokų vientisumą ir apsaugoti nuo manipuliacijos, kiekvieno bloko generavimas vykdomas per *Proof-of-Work* algoritmą.
4. Merkle Root Hash: Naudojama supaprastinta Merkle medžio versija – vietoj dvejetainio Merkle medžio suformuojama maišos reikšmė, kuri susiejama su visų bloko transakcijų ID.
5. Centralizuotas Blokų Valdymas: Vartotojai ir transakcijos yra generuojami ir valdomi per centralizuotą mazgą, kuris saugo ir apdoroja visą informaciją.


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

