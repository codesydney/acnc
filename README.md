# Charity Discovery Platform

A modern web application for discovering and searching Australian charities. Built with FastAPI, SQLModel, and TailwindCSS.

## Features

- 🔍 **Advanced Search**: Search charities by name, location, purpose, and beneficiary groups
- 📊 **Statistics Dashboard**: View sector-wide statistics and insights
- 🗺️ **Location-based Discovery**: Find charities by state and city
- 📱 **Responsive Design**: Beautiful, mobile-friendly interface
- ⚡ **Fast Performance**: Built with modern async Python and optimized queries

## Tech Stack

- **Backend**: FastAPI with SQLModel (SQLAlchemy)
- **Database**: SQLite with async support
- **Frontend**: HTML5, TailwindCSS, Vanilla JavaScript
- **Data**: Australian Charity and Not-for-profits Commission (ACNC) data

## Quick Start

### 1. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using poetry
poetry install
```

### 2. Import Data

```bash
python import_data.py
```

This will:
- Create the SQLite database
- Import all charity data from the CSV file
- Set up the database schema

### 3. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Search Charities
- `GET /api/v1/charities/search` - Search with query parameters
- `POST /api/v1/charities/search` - Search with request body

### Get Charity Details
- `GET /api/v1/charities/{charity_id}` - Get specific charity

### Statistics
- `GET /api/v1/charities/stats/overview` - Get sector statistics

### Location Search
- `GET /api/v1/charities/location/search` - Search by location

### Filter Options
- `GET /api/v1/charities/filters/options` - Get available filter options

## Search Parameters

- `query`: Search term for charity name
- `state`: State filter (ACT, NSW, NT, QLD, SA, TAS, VIC, WA)
- `charity_size`: Size filter (Small, Medium, Large)
- `purpose`: Purpose filter (education, health, environment, etc.)
- `beneficiary`: Beneficiary group filter (children, aged, disabled, etc.)
- `has_website`: Filter by website availability
- `limit`: Number of results per page (1-100)
- `offset`: Number of results to skip

## Data Structure

The application uses data from the Australian Charity and Not-for-profits Commission (ACNC) with the following key fields:

- **Basic Info**: ABN, legal name, other names, website
- **Location**: Address, state, postcode, country
- **Operations**: States of operation, international operations
- **Purpose**: 20+ charitable purpose categories
- **Beneficiaries**: 30+ beneficiary group categories
- **Organization**: Size, responsible persons, financial year end

## Development

### Project Structure

```
app/
├── models/          # SQLModel database models
├── controllers/     # Business logic layer
├── routes/          # API route definitions
├── templates/       # Jinja2 templates
├── utils/           # Utility functions
└── database.py      # Database configuration
```

### Adding New Features

1. **Models**: Add new models in `app/models/`
2. **Controllers**: Add business logic in `app/controllers/`
3. **Routes**: Add API endpoints in `app/routes/`
4. **Templates**: Add frontend pages in `app/templates/`

### Database Migrations

The application uses SQLModel which automatically handles schema changes. For production, consider using Alembic for proper migration management.

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python import_data.py

EXPOSE 8000
CMD ["python", "main.py"]
```

### Using Fly.io

1. Create `fly.toml` configuration
2. Deploy with `fly deploy`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data provided by the Australian Charity and Not-for-profits Commission (ACNC)
- Built with FastAPI, SQLModel, and TailwindCSS