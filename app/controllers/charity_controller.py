from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional, Dict, Any
from app.models.charity import (
    Charity, 
    CharityResponse, 
    CharitySearchRequest, 
    CharitySearchResponse,
    CharityStatsResponse
)


async def search_charities(
    db: AsyncSession, 
    search_request: CharitySearchRequest
) -> CharitySearchResponse:
    """Search charities based on various criteria."""
    
    # Build query
    query = select(Charity)
    conditions = []
    
    # Always exclude charities with null, empty, or invalid names
    conditions.append(Charity.charity_legal_name.isnot(None))
    conditions.append(Charity.charity_legal_name != "")
    # Exclude names that are too short (likely identifiers rather than proper names)
    conditions.append(func.length(Charity.charity_legal_name) >= 10)
    # Exclude names that contain only numbers, dashes, and letters (ABN-like patterns)
    conditions.append(~Charity.charity_legal_name.like('%-%'))
    
    # Text search in charity name and other names
    if search_request.query:
        search_term = f"%{search_request.query}%"
        conditions.append(
            or_(
                Charity.charity_legal_name.ilike(search_term),
                Charity.other_organisation_names.ilike(search_term)
            )
        )
    
    # State filter
    if search_request.state:
        state_field = f"operates_in_{search_request.state.lower()}"
        if hasattr(Charity, state_field):
            conditions.append(getattr(Charity, state_field) == True)
    
    # Size filter
    if search_request.charity_size:
        conditions.append(Charity.charity_size == search_request.charity_size)
    
    # Purpose filter
    if search_request.purpose:
        purpose_field = search_request.purpose.lower().replace(" ", "_").replace("-", "_")
        if hasattr(Charity, purpose_field):
            conditions.append(getattr(Charity, purpose_field) == True)
    
    # Beneficiary filter
    if search_request.beneficiary:
        beneficiary_field = search_request.beneficiary.lower().replace(" ", "_").replace("-", "_")
        if hasattr(Charity, beneficiary_field):
            conditions.append(getattr(Charity, beneficiary_field) == True)
    
    # Website filter
    if search_request.has_website is not None:
        if search_request.has_website:
            conditions.append(Charity.charity_website.isnot(None))
            conditions.append(Charity.charity_website != "")
        else:
            conditions.append(
                or_(
                    Charity.charity_website.is_(None),
                    Charity.charity_website == ""
                )
            )
    
    # Apply conditions (always have at least the unnamed charity filter)
    query = query.where(and_(*conditions))
    
    # Get total count (always exclude unnamed charities)
    count_query = select(func.count(Charity.id))
    count_query = count_query.where(and_(*conditions))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    query = query.offset(search_request.offset).limit(search_request.limit)
    
    # Execute query
    result = await db.execute(query)
    charities = result.scalars().all()
    
    # Convert to response models
    charity_responses = [CharityResponse.model_validate(charity) for charity in charities]
    
    return CharitySearchResponse(
        charities=charity_responses,
        total=total,
        limit=search_request.limit,
        offset=search_request.offset,
        has_more=search_request.offset + search_request.limit < total
    )


async def get_charity_by_id(db: AsyncSession, charity_id: int) -> Optional[CharityResponse]:
    """Get a specific charity by ID."""
    query = select(Charity).where(Charity.id == charity_id)
    result = await db.execute(query)
    charity = result.scalar_one_or_none()
    
    if charity:
        return CharityResponse.model_validate(charity)
    return None


async def get_charity_stats(db: AsyncSession) -> CharityStatsResponse:
    """Get charity statistics."""
    
    # Base condition to exclude unnamed and invalid charities
    base_condition = and_(
        Charity.charity_legal_name.isnot(None),
        Charity.charity_legal_name != "",
        func.length(Charity.charity_legal_name) >= 10,
        ~Charity.charity_legal_name.like('%-%')
    )
    
    # Total charities (excluding unnamed)
    total_query = select(func.count(Charity.id)).where(base_condition)
    total_result = await db.execute(total_query)
    total_charities = total_result.scalar()
    
    # By size
    size_query = select(Charity.charity_size, func.count(Charity.id)).where(base_condition).group_by(Charity.charity_size)
    size_result = await db.execute(size_query)
    by_size = {row[0] or "Unknown": row[1] for row in size_result.fetchall()}
    
    # By state (count charities that operate in each state)
    state_fields = [
        ('ACT', 'operates_in_act'),
        ('NSW', 'operates_in_nsw'),
        ('NT', 'operates_in_nt'),
        ('QLD', 'operates_in_qld'),
        ('SA', 'operates_in_sa'),
        ('TAS', 'operates_in_tas'),
        ('VIC', 'operates_in_vic'),
        ('WA', 'operates_in_wa')
    ]
    
    by_state = {}
    for state, field in state_fields:
        query = select(func.count(Charity.id)).where(
            and_(
                base_condition,
                getattr(Charity, field) == True
            )
        )
        result = await db.execute(query)
        by_state[state] = result.scalar()
    
    # By purpose (count charities with each purpose)
    purpose_fields = [
        ('Education', 'advancing_education'),
        ('Health', 'advancing_health'),
        ('Environment', 'advancing_natural_environment'),
        ('Religion', 'advancing_religion'),
        ('Social Welfare', 'advancing_social_or_public_welfare'),
        ('Culture', 'advancing_culture'),
        ('Human Rights', 'promoting_or_protecting_human_rights'),
        ('Animals', 'preventing_or_relieving_suffering_of_animals')
    ]
    
    by_purpose = {}
    for purpose, field in purpose_fields:
        query = select(func.count(Charity.id)).where(
            and_(
                base_condition,
                getattr(Charity, field) == True
            )
        )
        result = await db.execute(query)
        by_purpose[purpose] = result.scalar()
    
    # By beneficiary (count charities serving each beneficiary group)
    beneficiary_fields = [
        ('Children', 'children'),
        ('Aged Persons', 'aged_persons'),
        ('People with Disabilities', 'people_with_disabilities'),
        ('Families', 'families'),
        ('Youth', 'youth'),
        ('Adults', 'adults'),
        ('Financially Disadvantaged', 'financially_disadvantaged'),
        ('General Community', 'general_community_in_australia')
    ]
    
    by_beneficiary = {}
    for beneficiary, field in beneficiary_fields:
        query = select(func.count(Charity.id)).where(
            and_(
                base_condition,
                getattr(Charity, field) == True
            )
        )
        result = await db.execute(query)
        by_beneficiary[beneficiary] = result.scalar()
    
    return CharityStatsResponse(
        total_charities=total_charities,
        by_size=by_size,
        by_state=by_state,
        by_purpose=by_purpose,
        by_beneficiary=by_beneficiary
    )


async def get_charities_by_location(
    db: AsyncSession, 
    state: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 20
) -> List[CharityResponse]:
    """Get charities by location."""
    
    query = select(Charity)
    conditions = []
    
    if state:
        state_field = f"operates_in_{state.lower()}"
        if hasattr(Charity, state_field):
            conditions.append(getattr(Charity, state_field) == True)
    
    if city:
        conditions.append(Charity.town_city.ilike(f"%{city}%"))
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    charities = result.scalars().all()
    
    return [CharityResponse.model_validate(charity) for charity in charities]
