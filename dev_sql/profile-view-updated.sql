-- SQL VIEW for Complete User Profile Data (UPDATED - No Address Table)
-- This view merges all tables to provide complete profile information for display and matching

CREATE OR REPLACE VIEW vw_user_profiles_complete AS
SELECT 
  -- User Info
  u.id AS user_id,
  u.name,
  u.email_id,
  u.mobile,
  u.gender,
  u.country_code,
  u.is_verified,
  
  -- Profile Info (including address fields now in profiles table)
  p.id AS profile_id,
  p.serial_number,
  p.caste,
  p.religion,
  p.height_cm,
  p.birth_date,
  p.birth_time,
  p.country,
  p.state,
  p.city,
  p.physical_status,
  p.marital_status,
  p.food_preference,
  p.complexion,
  p.hobbies,
  p.about_me,
  p.address_line1,
  p.address_line2,
  p.postal_code,
  p.created_at AS profile_created_at,
  p.updated_at AS profile_updated_at,
  
  -- Astrology Info
  ast.star,
  ast.rasi,
  ast.lagnam,
  ast.birth_place,
  ast.dosham_details,
  ast.file_id AS astrology_file_id,
  
  -- Professional Info
  prof.education,
  prof.education_optional,
  prof.employment_type,
  prof.occupation,
  prof.company_name,
  prof.annual_income,
  prof.work_location,
  
  -- Family Info
  fam.father_name,
  fam.father_occupation,
  fam.mother_name,
  fam.mother_occupation,
  fam.family_type,
  fam.family_status,
  fam.brothers,
  fam.sisters,
  fam.married_brothers,
  fam.married_sisters,
  fam.family_description,
  fam.community_file_id,
  fam.photo_file_id_1,
  fam.photo_file_id_2,
  
  -- Partner Preferences Info
  pp.age_from,
  pp.age_to,
  pp.height_from,
  pp.height_to,
  pp.education_preference,
  pp.occupation_preference,
  pp.income_preference,
  pp.location_preference,
  pp.star_preference,
  pp.rasi_preference,
  
  -- Calculate age from birth_date
  YEAR(CURDATE()) - YEAR(p.birth_date) - (DATE_FORMAT(p.birth_date, '%m%d') > DATE_FORMAT(CURDATE(), '%m%d')) AS age
  
FROM Users u
LEFT JOIN profiles p ON u.profile_id = p.id
LEFT JOIN astrology_details ast ON p.id = ast.profile_id
LEFT JOIN professional_details prof ON p.id = prof.profile_id
LEFT JOIN family_details fam ON p.id = fam.profile_id
LEFT JOIN partner_preferences pp ON p.id = pp.profile_id
WHERE p.id IS NOT NULL;

-- Indexes for optimal query performance
CREATE INDEX idx_vw_profiles_user_id ON Users(id);
CREATE INDEX idx_vw_profiles_profile_id ON profiles(id);
CREATE INDEX idx_vw_profiles_birth_date ON profiles(birth_date);
CREATE INDEX idx_vw_profiles_gender ON Users(gender);
CREATE INDEX idx_vw_profiles_city ON profiles(city);
CREATE INDEX idx_vw_profiles_partner_prefs ON partner_preferences(profile_id);


-- VIEW for Profile Recommendations
-- This view helps filter profiles based on partner preferences with match scoring
-- Using GROUP BY to eliminate duplicate rows from LEFT JOINs in base view

CREATE OR REPLACE VIEW vw_profile_recommendations AS
SELECT 
  cp.profile_id AS current_profile_id,
  cp.user_id AS current_user_id,
  mp.profile_id AS match_profile_id,
  mp.user_id AS match_user_id,
  MAX(mp.serial_number) AS serial_number,
  MAX(mp.name) AS name,
  MAX(mp.age) AS age,
  MAX(mp.height_cm) AS height_cm,
  MAX(mp.gender) AS gender,
  MAX(mp.occupation) AS occupation,
  MAX(mp.star) AS star,
  MAX(mp.rasi) AS rasi,
  MAX(mp.city) AS city,
  MAX(mp.state) AS state,
  MAX(mp.country) AS country,
  MAX(mp.about_me) AS about_me,
  MAX(mp.photo_file_id_1) AS photo_file_id_1,
  MAX(mp.photo_file_id_2) AS photo_file_id_2,
  
  -- Calculate match score (0-8)
  MAX(
    CASE 
      WHEN mp.age BETWEEN cp.age_from AND cp.age_to THEN 1 ELSE 0 
    END +
    CASE 
      WHEN mp.height_cm BETWEEN cp.height_from AND cp.height_to THEN 1 ELSE 0 
    END +
    CASE 
      WHEN cp.education_preference IS NOT NULL 
        AND FIND_IN_SET(mp.education, cp.education_preference) > 0 THEN 1 ELSE 0 
    END +
    CASE 
      WHEN cp.occupation_preference IS NOT NULL 
        AND FIND_IN_SET(mp.employment_type, cp.occupation_preference) > 0 THEN 1 ELSE 0 
    END +
    CASE 
      WHEN cp.income_preference IS NOT NULL 
        AND FIND_IN_SET(mp.annual_income, cp.income_preference) > 0 THEN 1 ELSE 0 
    END +
    CASE 
      WHEN cp.location_preference IS NOT NULL 
        AND FIND_IN_SET(mp.city, cp.location_preference) > 0 THEN 1 ELSE 0 
    END +
    CASE 
      WHEN cp.star_preference IS NOT NULL 
        AND FIND_IN_SET(mp.star, cp.star_preference) > 0 THEN 1 ELSE 0 
    END +
    CASE 
      WHEN cp.rasi_preference IS NOT NULL 
        AND FIND_IN_SET(mp.rasi, cp.rasi_preference) > 0 THEN 1 ELSE 0 
    END
  ) AS match_score
  
FROM vw_user_profiles_complete cp
JOIN vw_user_profiles_complete mp 
  ON cp.profile_id != mp.profile_id 
  AND cp.user_id != mp.user_id
WHERE (cp.gender = 'Female' AND mp.gender = 'Male')
   OR (cp.gender = 'Male' AND mp.gender = 'Female')
GROUP BY cp.profile_id, cp.user_id, mp.profile_id, mp.user_id;

-- Query usage example:
-- SELECT * FROM vw_profile_recommendations 
-- WHERE current_user_id = 123 
-- ORDER BY match_score DESC, preferences_updated_at DESC 
-- LIMIT 20;
