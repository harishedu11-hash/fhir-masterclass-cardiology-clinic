import sqlite3
import requests
from datetime import datetime

# Local HAPI FHIR Endpoint
FHIR_BASE_URL = "http://localhost:8080/fhir"
DB_NAME = "omop_cdm_v5_4.db"

# ══════════════════════════════════════════════════════════════════════════════
# OHDSI OMOP Standard Concept ID Mappings
# ══════════════════════════════════════════════════════════════════════════════
OMOP_GENDER_MAP = {
    "male": 8507,      # Male
    "female": 8532,    # Female
    "other": 8521,     # Other
    "unknown": 0       # Unknown
}

OMOP_VISIT_MAP = {
    "IMP": 9201,       # Inpatient Visit
    "AMB": 9202,       # Outpatient Visit
    "EMER": 9203       # Emergency Room Visit
}

OMOP_MEASUREMENT_MAP = {
    "8867-4": 3027801   # LOINC Heart Rate -> OMOP Measurement Concept ID
}


def init_omop_db():
    """Initializes a lightweight OMOP CDM v5.4 Schema in SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. CARE_SITE Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CARE_SITE (
            care_site_id INTEGER PRIMARY KEY,
            care_site_name TEXT,
            place_of_service_concept_id INTEGER,
            location_id INTEGER,
            care_site_source_value TEXT,
            care_site_source_concept_id INTEGER
        )
    """)

    # 2. PERSON Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PERSON (
            person_id INTEGER PRIMARY KEY,
            gender_concept_id INTEGER,
            year_of_birth INTEGER,
            month_of_birth INTEGER,
            day_of_birth INTEGER,
            birth_datetime TEXT,
            race_concept_id INTEGER,
            ethnicity_concept_id INTEGER,
            location_id INTEGER,
            provider_id INTEGER,
            care_site_id INTEGER,
            person_source_value TEXT,
            gender_source_value TEXT,
            gender_source_concept_id INTEGER,
            race_source_value TEXT,
            race_source_concept_id INTEGER,
            ethnicity_source_value TEXT,
            ethnicity_source_concept_id INTEGER
        )
    """)

    # 3. VISIT_OCCURRENCE Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS VISIT_OCCURRENCE (
            visit_occurrence_id INTEGER PRIMARY KEY,
            person_id INTEGER,
            visit_concept_id INTEGER,
            visit_start_date TEXT,
            visit_start_datetime TEXT,
            visit_end_date TEXT,
            visit_end_datetime TEXT,
            visit_type_concept_id INTEGER,
            provider_id INTEGER,
            care_site_id INTEGER,
            visit_source_value TEXT,
            visit_source_concept_id INTEGER,
            admitted_from_concept_id INTEGER,
            admitted_from_source_value TEXT,
            discharged_to_concept_id INTEGER,
            discharged_to_source_value TEXT,
            preceding_visit_occurrence_id INTEGER
        )
    """)

    # 4. MEASUREMENT Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MEASUREMENT (
            measurement_id INTEGER PRIMARY KEY,
            person_id INTEGER,
            measurement_concept_id INTEGER,
            measurement_date TEXT,
            measurement_datetime TEXT,
            measurement_time TEXT,
            measurement_type_concept_id INTEGER,
            operator_concept_id INTEGER,
            value_as_number REAL,
            value_as_concept_id INTEGER,
            unit_concept_id INTEGER,
            range_low REAL,
            range_high REAL,
            provider_id INTEGER,
            visit_occurrence_id INTEGER,
            visit_detail_id INTEGER,
            measurement_source_value TEXT,
            measurement_source_concept_id INTEGER,
            unit_source_value TEXT,
            unit_source_value_raw TEXT,
            value_source_value TEXT
        )
    """)
    
    conn.commit()
    return conn


def etl_organizations_to_care_sites(conn):
    """Extracts FHIR Organization resources -> OMOP CARE_SITE table."""
    cursor = conn.cursor()
    res = requests.get(f"{FHIR_BASE_URL}/Organization")
    if res.status_code == 200 and "entry" in res.json():
        entries = res.json()["entry"]
        for item in entries:
            org = item["resource"]
            org_id = int(org["id"]) if org["id"].isdigit() else hash(org["id"]) % 1000000
            name = org.get("name", "Unknown Hospital")
            alias = org.get("alias", [""])[0] if org.get("alias") else ""
            
            cursor.execute("""
                INSERT OR REPLACE INTO CARE_SITE 
                (care_site_id, care_site_name, place_of_service_concept_id, location_id, care_site_source_value, care_site_source_concept_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (org_id, name, 8546, None, alias, 0))
            print(f"  [CARE_SITE] Mapped FHIR Organization/{org['id']} -> CARE_SITE ID: {org_id} ({name})")
    conn.commit()


