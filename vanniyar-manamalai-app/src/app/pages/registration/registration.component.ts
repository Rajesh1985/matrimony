import { Component } from '@angular/core';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { FooterComponent } from '../../layout/footer/footer.component';
import { UserApiService } from '../../user-api.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [NavbarComponent, FooterComponent, CommonModule],
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})

export class RegistrationComponent {
  backgroundimg: string = 'assets/images/gallery/background.png';
  step: number = 0;
  formData: any = {
    name: '',
    email: '',
    country_code: '+91',
    phone: '',
    gender: '',
    password: ''
    // Add more fields as needed for other steps
  };

  constructor(private userApi: UserApiService) {}

  nextStep() {
    // Step 0: User Information
    if (this.step === 0) {
      const nameInput = (document.getElementById('name') as HTMLInputElement)?.value?.trim();
      const emailInput = (document.getElementById('email') as HTMLInputElement)?.value?.trim();
      const countryCodeSelect = document.querySelector('select[name="country_code"]') as HTMLSelectElement;
      const country_code = countryCodeSelect?.value?.trim();
      const phoneInput = (document.getElementById('phone') as HTMLInputElement)?.value?.trim();
      const genderSelect = (document.getElementById('gender') as HTMLSelectElement)?.value;
      const passwordInput = (document.getElementById('password') as HTMLInputElement)?.value?.trim();

      if (!/^\+\d{1,4}$/.test(country_code)) {
        alert('Please enter a valid country code (e.g., +91).');
        return;
      }
      if (!/^\S+@\S+\.\S+$/.test(emailInput)) {
        alert('Please enter a valid email address.');
        return;
      }
      if (!/^.*(?=.{8,})(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$/.test(passwordInput)) {
        alert('Password must be at least 8 characters, include one uppercase letter, one number, and one symbol.');
        return;
      }
      if (!/^\d{10}$/.test(phoneInput)) {
        alert('Please enter a valid 10-digit mobile number.');
        return;
      }
      if (!/^[A-Za-z ]+$/.test(nameInput)) {
        alert('Name should contain only alphabets and spaces.');
        return;
      }
      this.formData.name = nameInput;
      this.formData.email = emailInput;
      this.formData.country_code = country_code;
      this.formData.phone = phoneInput;
      this.formData.gender = genderSelect;
      this.formData.password = passwordInput;

      // Call registerUser API
      const userData = {
        name: nameInput,
        email_id: emailInput,
        country_code: country_code,
        mobile: phoneInput,
        gender: genderSelect,
        password: passwordInput
      };
      this.userApi.registerUser(userData).subscribe(
        res => {
          alert('Registration successful!');
          this.step++;
        },
        err => {
          alert('Registration failed. Please try again.');
          // Do not increment step on error
        }
      );
      return;
    }
    // Step 1: Personal Details
    else if (this.step === 1) {
      // Collect personal details
      const birth_date = (document.getElementById('birth_date') as HTMLInputElement)?.value?.trim();
      const birth_time = (document.getElementById('birth_time') as HTMLInputElement)?.value?.trim();
      const height = (document.getElementById('height') as HTMLInputElement)?.value?.trim();
      const complexion = (document.getElementById('complexion') as HTMLSelectElement)?.value?.trim();
      const caste = (document.getElementById('caste') as HTMLInputElement)?.value?.trim();
      const sub_caste = (document.getElementById('sub_caste') as HTMLInputElement)?.value?.trim();
      const address_line1 = (document.getElementById('address_line1') as HTMLInputElement)?.value?.trim();
      const address_line2 = (document.getElementById('address_line2') as HTMLInputElement)?.value?.trim();
      const city = (document.getElementById('city') as HTMLInputElement)?.value?.trim();
      const state = (document.getElementById('state') as HTMLInputElement)?.value?.trim();
      const country = (document.getElementById('country') as HTMLInputElement)?.value?.trim();
      const postal_code = (document.getElementById('postal_code') as HTMLInputElement)?.value?.trim();

      // Validation checks
      if (!birth_date || !/^\d{4}-\d{2}-\d{2}$/.test(birth_date)) {
        alert('Please enter a valid birth date (YYYY-MM-DD).');
        return;
      }
      if (!birth_time || !/^([01]?\d|2[0-3]):[0-5]\d$/.test(birth_time)) {
        alert('Please enter a valid birth time (HH:mm, 24-hour format).');
        return;
      }
      if (!height || isNaN(Number(height)) || Number(height) < 100 || Number(height) > 250) {
        alert('Please enter a valid height in cm (100-250).');
        return;
      }
      if (!complexion) {
        alert('Please select complexion.');
        return;
      }
      if (!caste || !/^[A-Za-z ]+$/.test(caste)) {
        alert('Caste should contain only alphabets and spaces.');
        return;
      }
      if (sub_caste && !/^[A-Za-z ]+$/.test(sub_caste)) {
        alert('Sub-caste should contain only alphabets and spaces.');
        return;
      }
      if (!address_line1) {
        alert('Please enter address line 1.');
        return;
      }
      if (address_line2 && address_line2.length > 100) {
        alert('Address line 2 should be less than 100 characters.');
        return;
      }
      if (!city || !/^[A-Za-z ]+$/.test(city)) {
        alert('City should contain only alphabets and spaces.');
        return;
      }
      if (!state || !/^[A-Za-z ]+$/.test(state)) {
        alert('State should contain only alphabets and spaces.');
        return;
      }
      if (!country || !/^[A-Za-z ]+$/.test(country)) {
        alert('Country should contain only alphabets and spaces.');
        return;
      }
      if (!postal_code || !/^\d{6}$/.test(postal_code)) {
        alert('Please enter a valid 6-digit postal code.');
        return;
      }

      // Save to formData
      this.formData.birth_date = birth_date;
      this.formData.birth_time = birth_time;
      this.formData.height = height;
      this.formData.complexion = complexion;
      this.formData.caste = caste;
      this.formData.sub_caste = sub_caste;
      this.formData.address_line1 = address_line1;
      this.formData.address_line2 = address_line2;
      this.formData.city = city;
      this.formData.state = state;
      this.formData.country = country;
      this.formData.postal_code = postal_code;

      // Prepare profileData for backend
      const profileData = {
        name: this.formData.name,
        birth_date: birth_date,
        birth_time: birth_time,
        height_cm: height,
        complexion: complexion,
        caste: caste,
        sub_caste: sub_caste,
        mobile_number: this.formData.phone,
      };

      this.userApi.createNewProfile(profileData).subscribe(
        (profileRes: any) => {
          // Get profile_id from response
          let profile_id = profileRes?.id;
          this.formData.profile_id = profile_id;
          if (!profile_id) {
            // Try to get profile_id using mobile
            this.userApi.getProfileIdByMobileRoute(this.formData.phone).subscribe(
              (resp: any) => {
                profile_id = resp?.profile_id;
                this.formData.profile_id = profile_id;
                if (!profile_id) {
                  alert('Profile creation failed: No profile_id returned and not found by mobile.');
                  return;
                }
                // Update user profile_id by mobile (use phone from formData)
                this.userApi.updateProfileIdByMobile(this.formData.phone, profile_id).subscribe(
                  res => {
                    const address = {
                      address_type: 'Permanent',
                      address_line1: this.formData.address_line1,
                      address_line2: this.formData.address_line2,
                      city: this.formData.city,
                      state: this.formData.state,
                      country: this.formData.country,
                      postal_code: this.formData.postal_code,
                      profile_id: this.formData.profile_id, // This will be set after profile creation
                    };
                    this.userApi.createAddress(address).subscribe(
                      () => {
                        alert('Personal details saved!');
                        this.step++;
                      },
                      () => {
                        alert('Failed to save address.');
                        // Stay in same step
                      }
                    );
                  },
                  err => {
                    alert('Failed to update user profile_id.');
                    // Stay in same step
                  }
                );
              },
              () => {
                alert('Profile creation failed: No profile_id returned and not found by mobile.');
                return;
              }
            );
            return;
          }
          // Update user profile_id by mobile (use phone from formData)
          this.userApi.updateProfileIdByMobile(this.formData.phone, profile_id).subscribe(
            res => {
              const address = {
                address_type: 'Permanent',
                address_line1: this.formData.address_line1,
                address_line2: this.formData.address_line2,
                city: this.formData.city,
                state: this.formData.state,
                country: this.formData.country,
                postal_code: this.formData.postal_code,
                profile_id: this.formData.profile_id, // This will be set after profile creation
              };
              this.userApi.createAddress(address).subscribe(
                () => {
                  alert('Personal details saved!');
                  this.step++;
                },
                () => {
                  alert('Failed to save address.');
                  // Stay in same step
                }
              );
            },
            err => {
              alert('Failed to update user profile_id.');
              // Stay in same step
            }
          );
        },
        () => {
          alert('Profile creation failed. Please try again.');
          // Stay in same step
        }
      );
      return;
    }
    // Step 2: Family Details
    else if (this.step === 2) {
      // Collect family details
      const father_name = (document.getElementById('father_name') as HTMLInputElement)?.value?.trim();
      const father_occupation = (document.getElementById('father_occupation') as HTMLInputElement)?.value?.trim();
      const mother_name = (document.getElementById('mother_name') as HTMLInputElement)?.value?.trim();
      const mother_occupation = (document.getElementById('mother_occupation') as HTMLInputElement)?.value?.trim();
      const total_siblings = (document.getElementById('total_siblings') as HTMLInputElement)?.value?.trim();
      const married_siblings = (document.getElementById('married_siblings') as HTMLInputElement)?.value?.trim();
      const family_type = (document.getElementById('family_type') as HTMLSelectElement)?.value?.trim();

      // Validation checks
      if (!father_name || !/^[A-Za-z ]+$/.test(father_name)) {
        alert('Father name should contain only alphabets and spaces.');
        return;
      }
      if (father_occupation && !/^[A-Za-z ]+$/.test(father_occupation)) {
        alert('Father occupation should contain only alphabets and spaces.');
        return;
      }
      if (!mother_name || !/^[A-Za-z ]+$/.test(mother_name)) {
        alert('Mother name should contain only alphabets and spaces.');
        return;
      }
      if (mother_occupation && !/^[A-Za-z ]+$/.test(mother_occupation)) {
        alert('Mother occupation should contain only alphabets and spaces.');
        return;
      }
      if (!total_siblings || isNaN(Number(total_siblings)) || Number(total_siblings) < 0) {
        alert('Please enter a valid number for total siblings.');
        return;
      }
      if (!married_siblings || isNaN(Number(married_siblings)) || Number(married_siblings) < 0) {
        alert('Please enter a valid number for married siblings.');
        return;
      }
      if (!family_type) {
        alert('Please select family type.');
        return;
      }

      // Save to formData
      this.formData.father_name = father_name;
      this.formData.father_occupation = father_occupation;
      this.formData.mother_name = mother_name;
      this.formData.mother_occupation = mother_occupation;
      this.formData.total_siblings = total_siblings;
      this.formData.married_siblings = married_siblings;
      this.formData.family_type = family_type.toLowerCase();

      // Prepare family_data for backend
      const family_data = {
        profile_id: this.formData.profile_id,
        father_name: father_name,
        father_occupation: father_occupation,
        mother_name: mother_name,
        mother_occupation: mother_occupation,
        total_siblings: Number(total_siblings),
        married_siblings: Number(married_siblings),
        family_type: family_type,
        family_status: 'TBD',
        family_values: 'TBD'
      };

      this.userApi.createFamily(family_data).subscribe(
        () => {
          alert('Family details saved!');
          this.step++;
        },
        () => {
          alert('Failed to save family details.');
          // Stay in same step
        }
      );
      return;
    }
    // Step 3: Astrology Details
    else if (this.step === 3) {
      // Collect astrology details
      const star = (document.getElementById('star') as HTMLInputElement)?.value?.trim();
      const rasi = (document.getElementById('rasi') as HTMLInputElement)?.value?.trim();
      const lagnam = (document.getElementById('lagnam') as HTMLInputElement)?.value?.trim();
      const birth_place = (document.getElementById('birth_place') as HTMLInputElement)?.value?.trim();
      const gotram = (document.getElementById('gotram') as HTMLInputElement)?.value?.trim();
      const dosham_details = (document.getElementById('dosham_details') as HTMLInputElement)?.value?.trim();
      // Horoscope file handling (optional, not uploaded here)
      // const horoscopeFile = (document.getElementById('horoscope') as HTMLInputElement)?.files?.[0];

      // Validation checks
      if (!star || !/^[A-Za-z ]+$/.test(star)) {
        alert('Please enter a valid star (alphabets and spaces only).');
        return;
      }
      if (!rasi || !/^[A-Za-z ]+$/.test(rasi)) {
        alert('Please enter a valid rasi (alphabets and spaces only).');
        return;
      }
      if (!lagnam || !/^[A-Za-z ]+$/.test(lagnam)) {
        alert('Please enter a valid lagnam (alphabets and spaces only).');
        return;
      }
      if (!birth_place || !/^[A-Za-z ]+$/.test(birth_place)) {
        alert('Please enter a valid birth place (alphabets and spaces only).');
        return;
      }
      if (gotram && !/^[A-Za-z ]+$/.test(gotram)) {
        alert('Gotram should contain only alphabets and spaces.');
        return;
      }
      if (dosham_details && dosham_details.length > 100) {
        alert('Dosham details should be less than 100 characters.');
        return;
      }

      // Save to formData
      this.formData.star = star;
      this.formData.rasi = rasi;
      this.formData.lagnam = lagnam;
      this.formData.birth_place = birth_place;
      this.formData.gotram = gotram;
      this.formData.dosham_details = dosham_details;

      // Prepare astrology_data for backend
      const astrology_data = {
        profile_id: this.formData.profile_id,
        star,
        rasi,
        lagnam,
        birth_place,
        gotram,
        dosham_details,
        horoscope_url: null
      };

      this.userApi.createAstrology(astrology_data).subscribe(
        () => {
          alert('Astrology details saved!');
          this.step++;
        },
        () => {
          alert('Failed to save astrology details.');
          // Stay in same step
        }
      );
      return;
    }
    // Step 4: Professional Details
    else if (this.step === 4) {
      // Education block
      const degree = (document.getElementById('degree') as HTMLInputElement)?.value?.trim();
      const specialization = (document.getElementById('specialization') as HTMLInputElement)?.value?.trim();
      const institution = (document.getElementById('institution') as HTMLInputElement)?.value?.trim();

      // Professional block
      const company_name = (document.getElementById('company_name') as HTMLInputElement)?.value?.trim();
      const designation = (document.getElementById('designation') as HTMLInputElement)?.value?.trim();
      const experience_years = (document.getElementById('experience_years') as HTMLInputElement)?.value?.trim();
      const monthly_income = (document.getElementById('monthly_income') as HTMLInputElement)?.value?.trim();
      const annual_income = (document.getElementById('annual_income') as HTMLInputElement)?.value?.trim();
      const work_location = (document.getElementById('work_location') as HTMLInputElement)?.value?.trim();

      // Validation for education
      if (!degree || !/^[A-Za-z0-9 .,-]+$/.test(degree)) {
        alert('Please enter a valid degree.');
        return;
      }
      if (!specialization || !/^[A-Za-z0-9 .,-]+$/.test(specialization)) {
        alert('Please enter a valid specialization.');
        return;
      }
      if (!institution || !/^[A-Za-z0-9 .,-]+$/.test(institution)) {
        alert('Please enter a valid institution.');
        return;
      }

      // Validation for professional
      if (!company_name || !/^[A-Za-z0-9 .,-]+$/.test(company_name)) {
        alert('Please enter a valid company name.');
        return;
      }
      if (!designation || !/^[A-Za-z0-9 .,-]+$/.test(designation)) {
        alert('Please enter a valid designation.');
        return;
      }
      if (!experience_years || isNaN(Number(experience_years)) || Number(experience_years) < 0) {
        alert('Please enter a valid experience in years.');
        return;
      }
      if (!monthly_income || isNaN(Number(monthly_income)) || Number(monthly_income) < 0) {
        alert('Please enter a valid monthly income.');
        return;
      }
      if (!annual_income || isNaN(Number(annual_income)) || Number(annual_income) < 0) {
        alert('Please enter a valid annual income.');
        return;
      }
      if (!work_location || !/^[A-Za-z0-9 .,-]+$/.test(work_location)) {
        alert('Please enter a valid work location.');
        return;
      }

      // Save to formData
      this.formData.degree = degree;
      this.formData.specialization = specialization;
      this.formData.institution = institution;
      this.formData.company_name = company_name;
      this.formData.designation = designation;
      this.formData.experience_years = experience_years;
      this.formData.monthly_income = monthly_income;
      this.formData.annual_income = annual_income;
      this.formData.work_location = work_location;

      // Prepare education_data
      const education_data = {
        profile_id: this.formData.profile_id,
        degree: degree,
        specialization: specialization,
        institution: institution,
        location: "TBD",
        year_of_completion: 0,
        grade_percentage: 0.0
      };
      // Prepare professional_data
      const professional_data = {
        profile_id: this.formData.profile_id,
        company_name,
        designation,
        experience_years: Number(experience_years),
        monthly_income: Number(monthly_income),
        annual_income: Number(annual_income),
        work_location,
        industry: 'TBD'
      };

      // Call createEducations and createProfessional
      this.userApi.createEducations(education_data).subscribe(
        () => {
          this.userApi.createProfessional(professional_data).subscribe(
            () => {
              alert('Education and Professional details saved!');
              this.step++;
            },
            () => {
              alert('Failed to save professional details.');
              // Stay in same step
            }
          );
        },
        () => {
          alert('Failed to save education details.');
          // Stay in same step
        }
      );
      return;
    }
    // Step 5: Partner Preferences
    else if (this.step === 5) {
      // Collect partner preferences
      const age_from = (document.getElementById('age_from') as HTMLInputElement)?.value?.trim();
      const age_to = (document.getElementById('age_to') as HTMLInputElement)?.value?.trim();
      const height_from = (document.getElementById('height_from') as HTMLInputElement)?.value?.trim();
      const height_to = (document.getElementById('height_to') as HTMLInputElement)?.value?.trim();
      const education_preference = (document.getElementById('education_preference') as HTMLInputElement)?.value?.trim();
      const occupation_preference = (document.getElementById('occupation_preference') as HTMLInputElement)?.value?.trim();
      const income_preference = (document.getElementById('income_preference') as HTMLInputElement)?.value?.trim();
      const star_preference = (document.getElementById('star_preference') as HTMLInputElement)?.value?.trim();
      const rasi_preference = (document.getElementById('rasi_preference') as HTMLInputElement)?.value?.trim();
      const location_preference = (document.getElementById('location_preference') as HTMLInputElement)?.value?.trim();

      // Validation
      if (!age_from || isNaN(Number(age_from)) || Number(age_from) < 18) {
        alert('Please enter a valid age from (>=18).');
        return;
      }
      if (!age_to || isNaN(Number(age_to)) || Number(age_to) < Number(age_from)) {
        alert('Please enter a valid age to (>= age from).');
        return;
      }
      if (!height_from || isNaN(Number(height_from)) || Number(height_from) < 100) {
        alert('Please enter a valid height from (>=100 cm).');
        return;
      }
      if (!height_to || isNaN(Number(height_to)) || Number(height_to) < Number(height_from)) {
        alert('Please enter a valid height to (>= height from).');
        return;
      }
      if (!education_preference) {
        alert('Please enter education preference.');
        return;
      }
      if (!occupation_preference) {
        alert('Please enter occupation preference.');
        return;
      }
      if (!income_preference) {
        alert('Please enter income preference.');
        return;
      }
      if (!star_preference) {
        alert('Please enter star preference.');
        return;
      }
      if (!rasi_preference) {
        alert('Please enter rasi preference.');
        return;
      }
      if (!location_preference) {
        alert('Please enter location preference.');
        return;
      }

      // Save to formData
      this.formData.age_from = age_from;
      this.formData.age_to = age_to;
      this.formData.height_from = height_from;
      this.formData.height_to = height_to;
      this.formData.education_preference = education_preference;
      this.formData.occupation_preference = occupation_preference;
      this.formData.income_preference = income_preference;
      this.formData.star_preference = star_preference;
      this.formData.rasi_preference = rasi_preference;
      this.formData.location_preference = location_preference;

      // Prepare Partner_Preferences_data
      const Partner_Preferences_data = {
        profile_id: this.formData.profile_id,
        age_from: Number(age_from),
        age_to: Number(age_to),
        height_from: Number(height_from),
        height_to: Number(height_to),
        education_preference,
        occupation_preference,
        income_preference,
        star_preference,
        rasi_preference,
        location_preference,
        caste_preference: 'TBD',
        other_preferences: 'TBD'
      };

      this.userApi.createPartnerPreferences(Partner_Preferences_data).subscribe(
        () => {
          alert('Partner preferences saved!');
          this.step++;
        },
        () => {
          alert('Failed to save partner preferences.');
          // Stay in same step
        }
      );
      return;
    }
    // Step 6: Verification (OTP)
    else if (this.step === 6) {
      this.formData.otp = (document.getElementById('otp') as HTMLInputElement)?.value;
      // You can add OTP validation here
    }
    if (this.step < 6) {
      this.step++;
    }
  }

  prevStep() {
    if (this.step > 0) {
      this.step--;
    }
  }
}
