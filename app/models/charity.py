from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime


class CharityBase(SQLModel):
    """Base charity model with common fields."""
    abn: Optional[str] = Field(default=None, max_length=11)
    charity_legal_name: Optional[str] = Field(default=None, max_length=500)
    other_organisation_names: Optional[str] = Field(default=None, max_length=500)
    address_type: Optional[str] = Field(default=None, max_length=50)
    address_line_1: Optional[str] = Field(default=None, max_length=200)
    address_line_2: Optional[str] = Field(default=None, max_length=200)
    address_line_3: Optional[str] = Field(default=None, max_length=200)
    town_city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=10)
    postcode: Optional[str] = Field(default=None, max_length=10)
    country: Optional[str] = Field(default=None, max_length=50)
    charity_website: Optional[str] = Field(default=None, max_length=500)
    registration_date: Optional[str] = Field(default=None, max_length=20)
    date_organisation_established: Optional[str] = Field(default=None, max_length=20)
    charity_size: Optional[str] = Field(default=None, max_length=20)
    number_of_responsible_persons: Optional[int] = Field(default=None)
    financial_year_end: Optional[str] = Field(default=None, max_length=20)
    
    # State operations
    operates_in_act: Optional[bool] = Field(default=False)
    operates_in_nsw: Optional[bool] = Field(default=False)
    operates_in_nt: Optional[bool] = Field(default=False)
    operates_in_qld: Optional[bool] = Field(default=False)
    operates_in_sa: Optional[bool] = Field(default=False)
    operates_in_tas: Optional[bool] = Field(default=False)
    operates_in_vic: Optional[bool] = Field(default=False)
    operates_in_wa: Optional[bool] = Field(default=False)
    operating_countries: Optional[str] = Field(default=None, max_length=200)
    
    # Purpose categories
    pbi: Optional[bool] = Field(default=False)
    hpc: Optional[bool] = Field(default=False)
    preventing_or_relieving_suffering_of_animals: Optional[bool] = Field(default=False)
    advancing_culture: Optional[bool] = Field(default=False)
    advancing_education: Optional[bool] = Field(default=False)
    advancing_health: Optional[bool] = Field(default=False)
    promote_or_oppose_a_change_to_law: Optional[bool] = Field(default=False)
    advancing_natural_environment: Optional[bool] = Field(default=False)
    promoting_or_protecting_human_rights: Optional[bool] = Field(default=False)
    purposes_beneficial_to_general_public: Optional[bool] = Field(default=False)
    promoting_reconciliation: Optional[bool] = Field(default=False)
    advancing_religion: Optional[bool] = Field(default=False)
    advancing_social_or_public_welfare: Optional[bool] = Field(default=False)
    advancing_security_or_safety: Optional[bool] = Field(default=False)
    
    # Beneficiary groups
    aboriginal_or_tsi: Optional[bool] = Field(default=False)
    adults: Optional[bool] = Field(default=False)
    aged_persons: Optional[bool] = Field(default=False)
    children: Optional[bool] = Field(default=False)
    communities_overseas: Optional[bool] = Field(default=False)
    early_childhood: Optional[bool] = Field(default=False)
    ethnic_groups: Optional[bool] = Field(default=False)
    families: Optional[bool] = Field(default=False)
    females: Optional[bool] = Field(default=False)
    financially_disadvantaged: Optional[bool] = Field(default=False)
    lgbtiqa_plus: Optional[bool] = Field(default=False)
    general_community_in_australia: Optional[bool] = Field(default=False)
    males: Optional[bool] = Field(default=False)
    migrants_refugees_or_asylum_seekers: Optional[bool] = Field(default=False)
    other_beneficiaries: Optional[bool] = Field(default=False)
    other_charities: Optional[bool] = Field(default=False)
    people_at_risk_of_homelessness: Optional[bool] = Field(default=False)
    people_with_chronic_illness: Optional[bool] = Field(default=False)
    people_with_disabilities: Optional[bool] = Field(default=False)
    pre_post_release_offenders: Optional[bool] = Field(default=False)
    rural_regional_remote_communities: Optional[bool] = Field(default=False)
    unemployed_person: Optional[bool] = Field(default=False)
    veterans_or_their_families: Optional[bool] = Field(default=False)
    victims_of_crime: Optional[bool] = Field(default=False)
    victims_of_disasters: Optional[bool] = Field(default=False)
    youth: Optional[bool] = Field(default=False)
    animals: Optional[bool] = Field(default=False)
    environment: Optional[bool] = Field(default=False)
    other_gender_identities: Optional[bool] = Field(default=False)


class Charity(CharityBase, table=True):
    """Charity database model."""
    __tablename__ = "charities"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CharityResponse(CharityBase):
    """Charity response model for API."""
    id: int
    created_at: datetime
    updated_at: datetime


class CharitySearchRequest(SQLModel):
    """Charity search request model."""
    query: Optional[str] = Field(default=None, max_length=200)
    state: Optional[str] = Field(default=None, max_length=10)
    charity_size: Optional[str] = Field(default=None, max_length=20)
    purpose: Optional[str] = Field(default=None, max_length=100)
    beneficiary: Optional[str] = Field(default=None, max_length=100)
    has_website: Optional[bool] = Field(default=None)
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class CharitySearchResponse(SQLModel):
    """Charity search response model."""
    charities: List[CharityResponse]
    total: int
    limit: int
    offset: int
    has_more: bool


class CharityStatsResponse(SQLModel):
    """Charity statistics response model."""
    total_charities: int
    by_size: dict
    by_state: dict
    by_purpose: dict
    by_beneficiary: dict
