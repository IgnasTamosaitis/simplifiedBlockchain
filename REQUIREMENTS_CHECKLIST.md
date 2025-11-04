# Užduoties Reikalavimų Patikrinimas

## Pagrindinė Užduotis

### ✅ 1. Vartotojų generavimas (~1000 vartotojų)
- **Implementacija:** `blockchain.generate_users(n=1000)`
- **Laukai:**
  - ✅ `name` - vartotojo vardas
  - ✅ `public_key` - viešasis raktas (UUID hex)
  - ✅ `balance` - balansas (random.randint(100, 1_000_000))
- **Failas:** `models/user.py`

### ✅ 2. Transakcijų generavimas (~10,000 įrašų)
- **Implementacija:** `blockchain.generate_transactions(m=10000)`
- **Laukai:**
  - ✅ `transaction_id` - unikalus ID (UUID)
  - ✅ `sender` - siuntėjo raktas
  - ✅ `receiver` - gavėjo raktas
  - ✅ `amount` - siunčiama suma
  - ✅ `timestamp` - laiko žyma
  - ✅ Hash skaičiavimas (`_calculate_hash()`)
- **Failas:** `models/transaction.py`
- **Modelis:** Account model (balansų sistema)

### ✅ 3. Naujo bloko formavimas
- **Implementacija:** `pick_transactions_for_block(k=100)`
- ✅ Pasirenka 100 transakcijų iš sąrašo
- ✅ Paruošia jas įtraukimui į naują bloką
- **Failas:** `models/blockchain.py`

### ✅ 4. Bloko kasimas (Proof-of-Work)
- **Implementacija:** `mine()` metodas `models/block.py`
- ✅ Naudojama pasirinktinė maišos funkcija (iš 1-os užduoties)
- ✅ Difficulty target: `"000"` (hash prasideda trimis nuliais)
- ✅ Hash'uoja 6 pagrindinius bloko antraštės elementus:
  - `version`
  - `index`
  - `prev_block_hash`
  - `merkle_root`
  - `timestamp`
  - `difficulty_target`
  - `nonce`
- ✅ Nonce iteracija iki tinkamo hash

### ✅ 5. Bloko patvirtinimas ir įtraukimas
- **Implementacija:** `apply_block_state_changes()` ir `add_block_to_chain()`
- ✅ Pašalina į bloką įtrauktas transakcijas iš sąrašo
- ✅ Atnaujina vartotojų balansus (debit/credit)
- ✅ Prideda naują bloką prie grandinės
- **Failas:** `models/blockchain.py`

### ✅ 6. Procesų kartojimas
- **Implementacija:** `mine_until_done(block_tx_count=100)`
- ✅ Kartoja 3–5 žingsnius kol neliks neįtrauktų transakcijų
- **Failas:** `models/blockchain.py`

---

## v0.1 Reikalavimai (iki 2025-10-29) ✅

### ✅ Centralizuota blokų grandinė
- ✅ Sukurta pilna blockchain struktūra
- ✅ Blokų sąrašas `chain: List[Block]`
- ✅ Genesis blokas
- ✅ Blokų susiejimas per `prev_block_hash`

### ✅ Pasirinktinė maišos funkcija
- **Failas:** `hash_utils.py`
- ✅ Pilnai custom implementacija (4 būsenos, rotacijos, XOR operacijos)
- ✅ Naudoja jokių išorinių hash bibliotekų
- ✅ Generuoja 256-bit (64 hex) hash
- ✅ Algoritmas:
  - 4 x 64-bit būsenos (a, b, c, d)
  - Rotation operacijos
  - XOR mixing
  - Prime skaičiai (33, 29, 35, 39)

### ✅ Bloko struktūra
- **BlockHeader:** (`models/block.py`)
  - ✅ `version` - versija
  - ✅ `index` - bloko numeris
  - ✅ `prev_block_hash` - ankstesnio bloko hash
  - ✅ `merkle_root` - Merkle root hash (v0.1: transakcijų hash)
  - ✅ `timestamp` - laiko žyma
  - ✅ `difficulty_target` - sudėtingumo lygis
  - ✅ `nonce` - atsitiktinis skaičius PoW
- **Block:**
  - ✅ `header` - antraštė
  - ✅ `transactions` - transakcijų sąrašas

### ✅ Konsolės išvedimas
- ✅ **Vizualus transakcijų kūrimo procesas:**
  - Rodomi pirmieji 5 transakcijų su detalėmis
  - ID, siuntėjas, gavėjas, suma, balansas, hash, timestamp
  - Validacijos statusas (✅ VALID / ❌ INVALID)
- ✅ **Detalus blokų kasimo procesas:**
  - Mining progress su attempts
  - Kandidatų blokai
  - Winner informacija
- ✅ **Blockchain būsenos atnaujinimai:**
  - Block explorer stiliaus išvestis
  - Bloko informacija (hash, merkle root, nonce, tx skaičius)
  - Transakcijų sąrašas bloke
- ✅ **Galutinė santrauka:**
  - Blokų skaičius
  - Vartotojų skaičius
  - Apdorotų transakcijų
  - Genesis ir paskutinio bloko info

### ✅ OOP praktikos
- ✅ **Enkapsuliacija:**
  - Private metodai su `_` prefiksu
  - Private duomenys klasėse
- ✅ **Konstruktoriai:**
  - Visi su `__init__` metodais
  - Parametrų validacija
  - Default reikšmės
