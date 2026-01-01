from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional

def get_profiles_complete(db: Session, profile_id: int) -> Optional[dict]:
    """
    Get complete profile with all related information from vw_user_profiles_complete view
    
    Args:
        db: Database session
        profile_id: The profile ID to retrieve
    
    Returns:
        Dictionary containing complete profile data or None if not found
    
    Example:
        profile = get_profiles_complete(db, profile_id=1)
    """
    query = """
    SELECT 
        user_id, name, email_id, mobile, gender, country_code, is_verified,
        profile_id, serial_number, caste, religion, height_cm, birth_date,
        country, state, city, physical_status, marital_status, food_preference,
        complexion, hobbies, about_me, address_line1, address_line2, postal_code,
        profile_created_at, profile_updated_at,
        star, rasi, lagnam, birth_place, dosham_details, astrology_file_id,
        education, education_optional, employment_type, occupation, company_name,
        annual_income, work_location,
        father_name, father_occupation, mother_name, mother_occupation,
        family_type, family_status, brothers, sisters, married_brothers, married_sisters,
        family_description, community_file_id, photo_file_id_1, photo_file_id_2,
        age_from, age_to, height_from, height_to, education_preference,
        occupation_preference, income_preference, location_preference,
        star_preference, rasi_preference, age,
        plan_name, start_date, end_date
    FROM vw_user_profiles_complete
    WHERE profile_id = :profile_id
    """
    
    result = db.execute(text(query), {"profile_id": profile_id}).fetchone()
    
    if not result:
        return None
    
    # Convert row to dictionary
    columns = [
        'user_id', 'name', 'email_id', 'mobile', 'gender', 'country_code', 'is_verified',
        'profile_id', 'serial_number', 'caste', 'religion', 'height_cm', 'birth_date',
        'country', 'state', 'city', 'physical_status', 'marital_status', 'food_preference',
        'complexion', 'hobbies', 'about_me', 'address_line1', 'address_line2', 'postal_code',
        'profile_created_at', 'profile_updated_at',
        'star', 'rasi', 'lagnam', 'birth_place', 'dosham_details', 'astrology_file_id',
        'education', 'education_optional', 'employment_type', 'occupation', 'company_name',
        'annual_income', 'work_location',
        'father_name', 'father_occupation', 'mother_name', 'mother_occupation',
        'family_type', 'family_status', 'brothers', 'sisters', 'married_brothers', 'married_sisters',
        'family_description', 'community_file_id', 'photo_file_id_1', 'photo_file_id_2',
        'age_from', 'age_to', 'height_from', 'height_to', 'education_preference',
        'occupation_preference', 'income_preference', 'location_preference',
        'star_preference', 'rasi_preference', 'age',
        'plan_name', 'start_date', 'end_date'
    ]
    
    return dict(zip(columns, result))


