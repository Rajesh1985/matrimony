-- Sample data insertion based on provided information
INSERT INTO profiles (
    serial_number, name, birth_date, star, rasi, lagnam, dosham, 
    height_cm, complexion, caste, sub_caste, education, occupation, 
    monthly_income_rs, father_name, mother_name, siblings, address, 
    property_details, expectations, mobile_number, compatible_stars, 
    introducer_name, introducer_mobile
) VALUES (
    '1', 
    'S. Deepalakshmi', 
    '1997-07-15', 
    'Visagam', 
    'Thulam', 
    NULL, 
    'இல்லை',
    167, 
    'Fair', 
    'இந்து வன்னிய குலசத்திரியர்', 
    NULL,
    'B.Tech Water and Environment, Strasbourg, France; M.Tech Water and Environment, Hanoi University, Vietnam @ France',
    'Fonctionnaire Charge de mission "Biometal" La Defense, Paris, France',
    500000.00,
    'Dr. K. R. Sundaravaradarajan (VICE CHANCELLOR)',
    'Prof. S. Sarala Dept. of Maths, Paris (France)',
    'Brother 1',
    '25, Vinayagar Street, MGR Nagar, Marapallam. Puducherry, (7 Rue-Eric Tabaraly, 91300 MASSY, France, Paris)',
    'நேரில்',
    'Good Family',
    '8778185513',
    'Refre Jathagam',
    'R. உமாபதி',
    '9789705519'
);

-- Sample membership plans data
INSERT INTO membership_plans (plan_name, plan_type, duration_months, price, features, contact_limit, photo_limit, priority_listing, horoscope_matching, profile_highlighting) VALUES
('Basic Plan', 'basic', 3, 999.00, 'Basic profile listing, limited contacts', 10, 1, FALSE, FALSE, FALSE),
('Premium Plan', 'premium', 6, 2999.00, 'Enhanced profile, more contacts, photo gallery', 50, 5, TRUE, TRUE, FALSE),
('Gold Plan', 'gold', 12, 4999.00, 'Priority listing, unlimited contacts, horoscope matching', 0, 10, TRUE, TRUE, TRUE),
('Platinum Plan', 'platinum', 24, 8999.00, 'VIP treatment, personalized service, unlimited features', 0, 20, TRUE, TRUE, TRUE);

-- Sample subscription for the profile
INSERT INTO member_subscriptions (
    profile_id, membership_plan_id, subscription_number, start_date, end_date, 
    payment_amount, payment_method, payment_date, status, created_by, notes
) VALUES (
    1, 2, 'SUB-2025-001', '2025-06-01', '2025-12-01', 
    2999.00, 'online', '2025-06-01', 'active', 'Admin', 'Initial subscription'
);
