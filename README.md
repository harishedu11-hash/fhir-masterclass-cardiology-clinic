\# 🏥 HL7 FHIR Practical Masterclass (Postman + HAPI FHIR)



A hands-on implementation of HL7 FHIR (Fast Healthcare Interoperability Resources) RESTful API capabilities built and tested using \*\*Postman\*\* against a local \*\*Dockerized HAPI FHIR JPA Server\*\*.



\---



\## 🚀 Projects Overview



This repository contains a complete Postman collection covering real-world clinical workflow scenarios across \*\*Categories 1–5\*\* of the FHIR specification:



\### 🏥 Project 1: Core Resource Anatomy \& Modeling

\* \*\*Concepts:\*\* Primitive vs. Complex Data Types (`HumanName`, `ContactPoint`, `Address`), XHTML Narratives (`text.div`), and custom extensions.

\* \*\*Payloads Built:\*\* Manual construction of standard `Patient` resources and `US Core Patient Language` extensions.



\### 📝 Project 2: Basic CRUD \& Safe Operations

\* \*\*Concepts:\*\* HTTP Verbs (`POST`, `GET`, `PUT`, `DELETE`), Idempotent Operations, and Logical Deletions.

\* \*\*Highlights:\*\* 

&#x20; \* Full resource replacement using `PUT`.

&#x20; \* Idempotent registration using `If-None-Exist` headers (`identifier=http://hospital.org/mrn|MRN-555`).

&#x20; \* Logical deletion handling (`410 Gone` / `404 Not Found`).



\### 🔍 Project 3: Clinic Directory \& Advanced Filtering

\* \*\*Concepts:\*\* RESTful Search Parameters, Modifiers, Numeric/Date Prefixes, and `searchset` Bundle parsing.

\* \*\*Queries Implemented:\*\*

&#x20; \* String matching modifiers (`:contains`, `:exact`).

&#x20; \* Comparative numeric filters (`value-quantity=gt100`).

&#x20; \* Date range filters (`date=ge2026-01-01`).



\### 🔗 Project 4: Connected Patient Charts \& Relationship Traversal

\* \*\*Concepts:\*\* Reference Modeling (`subject.reference`), Chained Searching, Reverse Chaining, and Payload Optimization.

\* \*\*Queries Implemented:\*\*

&#x20; \* \*\*Chained Search:\*\* `GET /Observation?patient.family=Skywalker`

&#x20; \* \*\*Reverse Chaining:\*\* `GET /Patient?\_has:Observation:patient:code=8867-4`

&#x20; \* \*\*Forward Include:\*\* `GET /Observation?\_id=1004\&\_include=Observation:patient`

&#x20; \* \*\*Reverse Include:\*\* `GET /Patient?\_id=1000\&\_revinclude=Observation:patient`



\### ⏳ Project 5: Audit Trail \& Concurrency Control

\* \*\*Concepts:\*\* Audit logging, historical version reads, and Optimistic Concurrency Control (OCC).

\* \*\*Highlights:\*\*

&#x20; \* Inspection of full modification logs using `/\_history`.

&#x20; \* Historical snapshot retrieval using `vread` (`/\_history/1`).

&#x20; \* Concurrency protection using `If-Match: W/"<version>"` headers.

&#x20; \* Conflict rejection verification via HTTP `409 Conflict` / `412 Precondition Failed`.



\---



\## 🛠️ How to Import and Run



1\. \*\*Start Local FHIR Server (Docker Desktop):\*\*

&#x20;  ```bash

&#x20;  docker start local-fhir

