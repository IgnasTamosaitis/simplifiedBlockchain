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

### Paleidimas ir naudojimasis

Reikalavimai:
- **Python 3.8+**
- Papildomų bibliotekų nereikia (naudojama tik standartinė biblioteka)

Paleidimas:
```bash
python main.py
```
Paleidus programą terminale matysite:
- kuriamas „Genesis“ blokas
- sugeneruojami vartotojai
- sukuriamos transakcijos
- vyksta konkurencinis kasimas
- blokai pridedami prie grandinės
- galiausiai rodoma suvestinė

```less
[INIT] Kuriamas GENESIS blokas...
[INFO] Sugeneruota 1000 vartotojų.
[INFO] Generuojama 10000 transakcijų...
[MINING] Pradedamas konkurencinis kasimas...
✅ BLOCK #1 iškastas
✅ BLOCK #2 iškastas
...
🎉 BLOCKCHAIN SUMMARY

```
Blokų informacija spausdinama kas kartą, kai blokas iškasamas:
-  blokų hash
- previous hash
-  Merkle root
-  nonce
-  pirmos 3 transakcijos bloke

---

## Programos veikimas

## ✅ Kaip veikia programa (trumpas paaiškinimas)

Programa imituoja supaprastintą Bitcoin tipo blokų grandinę. Viskas vyksta tokia tvarka:

1. **Sukuriama blockchain sistema**
   Sukuriamas pirmasis – „Genesis“ blokas, nustatomas Proof-of-Work sunkumas.

2. **Sugeneruojami vartotojai**
   Sistema sukuria atsitiktinius vartotojus su unikaliu raktu ir balansu.

3. **Sugeneruojamos transakcijos**
   Atsitiktiniai vartotojai siunčia pinigus vieni kitiems.  
   Kiekviena transakcija turi ID, siuntėją, gavėją, sumą, laiką ir hash.

4. **Transakcijos tikrinamos**
   Prieš dedant į bloką tikrinama:
   * ar vartotojai egzistuoja  
   * ar siuntėjas turi pakankamai lėšų  
   * ar transakcijos hash yra teisingas

5. **Formuojami blokai**
   Surinkus tam tikrą kiekį transakcijų, sukuriamas naujas blokas su:
   - ankstesnio bloko hash
   - savo hash
   - Merkle Root (transakcijų suvestinis hash)
   - nonce (kasimo skaitiklis)

6. **Proof-of-Work kasimas**
   Blokas laikomas galiojančiu tik jei jo hash prasideda nustatytu kiekiu nulių (pvz. `000`).  
   Programa didina nonce, kol randa tinkamą hash.

7. **Konkurencinis kasimas (v0.2)**
   Vienu metu kasa keli „kasėjai“ – sukuriami keli blokų kandidatai.  
   Laimi tas, kurio blokas pirmas randa tinkamą hash.

8. **Blokas pridedamas į grandinę**
   Transakcijos pritaikomos vartotojų balansams
   Naudotos transakcijos pašalinamos
   Blokas pridedamas prie blockchain

9. **Procesas kartojamas**
   Sistema kasa blokus tol, kol nebelieka transakcijų.  
   Galiausiai parodoma santrauka – kiek blokų, transakcijų, koks paskutinio bloko hash ir Merkle root.

Trumpai: programa kuria vartotojus → generuoja transakcijas → tikrina jas → sudeda į blokus → kasa juos su Proof-of-Work → prideda į blokų grandinę, kol visos transakcijos apdorotos.

---
## Veikimo esmė: v0.1 → v0.2

Ši sistema imituoja supaprastintą blockchain veikimą: sukuriami vartotojai, formuojamos transakcijos, jos tikrinamos, blokuojamos į blokus, skaičiuojamas Merkle Root ir vykdomas Proof-of-Work kasimas. Pabaigoje gaunama nuosekli blokų grandinė, kurioje kiekvienas blokas priklausomas nuo ankstesnio.

---

