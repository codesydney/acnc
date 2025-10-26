import csv
import asyncio
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.charity import Charity
from app.database import async_session


def parse_boolean(value: str) -> bool:
    """Parse boolean values from CSV."""
    if not value or value.strip() == "":
        return False
    return value.strip().upper() == "Y"


def parse_int(value: str) -> Optional[int]:
    """Parse integer values from CSV."""
    if not value or value.strip() == "":
        return None
    try:
        return int(value.strip())
    except ValueError:
        return None


def clean_string(value: str) -> Optional[str]:
    """Clean string values from CSV."""
    if not value or value.strip() == "":
        return None
    return value.strip()


async def import_charity_data(csv_file_path: str) -> None:
    """Import charity data from CSV file."""
    async with async_session() as session:
        # Check if data already exists
        result = await session.execute(select(Charity).limit(1))
        if result.scalar_one_or_none():
            print("Data already exists in database. Skipping import.")
            return
        
        print(f"Starting import from {csv_file_path}...")
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            batch_size = 1000
            batch = []
            total_imported = 0
            
            for row in reader:
                # Map CSV columns to model fields
                charity_data = {
                    'abn': clean_string(row.get('ABN')),
                    'charity_legal_name': clean_string(row.get('Charity_Legal_Name')),
                    'other_organisation_names': clean_string(row.get('Other_Organisation_Names')),
                    'address_type': clean_string(row.get('Address_Type')),
                    'address_line_1': clean_string(row.get('Address_Line_1')),
                    'address_line_2': clean_string(row.get('Address_Line_2')),
                    'address_line_3': clean_string(row.get('Address_Line_3')),
                    'town_city': clean_string(row.get('Town_City')),
                    'state': clean_string(row.get('State')),
                    'postcode': clean_string(row.get('Postcode')),
                    'country': clean_string(row.get('Country')),
                    'charity_website': clean_string(row.get('Charity_Website')),
                    'registration_date': clean_string(row.get('Registration_Date')),
                    'date_organisation_established': clean_string(row.get('Date_Organisation_Established')),
                    'charity_size': clean_string(row.get('Charity_Size')),
                    'number_of_responsible_persons': parse_int(row.get('Number_of_Responsible_Persons')),
                    'financial_year_end': clean_string(row.get('Financial_Year_End')),
                    
                    # State operations
                    'operates_in_act': parse_boolean(row.get('Operates_in_ACT')),
                    'operates_in_nsw': parse_boolean(row.get('Operates_in_NSW')),
                    'operates_in_nt': parse_boolean(row.get('Operates_in_NT')),
                    'operates_in_qld': parse_boolean(row.get('Operates_in_QLD')),
                    'operates_in_sa': parse_boolean(row.get('Operates_in_SA')),
                    'operates_in_tas': parse_boolean(row.get('Operates_in_TAS')),
                    'operates_in_vic': parse_boolean(row.get('Operates_in_VIC')),
                    'operates_in_wa': parse_boolean(row.get('Operates_in_WA')),
                    'operating_countries': clean_string(row.get('Operating_Countries')),
                    
                    # Purpose categories
                    'pbi': parse_boolean(row.get('PBI')),
                    'hpc': parse_boolean(row.get('HPC')),
                    'preventing_or_relieving_suffering_of_animals': parse_boolean(row.get('Preventing_or_relieving_suffering_of_animals')),
                    'advancing_culture': parse_boolean(row.get('Advancing_Culture')),
                    'advancing_education': parse_boolean(row.get('Advancing_Education')),
                    'advancing_health': parse_boolean(row.get('Advancing_Health')),
                    'promote_or_oppose_a_change_to_law': parse_boolean(row.get('Promote_or_oppose_a_change_to_law__government_poll_or_prac')),
                    'advancing_natural_environment': parse_boolean(row.get('Advancing_natual_environment')),
                    'promoting_or_protecting_human_rights': parse_boolean(row.get('Promoting_or_protecting_human_rights')),
                    'purposes_beneficial_to_general_public': parse_boolean(row.get('Purposes_beneficial_to_ther_general_public_and_other_analogous')),
                    'promoting_reconciliation': parse_boolean(row.get('Promoting_reconciliation__mutual_respect_and_tolerance')),
                    'advancing_religion': parse_boolean(row.get('Advancing_Religion')),
                    'advancing_social_or_public_welfare': parse_boolean(row.get('Advancing_social_or_public_welfare')),
                    'advancing_security_or_safety': parse_boolean(row.get('Advancing_security_or_safety_of_Australia_or_Australian_public')),
                    
                    # Beneficiary groups
                    'aboriginal_or_tsi': parse_boolean(row.get('Aboriginal_or_TSI')),
                    'adults': parse_boolean(row.get('Adults')),
                    'aged_persons': parse_boolean(row.get('Aged_Persons')),
                    'children': parse_boolean(row.get('Children')),
                    'communities_overseas': parse_boolean(row.get('Communities_Overseas')),
                    'early_childhood': parse_boolean(row.get('Early_Childhood')),
                    'ethnic_groups': parse_boolean(row.get('Ethnic_Groups')),
                    'families': parse_boolean(row.get('Families')),
                    'females': parse_boolean(row.get('Females')),
                    'financially_disadvantaged': parse_boolean(row.get('Financially_Disadvantaged')),
                    'lgbtiqa_plus': parse_boolean(row.get('LGBTIQA+')),
                    'general_community_in_australia': parse_boolean(row.get('General_Community_in_Australia')),
                    'males': parse_boolean(row.get('Males')),
                    'migrants_refugees_or_asylum_seekers': parse_boolean(row.get('Migrants_Refugees_or_Asylum_Seekers')),
                    'other_beneficiaries': parse_boolean(row.get('Other_Beneficiaries')),
                    'other_charities': parse_boolean(row.get('Other_Charities')),
                    'people_at_risk_of_homelessness': parse_boolean(row.get('People_at_risk_of_homelessness')),
                    'people_with_chronic_illness': parse_boolean(row.get('People_with_Chronic_Illness')),
                    'people_with_disabilities': parse_boolean(row.get('People_with_Disabilities')),
                    'pre_post_release_offenders': parse_boolean(row.get('Pre_Post_Release_Offenders')),
                    'rural_regional_remote_communities': parse_boolean(row.get('Rural_Regional_Remote_Communities')),
                    'unemployed_person': parse_boolean(row.get('Unemployed_Person')),
                    'veterans_or_their_families': parse_boolean(row.get('Veterans_or_their_families')),
                    'victims_of_crime': parse_boolean(row.get('Victims_of_crime')),
                    'victims_of_disasters': parse_boolean(row.get('Victims_of_Disasters')),
                    'youth': parse_boolean(row.get('Youth')),
                    'animals': parse_boolean(row.get('animals')),
                    'environment': parse_boolean(row.get('environment')),
                    'other_gender_identities': parse_boolean(row.get('other_gender_identities')),
                }
                
                # Create charity instance
                charity = Charity(**charity_data)
                batch.append(charity)
                
                # Process batch when it reaches batch_size
                if len(batch) >= batch_size:
                    session.add_all(batch)
                    await session.commit()
                    total_imported += len(batch)
                    print(f"Imported {total_imported} charities...")
                    batch = []
            
            # Process remaining batch
            if batch:
                session.add_all(batch)
                await session.commit()
                total_imported += len(batch)
            
            print(f"Import completed! Total charities imported: {total_imported}")


if __name__ == "__main__":
    asyncio.run(import_charity_data("datadotgov_main.csv"))