def get_all_profiles_complete(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all complete profiles with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of dictionaries containing complete profile data
    
    Example:
        profiles = get_all_profiles_complete(db, skip=0, limit=20)
    """
    query = """
    SELECT 
        user_id, name, email_id, mobile, gender, country_code, is_verified,
        profile_id, serial_number, caste, religion, height_cm, birth_date, birth_time,
        country, state, city, physical_status, marital_status, food_preference,
        complexion, hobbies, about_me, address_line1, address_line2, postal_code,
        profile_created_at, profile_updated_at,
        star, rasi, lagnam, birth_place, dosham_details, astrology_file_id,
        education, education_optional, employment_type, occupation, company_name,
        annual_income, work_location,
        father_name, father_occupation, mother_name, mother_occupation,
        family_type, family_status, brothers, sisters, married_brothers, married_sisters,
        family_description, community_file_id, photo_file_id_1, photo_file_id_2,
        age_from, age_to, height_from, height_to, education_preference,
        occupation_preference, income_preference, location_preference,
        star_preference, rasi_preference, age,
        plan_name, start_date, end_date
    FROM vw_user_profiles_complete
    ORDER BY profile_id DESC
    LIMIT :limit OFFSET :skip
    """
    
    results = db.execute(text(query), {"limit": limit, "skip": skip}).fetchall()
    
    columns = [
        'user_id', 'name', 'email_id', 'mobile', 'gender', 'country_code', 'is_verified',
        'profile_id', 'serial_number', 'caste', 'religion', 'height_cm', 'birth_date', 'birth_time',
        'country', 'state', 'city', 'physical_status', 'marital_status', 'food_preference',
        'complexion', 'hobbies', 'about_me', 'address_line1', 'address_line2', 'postal_code',
        'profile_created_at', 'profile_updated_at',
        'star', 'rasi', 'lagnam', 'birth_place', 'dosham_details', 'astrology_file_id',
        'education', 'education_optional', 'employment_type', 'occupation', 'company_name',
        'annual_income', 'work_location',
        'father_name', 'father_occupation', 'mother_name', 'mother_occupation',
        'family_type', 'family_status', 'brothers', 'sisters', 'married_brothers', 'married_sisters',
        'family_description', 'community_file_id', 'photo_file_id_1', 'photo_file_id_2',
        'age_from', 'age_to', 'height_from', 'height_to', 'education_preference',
        'occupation_preference', 'income_preference', 'location_preference',
        'star_preference', 'rasi_preference', 'age',
        'plan_name', 'start_date', 'end_date'
    ]
    
    return [dict(zip(columns, row)) for row in results]

def get_recommended_profiles(db: Session, profile_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get recommended profiles based on partner preferences of a specific profile
    Uses vw_profile_recommendations view with match scoring
    
    Args:
        db: Database session
        profile_id: The profile ID to get recommendations for
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of dictionaries containing recommended profile data with match scores and photo file IDs
    
    Example:
        recommendations = get_recommended_profiles(db, profile_id=4, limit=20)
    """
    query = """
    SELECT 
        current_profile_id, current_user_id, 
        match_profile_id, match_user_id, serial_number, name, age, height_cm, gender, 
        occupation, star, rasi, city, state, country, about_me, 
        photo_file_id_1, photo_file_id_2, match_score
    FROM vw_profile_recommendations
    WHERE current_profile_id = :profile_id
    ORDER BY match_score DESC, match_profile_id DESC
    LIMIT :limit OFFSET :skip
    """

    results = db.execute(text(query), {"profile_id": profile_id, "limit": limit, "skip": skip}).fetchall()

    columns = [
        'current_profile_id', 'current_user_id', 
        'match_profile_id', 'match_user_id', 'serial_number', 'name', 'age', 'height_cm', 'gender', 
        'occupation', 'star', 'rasi', 'city', 'state', 'country', 'about_me', 
        'photo_file_id_1', 'photo_file_id_2', 'match_score'
    ]

    return [dict(zip(columns, row)) for row in results]

def get_profiles_complete_by_city(db: Session, city: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get complete profiles filtered by city
    
    Args:
        db: Database session
        city: City name to filter by
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of dictionaries containing complete profile data for specified city
    
    Example:
        profiles = get_profiles_complete_by_city(db, city="Chennai", limit=10)
    """
    query = """
    SELECT 
        user_id, name, email_id, mobile, gender, country_code, is_verified,
        profile_id, serial_number, caste, religion, height_cm, birth_date, birth_time,
        country, state, city, physical_status, marital_status, food_preference,
        complexion, hobbies, about_me, address_line1, address_line2, postal_code,
        profile_created_at, profile_updated_at,
        star, rasi, lagnam, birth_place, dosham_details,
        education, education_optional, employment_type, occupation, company_name,
        annual_income, work_location,
        father_name, father_occupation, mother_name, mother_occupation,
        family_type, family_status, brothers, sisters, married_brothers, married_sisters,
        family_description,
        age_from, age_to, height_from, height_to, education_preference,
        occupation_preference, income_preference, location_preference,
        star_preference, rasi_preference, age,
        plan_name, start_date, end_date
    FROM vw_user_profiles_complete
    WHERE city = :city
    ORDER BY profile_id DESC
    LIMIT :limit OFFSET :skip
    """
    
    results = db.execute(text(query), {"city": city, "limit": limit, "skip": skip}).fetchall()
    
    columns = [
        'user_id', 'name', 'email_id', 'mobile', 'gender', 'country_code', 'is_verified',
        'profile_id', 'serial_number', 'caste', 'religion', 'height_cm', 'birth_date', 'birth_time',
        'country', 'state', 'city', 'physical_status', 'marital_status', 'food_preference',
        'complexion', 'hobbies', 'about_me', 'address_line1', 'address_line2', 'postal_code',
        'profile_created_at', 'profile_updated_at',
        'star', 'rasi', 'lagnam', 'birth_place', 'dosham_details',
        'education', 'education_optional', 'employment_type', 'occupation', 'company_name',
        'annual_income', 'work_location',
        'father_name', 'father_occupation', 'mother_name', 'mother_occupation',
        'family_type', 'family_status', 'brothers', 'sisters', 'married_brothers', 'married_sisters',
        'family_description',
        'age_from', 'age_to', 'height_from', 'height_to', 'education_preference',
        'occupation_preference', 'income_preference', 'location_preference',
        'star_preference', 'rasi_preference', 'age',
        'plan_name', 'start_date', 'end_date'
    ]
    
    return [dict(zip(columns, row)) for row in results]


def get_profiles_complete_by_gender(db: Session, gender: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get complete profiles filtered by gender
    
    Args:
        db: Database session
        gender: Gender value ('Male' or 'Female' or 'Other')
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of dictionaries containing complete profile data for specified gender
    
    Example:
        profiles = get_profiles_complete_by_gender(db, gender="Female", limit=10)
    """
    query = """
    SELECT 
        user_id, name, email_id, mobile, gender, country_code, is_verified,
        profile_id, serial_number, caste, religion, height_cm, birth_date, birth_time,
        country, state, city, physical_status, marital_status, food_preference,
        complexion, hobbies, about_me, address_line1, address_line2, postal_code,
        profile_created_at, profile_updated_at,
        star, rasi, lagnam, birth_place, dosham_details,
        education, education_optional, employment_type, occupation, company_name,
        annual_income, work_location,
        father_name, father_occupation, mother_name, mother_occupation,
        family_type, family_status, brothers, sisters, married_brothers, married_sisters,
        family_description,
        age_from, age_to, height_from, height_to, education_preference,
        occupation_preference, income_preference, location_preference,
        star_preference, rasi_preference, age,
        plan_name, start_date, end_date
    FROM vw_user_profiles_complete
    WHERE gender = :gender
    ORDER BY profile_id DESC
    LIMIT :limit OFFSET :skip
    """
    
    results = db.execute(text(query), {"gender": gender, "limit": limit, "skip": skip}).fetchall()
    
    columns = [
        'user_id', 'name', 'email_id', 'mobile', 'gender', 'country_code', 'is_verified',
        'profile_id', 'serial_number', 'caste', 'religion', 'height_cm', 'birth_date', 'birth_time',
        'country', 'state', 'city', 'physical_status', 'marital_status', 'food_preference',
        'complexion', 'hobbies', 'about_me', 'address_line1', 'address_line2', 'postal_code',
        'profile_created_at', 'profile_updated_at',
        'star', 'rasi', 'lagnam', 'birth_place', 'dosham_details',
        'education', 'education_optional', 'employment_type', 'occupation', 'company_name',
        'annual_income', 'work_location',
        'father_name', 'father_occupation', 'mother_name', 'mother_occupation',
        'family_type', 'family_status', 'brothers', 'sisters', 'married_brothers', 'married_sisters',
        'family_description',
        'age_from', 'age_to', 'height_from', 'height_to', 'education_preference',
        'occupation_preference', 'income_preference', 'location_preference',
        'star_preference', 'rasi_preference', 'age',
        'plan_name', 'start_date', 'end_date'
    ]
    
    return [dict(zip(columns, row)) for row in results]