### v0.1 – (vienas kasėjas, PoW)

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
---
### v0.2 – (Merkle Tree + tikrinimas + konkurencinis kasimas)

* Tikras Merkle Tree, o ne tik sujungtas hash
* Transakcijų validacija (balansas, hash, siuntėjo/gavėjo egzistavimas)
* Konkurencinė kasyba su 5 kandidatais
* Laiko ir bandymų limitai
* Fallback mechanizmas – jei niekas neranda teisingo hash, priimamas geriausias (mažiausias) hash

Pagrindinis veikimas:

```python
from models.blockchain import Blockchain

blockchain = Blockchain(difficulty_target="000")

# 1. Sugeneruojami vartotojai
blockchain.generate_users(n=1000)

# 2. Sugeneruojamos transakcijos tarp jų
blockchain.generate_transactions(m=10000)

# 3. Pradedamas konkurencinis kasimas (5 kandidatai, 100 transakcijų per bloką)
blockchain.mine_until_done(block_tx_count=100)

# 4. Suvestinė
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

- Sukuriami 5 skirtingi blokų kandidatai. Visi turi skirtingus transakcijų rinkinius ir skirtingus timestamp.
- Kiekvienas kandidatas bando rasti hash, kuris prasideda „000“
- Kas pirmas suranda – tas laimi
- Jei nei vienas per nustatytą laiką neranda, sistema:
* padidina laiko ir bandymų limitus
* jei ir tada nepavyksta, priima „geriausią“ (mažiausią hash) bloką


v0.2 rezultatas: 

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
---

### Parametrų keitimas

Programos veikimą galima nesunkiai keisti tiesiog redaguojant kelias eilutes `main.py` arba `blockchain.py` faile.

#### Keisti sunkumo lygį (kiek nulių turi prasidėti hash)

```python
# Mažiau nulių → greitesnis kasimas
blockchain = Blockchain(difficulty_target="00")

# Daugiau nulių → žymiai sunkiau kasti (ilgiau)
blockchain = Blockchain(difficulty_target="0000")

# Sugeneruos daugiau vartotojų atsitiktiniais balansais
blockchain.generate_users(n=2000)

# Kuo daugiau transakcijų — tuo daugiau blokų bus iškasta
blockchain.generate_transactions(m=20000)

# Daugiau transakcijų viename bloke → mažiau blokų, ilgesnis kasimas
blockchain.mine_until_done(block_tx_count=200)

# Mažiau transakcijų viename bloke → daugiau blokų, greitesni blokai
blockchain.mine_until_done(block_tx_count=50)

```
#### Keisti kasėjų (kandidatų) skaičių MiningPool `models/mining_pool.py` faile:

```python
# Pagal nutylėjimą 5 kandidatai
self.mining_pool = MiningPool(num_candidates=5)

# Pvz. 10 kandidatų
self.mining_pool = MiningPool(num_candidates=10)
```
Daugiau kandidatų → didesnė konkurencija → didesnė tikimybė greičiau rasti tinkamą hash.

#### Keisti kasimo laiką ir bandymų ribas MiningPool.mine_competitively() funkcijoje:

```python
winner = self.mining_pool.mine_competitively(
    candidates=candidates,
    time_limit=3.0,            # Laikas vienam raundui (sekundėmis)
    max_attempts_per_round=150000,  # Kiek bandymų leidžiama per raundą
)

```
- Didesni skaičiai → greičiau ras tinkamą bloką, bet ilgiau užtruks skaičiavimai.
- Mažesni skaičiai → greičiau pereis prie fallback (mažiausio hash) varianto.

---

## Objektinio programavimo praktikos

Projektas parašytas pagal OOP principus: kiekviena klasė atlieka aiškiai apibrėžtą funkciją (`User`, `Transaction`, `Block`, `Blockchain`, `MiningPool`). Duomenys enkapsuliuoti, balansas keičiama tik per metodus, blokas sukuriamas per `Block.build()` (Merkle root apskaičiuojamas prieš header), o konkurencinis kasimas imituoja kelis kasėjus.

**Pavyzdys:**

```python
# Vartotojo operacijos
user = User(name="User_1", public_key="abc123", balance=1000)
user.debit(200)
user.credit(50)
print(user.balance)   # 850

