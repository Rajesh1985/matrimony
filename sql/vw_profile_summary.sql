USE [manamalai];
GO

CREATE VIEW vw_profile_summary AS
SELECT
    p.id,
    p.name,
    p.serial_number,
    p.birth_date,
    p.birth_time,
    p.height_cm,
    p.complexion,
    p.caste,
    p.sub_caste,
    p.mobile_number,
    p.is_active,

    ad.star,
    ad.rasi,
    ad.lagnam,
    ad.birth_place,
    ad.gotram,
    ad.dosham_details,
    ad.horoscope_url,

    fd.father_name,
    fd.father_occupation,
    fd.mother_name,
    fd.mother_occupation,
    fd.total_siblings,
    fd.family_type,

    ed.degree,
    ed.specialization,

    pd.designation,
    pd.company_name,
    pd.monthly_income,
    pd.work_location,

    a.city,
    a.state,
    a.country

FROM profiles p
LEFT JOIN astrology_details ad ON p.id = ad.profile_id
LEFT JOIN family_details fd ON p.id = fd.profile_id
LEFT JOIN education_details ed ON p.id = ed.profile_id
LEFT JOIN professional_details pd ON p.id = pd.profile_id
LEFT JOIN addresses a ON p.id = a.profile_id AND a.is_primary = 1;
GO