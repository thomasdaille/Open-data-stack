# Open-data-stack

This repository show a complete open-source and **local ELT data stack** built with **Docker**

The stack integrates the following components:

- [Airbyte](https://airbyte.com/) — ingestion pipelines  
- [Postgres](https://www.postgresql.org/) — data warehouse
- [DBT](https://www.getdbt.com/) — transformations, modeling, testing, documentation  
- [Metabase](https://www.metabase.com/) — analytics & dashboards  
- [OpenMetadata](https://open-metadata.org/) — governance, lineage, data quality  

---

## 🛠️ Architecture Overview

The data warehouse is structured using a modern multi‑zone approach:

- **ODS (Operational Data Store)** — raw + normalized landing zone  
- **EDW (Enterprise Data Warehouse)** — centralized business models  
- **DM_xxx (Data Marts)** — domain‑specific analytical layers (sales, marketing, finance, etc.)

This layered architecture enables:

- clear separation of responsibilities  
- progressive data quality improvements  
- robust DBT modeling and documentation  
- consistent analytical exposure for Metabase  

---

## 📃 Data sources

[...]

## 🧠 DBT Modeling Structure

[...]

---

## 📊 Metabase Dashboards

Metabase dashboards are built on top of the DM schemas and provide:

- business KPIs  
- exploratory analytics  
- clean and reproducible visualizations  

Screenshots and dashboard descriptions are available in the `metabase/` directory.

---

## 🔍 Data Governance with OpenMetadata

OpenMetadata provides:

- full lineage from Airbyte → DBT → Postgres → Metabase  
- dataset documentation  
- ownership & tagging  
- quality checks  

---

## 📚 Documentation

Full documentation is available in the `docs/` directory:

- Global architecture  
- ELT pipelines  
- EDW modeling  
- Metabase dashboards  
- OpenMetadata governance  