# Transakcija
tx = Transaction(sender_key="abc123", receiver_key="def456", amount=200)
print(tx.get_hash())    # 64 simbolių hash
print(tx.verify_hash()) # True

# Bloko kūrimas (Merkle root apskaičiuojamas viduje)
block = Block.build(
    index=1,
    prev_block_hash="0000000000000000...",
    version=1,
    transactions=[tx],
    difficulty_target="000"
)
print(block.get_merkle_root())
print(block.get_hash())

```


## AI pagalbos panaudojimas

Projekte buvo naudojama AI (ChatGPT / Copilot) pagalba, tačiau tik kaip papildomas įrankis, o ne pagrindinis kūrimo šaltinis.

### Kur AI padėjo
- Padėjo apsispręsti **nuo ko pradėti** ir kaip logiškai suskirstyti projektą į klases (`User`, `Transaction`, `Block`, `Blockchain`, `MerkleTree`, `MiningPool`)
- Pasiūlė OOP gerąsias praktikas ir projekto katalogų struktūrą
- Padėjo suprasti Proof-of-Work, Merkle Tree ir konkurencinio kasimo principus
- Padėjo README tvarkingai parašyti
- Debugging situacijose:
  - import problemos
  - Merkle Tree kraštiniai atvejai (nelyginis transakcijų skaičius)
  - kasimo limitų reguliavimas
- Pasiūlė idėjų optimizacijoms (hash funkcijos efektyvumas, mažiau nereikalingų skaičiavimų)
- Padėjo patobulinti mūsų pačių parašytą hash funkciją remiantis DJB2 logika

### Kas **nebuvo** generuota AI
- Blockchain struktūra ir veikimo logika
- Proof-of-Work realizacija ir konkurencinės kasybos algoritmas
- Transakcijų ir balansų tikrinimas
- Merkle Tree realizacija ir duomenų apdorojimas
- Testavimas ir rezultatų analizė
- Galutinių sprendimų priėmimas bei parametrų parinkimas


## Papildomos užduotys

**Lygiagretus blokų kasimo proceso realizavimas v0.2 versijoje (+0.5 balo)**:

v0.2 versijoje kasimas nebėra atliekamas tik vieno kasėjo. Vietoje to sistema sukuria **kelis kandidatus (5 blokai)**, ir visi jie bando rasti tinkamą hash tuo pačiu metu. Laimi tas, kurio blokas pirmas turi hash, prasidedantį `000`.

**Kur tai padaryta:**
- Failas: `models/mining_pool.py`
- Funkcijos: `create_candidates()` ir `mine_competitively()`
- Iškvietimas vyksta per `Blockchain.mine_block_competitively()`

**Veikimas:**

```python
# blockchain.py
winner = self.mining_pool.mine_competitively(
    candidates=candidates,
    time_limit=3.0,
    max_attempts_per_round=150000,
)
```
*  `create_candidates()` paima transakcijas, jas išmaišo ir sukuria 5 skirtingus "kasėjus" (kandidatus). Kiekvienas kandidatas turi savo bloką su skirtinga transakcijų kombinacija ir visi jie bando iškasti tą patį sekantį bloką.
Penki kasėjai, nes: 
```python
self.mining_pool = MiningPool(num_candidates=5)
```
*  `mine_competitively()` visi 5 blokai „varžosi“, kuris ras tinkamą hash.
*  Jeigu niekas nespėja per nustatytą laiką – didinami limitai.
*  Jeigu vis tiek nepavyksta – priimamas geriausias blokas pagal mažiausią hash, kad grandinė nesustotų.

Ką tai duoda:
- Kasimas tampa „decentralizuotas“ – kaip keli kasėjai vienu metu.
- Greitesnė tikimybė surasti hash.
- Grandinė niekada neįstringa, nes yra atsarginis sprendimas (fallback).