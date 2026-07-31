
# 🇸🇬 Singapore Healthcare Interoperability & AI-Ready Pipeline
### **HL7 FHIR (HAPI) $\rightarrow$ OMOP CDM v5.4 ETL $\rightarrow$ Clinical AI Feature Matrix**

An end-to-end clinical data architecture and interoperability workspace built using **Python**, **HL7 FHIR RESTful APIs (HAPI FHIR)**, **Postman**, and **OHDSI OMOP CDM v5.4**. 

This repository demonstrates how operational hospital data from Singapore's **Ministry of Health (MOH)** public healthcare clusters (**SingHealth, NHG, NUHS**) can be ingested via standard FHIR resources, harmonized into an **OMOP Common Data Model**, and converted into an **AI-ready Feature Matrix** suitable for training clinical decision support and healthcare foundation models.

---

## 🏗️ 4-Stage End-to-End Architecture

<div align="center" style="background-color: #0d1117; padding: 24px; border-radius: 8px; border: 1px solid #30363d;">

  <!-- Data Source -->
  <div style="background-color: #161b22; color: #58a6ff; padding: 12px 20px; border-radius: 6px; font-weight: bold; width: 60%; border: 1px solid #1f6feb;">
    🇸🇬 MOH Singapore Open Data
  </div>

  <div style="color: #8b949e; margin: 8px 0;">↓ <i>Stage 1: Operational RESTful Modeling (ingest_sg_moh_fhir.py)</i></div>

  <!-- FHIR Container -->
  <div style="background-color: #161b22; border: 1px dashed #30363d; border-radius: 6px; padding: 16px; width: 85%;">
    <div style="color: #79c0ff; font-weight: bold; margin-bottom: 10px;">🐳 HAPI FHIR Server (Docker)</div>
    <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;">
      <span style="background-color: #21262d; color: #c9d1d9; padding: 6px 12px; border-radius: 4px; font-size: 13px;"><b>/Organization</b> (SingHealth, NHG, NUHS)</span>
      <span style="background-color: #21262d; color: #c9d1d9; padding: 6px 12px; border-radius: 4px; font-size: 13px;"><b>/Encounter</b> (Admissions & Occupancy)</span>
      <span style="background-color: #21262d; color: #c9d1d9; padding: 6px 12px; border-radius: 4px; font-size: 13px;"><b>/Patient</b> (Demographics)</span>
      <span style="background-color: #21262d; color: #c9d1d9; padding: 6px 12px; border-radius: 4px; font-size: 13px;"><b>/Observation</b> (LOINC Vitals & Signals)</span>
    </div>
  </div>

  <div style="color: #8b949e; margin: 8px 0;">↓ <i>Stage 2: Standardized Terminology ETL (fhir_to_omop_etl.py)</i></div>

  <!-- OMOP Container -->
  <div style="background-color: #161b22; border: 1px dashed #30363d; border-radius: 6px; padding: 16px; width: 85%;">
    <div style="color: #7ee787; font-weight: bold; margin-bottom: 10px;">🗄️ OMOP CDM v5.4 Database</div>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; text-align: left; font-size: 13px;">
      <div style="background-color: #21262d; color: #c9d1d9; padding: 8px; border-radius: 4px;"><b>CARE_SITE</b> ◄ Organization</div>
      <div style="background-color: #21262d; color: #c9d1d9; padding: 8px; border-radius: 4px;"><b>VISIT_OCCURRENCE</b> ◄ Encounter (Concept 9201)</div>
      <div style="background-color: #21262d; color: #c9d1d9; padding: 8px; border-radius: 4px;"><b>PERSON</b> ◄ Patient (Concept 8507/8532)</div>
      <div style="background-color: #21262d; color: #c9d1d9; padding: 8px; border-radius: 4px;"><b>MEASUREMENT</b> ◄ Observation (Concept 3027801)</div>
    </div>
  </div>

  <div style="color: #8b949e; margin: 8px 0;">↓ <i>Stage 3: Population Health Analytics</i></div>

  <!-- Analytics -->
  <div style="background-color: #161b22; color: #d2a8ff; padding: 10px 20px; border-radius: 6px; font-weight: bold; width: 70%; border: 1px solid #8957e5;">
    📊 OMOP Cohort Analytics (omop_cohort_analytics.py)
  </div>

  <div style="color: #8b949e; margin: 8px 0;">↓ <i>Stage 4: Feature Engineering</i></div>

  <!-- Feature Matrix & Output -->
  <div style="background-color: #161b22; color: #ffa657; padding: 10px 20px; border-radius: 6px; font-weight: bold; width: 75%; border: 1px solid #d29922;">
    🤖 Clinical AI Feature Matrix (omop_ai_feature_matrix.py)
  </div>

  <div style="color: #8b949e; margin: 8px 0;">↓</div>

  <div style="background-color: #238636; color: #ffffff; padding: 12px 20px; border-radius: 6px; font-weight: bold; width: 80%;">
    📄 Tabular Feature Vector X (sg_cardiometabolic_ai_features.csv)<br>
    <span style="font-size: 12px; font-weight: normal; opacity: 0.9;">🚀 Input to PyTorch / Scikit-Learn / Healthcare Foundation Models</span>
  </div>

