from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.controllers.charity_controller import (
    search_charities,
    get_charity_by_id,
    get_charity_stats,
    get_charities_by_location
)
from app.models.charity import (
    CharitySearchRequest,
    CharitySearchResponse,
    CharityResponse,
    CharityStatsResponse
)

router = APIRouter(prefix="/api/v1/charities", tags=["charities"])


@router.post("/search", response_model=CharitySearchResponse)
async def search_charities_endpoint(
    search_request: CharitySearchRequest,
    db: AsyncSession = Depends(get_db)
) -> CharitySearchResponse:
    """Search charities based on various criteria."""
    return await search_charities(db, search_request)


@router.get("/search", response_model=CharitySearchResponse)
async def search_charities_get(
    query: Optional[str] = Query(None, description="Search term for charity name"),
    state: Optional[str] = Query(None, description="State filter (ACT, NSW, NT, QLD, SA, TAS, VIC, WA)"),
    charity_size: Optional[str] = Query(None, description="Charity size filter (Small, Medium, Large)"),
    purpose: Optional[str] = Query(None, description="Purpose filter"),
    beneficiary: Optional[str] = Query(None, description="Beneficiary group filter"),
    has_website: Optional[bool] = Query(None, description="Filter by website availability"),
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: AsyncSession = Depends(get_db)
) -> CharitySearchResponse:
    """Search charities using query parameters."""
    search_request = CharitySearchRequest(
        query=query,
        state=state,
        charity_size=charity_size,
        purpose=purpose,
        beneficiary=beneficiary,
        has_website=has_website,
        limit=limit,
        offset=offset
    )
    return await search_charities(db, search_request)


@router.get("/{charity_id}", response_model=CharityResponse)
async def get_charity(
    charity_id: int,
    db: AsyncSession = Depends(get_db)
) -> CharityResponse:
    """Get a specific charity by ID."""
    charity = await get_charity_by_id(db, charity_id)
    if not charity:
        raise HTTPException(status_code=404, detail="Charity not found")
    return charity


@router.get("/stats/overview", response_model=CharityStatsResponse)
async def get_charity_stats_endpoint(
    db: AsyncSession = Depends(get_db)
) -> CharityStatsResponse:
    """Get charity statistics overview."""
    return await get_charity_stats(db)


@router.get("/location/search", response_model=List[CharityResponse])
async def search_charities_by_location(
    state: Optional[str] = Query(None, description="State filter"),
    city: Optional[str] = Query(None, description="City filter"),
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    db: AsyncSession = Depends(get_db)
) -> List[CharityResponse]:
    """Search charities by location."""
    return await get_charities_by_location(db, state, city, limit)


@router.get("/filters/options")
async def get_filter_options() -> dict:
    """Get available filter options."""
    return {
        "states": ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"],
        "sizes": ["Small", "Medium", "Large"],
        "purposes": [
            "advancing_education",
            "advancing_health", 
            "advancing_natural_environment",
            "advancing_religion",
            "advancing_social_or_public_welfare",
            "advancing_culture",
            "promoting_or_protecting_human_rights",
            "preventing_or_relieving_suffering_of_animals"
        ],
        "beneficiaries": [
            "children",
            "aged_persons",
            "people_with_disabilities",
            "families",
            "youth",
            "adults",
            "financially_disadvantaged",
            "general_community_in_australia"
        ]
    }
