// src/app/pages/registration/registration.component.ts

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { FooterComponent } from '../../layout/footer/footer.component';
import { MultiSelectDropdownComponent } from '../../shared/components/multi-select-dropdown/multi-select-dropdown.component';
import { UserApiService } from '../../user-api.service';
import { LocationService, CountryCode } from '../../shared/services/location.service';
import { GlobalStateService } from '../../global-state.service';
import { REGISTRATION_DATA, LOCATION_DATA } from '../../shared/constants/registration-data.constants';

@Component({
  selector: 'app-registration',
  imports: [
    NavbarComponent,
    FooterComponent,
    CommonModule,
    FormsModule,
    RouterModule,
    MultiSelectDropdownComponent
  ],
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  backgroundimg: string = 'assets/images/gallery/background.png';
  step: number = 0;
  maxSteps: number = 6;

  // Form data
  formData: any = {
    // Step 0: User
    country_code: '+91',
    name: '',
    email: '',
    mobile: '',
    gender: '',
    password: '',
    confirmPassword: '',

    // Step 1: Profile
    caste: 'Vanniyar',
    religion: 'Hindu',
    height_cm: '',
    birth_date: '',
    birth_time: '',
    country: '',
    state: '',
    city: '',
    physical_status: '',
    marital_status: '',
    food_preference: '',
    complexion: '',
    hobbies: '',
    about_me: '',
    address_line1: '',
    address_line2: '',
    postal_code: '',

    // Step 2: Family
    family_type: '',
    family_status: '',
    brothers: 0,
    sisters: 0,
    married_brothers: [],
    married_sisters: [],
    father_name: '',
    father_occupation: '',
    mother_name: '',
    mother_occupation: '',
    family_description: '',

    // Step 3: Astrology
    star: '',
    rasi: '',
    kotturam: 'Jumbo_Maha_Rishi',
    lagnam: '',
    birth_place: '',
    dosham_details: '',

    // Step 4: Professional
    education: '',
    education_optional: '',
    employment_type: '',
    occupation: '',
    company_name: '',
    annual_income: '',
    work_location: '',

    // Step 5: Partner Preferences
    age_from: '',
    age_to: '',
    height_from: '',
    height_to: '',
    education_preference: [],
    occupation_preference: [],
    income_preference: [],
    location_preference: [],
    star_preference: [],
    rasi_preference: [],

    // Step 6: Verification
    profile_id: null,
    user_id: null
  };

  // Dropdown options
  registrationData = REGISTRATION_DATA;
  countryCodes: CountryCode[] = [];
  countries: string[] = [];
  states: string[] = [];
  cities: string[] = [];

  // Multi-select options
  educationOptions: { value: string; label: string }[] = [];
  occupationOptions: { value: string; label: string }[] = [];
  incomeOptions: { value: string; label: string }[] = [];
  locationOptions: { value: string; label: string }[] = [];
  starOptions: { value: string; label: string }[] = [];
  rasiOptions: { value: string; label: string }[] = [];

  // Validation errors
  errors: { [key: string]: string } = {};
  brothersArray: number[] = [];
  sistersArray: number[] = [];

  constructor(
    private userApi: UserApiService,
    private locationService: LocationService,
    private globalState: GlobalStateService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadCountryCodes();
    this.loadCountries();
    this.loadMultiSelectOptions();
  }

  // ==================== LOAD OPTIONS ====================

  loadMultiSelectOptions(): void {
    // Convert to dropdown format
    this.educationOptions = this.registrationData.EDUCATION_OPTIONS.map(opt => ({
      value: opt.value,
      label: opt.label
    }));

    this.occupationOptions = this.registrationData.EMPLOYMENT_TYPE_OPTIONS.map(opt => ({
      value: opt.value,
      label: opt.label
    }));

    this.incomeOptions = this.registrationData.ANNUAL_INCOME_OPTIONS.map(opt => ({
      value: opt.value,
      label: opt.label
    }));

    this.starOptions = this.registrationData.STAR_OPTIONS.map(opt => ({
      value: opt.value,
      label: opt.label
    }));

    this.rasiOptions = this.registrationData.RASI_OPTIONS.map(opt => ({
      value: opt.value,
      label: opt.label
    }));

    // Load location options from LOCATION_DATA cities
    const allCities = new Set<string>();
    Object.values(LOCATION_DATA).forEach(statesObj => {
      Object.values(statesObj).forEach(cityArray => {
        cityArray.forEach(city => allCities.add(city));
      });
    });

    this.locationOptions = Array.from(allCities).sort().map(city => ({
      value: city,
      label: city
    }));
  }

  // ==================== LOCATION METHODS ====================

  loadCountryCodes(): void {
    this.locationService.getCountryCodes().subscribe(codes => {
      this.countryCodes = codes;
    });
  }

  loadCountries(): void {
    this.locationService.getCountries().subscribe(countries => {
      this.countries = countries;
    });
  }

  onCountryChange(country: string): void {
    this.formData.country = country;
    this.formData.state = '';
    this.formData.city = '';
    this.states = [];
    this.cities = [];

    this.locationService.getStates(country).subscribe(states => {
      this.states = states;
    });
  }

  onStateChange(state: string): void {
    this.formData.state = state;
    this.formData.city = '';
    this.cities = [];

    this.locationService.getCities(this.formData.country, state).subscribe(cities => {
      this.cities = cities;
    });
  }

  // ==================== VALIDATION METHODS ====================

  validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  validatePassword(password: string): boolean {
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
  }

  validateMobile(mobile: string): boolean {
    return /^\d{10}$/.test(mobile);
  }

  validateName(name: string): boolean {
    return /^[A-Za-z\s]{2,50}$/.test(name);
  }

  clearErrors(): void {
    this.errors = {};
  }

  addError(field: string, message: string): void {
    this.errors[field] = message;
  }

  hasError(field: string): boolean {
    return !!this.errors[field];
  }

  // ==================== STEP 0: USER REGISTRATION ====================

  validateStep0(): boolean {
    this.clearErrors();
    const { country_code, name, email, mobile, gender, password, confirmPassword } = this.formData;

    if (!country_code) {
      this.addError('country_code', 'Country code is required');
      return false;
    }

    if (!this.validateName(name)) {
      this.addError('name', 'Name must be 2-50 characters, alphabets and spaces only');
      return false;
    }

    if (!this.validateEmail(email)) {
      this.addError('email', 'Invalid email address');
      return false;
    }

    if (!this.validateMobile(mobile)) {
      this.addError('mobile', 'Mobile must be 10 digits');
      return false;
    }

    if (!gender) {
      this.addError('gender', 'Gender is required');
      return false;
    }

    if (!this.validatePassword(password)) {
      this.addError('password', 'Password must have 8+ chars, 1 uppercase, 1 number, 1 symbol');
      return false;
    }

    if (password !== confirmPassword) {
      this.addError('confirmPassword', 'Passwords do not match');
      return false;
    }

    return true;
  }

  submitStep0(): void {
    if (!this.validateStep0()) {
      alert('Please fix all errors before proceeding');
      return;
    }

    const userData = {
      country_code: this.formData.country_code,
      name: this.formData.name,
      email_id: this.formData.email,
      mobile: this.formData.mobile,
      gender: this.formData.gender,
      password: this.formData.password
    };

    this.userApi.registerUser(userData).subscribe({
      next: (res: any) => {
        this.formData.user_id = res.id;
        alert('User registration successful!');
        this.step++;
      },
      error: (err: any) => {
        alert(`Registration failed: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  // ==================== STEP 1: PROFILE DETAILS ====================

  validateStep1(): boolean {
    this.clearErrors();
    const {
      height_cm, birth_date, birth_time, country, state, city,
      physical_status, marital_status, food_preference, complexion,
      address_line1, postal_code
    } = this.formData;

    if (!height_cm || isNaN(Number(height_cm)) || Number(height_cm) < 100 || Number(height_cm) > 250) {
      this.addError('height_cm', 'Height must be between 100-250 cm');
      return false;
    }

    if (!birth_date || !/^\d{4}-\d{2}-\d{2}$/.test(birth_date)) {
      this.addError('birth_date', 'Birth date required (YYYY-MM-DD format)');
      return false;
    }

    if (!country) {
      this.addError('country', 'Country is required');
      return false;
    }

    if (!state) {
      this.addError('state', 'State is required');
      return false;
    }

    if (!city) {
      this.addError('city', 'City is required');
      return false;
    }

    if (!physical_status) {
      this.addError('physical_status', 'Physical status is required');
      return false;
    }

    if (!marital_status) {
      this.addError('marital_status', 'Marital status is required');
      return false;
    }

    if (!food_preference) {
      this.addError('food_preference', 'Food preference is required');
      return false;
    }

    if (!complexion) {
      this.addError('complexion', 'Complexion is required');
      return false;
    }

    if (!address_line1) {
      this.addError('address_line1', 'Address line 1 is required');
      return false;
    }

    if (address_line1.length > 100) {
      this.addError('address_line1', 'Address line 1 must be less than 100 characters');
      return false;
    }

    if (this.formData.address_line2 && this.formData.address_line2.length > 100) {
      this.addError('address_line2', 'Address line 2 must be less than 100 characters');
      return false;
    }

    if (!postal_code || !/^\d{5,6}$/.test(postal_code)) {
      this.addError('postal_code', 'Postal code must be 5-6 digits');
      return false;
    }

    return true;
  }

  submitStep1(): void {
    if (!this.validateStep1()) {
      alert('Please fix all errors before proceeding');
      return;
    }


    const profileData = {
      name: this.formData.name,
      caste: this.formData.caste,
      religion: this.formData.religion,
      height_cm: Number(this.formData.height_cm),
      birth_date: this.formData.birth_date,
      gender: this.formData.gender,
      physical_status: this.formData.physical_status,
      marital_status: this.formData.marital_status,
      food_preference: this.formData.food_preference,
      complexion: this.formData.complexion,
      mobile_number: this.formData.mobile,
      country: this.formData.country,
      state: this.formData.state,
      city: this.formData.city,
      address_line1: this.formData.address_line1 || '',
      address_line2: this.formData.address_line2 || '',
      postal_code: this.formData.postal_code || '',
      hobbies: this.formData.hobbies || '',
      about_me: this.formData.about_me || ''
    };

    this.userApi.createNewProfile(profileData).subscribe({
      next: (profileRes: any) => {
        let profile_id = profileRes?.id;

        if (!profile_id) {
          this.userApi.getProfileIdByMobileRoute(this.formData.mobile).subscribe({
            next: (resp: any) => {
              profile_id = resp?.profile_id;
              this.formData.profile_id = profile_id;

              if (!profile_id) {
                alert('Profile creation failed: No profile_id returned');
                return;
              }

              this.linkUserToProfile(profile_id);
            },
            error: () => {
              alert('Failed to fetch profile_id');
            }
          });
        } else {
          this.formData.profile_id = profile_id;
          this.linkUserToProfile(profile_id);
        }
      },
      error: (err: any) => {
        alert(`Profile creation failed: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  private linkUserToProfile(profile_id: number): void {
    this.userApi.updateProfileIdByMobile(this.formData.mobile, profile_id).subscribe({
      next: () => {
        alert('Profile created and linked successfully!');
        this.step++;
      },
      error: (err: any) => {
        alert(`Failed to link profile: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  // ==================== STEP 2: FAMILY DETAILS ====================

  validateStep2(): boolean {
    this.clearErrors();
    const { family_type, family_status, brothers, sisters } = this.formData;

    if (!family_type) {
      this.addError('family_type', 'Family type is required');
      return false;
    }

    if (!family_status) {
      this.addError('family_status', 'Family status is required');
      return false;
    }

    if (brothers === null || brothers === '' || isNaN(Number(brothers)) || Number(brothers) < 0) {
      this.addError('brothers', 'Valid number of brothers required');
      return false;
    }

    if (sisters === null || sisters === '' || isNaN(Number(sisters)) || Number(sisters) < 0) {
      this.addError('sisters', 'Valid number of sisters required');
      return false;
    }

    return true;
  }

  onBrothersChange(): void {
    const count = Number(this.formData.brothers) || 0;
    this.brothersArray = Array(count).fill(0).map((_, i) => i);
    this.formData.married_brothers = new Array(count).fill(false);
  }

  onSistersChange(): void {
    const count = Number(this.formData.sisters) || 0;
    this.sistersArray = Array(count).fill(0).map((_, i) => i);
    this.formData.married_sisters = new Array(count).fill(false);
  }

  submitStep2(): void {
    if (!this.validateStep2()) {
      alert('Please fix all errors before proceeding');
      return;
    }

    const married_brothers_count = this.formData.married_brothers.filter((m: boolean) => m).length;
    const married_sisters_count = this.formData.married_sisters.filter((m: boolean) => m).length;

    const familyData = {
      profile_id: this.formData.profile_id,
      family_type: this.formData.family_type,
      family_status: this.formData.family_status,
      brothers: Number(this.formData.brothers),
      sisters: Number(this.formData.sisters),
      Married_brothers: married_brothers_count,
      Married_sisters: married_sisters_count,
      father_name: this.formData.father_name || '',
      father_occupation: this.formData.father_occupation || '',
      mother_name: this.formData.mother_name || '',
      mother_occupation: this.formData.mother_occupation || '',
      Family_description: this.formData.family_description || ''
    };

    this.userApi.createFamily(familyData).subscribe({
      next: () => {
        alert('Family details saved!');
        this.step++;
      },
      error: (err: any) => {
        alert(`Failed to save family details: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  // ==================== STEP 3: ASTROLOGY DETAILS ====================

  validateStep3(): boolean {
    this.clearErrors();
    const { star, rasi, lagnam, birth_place } = this.formData;

    if (!star) {
      this.addError('star', 'Star is required');
      return false;
    }

    if (!rasi) {
      this.addError('rasi', 'Rasi is required');
      return false;
    }

    if (!lagnam) {
      this.addError('lagnam', 'Lagnam is required');
      return false;
    }

    if (!birth_place) {
      this.addError('birth_place', 'Birth place is required');
      return false;
    }

    if (this.formData.dosham_details && this.formData.dosham_details.length > 200) {
      this.addError('dosham_details', 'Dosham details must be less than 200 characters');
      return false;
    }

    return true;
  }

  submitStep3(): void {
    if (!this.validateStep3()) {
      alert('Please fix all errors before proceeding');
      return;
    }

    const astrologyData = {
      profile_id: this.formData.profile_id,
      star: this.formData.star,
      rasi: this.formData.rasi,
      kotturam: this.formData.kotturam,
      lagnam: this.formData.lagnam,
      birth_place: this.formData.birth_place,
      dosham_details: this.formData.dosham_details || ''
    };

    this.userApi.createAstrology(astrologyData).subscribe({
      next: () => {
        alert('Astrology details saved!');
        this.step++;
      },
      error: (err: any) => {
        alert(`Failed to save astrology details: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  // ==================== STEP 4: PROFESSIONAL DETAILS ====================

  validateStep4(): boolean {
    this.clearErrors();
    const { education, employment_type, occupation, company_name, annual_income, work_location } = this.formData;

    if (!education) {
      this.addError('education', 'Education is required');
      return false;
    }

    if (education === 'Others' && !this.formData.education_optional) {
      this.addError('education_optional', 'Please specify other education');
      return false;
    }

    if (!employment_type) {
      this.addError('employment_type', 'Employment type is required');
      return false;
    }

    if (!occupation) {
      this.addError('occupation', 'Occupation is required');
      return false;
    }

    if (!company_name) {
      this.addError('company_name', 'Company name is required');
      return false;
    }

    if (!annual_income) {
      this.addError('annual_income', 'Annual income is required');
      return false;
    }

    if (!work_location) {
      this.addError('work_location', 'Work location is required');
      return false;
    }

    return true;
  }

  submitStep4(): void {
    if (!this.validateStep4()) {
      alert('Please fix all errors before proceeding');
      return;
    }

    const educationValue = this.formData.education === 'Others'
      ? this.formData.education_optional
      : this.formData.education;

    const professionalData = {
      profile_id: this.formData.profile_id,
      education: educationValue,
      education_optional: this.formData.education_optional || '',
      employment_type: this.formData.employment_type,
      occupation: this.formData.occupation,
      company_name: this.formData.company_name,
      annual_income: this.formData.annual_income,
      work_location: this.formData.work_location
    };

    this.userApi.createProfessional(professionalData).subscribe({
      next: () => {
        alert('Professional details saved!');
        this.step++;
      },
      error: (err: any) => {
        alert(`Failed to save professional details: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  // ==================== STEP 5: PARTNER PREFERENCES ====================

  validateStep5(): boolean {
    this.clearErrors();
    const { age_from, age_to, height_from, height_to } = this.formData;

    if (!age_from || isNaN(Number(age_from)) || Number(age_from) < 18) {
      this.addError('age_from', 'Age from must be 18 or greater');
      return false;
    }

    if (!age_to || isNaN(Number(age_to)) || Number(age_to) < Number(age_from)) {
      this.addError('age_to', 'Age to must be greater than age from');
      return false;
    }

    if (!height_from || isNaN(Number(height_from)) || Number(height_from) < 100) {
      this.addError('height_from', 'Height from must be 100 cm or greater');
      return false;
    }

    if (!height_to || isNaN(Number(height_to)) || Number(height_to) < Number(height_from)) {
      this.addError('height_to', 'Height to must be greater than height from');
      return false;
    }

    if (!this.formData.education_preference || this.formData.education_preference.length === 0) {
      this.addError('education_preference', 'Please select at least one education preference');
      return false;
    }

    if (!this.formData.occupation_preference || this.formData.occupation_preference.length === 0) {
      this.addError('occupation_preference', 'Please select at least one occupation preference');
      return false;
    }

    if (!this.formData.income_preference || this.formData.income_preference.length === 0) {
      this.addError('income_preference', 'Please select at least one income preference');
      return false;
    }

    if (!this.formData.location_preference || this.formData.location_preference.length === 0) {
      this.addError('location_preference', 'Please select at least one location preference');
      return false;
    }

    if (!this.formData.star_preference || this.formData.star_preference.length === 0) {
      this.addError('star_preference', 'Please select at least one star preference');
      return false;
    }

    if (!this.formData.rasi_preference || this.formData.rasi_preference.length === 0) {
      this.addError('rasi_preference', 'Please select at least one rasi preference');
      return false;
    }

    return true;
  }

  submitStep5(): void {
    if (!this.validateStep5()) {
      alert('Please fix all errors before proceeding');
      return;
    }

    const preferencesData = {
      profile_id: this.formData.profile_id,
      age_from: Number(this.formData.age_from),
      age_to: Number(this.formData.age_to),
      height_from: Number(this.formData.height_from),
      height_to: Number(this.formData.height_to),
      education_preference: this.formData.education_preference.join(', '),
      occupation_preference: this.formData.occupation_preference.join(', '),
      income_preference: this.formData.income_preference.join(', '),
      location_preference: this.formData.location_preference.join(', '),
      star_preference: this.formData.star_preference.join(', '),
      rasi_preference: this.formData.rasi_preference.join(', ')
    };

    this.userApi.createPartnerPreferences(preferencesData).subscribe({
      next: () => {
        alert('Partner preferences saved!');
        this.step++;
      },
      error: (err: any) => {
        alert(`Failed to save partner preferences: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  onEducationPreferenceChanged(selected: string[]): void {
    this.formData.education_preference = selected;
  }

  onOccupationPreferenceChanged(selected: string[]): void {
    this.formData.occupation_preference = selected;
  }

  onIncomePreferenceChanged(selected: string[]): void {
    this.formData.income_preference = selected;
  }

  onLocationPreferenceChanged(selected: string[]): void {
    this.formData.location_preference = selected;
  }

  onStarPreferenceChanged(selected: string[]): void {
    this.formData.star_preference = selected;
  }

  onRasiPreferenceChanged(selected: string[]): void {
    this.formData.rasi_preference = selected;
  }

  generateSerialNumber(id: number): string {
    // Convert id to string
    const idStr = id.toString();

    // Pad with leading zeros to length 11
    const padded = idStr.padStart(11, '0');

    // Prefix with 'CVM'
    return `CVM${padded}`;
  }

  // ==================== STEP 6: VERIFICATION & COMPLETION ====================

  completeRegistration(): void {
    this.globalState.profileId = this.formData.profile_id;
    this.globalState.isUserSignedIn = true;

    const serial_number = this.generateSerialNumber(this.formData.profile_id);
    this.userApi.updateSerialNumberByProfileID(serial_number, this.formData.profile_id).subscribe({
      error: (err: any) => {
        alert(`Failed to set serial_number in Profile: ${err.error?.detail || 'Unknown error'}`);
        this.router.navigate(['/login']);
      }
    });      

    this.userApi.updateIsVerifiedbyProfileID(true, this.formData.profile_id).subscribe({
      next: () => {
        alert('Registration completed successfully!');
        this.router.navigate(['/user-page']);
      },
      error: (err: any) => {
        alert(`Failed to set Verify in User: ${err.error?.detail || 'Unknown error'}`);
        this.router.navigate(['/login']);
      }
    });
  }

  // ==================== NAVIGATION ====================

  nextStep(): void {
    if (this.step === 0) {
      this.submitStep0();
    } else if (this.step === 1) {
      this.submitStep1();
    } else if (this.step === 2) {
      this.submitStep2();
    } else if (this.step === 3) {
      this.submitStep3();
    } else if (this.step === 4) {
      this.submitStep4();
    } else if (this.step === 5) {
      this.submitStep5();
    } else if (this.step === 6) {
      this.completeRegistration();
    }
  }

  prevStep(): void {
    if (this.step > 0) {
      this.step--;
      this.clearErrors();
    }
  }

  getStepTitle(): string {
    const titles = [
      'User Registration',
      'Personal Details',
      'Family Background',
      'Astrological Details',
      'Professional Information',
      'Partner Preferences',
      'Verification & Completion'
    ];
    return titles[this.step] || 'Registration';
  }
}
