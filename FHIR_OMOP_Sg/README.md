\# 🇸🇬 Singapore Healthcare Interoperability \& AI-Ready Pipeline

\### \*\*HL7 FHIR (HAPI) $\\rightarrow$ OMOP CDM v5.4 ETL $\\rightarrow$ Clinical AI Feature Matrix\*\*



An end-to-end clinical data architecture and interoperability workspace built using \*\*Python\*\*, \*\*HL7 FHIR RESTful APIs (HAPI FHIR)\*\*, \*\*Postman\*\*, and \*\*OHDSI OMOP CDM v5.4\*\*. 



This repository demonstrates how operational hospital data from Singapore's \*\*Ministry of Health (MOH)\*\* public healthcare clusters (\*\*SingHealth, NHG, NUHS\*\*) can be ingested via standard FHIR resources, harmonized into an \*\*OMOP Common Data Model\*\*, and converted into an \*\*AI-ready Feature Matrix\*\* suitable for training clinical decision support and healthcare foundation models.



\---



\## 🏗️ 4-Stage End-to-End Architecture



```mermaid

flowchart TD

&#x20;   A\["🇸🇬 MOH Singapore Open Data"] -->|Stage 1: Operational RESTful Modeling| B\["🐳 HAPI FHIR Server (Docker)"]

&#x20;   

&#x20;   subgraph FHIR \["HL7 FHIR Resources"]

&#x20;       B --> B1\["/Organization (SingHealth, NHG, NUHS)"]

&#x20;       B --> B2\["/Encounter (Inpatient Admissions \& Occupancy)"]

&#x20;       B --> B3\["/Patient (Demographics)"]

&#x20;       B --> B4\["/Observation (LOINC Vitals \& Signals)"]

&#x20;   end



&#x20;   FHIR -->|Stage 2: Standardized Terminology ETL| C\["🗄️ OMOP CDM v5.4 Database"]



&#x20;   subgraph OMOP \["OMOP CDM v5.4 Tables"]

&#x20;       C --> C1\["CARE\_SITE ◄-- Mapped from Organization"]

&#x20;       C --> C2\["VISIT\_OCCURRENCE ◄-- Mapped from Encounter (Concept 9201)"]

&#x20;       C --> C3\["PERSON ◄-- Mapped from Patient (Concept 8507/8532)"]

&#x20;       C --> C4\["MEASUREMENT ◄-- Mapped from Observation (Concept 3027801)"]

&#x20;   end



&#x20;   OMOP -->|Stage 3: Population Health Analytics| D\["📊 OMOP Cohort Analytics (omop\_cohort\_analytics.py)"]

&#x20;   D -->|Stage 4: Feature Engineering| E\["🤖 Clinical AI Feature Matrix (omop\_ai\_feature\_matrix.py)"]

&#x20;   E --> F\["📄 Tabular Feature Vector X (sg\_cardiometabolic\_ai\_features.csv)"]

&#x20;   F --> G\["🚀 Input to PyTorch / Scikit-Learn / Healthcare Foundation Models"]

```



\----

\## 📁 Repository Structure



| File | Description |

| :--- | :--- |

| `FHIR Masterclass - Cardiology Clinic.postman\_collection.json` | Complete 5-project Postman collection covering core anatomy, CRUD, search modifiers (`:exact`, `:contains`), reference chaining (`\_has`, `\_include`, `\_revinclude`), and Optimistic Concurrency Control (`If-Match` / `409 Conflict`). |

| `ingest\_sg\_moh\_fhir.py` | Stage 1 script that parses Singapore public hospital operational metrics and posts them as live FHIR `Organization` and `Encounter` payloads to HAPI FHIR. |

| `fhir\_to\_omop\_etl.py` | Stage 2 ETL script that extracts live FHIR JSON resources, maps local/LOINC codes to OHDSI Standard Concept IDs, and populates an OMOP CDM v5.4 relational database. |

| `omop\_cohort\_analytics.py` | Stage 3 population health analytics engine that runs OHDSI-style aggregations on hospital bed utilization, cohort age/gender splits, and cardiometabolic vital stats. |

| `omop\_ai\_feature\_matrix.py` | Stage 4 feature extraction engine that joins `PERSON`, `VISIT\_OCCURRENCE`, and `MEASUREMENT` tables to output a machine-learning training matrix `X` with clinical risk scores. |



\---



\## 🛠️ Execution \& Deployment Guide



\### Prerequisites

\* Docker Desktop (running local HAPI FHIR container)

\* Python 3.9+

\* Postman



\### Step 1: Start Local HAPI FHIR Server

```bash

docker run -d -p 8080:8080 hapiproject/hapi:latest



\### Step 2: Install Python Dependencies

pip install requests pandas numpy

### Step 3: Run the 4-Stage Pipeline

&#x09;- Ingest Singapore MOH Data into FHIR: python ingest\_sg\_moh\_fhir.py



&#x09;- Run FHIR-to-OMOP CDM v5.4 ETL Transformer: python fhir\_to\_omop\_etl.py



&#x09;- Run Population Cohort Analytics: python omop\_cohort\_analytics.py



&#x09;- Extract AI Feature Matrix \& Risk Vectors: python omop\_ai\_feature\_matrix.py



========================================================================

🤖 CLINICAL AI FEATURE EXTRACTION: OMOP CDM v5.4 -> ML TRAINING MATRIX

========================================================================



Patient\_ID  Age  Is\_Male  Total\_Inpatient\_Visits  Mean\_Heart\_Rate\_BPM  Max\_Heart\_Rate\_BPM  Cardiometabolic\_Risk\_Score Risk\_Category

&#x20;     1000   49        1                       5                88.50               108.0                        4.98 High         

&#x20;     1001   41        1                       2                76.00                82.0                        2.42 Moderate     

&#x20;     1002   34        0                       2                92.10               104.0                        3.68 High         



💾 Saved AI Training Feature Matrix to: sg\_cardiometabolic\_ai\_features.csv

========================================================================



🎯 Clinical Standards \& Frameworks Used

HL7 FHIR Release 4 (R4): Operational messaging standard for electronic healthcare records.



OHDSI OMOP Common Data Model (v5.4): Standardized analytical model for observational research and AI.



LOINC \& SNOMED CT: Standardized clinical terminologies for vital signs and hospital admissions.





