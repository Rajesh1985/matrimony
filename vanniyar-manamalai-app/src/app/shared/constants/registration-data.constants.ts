// src/app/shared/constants/registration-data.constants.ts

export const REGISTRATION_DATA = {
  // Caste options
  CASTE_OPTIONS: [
    { value: 'Vanniyar', label: 'Vanniyar' }
  ],

  // Religion options
  RELIGION_OPTIONS: [
    { value: 'Hindu', label: 'Hindu' }
  ],

  // Gender options (from user table)
  GENDER_OPTIONS: [
    { value: 'Male', label: 'Male' },
    { value: 'Female', label: 'Female' },
  ],

  // Physical status (radio)
  PHYSICAL_STATUS_OPTIONS: [
    { value: 'Normal', label: 'Normal' },
    { value: 'Physically Challenged', label: 'Physically Challenged' }
  ],

  // Marital status (radio)
  MARITAL_STATUS_OPTIONS: [
    { value: 'Unmarried', label: 'Never Married' },
    { value: 'Divorced', label: 'Divorced' },
    { value: 'Widow_Widower', label: 'Widow / Widower' },
    { value: 'Separated', label: 'Separated' }
  ],

  // Food preference (radio)
  FOOD_PREFERENCE_OPTIONS: [
    { value: 'Veg', label: 'Vegetarian' },
    { value: 'NonVeg', label: 'Non-Vegetarian' }
  ],

  // Complexion (radio)
  COMPLEXION_OPTIONS: [
    { value: 'Fair', label: 'Fair' },
    { value: 'Light Brown', label: 'Light Brown' },
    { value: 'Brown', label: 'Brown' },
    { value: 'Dark', label: 'Dark' }
  ],

  // Family type (dropdown)
  FAMILY_TYPE_OPTIONS: [
    { value: 'joint', label: 'Joint Family' },
    { value: 'nuclear', label: 'Nuclear Family' },
    { value: 'extended', label: 'Extended Family' }
  ],

  // Family status (dropdown)
  FAMILY_STATUS_OPTIONS: [
    { value: 'Upper_Middle_Class', label: 'Upper Middle Class' },
    { value: 'Middle_Class', label: 'Middle Class' },
    { value: 'Rich_Elite', label: 'Rich/Elite' }
  ],

  // Astrology - Star/Nakshatra
  STAR_OPTIONS: [
    { value: 'Ashwini', label: 'Ashwini' },
    { value: 'Bharani', label: 'Bharani' },
    { value: 'Krittika', label: 'Krittika' },
    { value: 'Rohini', label: 'Rohini' },
    { value: 'Mrigashirsha', label: 'Mrigashirsha' },
    { value: 'Arudra', label: 'Arudra' },
    { value: 'Punarvasu', label: 'Punarvasu' },
    { value: 'Pushya', label: 'Pushya' },
    { value: 'Ashlesha', label: 'Ashlesha' },
    { value: 'Magha', label: 'Magha' },
    { value: 'Purva_Phalguni', label: 'Purva Phalguni' },
    { value: 'Uttara_Phalguni', label: 'Uttara Phalguni' },
    { value: 'Hastha', label: 'Hastha' },
    { value: 'Chitra', label: 'Chitra' },
    { value: 'Swati', label: 'Swati' },
    { value: 'Vishakha', label: 'Vishakha' },
    { value: 'Anuradha', label: 'Anuradha' },
    { value: 'Jyeshtha', label: 'Jyeshtha' },
    { value: 'Mula', label: 'Mula' },
    { value: 'Purva_Ashadha', label: 'Purva Ashadha' },
    { value: 'Uttara_Ashadha', label: 'Uttara Ashadha' },
    { value: 'Shravana', label: 'Shravana' },
    { value: 'Dhanishta', label: 'Dhanishta' },
    { value: 'Shatabhisha', label: 'Shatabhisha' },
    { value: 'Purva_Bhadrapada', label: 'Purva Bhadrapada' },
    { value: 'Uttara_Bhadrapada', label: 'Uttara Bhadrapada' },
    { value: 'Revati', label: 'Revati' }
  ],

  // Astrology - Rasi/Zodiac
  RASI_OPTIONS: [
    { value: 'Aries', label: 'Aries' },
    { value: 'Taurus', label: 'Taurus' },
    { value: 'Gemini', label: 'Gemini' },
    { value: 'Cancer', label: 'Cancer' },
    { value: 'Leo', label: 'Leo' },
    { value: 'Virgo', label: 'Virgo' },
    { value: 'Libra', label: 'Libra' },
    { value: 'Scorpio', label: 'Scorpio' },
    { value: 'Sagittarius', label: 'Sagittarius' },
    { value: 'Capricorn', label: 'Capricorn' },
    { value: 'Aquarius', label: 'Aquarius' },
    { value: 'Pisces', label: 'Pisces' }
  ],

  // Astrology - Kotturam (Jumbo Maha Rishi only)
  KOTTURAM_OPTIONS: [
    { value: 'Jumbo_Maha_Rishi', label: 'Jumbo Maha Rishi' }
  ],

  // Professional - Education
  EDUCATION_OPTIONS: [
    { value: 'High School', label: 'High School' },
    { value: 'Diploma', label: 'Diploma' },
    { value: 'Bachelor Degree', label: 'Bachelor Degree' },
    { value: 'Master Degree', label: 'Master Degree' },
    { value: 'PhD', label: 'PhD' },
    { value: 'Engineering', label: 'Engineering' },
    { value: 'Medical', label: 'Medical' },
    { value: 'Law', label: 'Law' },
    { value: 'Commerce', label: 'Commerce' },
    { value: 'Arts', label: 'Arts' },
    { value: 'Science', label: 'Science' },
    { value: 'Computer Science', label: 'Computer Science' },
    { value: 'Others', label: 'Others' }
  ],

  // Professional - Employment type
  EMPLOYMENT_TYPE_OPTIONS: [
    { value: 'Private', label: 'Private' },
    { value: 'Business', label: 'Business' },
    { value: 'Defence', label: 'Defence' },
    { value: 'Government/PSU', label: 'Government/PSU' },
    { value: 'Self Employed', label: 'Self Employed' },
    { value: 'Not Working', label: 'Not Working' }
  ],

  // Professional - Annual income ranges
  ANNUAL_INCOME_OPTIONS: [
    { value: '1-5 LPA', label: '>= 1 Lakh' },
    { value: '5-10 LPA', label: '1 Lakh to 5 Lakh' },
    { value: '10-15 LPA', label: '5 Lakh to 10 Lakh' },
    { value: '15-20 LPA', label: '10 Lakh to 15 Lakh' },
    { value: '20-30 LPA', label: '15 Lakh to 20 Lakh' },
    { value: '30-50 LPA', label: '20 Lakh to 30 Lakh' },
    { value: '50+ LPA', label: '50 Lakh+' }
  ],

  // Professional - Occupation
  OCCUPATION_OPTIONS: [
    { value: 'Engineer', label: 'Engineer' },
    { value: 'Doctor', label: 'Doctor' },
    { value: 'Teacher', label: 'Teacher' },
    { value: 'Software Developer', label: 'Software Developer' },
    { value: 'Manager', label: 'Manager' },
    { value: 'Business Owner', label: 'Business Owner' },
    { value: 'Lawyer', label: 'Lawyer' },
    { value: 'Accountant', label: 'Accountant' },
    { value: 'Government Employee', label: 'Government Employee' },
    { value: 'Bank Employee', label: 'Bank Employee' },
    { value: 'Consultant', label: 'Consultant' },
    { value: 'Entrepreneur', label: 'Entrepreneur' },
    { value: 'Freelancer', label: 'Freelancer' },
    { value: 'Architect', label: 'Architect' },
    { value: 'Pharmacist', label: 'Pharmacist' },
    { value: 'Nurse', label: 'Nurse' },
    { value: 'Professor', label: 'Professor' },
    { value: 'Scientist', label: 'Scientist' },
    { value: 'Others', label: 'Others' }
  ],

  // Professional - Work Location
  WORK_LOCATION_OPTIONS: [
    { value: 'Chennai', label: 'Chennai' },
    { value: 'Bangalore', label: 'Bangalore' },
    { value: 'Hyderabad', label: 'Hyderabad' },
    { value: 'Mumbai', label: 'Mumbai' },
    { value: 'Delhi', label: 'Delhi' },
    { value: 'Pune', label: 'Pune' },
    { value: 'Coimbatore', label: 'Coimbatore' },
    { value: 'Madurai', label: 'Madurai' },
    { value: 'USA', label: 'USA' },
    { value: 'UK', label: 'UK' },
    { value: 'Canada', label: 'Canada' },
    { value: 'Australia', label: 'Australia' },
    { value: 'Singapore', label: 'Singapore' },
    { value: 'UAE', label: 'UAE' },
    { value: 'Germany', label: 'Germany' },
    { value: 'Others', label: 'Others' }
  ]
};

