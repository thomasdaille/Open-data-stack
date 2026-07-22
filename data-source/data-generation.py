import csv
import random
from datetime import datetime, date, timedelta
from pathlib import Path

from faker import Faker

fake_fr = Faker("fr_FR")
Faker.seed(42)
random.seed(42)

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

NOW = datetime(2025, 1, 1)


def ts():
    # même timestamp pour création / modif (OLTP simple)
    return NOW.strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------
# 1. Référentiels
# ---------------------------------------------------------

def write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def gen_ref_sexe():
    header = ["sexe_code", "sexe_libelle", "date_creation", "date_derniere_modification"]
    rows = [
        ["M", "Masculin", ts(), ts()],
        ["F", "Féminin", ts(), ts()],
        ["IN", "Inconnu", ts(), ts()],
    ]
    write_csv(OUTPUT_DIR / "ref_sexe.csv", header, rows)


def gen_ref_etat_civil():
    header = ["etat_civil_code", "etat_civil_libelle", "date_creation", "date_derniere_modification"]
    mapping = {
        "MA": "Marié(e)",
        "DI": "Divorcé(e)",
        "CE": "Célibataire",
        "VE": "Veuf(ve)",
        "SE": "Séparé(e)",
        "IN": "Inconnu",
    }
    rows = [[code, lib, ts(), ts()] for code, lib in mapping.items()]
    write_csv(OUTPUT_DIR / "ref_etat_civil.csv", header, rows)


def gen_ref_confession():
    header = ["confession_code", "confession_libelle", "date_creation", "date_derniere_modification"]
    mapping = {
        "INC": "Appartenance religieuse inconnue",
        "RF": "Réformée (évangélique)",
        "SANS": "Sans appartenance religieuse",
        "JUI": "Communauté juive",
        "CATH": "Catholique",
        "CHR": "Autre communauté chrétienne",
        "TJ": "Témoin de Jéhovah",
        "AUT": "Autre communauté religieuse",
        "PROT": "Protestant",
        "MORM": "Mormon",
        "MUS": "Musulman",
    }
    rows = [[code, lib, ts(), ts()] for code, lib in mapping.items()]
    write_csv(OUTPUT_DIR / "ref_confession.csv", header, rows)


def gen_ref_type_cas():
    header = ["type_cas_code", "type_cas", "date_creation", "date_derniere_modification"]
    rows = [
        ["S", "stationnaire", ts(), ts()],
        ["A", "ambulatoire", ts(), ts()],
    ]
    write_csv(OUTPUT_DIR / "ref_type_cas.csv", header, rows)


def gen_ref_categorie_cas():
    header = ["categorie_cas_code", "type_cas_code", "categorie_cas", "date_creation", "date_derniere_modification"]
    rows = [
        ["AP", "A", "Ambul. aigu (psychiatrie)", ts(), ts()],
        ["AS", "A", "Ambul. aigu (somatique)", ts(), ts()],
        ["NN", "S", "Nouveau-né", ts(), ts()],
        ["HP", "S", "Hosp. aigu (psychiatrie)", ts(), ts()],
        ["HS", "S", "Hosp. aigu (somatique)", ts(), ts()],
    ]
    write_csv(OUTPUT_DIR / "ref_categorie_cas.csv", header, rows)


def gen_ref_pays():
    # focus CH, FR, IT, DE + quelques autres pour nationalités divergentes
    header = ["pays_code", "pays_libelle", "pays_code_iso2", "pays_code_iso3", "pays_nationalite",
              "date_creation", "date_derniere_modification"]
    rows = [
        ["CH", "Suisse", "CH", "CHE", "Suisse", ts(), ts()],
        ["FR", "France", "FR", "FRA", "Française", ts(), ts()],
        ["IT", "Italie", "IT", "ITA", "Italienne", ts(), ts()],
        ["DE", "Allemagne", "DE", "DEU", "Allemande", ts(), ts()],
        ["ES", "Espagne", "ES", "ESP", "Espagnole", ts(), ts()],
        ["GB", "Royaume-Uni", "GB", "GBR", "Britannique", ts(), ts()],
        ["US", "États-Unis", "US", "USA", "Américaine", ts(), ts()],
    ]
    write_csv(OUTPUT_DIR / "ref_pays.csv", header, rows)
    return {r[0]: r for r in rows}  # dict pour lookup