</div>

---

## 📁 Repository Structure

| File | Description |
| :--- | :--- |
| `FHIR Masterclass - Cardiology Clinic.postman_collection.json` | Complete 5-project Postman collection covering core anatomy, CRUD, search modifiers (`:exact`, `:contains`), reference chaining (`_has`, `_include`, `_revinclude`), and Optimistic Concurrency Control (`If-Match` / `409 Conflict`). |
| `ingest_sg_moh_fhir.py` | Stage 1 script that parses Singapore public hospital operational metrics and posts them as live FHIR `Organization` and `Encounter` payloads to HAPI FHIR. |
| `fhir_to_omop_etl.py` | Stage 2 ETL script that extracts live FHIR JSON resources, maps local/LOINC codes to OHDSI Standard Concept IDs, and populates an OMOP CDM v5.4 relational database. |
| `omop_cohort_analytics.py` | Stage 3 population health analytics engine that runs OHDSI-style aggregations on hospital bed utilization, cohort age/gender splits, and cardiometabolic vital stats. |
| `omop_ai_feature_matrix.py` | Stage 4 feature extraction engine that joins `PERSON`, `VISIT_OCCURRENCE`, and `MEASUREMENT` tables to output a machine-learning training matrix `X` with clinical risk scores. |

---

## 🛠️ Execution & Deployment Guide

### Prerequisites
* **Docker Desktop** (running local HAPI FHIR container)
* **Python 3.9+**
* **Postman**

### Step 1: Start Local HAPI FHIR Server
```bash
docker run -d -p 8080:8080 hapiproject/hapi:latest

```

### Step 2: Install Python Dependencies

```bash
pip install requests pandas numpy

```

### Step 3: Run the 4-Stage Pipeline

1. **Ingest Singapore MOH Data into FHIR:**
```bash
python ingest_sg_moh_fhir.py

```


2. **Run FHIR-to-OMOP CDM v5.4 ETL Transformer:**
```bash
python fhir_to_omop_etl.py

```


3. **Run Population Cohort Analytics:**
```bash
python omop_cohort_analytics.py

```


4. **Extract AI Feature Matrix & Risk Vectors:**
```bash
python omop_ai_feature_matrix.py

```



---

## 📊 Sample Output (AI Feature Matrix Extraction)

```text
========================================================================
🤖 CLINICAL AI FEATURE EXTRACTION: OMOP CDM v5.4 -> ML TRAINING MATRIX
========================================================================

Patient_ID  Age  Is_Male  Total_Inpatient_Visits  Mean_Heart_Rate_BPM  Max_Heart_Rate_BPM  Cardiometabolic_Risk_Score Risk_Category
      1000   49        1                       5                88.50               108.0                        4.98 High         
      1001   41        1                       2                76.00                82.0                        2.42 Moderate     
      1002   34        0                       2                92.10               104.0                        3.68 High         

💾 Saved AI Training Feature Matrix to: sg_cardiometabolic_ai_features.csv
========================================================================

```

---

## 🎯 Clinical Standards & Frameworks Used

* **HL7 FHIR Release 4 (R4):** Operational messaging standard for electronic healthcare records.
* **OHDSI OMOP Common Data Model (v5.4):** Standardized analytical model for observational research and AI.
* **LOINC & SNOMED CT:** Standardized clinical terminologies for vital signs and hospital admissions.

```

---