def etl_patients_to_person(conn):
    """Extracts FHIR Patient resources -> OMOP PERSON table."""
    cursor = conn.cursor()
    res = requests.get(f"{FHIR_BASE_URL}/Patient")
    if res.status_code == 200 and "entry" in res.json():
        entries = res.json()["entry"]
        for item in entries:
            p = item["resource"]
            patient_id = int(p["id"]) if p["id"].isdigit() else hash(p["id"]) % 1000000
            gender = p.get("gender", "unknown")
            gender_cid = OMOP_GENDER_MAP.get(gender, 0)
            
            birth_date_str = p.get("birthDate", "1990-01-01")
            dt = datetime.strptime(birth_date_str, "%Y-%m-%d") if len(birth_date_str) == 10 else datetime(1990, 1, 1)
            
            cursor.execute("""
                INSERT OR REPLACE INTO PERSON
                (person_id, gender_concept_id, year_of_birth, month_of_birth, day_of_birth, birth_datetime, 
                 race_concept_id, ethnicity_concept_id, location_id, provider_id, care_site_id, 
                 person_source_value, gender_source_value, gender_source_concept_id, 
                 race_source_value, race_source_concept_id, ethnicity_source_value, ethnicity_source_concept_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, gender_cid, dt.year, dt.month, dt.day, birth_date_str,
                  0, 0, None, None, None, f"Patient/{p['id']}", gender, 0, None, 0, None, 0))
            print(f"  [PERSON] Mapped FHIR Patient/{p['id']} -> PERSON ID: {patient_id} (Gender Concept: {gender_cid})")
    conn.commit()


def etl_encounters_to_visit_occurrence(conn):
    """Extracts FHIR Encounter resources -> OMOP VISIT_OCCURRENCE table."""
    cursor = conn.cursor()
    res = requests.get(f"{FHIR_BASE_URL}/Encounter")
    if res.status_code == 200 and "entry" in res.json():
        entries = res.json()["entry"]
        for item in entries:
            enc = item["resource"]
            enc_id = int(enc["id"]) if enc["id"].isdigit() else hash(enc["id"]) % 1000000
            
            # Map Patient reference
            subject_ref = enc.get("subject", {}).get("reference", "Patient/0")
            patient_id_raw = subject_ref.split("/")[-1]
            patient_id = int(patient_id_raw) if patient_id_raw.isdigit() else 0
            
            # Map CareSite reference
            org_ref = enc.get("serviceProvider", {}).get("reference", "Organization/0")
            org_id_raw = org_ref.split("/")[-1]
            care_site_id = int(org_id_raw) if org_id_raw.isdigit() else 0
            
            enc_class = enc.get("class", {}).get("code", "IMP")
            visit_concept_id = OMOP_VISIT_MAP.get(enc_class, 9201)
            
            start_date = enc.get("period", {}).get("start", datetime.now().isoformat())[:10]
            
            cursor.execute("""
                INSERT OR REPLACE INTO VISIT_OCCURRENCE
                (visit_occurrence_id, person_id, visit_concept_id, visit_start_date, visit_start_datetime, 
                 visit_end_date, visit_end_datetime, visit_type_concept_id, provider_id, care_site_id, 
                 visit_source_value, visit_source_concept_id, admitted_from_concept_id, admitted_from_source_value, 
                 discharged_to_concept_id, discharged_to_source_value, preceding_visit_occurrence_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (enc_id, patient_id, visit_concept_id, start_date, start_date,
                  start_date, start_date, 44818518, None, care_site_id,
                  enc_class, 0, 0, None, 0, None, None))
            print(f"  [VISIT_OCCURRENCE] Mapped FHIR Encounter/{enc['id']} -> VISIT_OCCURRENCE ID: {enc_id} (CareSite ID: {care_site_id})")
    conn.commit()


def etl_observations_to_measurement(conn):
    """Extracts FHIR Observation resources -> OMOP MEASUREMENT table."""
    cursor = conn.cursor()
    res = requests.get(f"{FHIR_BASE_URL}/Observation")
    if res.status_code == 200 and "entry" in res.json():
        entries = res.json()["entry"]
        for item in entries:
            obs = item["resource"]
            obs_id = int(obs["id"]) if obs["id"].isdigit() else hash(obs["id"]) % 1000000
            
            # Subject reference
            subject_ref = obs.get("subject", {}).get("reference", "Patient/0")
            patient_id_raw = subject_ref.split("/")[-1]
            patient_id = int(patient_id_raw) if patient_id_raw.isdigit() else 0
            
            # LOINC code mapping
            codings = obs.get("code", {}).get("coding", [])
            loinc_code = codings[0].get("code", "") if codings else ""
            measurement_concept_id = OMOP_MEASUREMENT_MAP.get(loinc_code, 0)
            
            # Quantity value
            val_qty = obs.get("valueQuantity", {})
            value_num = val_qty.get("value", None)
            unit_str = val_qty.get("unit", "")
            
            effective_date = obs.get("effectiveDateTime", datetime.now().isoformat())[:10]
            
            cursor.execute("""
                INSERT OR REPLACE INTO MEASUREMENT
                (measurement_id, person_id, measurement_concept_id, measurement_date, measurement_datetime, 
                 measurement_time, measurement_type_concept_id, operator_concept_id, value_as_number, 
                 value_as_concept_id, unit_concept_id, range_low, range_high, provider_id, visit_occurrence_id, 
                 visit_detail_id, measurement_source_value, measurement_source_concept_id, unit_source_value, 
                 unit_source_value_raw, value_source_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (obs_id, patient_id, measurement_concept_id, effective_date, effective_date,
                  None, 44818702, 4172703, value_num,
                  0, 8541, None, None, None, None,
                  None, loinc_code, 0, unit_str, unit_str, str(value_num)))
            print(f"  [MEASUREMENT] Mapped FHIR Observation/{obs['id']} -> MEASUREMENT ID: {obs_id} (Val: {value_num} {unit_str})")
    conn.commit()


def main():
    print("🔄 Starting FHIR -> OMOP CDM v5.4 ETL Pipeline Execution...\n")
    conn = init_omop_db()
    
    print("1️⃣ Mapping Organizations -> OMOP CARE_SITE...")
    etl_organizations_to_care_sites(conn)
    
    print("\n2️⃣ Mapping Patients -> OMOP PERSON...")
    etl_patients_to_person(conn)
    
    print("\n3️⃣ Mapping Encounters -> OMOP VISIT_OCCURRENCE...")
    etl_encounters_to_visit_occurrence(conn)
    
    print("\n4️⃣ Mapping Observations -> OMOP MEASUREMENT...")
    etl_observations_to_measurement(conn)
    
    conn.close()
    print(f"\n🎉 ETL Success! OMOP CDM v5.4 Database successfully created at: {DB_NAME}")


if __name__ == "__main__":
    main()