def gen_ref_etablissement():
    header = ["etablissement_code", "etablissement", "type_etablissement",
              "date_creation", "date_derniere_modification"]
    types = ["Hôpital universitaire", "Clinique privée", "Centre de rééducation", "Centre psychiatrique"]
    rows = []
    for i in range(1, 21):
        code = f"ETAB_{i:03d}"
        name = f"{fake_fr.city()} - {random.choice(['Hôpital', 'Clinique', 'Centre'])}"
        t = random.choice(types)
        rows.append([code, name, t, ts(), ts()])
    write_csv(OUTPUT_DIR / "ref_etablissement.csv", header, rows)
    return [r[0] for r in rows]


def gen_ref_unite_fonctionnelle():
    header = ["unite_code", "unite_libelle", "type_unite", "date_creation", "date_derniere_modification"]
    units = [
        ("CHIR", "Chirurgie", "somatique"),
        ("ORTHO", "Orthopédie", "somatique"),
        ("NEPH", "Néphrologie", "somatique"),
        ("CARDIO", "Cardiologie", "somatique"),
        ("ONCO", "Oncologie", "somatique"),
        ("PED", "Pédiatrie", "somatique"),
        ("PSY", "Psychiatrie", "psychiatrie"),
        ("GER", "Gériatrie", "somatique"),
        ("URGEN", "Urgences", "somatique"),
        ("REHAB", "Rééducation", "somatique"),
        ("OBST", "Obstétrique", "somatique"),
    ]
    rows = []
    for code, lib, t in units:
        rows.append([code, lib, t, ts(), ts()])
    write_csv(OUTPUT_DIR / "ref_unite_fonctionnelle.csv", header, rows)
    return [u[0] for u in units]


# ---------------------------------------------------------
# 2. Patients
# ---------------------------------------------------------

