import sqlite3
import pandas as pd

DB_NAME = "omop_cdm_v5_4.db"

def run_analytics():
    conn = sqlite3.connect(DB_NAME)
    print("======================================================================")
    print("🇸🇬 SINGAPORE CLINICAL DATASET: OMOP CDM v5.4 COHORT ANALYTICS SUMMARY")
    print("======================================================================\n")

    # 1. Hospital Utilization Summary (CARE_SITE + VISIT_OCCURRENCE)
    query_hospitals = """
    SELECT 
        c.care_site_name AS Hospital_Name,
        c.care_site_source_value AS Cluster,
        COUNT(v.visit_occurrence_id) AS Total_Inpatient_Visits
    FROM CARE_SITE c
    LEFT JOIN VISIT_OCCURRENCE v ON c.care_site_id = v.care_site_id
    GROUP BY c.care_site_id;
    """
    df_hospitals = pd.read_sql_query(query_hospitals, conn)
    print("📊 1. Hospital Inpatient Bed Occupancy & Visit Distribution:")
    print(df_hospitals.to_string(index=False))
    print("\n" + "-"*65 + "\n")

    # 2. Demographics & Gender Breakdown (PERSON)
    query_gender = """
    SELECT 
        CASE gender_concept_id
            WHEN 8507 THEN 'Male'
            WHEN 8532 THEN 'Female'
            ELSE 'Other/Unknown'
        END AS Gender,
        COUNT(person_id) AS Patient_Count,
        ROUND(AVG(strftime('%Y', 'now') - year_of_birth), 1) AS Average_Age
    FROM PERSON
    GROUP BY gender_concept_id;
    """
    df_gender = pd.read_sql_query(query_gender, conn)
    print("📊 2. Patient Population Demographics:")
    print(df_gender.to_string(index=False))
    print("\n" + "-"*65 + "\n")

    # 3. Clinical Vital Signs Analysis (MEASUREMENT)
    query_vitals = """
    SELECT 
        m.measurement_source_value AS LOINC_Code,
        COUNT(m.measurement_id) AS Total_Measurements,
        ROUND(AVG(m.value_as_number), 2) AS Mean_Heart_Rate_BPM,
        MIN(m.value_as_number) AS Min_BPM,
        MAX(m.value_as_number) AS Max_BPM,
        m.unit_source_value AS Unit
    FROM MEASUREMENT m
    WHERE m.measurement_concept_id = 3027801
    GROUP BY m.measurement_concept_id;
    """
    df_vitals = pd.read_sql_query(query_vitals, conn)
    print("📊 3. Cardiometabolic Feature Extraction (Heart Rate Vitals):")
    print(df_vitals.to_string(index=False))
    print("\n======================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    run_analytics()