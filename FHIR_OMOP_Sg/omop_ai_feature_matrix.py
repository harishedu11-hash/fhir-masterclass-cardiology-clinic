import sqlite3
import pandas as pd
import numpy as np

DB_NAME = "omop_cdm_v5_4.db"
OUTPUT_CSV = "sg_cardiometabolic_ai_features.csv"

def extract_ml_feature_matrix():
    print("========================================================================")
    print("🤖 CLINICAL AI FEATURE EXTRACTION: OMOP CDM v5.4 -> ML TRAINING MATRIX")
    print("========================================================================\n")
    
    conn = sqlite3.connect(DB_NAME)
    
    # SQL Query performing multi-table OMOP join & feature engineering
    feature_query = """
    SELECT 
        p.person_id AS Patient_ID,
        p.person_source_value AS FHIR_Reference,
        (strftime('%Y', 'now') - p.year_of_birth) AS Age,
        p.gender_concept_id AS Gender_Concept_ID,
        CASE p.gender_concept_id 
            WHEN 8507 THEN 1 
            WHEN 8532 THEN 0 
            ELSE 0 
        END AS Is_Male,
        
        -- Hospital Inpatient Utilization Feature
        COALESCE(v.total_inpatient_visits, 0) AS Total_Inpatient_Visits,
        
        -- Cardiometabolic Vital Sign Features (LOINC 8867-4 / OMOP 3027801)
        COALESCE(m.mean_heart_rate, 75.0) AS Mean_Heart_Rate_BPM,
        COALESCE(m.max_heart_rate, 75.0) AS Max_Heart_Rate_BPM,
        COALESCE(m.total_measurements, 0) AS Heart_Rate_Measurement_Count
        
    FROM PERSON p
    LEFT JOIN (
        SELECT person_id, COUNT(visit_occurrence_id) AS total_inpatient_visits
        FROM VISIT_OCCURRENCE
        GROUP BY person_id
    ) v ON p.person_id = v.person_id
    LEFT JOIN (
        SELECT 
            person_id, 
            ROUND(AVG(value_as_number), 2) AS mean_heart_rate,
            MAX(value_as_number) AS max_heart_rate,
            COUNT(measurement_id) AS total_measurements
        FROM MEASUREMENT
        WHERE measurement_concept_id = 3027801
        GROUP BY person_id
    ) m ON p.person_id = m.person_id;
    """
    
    df = pd.read_sql_query(feature_query, conn)
    conn.close()

    # Risk vector simulation
    df['Cardiometabolic_Risk_Score'] = (
        (df['Age'] * 0.02) + 
        (np.where(df['Max_Heart_Rate_BPM'] > 100, 1.5, 0.0)) + 
        (df['Total_Inpatient_Visits'] * 0.8)
    ).round(2)
    
    df['Risk_Category'] = pd.cut(
        df['Cardiometabolic_Risk_Score'], 
        bins=[-1, 1.5, 2.5, 10.0], 
        labels=['Low', 'Moderate', 'High']
    )

    print("✅ Successfully Extracted Feature Matrix (X) for ML Pipeline:")
    print(df.to_string(index=False))
    
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n💾 Saved AI Training Feature Matrix to: {OUTPUT_CSV}")
    print("========================================================================\n")

if __name__ == "__main__":
    extract_ml_feature_matrix()