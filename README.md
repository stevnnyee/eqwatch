# EQWatch

A web app that ingests real-time earthquake data from the USGS Earthquake Hazards API and lets users track seismic activity in saved regions.

## Tech Stack

- **Database:** MySQL (Docker)
- **Backend:** FastAPI + raw SQL via `mysql-connector-python`
- **Frontend:** React + Tailwind CSS

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/eqwatch.git
cd eqwatch
```

### 2. Configure environment variables

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials
```

### 3. Start the database

```bash
make db
```

### 4. Install backend dependencies

```bash
make install
```

### 5. Run the backend

```bash
make backend
```

### 6. Install and run the frontend

```bash
cd frontend
npm install
npm run dev
```

## Seeding Data

```bash
make seed
```

## API Docs

Once the backend is running, visit `http://localhost:8000/docs` for the interactive Swagger UI.