- ✅ **RAII principai:**
  - Resource kūrimas konstruktoriuose
  - Merkle tree automatinis statymas
  - Hash skaičiavimas sukūrus objektą
- ✅ **Aiški klasių struktūra:**
  - `User` - vartotojas
  - `Transaction` - transakcija
  - `BlockHeader` - bloko antraštė
  - `Block` - blokas
  - `MerkleTree` - Merkle medis (v0.2)
  - `MiningPool` - kasimo valdymas (v0.2)
  - `Blockchain` - pagrindinė sistema

### ✅ README failas
- ✅ Aprašymas
- ✅ Projekto struktūra
- ✅ Naudojimosi instrukcija
- ✅ Ekranvaizdžiai (sample output)
- ✅ Funkcionalumas
- ✅ AI pagalbos skyrius

---

## v0.2 Reikalavimai (iki 2025-11-05) ✅

### ✅ Merkle Tree implementacija
- **Failas:** `models/merkle_tree.py`
- ✅ Pilnas binarinis Merkle medis
- ✅ Tikras Merkle Root Hash skaičiavimas
- ✅ Lyginių/nelyginių transakcijų apdorojimas
- ✅ `_build_tree()` metodas
- ✅ `get_root()` metodas
- ✅ `get_proof()` ir `verify_transaction()` metodai

### ✅ Transakcijų verifikacija
- **Failas:** `models/transaction.py` ir `models/blockchain.py`
- ✅ **Balanso tikrinimas:**
  - `verify_balance(sender_balance)` metodas
  - Siuntėjas negali siųsti daugiau nei turi
  - Validacija prieš pridedant į pool
- ✅ **Transakcijos ID tikrinimas:**
  - `verify_hash()` metodas
  - Maišos reikšmės teisingumas
  - Hash perskaičiavimas ir palyginimas
- ✅ **`validate_transaction()` metodas:**
  - Tikrina hash, balansą, siuntėją, gavėją
  - Atmeta netinkamas transakcijas

### ✅ Patobulintas kasimo procesas
- **Failas:** `models/mining_pool.py`
- ✅ **5 kandidatiniai blokai:**
  - `MiningPool(num_candidates=5)`
  - Kiekvienas su ~100 transakcijų
  - Skirtingos transakcijos kiekvienam
- ✅ **Ribotas laikas:**
  - `time_limit=10.0` (10 sekundžių)
  - Timeout tikrinimas
- ✅ **Ribotas bandymų skaičius:**
  - `max_attempts_per_round=500000`
  - Per candidate: `attempts_per_candidate`
- ✅ **Automatinis didinimas:**
  - `time_limit *= 1.5`
  - `max_attempts_per_round *= 1.5`
  - Kartojimas iki 10 roundų
- ✅ **Fallback mechanizmas:**
  - Priima geriausią kandidatą jei nepasiseka
  - Užtikrina progresą
- ✅ **Decentralizuoto kasimo simuliacija:**
  - Konkuruojantys kandidatai
  - Round-robin mining
  - Winner selection

### ✅ README papildymas
- ✅ v0.2 versijos skyrius
- ✅ Naujos funkcijos aprašymas
- ✅ Merkle Tree dokumentacija
- ✅ Transakcijų verifikacijos aprašymas
- ✅ Konkurencinio kasimo aprašymas
- ✅ **AI pagalbos skyrius:**
  - Aiškiai išskirta kur AI padėjo
  - Kas buvo AI generuota
  - Kas NEBUVO AI generuota
  - AI įrankių apibūdinimas

---

## Parametrų Santrauka

| Parametras | Reikalavimas | Implementacija | Statusas |
|------------|--------------|----------------|----------|
| Vartotojai | ~1000 | `n=1000` | ✅ |
| Transakcijos | ~10,000 | `m=10000` | ✅ |
| Tx per bloką | ~100 | `block_tx_count=100` | ✅ |
| Difficulty | "000" | `difficulty_target="000"` | ✅ |
| Kandidatai | 5 | `num_candidates=5` | ✅ |
| Kasimo laikas | 5-10s | `time_limit=10.0` | ✅ |

---

## Failų Struktūra

```
simplified_blockchain/
├── models/
│   ├── __init__.py           ✅
│   ├── blockchain.py         ✅ Pagrindinė logika
│   ├── block.py              ✅ Block + BlockHeader
│   ├── transaction.py        ✅ Transaction + validation
│   ├── user.py               ✅ User + balance
│   ├── merkle_tree.py        ✅ Merkle Tree (v0.2)
│   └── mining_pool.py        ✅ Competitive mining (v0.2)
├── hash_utils.py             ✅ Custom hash function
├── main.py                   ✅ Entry point
├── README.md                 ✅ Documentation
└── REQUIREMENTS_CHECKLIST.md ✅ Šis failas
```

---

## Išvada

✅ **VISOS užduoties reikalavimai įgyvendinti:**
- ✅ v0.1 reikalavimai (centralizuota blockchain, custom hash, PoW, OOP, konsolės išvedimas)
- ✅ v0.2 reikalavimai (Merkle Tree, transakcijų verifikacija, konkurencinis kasimas)
- ✅ Parametrai atitinka užduotį (1000/10000/100/000)
- ✅ README su AI pagalbos skyriumi
- ✅ Pilna OOP struktūra
- ✅ Vizualus konsolės išvedimas

**Projektas paruoštas vertinimui!**