// Cascading location data
export const LOCATION_DATA: { [country: string]: { [state: string]: string[] } } = {
  'India': {
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruppur', 'Erode', 'Vellore', 'Kanyakumari'],
    'Karnataka': ['Bangalore', 'Mysore', 'Mangalore', 'Belgaum', 'Hubballi', 'Davangere'],
    'Andhra Pradesh': ['Hyderabad', 'Visakhapatnam', 'Vijayawada', 'Tirupati', 'Nellore'],
    'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Aurangabad', 'Nashik', 'Kolhapur'],
    'Delhi': ['New Delhi', 'Delhi', 'Noida', 'Ghaziabad'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Allahabad'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Jamnagar'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Ajmer', 'Bikaner', 'Udaipur'],
    'West Bengal': ['Kolkata', 'Siliguri', 'Durgapur', 'Asansol']
  },
  'USA': {
    'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
    'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
    'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany'],
    'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
    'Illinois': ['Chicago', 'Springfield', 'Peoria']
  },
  'UK': {
    'England': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Liverpool'],
    'Scotland': ['Edinburgh', 'Glasgow', 'Aberdeen'],
    'Wales': ['Cardiff', 'Swansea', 'Newport']
  },
  'Canada': {
    'Ontario': ['Toronto', 'Ottawa', 'Hamilton'],
    'Quebec': ['Montreal', 'Quebec City'],
    'British Columbia': ['Vancouver', 'Victoria'],
    'Alberta': ['Calgary', 'Edmonton']
  },
  'Australia': {
    'New South Wales': ['Sydney', 'Newcastle', 'Wollongong'],
    'Victoria': ['Melbourne', 'Ballarat', 'Bendigo'],
    'Queensland': ['Brisbane', 'Gold Coast', 'Cairns'],
    'Western Australia': ['Perth', 'Fremantle']
  }
};
