# Computer Networks Course Assignments

This repository contains a collection of scripts developed as part of the **Computer Networks** course. Each script corresponds to one of five practical assignments, showcasing the use of modern technologies and tools for building backend systems, parsing web data, and working with databases and containers.

## Tech Stack

The code in this repository demonstrates the integration and use of various technologies commonly used in real-world backend and data engineering applications:

- **FastAPI** — for building lightweight and high-performance web APIs.
- **Pandas** — for working with structured data and DataFrames.
- **Selenium** + **webdriver-manager** — for web scraping and browser automation.
- **SQLAlchemy** — for interacting with relational databases using Pythonic ORM.
- **PostgreSQL** — as the main relational database for storing parsed and processed data.
- **psycopg2** — PostgreSQL adapter for Python.
- **Uvicorn** — ASGI server for running FastAPI applications.
- **Docker** — for containerization and reproducible development environments.

## Structure

Each assignment is placed in its own folder and demonstrates different aspects of networked application development:

- Web data scraping with browser automation.
- API development and interaction.
- Database connection and data storage.
- Containerization of services for deployment and testing.

## Getting Started

To run the project locally, make sure you have the following installed:

- Python 3.10+
- Docker (optional, for containerized execution)
- PostgreSQL (if not using Docker)

Install dependencies:

```bash
pip install -r requirements.txt
