-- Create new database
CREATE DATABASE IF NOT EXISTS manamalai_dev;

-- Use the new database
USE manamalai_dev;

-- astrology_details table (rasi and star as ENUMs, gotram renamed to Kotturam, removed horoscope_url, added file_id)
CREATE TABLE astrology_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    star ENUM(
        'Ashwini','Bharani','Krittika','Rohini','Arudra','Punarvasu','Pushya','Ashlesha',
        'Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishakha',
        'Anuradha','Jyeshtha','Mula','Purva Ashadha','Uttara Ashadha','Shravana',
        'Dhanishta','Shatabhisha','Purva Bhadrapada','Uttara Bhadrapada','Revati'
    ),
    rasi ENUM(
        'Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio',
        'Sagittarius','Capricorn','Aquarius','Pisces'
    ),
    lagnam VARCHAR(100),
    birth_place VARCHAR(100),
    Kotturam ENUM('Jumbo_Maha_Rishi'),
    dosham_details TEXT,
    file_id CHAR(36),
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE SET NULL,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- UI display mapping (for reference)
-- rasi UI mapping:
-- மேஷம்/Aries, ரிஷபம்/Taurus, மிதுனம்/Gemini, கடகம்/Cancer, சிம்மம்/Leo, கன்னி/Virgo,
-- துலாம்/Libra, விருச்சிகம்/Scorpio, தனுசு/Sagittarius, மகரம்/Capricorn, கும்பம்/Aquarius, மீனம்/Pisces
-- star UI mapping:
-- அசுவனி/Ashwini, பரணி/Bharani, கார்த்திகை/Krittika, ரோகிணி/Rohini, திருவாதிரை/Arudra,
-- புனர்பூசம்/Punarvasu, பூசம்/Pushya, ஆயில்யம்/Ashlesha, மகம்/Magha, பூரம்/Purva Phalguni,
-- உத்திரம்/Uttara Phalguni, அஸ்தம்/Hasta, சித்திரை/Chitra, சுவாதி/Swati, விசாகம்/Vishakha,
-- அனுஷம்/Anuradha, கேட்டை/Jyeshtha, மூலம்/Mula, பூராடம்/Purva Ashadha, ਉத்திராடம்/Uttara Ashadha,
-- திருவோணம்/Shravana, அவிட்டம்/Dhanishta, சதயம்/Shatabhisha, பூரட்டாதி/Purva Bhadrapada,
-- உத்திரட்டாதி/Uttara Bhadrapada, ரேவதி/Revati
