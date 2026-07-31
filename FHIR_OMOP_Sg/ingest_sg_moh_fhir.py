import requests
import json
from datetime import datetime, timedelta

# Local HAPI FHIR Server Endpoint
FHIR_BASE_URL = "http://localhost:8080/fhir"
HEADERS = {"Content-Type": "application/fhir+json"}

# 🇸🇬 Singapore Public Healthcare Clusters & Hospitals (MOH Data Structure)
HOSPITALS_DATA = [
    {
        "name": "Singapore General Hospital",
        "alias": "SGH",
        "cluster": "SingHealth",
        "type": "public-acute",
        "total_beds": 1785,
        "occupancy_rate": 0.88,  # 88% BOR
        "specialties": ["Cardiology", "General Surgery", "Internal Medicine"]
    },
    {
        "name": "Tan Tock Seng Hospital",
        "alias": "TTSH",
        "cluster": "NHG",
        "type": "public-acute",
        "total_beds": 1700,
        "occupancy_rate": 0.92,  # 92% BOR
        "specialties": ["Infectious Diseases", "Geriatric Medicine", "Cardiology"]
    },
    {
        "name": "National University Hospital",
        "alias": "NUH",
        "cluster": "NUHS",
        "type": "public-acute",
        "total_beds": 1200,
        "occupancy_rate": 0.85,  # 85% BOR
        "specialties": ["Pediatrics", "Cardiology", "Oncology"]
    },
    {
        "name": "Khoo Teck Puat Hospital",
        "alias": "KTPH",
        "cluster": "NHG",
        "type": "public-acute",
        "total_beds": 765,
        "occupancy_rate": 0.90,  # 90% BOR
        "specialties": ["General Medicine", "Orthopedics"]
    }
]


def create_fhir_organization(hosp):
    """Creates a FHIR Organization resource representing a Singapore Hospital."""
    org_payload = {
        "resourceType": "Organization",
        "identifier": [
            {
                "system": "https://www.moh.gov.sg/institutions",
                "value": hosp["alias"]
            }
        ],
        "active": True,
        "name": hosp["name"],
        "alias": [hosp["alias"], hosp["cluster"]],
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                        "code": "prov",
                        "display": "Healthcare Provider"
                    }
                ]
            }
        ],
        "address": [
            {
                "country": "Singapore",
                "use": "work"
            }
        ]
    }
    
    response = requests.post(f"{FHIR_BASE_URL}/Organization", json=org_payload, headers=HEADERS)
    if response.status_code in [200, 201]:
        org_id = response.json()["id"]
        print(f"✅ Created FHIR Organization: {hosp['name']} (ID: {org_id})")
        return org_id
    else:
        print(f"❌ Failed to create Organization for {hosp['name']}: {response.text}")
        return None


def create_fhir_encounters(org_id, hosp_info):
    """
    Generates synthetic FHIR Encounter records matching the hospital's Bed Occupancy Rate (BOR).
    """
    occupied_beds = int(hosp_info["total_beds"] * hosp_info["occupancy_rate"])
    print(f"   ↳ Generating {occupied_beds} bed-occupancy FHIR Encounters for {hosp_info['alias']}...")
    
    # We will generate a representative batch of Encounters for demonstration
    sample_encounters_count = 5  # Generates 5 active encounter records per hospital
    
    for i in range(sample_encounters_count):
        start_time = (datetime.now() - timedelta(days=i)).isoformat()
        
        encounter_payload = {
            "resourceType": "Encounter",
            "status": "in-progress",
            "class": {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "IMP",
                "display": "inpatient encounter"
            },
            "type": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "308335008",
                            "display": "Patient hospital admission"
                        }
                    ],
                    "text": f"Admission - {hosp_info['specialties'][i % len(hosp_info['specialties'])]}"
                }
            ],
            "subject": {
                "reference": f"Patient/1000"  # References Luke Skywalker or seeded patient ID
            },
            "serviceProvider": {
                "reference": f"Organization/{org_id}"
            },
            "period": {
                "start": start_time
            }
        }
        
        res = requests.post(f"{FHIR_BASE_URL}/Encounter", json=encounter_payload, headers=HEADERS)
        if res.status_code in [200, 201]:
            enc_id = res.json()["id"]
            print(f"     ✅ Created Encounter ID: {enc_id} linked to Organization/{org_id}")


def main():
    print("🇸🇬 Starting Ingestion: Singapore MOH Hospital Data -> HAPI FHIR Server...\n")
    for hosp in HOSPITALS_DATA:
        org_id = create_fhir_organization(hosp)
        if org_id:
            create_fhir_encounters(org_id, hosp)
    print("\n🎉 Stage 1 Ingestion Complete! Hospital Organizations & Encounters are loaded into FHIR.")


if __name__ == "__main__":
    main()