def random_birth_date():
    # distribution 1950-2000: 1-2% par année, >2000: 0-1%
    year = None
    r = random.random()
    if r < 0.9:
        # 1950-2000
        year = random.randint(1950, 2000)
    else:
        year = random.randint(2001, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return date(year, month, day)


def gen_patients(n=10000, pays_ref=None):
    header = [
        "patient_code", "prenom", "nom", "sexe_code", "date_naissance",
        "ville_naissance", "pays_naissance_code", "nationalite_code",
        "date_deces", "ville_deces", "etat_civil_code",
        "numero_securite_sociale", "confession_code", "indicateur_vip",
        "date_creation", "date_derniere_modification",
    ]

    sexes = ["M", "F"]
    # légèrement plus de femmes
    def random_sexe():
        return "F" if random.random() < 0.55 else "M"

    etats_civil = ["MA", "DI", "CE", "VE", "SE", "IN"]
    confs = ["INC", "RF", "SANS", "JUI", "CATH", "CHR", "TJ", "AUT", "PROT", "MORM", "MUS"]
    pays_codes = list(pays_ref.keys())

    rows = []
    ssn_list = []

    for i in range(1, n + 1):
        code = f"PAT_{i:05d}"
        prenom = fake_fr.first_name()
        nom = fake_fr.last_name()

        sexe = random_sexe()
        birth = random_birth_date()
        ville_naissance = fake_fr.city()
        pays_naissance = random.choice(["CH", "FR", "IT", "DE"])

        # nationalité: majoritairement = pays_naissance
        if random.random() < 0.8:
            nationalite = pays_naissance
        else:
            nationalite = random.choice(pays_codes)

        # état civil
        etat_civil = random.choice(etats_civil)
        confession = random.choice(confs)

        # VIP
        indicateur_vip = "true" if random.random() < 0.003 else "false"

        # décès (réaliste, faible taux)
        if random.random() < 0.1:
            # décédé
            min_death_year = birth.year + 1
            max_death_year = min(2025, birth.year + random.randint(1, 80))
            if min_death_year > max_death_year:
                date_deces = ""
                ville_deces = ""
            else:
                dy = random.randint(min_death_year, max_death_year)
                dm = random.randint(1, 12)
                dd = random.randint(1, 28)
                date_deces = date(dy, dm, dd).strftime("%Y-%m-%d")
                # lieu de décès parfois manquant
                ville_deces = fake_fr.city() if random.random() < 0.8 else ""
        else:
            date_deces = ""
            ville_deces = ""

        # numéro de sécu (format simple)
        ssn = "".join(str(random.randint(0, 9)) for _ in range(13))
        ssn_list.append(ssn)

        row = [
            code,
            prenom,
            nom,
            sexe,
            birth.strftime("%Y-%m-%d"),
            ville_naissance,
            pays_naissance,
            nationalite,
            date_deces,
            ville_deces,
            etat_civil,
            ssn,
            confession,
            indicateur_vip,
            ts(),
            ts(),
        ]
        rows.append(row)

    # anomalies sur patients (0.5-2% par type)
    nb_anom = max(1, int(0.01 * n))

    # 1) numéros de sécu invalides
    for idx in random.sample(range(n), nb_anom):
        kind = random.choice(["length", "chars", "duplicate"])
        if kind == "length":
            rows[idx][11] = "".join(str(random.randint(0, 9)) for _ in range(random.randint(5, 20)))
        elif kind == "chars":
            rows[idx][11] = "ABC" + rows[idx][11][3:]
        elif kind == "duplicate":
            rows[idx][11] = rows[0][11]

    # 2) dates de naissance aberrantes
    for idx in random.sample(range(n), nb_anom):
        kind = random.choice(["future", "ancient"])
        if kind == "future":
            rows[idx][4] = date(2100, 1, 1).strftime("%Y-%m-%d")
        else:
            rows[idx][4] = date(1800, 1, 1).strftime("%Y-%m-%d")

    # 3) décès avant naissance
    for idx in random.sample(range(n), nb_anom):
        birth = datetime.strptime(rows[idx][4], "%Y-%m-%d").date()
        bad_death = birth - timedelta(days=random.randint(1, 365))
        rows[idx][8] = bad_death.strftime("%Y-%m-%d")
        rows[idx][9] = fake_fr.city()

    # 4) nationalités invalides
    for idx in random.sample(range(n), nb_anom):
        rows[idx][7] = "XXX"

    # 5) sexe inconnu
    for idx in random.sample(range(n), nb_anom):
        rows[idx][3] = "IN"

    # 6) confession inconnue
    for idx in random.sample(range(n), nb_anom):
        rows[idx][12] = "UNKNOWN"

    # 7) valeurs NULL inattendues (ex: etat civil)
    for idx in random.sample(range(n), nb_anom):
        rows[idx][10] = ""

    write_csv(OUTPUT_DIR / "patient.csv", header, rows)
    return rows  # pour adresses & cas


# ---------------------------------------------------------
# 3. Adresses
# ---------------------------------------------------------

def gen_adresses(patients, pays_ref):
    header = [
        "adresse_code", "patient_code", "pays_code", "ville", "code_postal",
        "rue", "numero_rue", "date_debut_validite", "date_fin_validite",
        "date_creation", "date_derniere_modification",
    ]

    rows = []
    addr_id = 1

    for p in patients:
        patient_code = p[0]
        birth = datetime.strptime(p[4], "%Y-%m-%d").date()

        # nombre d'adresses: 1 à 3
        nb_addr = random.randint(1, 3)
        current_start = birth + timedelta(days=random.randint(0, 365 * 20))

        for i in range(nb_addr):
            pays_code = random.choice(["CH", "FR", "IT", "DE"])
            ville = fake_fr.city()
            # codes postaux simples mais plausibles
            if pays_code == "CH":
                cp = f"{random.randint(1000, 9999)}"
            elif pays_code == "FR":
                cp = f"{random.randint(10000, 95999)}"
            elif pays_code == "DE":
                cp = f"{random.randint(10000, 99999)}"
            else:  # IT
                cp = f"{random.randint(10000, 99999)}"

            rue = fake_fr.street_name()
            numero = random.randint(1, 200)

            start = current_start
            # fin pour toutes sauf la dernière
            if i < nb_addr - 1:
                end = start + timedelta(days=random.randint(365, 365 * 5))
                current_start = end + timedelta(days=random.randint(30, 365))
                date_fin = end.strftime("%Y-%m-%d")
            else:
                # adresse active
                date_fin = ""

            row = [
                f"ADR_{addr_id:07d}",
                patient_code,
                pays_code,
                ville,
                cp,
                rue,
                str(numero),
                start.strftime("%Y-%m-%d"),
                date_fin,
                ts(),
                ts(),
            ]
            rows.append(row)
            addr_id += 1

    write_csv(OUTPUT_DIR / "adresse.csv", header, rows)
    return rows


# ---------------------------------------------------------
# 4. Cas
# ---------------------------------------------------------

def gen_cas(patients, etabs, unites):
    header = [
        "cas_code", "patient_code", "type_cas_code", "categorie_cas_code",
        "etablissement_provenance_code", "etablissement_destination_code",
        "unite_fonctionnelle_code", "date_debut", "heure_debut",
        "date_fin", "heure_fin", "date_creation", "date_derniere_modification",
    ]

    rows = []
    cas_id = 1

    # distribution d'âge au début du cas (global)
    def age_bucket():
        r = random.random()
        if r < 0.0222:
            return "0"
        elif r < 0.0222 + 0.1398:
            return "0-17"
        elif r < 0.0222 + 0.1398 + 0.2595:
            return "18-39"
        elif r < 0.0222 + 0.1398 + 0.2595 + 0.3479:
            return "40-64"
        else:
            return "65+"

    for p in patients:
        patient_code = p[0]
        birth = datetime.strptime(p[4], "%Y-%m-%d").date()
        death_str = p[8]
        death = datetime.strptime(death_str, "%Y-%m-%d").date() if death_str else None

        # fenêtre globale 1990-2025
        min_date = max(date(1990, 1, 1), birth)
        max_date = date(2025, 12, 31)
        if death:
            max_date = min(max_date, death)

        if min_date >= max_date:
            # pas de cas possible
            continue

        nb_cas = random.randint(1, 3)
        # certains patients "gros consommateurs"
        if random.random() < 0.05:
            nb_cas = random.randint(4, 8)

        # NN éventuel (premier cas)
        has_nn = False
        if birth >= date(1990, 1, 1) and birth <= date(2025, 12, 31) and random.random() < 0.1:
            # cas NN
            type_cas = "S"
            cat = "NN"
            date_debut = birth
            date_fin = birth
            heure_debut = "08:00:00"
            heure_fin = "12:00:00"
            etab_dest = random.choice(etabs)
            etab_prov = "" if random.random() < 0.5 else random.choice(etabs)
            unite = random.choice(unites)

            rows.append([
                f"CAS_{cas_id:07d}",
                patient_code,
                type_cas,
                cat,
                etab_prov,
                etab_dest,
                unite,
                date_debut.strftime("%Y-%m-%d"),
                heure_debut,
                date_fin.strftime("%Y-%m-%d"),
                heure_fin,
                ts(),
                ts(),
            ])
            cas_id += 1
            has_nn = True
            nb_cas -= 1

        for _ in range(nb_cas):
            bucket = age_bucket()
            # choisir une date de début compatible avec le bucket
            if bucket == "0":
                # proche de la naissance
                date_debut = birth + timedelta(days=random.randint(0, 30))
            elif bucket == "0-17":
                date_debut = birth + timedelta(days=random.randint(0, 17 * 365))
            elif bucket == "18-39":
                date_debut = birth + timedelta(days=random.randint(18 * 365, 39 * 365))
            elif bucket == "40-64":
                date_debut = birth + timedelta(days=random.randint(40 * 365, 64 * 365))
            else:
                date_debut = birth + timedelta(days=random.randint(65 * 365, 90 * 365))

            # clamp dans fenêtre globale
            if date_debut < min_date:
                date_debut = min_date
            if date_debut > max_date:
                date_debut = min_date + timedelta(days=random.randint(0, (max_date - min_date).days))

            # type cas: 85% ambulatoire
            if random.random() < 0.85:
                type_cas = "A"
                cat = random.choice(["AP", "AS"])
            else:
                type_cas = "S"
                cat = random.choice(["HP", "HS"])

            # dates/heure: ambulatoire <24h, date_fin = date_debut
            heure_debut = f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}:00"
            # durée 1-8h
            h_end = min(23, int(heure_debut[:2]) + random.randint(1, 8))
            heure_fin = f"{h_end:02d}:{random.randint(0, 59):02d}:00"
            date_fin = date_debut

            etab_dest = random.choice(etabs)
            etab_prov = "" if random.random() < 0.3 else random.choice(etabs)
            unite = random.choice(unites)

            rows.append([
                f"CAS_{cas_id:07d}",
                patient_code,
                type_cas,
                cat,
                etab_prov,
                etab_dest,
                unite,
                date_debut.strftime("%Y-%m-%d"),
                heure_debut,
                date_fin.strftime("%Y-%m-%d"),
                heure_fin,
                ts(),
                ts(),
            ])
            cas_id += 1

    # anomalies sur cas (0.5-2% par type)
    n = len(rows)
    nb_anom = max(1, int(0.01 * n))

    # 1) date_fin < date_debut
    for idx in random.sample(range(n), nb_anom):
        d_deb = datetime.strptime(rows[idx][7], "%Y-%m-%d").date()
        bad = d_deb - timedelta(days=random.randint(1, 10))
        rows[idx][9] = bad.strftime("%Y-%m-%d")

    # 2) cas ambulatoires > 24h (on joue sur heure)
    for idx in random.sample(range(n), nb_anom):
        if rows[idx][2] == "A":
            rows[idx][8] = "08:00:00"
            rows[idx][10] = "08:00:00"
            # on ne touche pas date_fin (mais DBT peut considérer incohérence)

    # 3) cas NN incohérents
    for idx in random.sample(range(n), nb_anom):
        rows[idx][3] = "NN"
        # date_debut != naissance (mais on ne connaît pas naissance ici)

    # 4) FK invalides
    for idx in random.sample(range(n), nb_anom):
        rows[idx][2] = "X"
    for idx in random.sample(range(n), nb_anom):
        rows[idx][3] = "ZZZ"

    # 5) dates hors fenêtre
    for idx in random.sample(range(n), nb_anom):
        rows[idx][7] = "2080-01-01"
        rows[idx][9] = "2080-01-02"

    # 6) valeurs NULL inattendues
    for idx in random.sample(range(n), nb_anom):
        rows[idx][5] = ""

    write_csv(OUTPUT_DIR / "cas.csv", header, rows)


# ---------------------------------------------------------
# main
# ---------------------------------------------------------

def main():
    gen_ref_sexe()
    pays_ref = gen_ref_pays()
    gen_ref_etat_civil()
    gen_ref_confession()
    gen_ref_type_cas()
    gen_ref_categorie_cas()
    etabs = gen_ref_etablissement()
    unites = gen_ref_unite_fonctionnelle()

    patients = gen_patients(n=10000, pays_ref=pays_ref)
    gen_adresses(patients, pays_ref)
    gen_cas(patients, etabs, unites)


if __name__ == "__main__":
    main()
