🩺 HL7 FHIR Practical Masterclass
Postman + Dockerized HAPI FHIR

A hands-on implementation of HL7 FHIR RESTful API capabilities, built and tested using Postman against a local Dockerized HAPI FHIR JPA Server.

📁 PROJECT OVERVIEW

Five practical projects exploring FHIR resource modeling, API operations, clinical workflows, and version management.

▸ Project 1: Core Resource Anatomy & Modeling
• Primitive and complex data types: HumanName, ContactPoint, and Address
• XHTML narratives and custom extensions
• Manual construction of Patient resources

▸ Project 2: Basic CRUD & Safe Operations
• Create, read, update, and delete resources
• Full resource replacement using PUT
• Conditional creation using If-None-Exist
• Logical deletion and response handling

▸ Project 3: Clinic Directory & Advanced Filtering
• Search parameters and string modifiers
• Numeric comparisons and date-range filters
• Search-result Bundle parsing

▸ Project 4: Connected Patient Charts
• References between clinical resources
• Chained and reverse-chained searches
• Related-resource retrieval using _include and _revinclude

▸ Project 5: Resource History & Concurrency Control
• Resource modification history using _history
• Historical version retrieval using vread
• Optimistic concurrency control using If-Match
• Conflict-response verification

🛠️ TOOLS USED
• Postman
• HAPI FHIR JPA Server
• Docker Desktop

▶️ GETTING STARTED
Start the local FHIR server:
docker start local-fhir
