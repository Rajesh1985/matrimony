// src/app/pages/user-page/user-page.component.ts (UPDATED - Address in profiles table)
import '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { DomSanitizer, SafeUrl, SafeResourceUrl } from '@angular/platform-browser';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { FooterComponent } from '../../layout/footer/footer.component';
import { GlobalStateService } from '../../global-state.service';
import { UserPageService, UserProfileComplete, RecommendedProfile } from '../../shared/services/user-page.service';
import { UserApiService } from '../../user-api.service';
import { AvatarComponent } from '../../shared/components/avatar/avatar.component';
import { MultiSelectDropdownComponent } from '../../shared/components/multi-select-dropdown/multi-select-dropdown.component';
import { REGISTRATION_DATA, LOCATION_DATA } from '../../shared/constants/registration-data.constants';
import { STAR_TAMIL_MAP, RASI_TAMIL_MAP } from '../../shared/constants/astrology-maps';

@Component({
  selector: 'app-user-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    NavbarComponent,
    FooterComponent,
    AvatarComponent,
    MultiSelectDropdownComponent
  ],
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss']
})
export class UserPageComponent implements OnInit {
  // User profile data
  currentProfile: UserProfileComplete | null = null;
  recommendedProfiles: RecommendedProfile[] = [];
  
  // Profile photo URLs (for current and recommended profiles)
  profilePhotoUrl: SafeUrl | null = null;
  recommendedProfilePhotos: { [key: number]: SafeUrl | null } = {};
  
  // Profile modal state
  selectedProfile: UserProfileComplete | null = null;
  selectedProfilePhotos: SafeUrl[] = [];
  selectedProfilePhotoIndex = 0;
  showProfileModal = false;

  // Loading and error states
  isLoading = true;
  isLoadingRecommendations = true;
  error: string | null = null;

  // UI state
  expandedSections = {
    personal: false,
    professional: false,
    family: false,
    astrology: false,
    address: false,
    preferences: false
  };

  // Make Array accessible in template
  Array = Array;

  // Modal expandable sections state
  modalExpandedSections = {
    personal: false,
    professional: false,
    family: false,
    astrology: false,
    address: false
  };

  // Edit modal state
  showEditModal = false;
  editingSection: string | null = null;
  editFormData: any = {};

  // Horoscope modal state
  showHoroscopeModal = false;
  horoscopeUrl: SafeResourceUrl | null = null;
  horoscopeBlobUrl: string = ''; // Store the actual blob URL for downloads
  horoscopeFileName: string = '';
  horoscopeLoading = false;
  horoscopeError: string | null = null;

  // File upload/view modal states for family section
  showCommunityCertViewModal = false;
  communityCertViewUrl: SafeResourceUrl | null = null;
  communityCertViewBlobUrl: string = '';
  communityCertViewFileName: string = '';
  communityCertViewLoading = false;
  communityCertViewError: string | null = null;

  showProfilePhotoViewModal = false;
  profilePhotoViewUrl: SafeUrl | null = null;
  profilePhotoViewBlobUrl: string = '';
  profilePhotoViewLoading = false;
  profilePhotoViewError: string | null = null;
  profilePhotoViewFileId: string | null = null; // Track which photo is being viewed

  // File upload states
  isUploadingCommunityCert = false;
  certificateUploadError: string | null = null;
  isUploadingProfilePhoto = false;
  photoUploadError: string | null = null;

  // Dropdown options for personal section
  complexionOptions = REGISTRATION_DATA.COMPLEXION_OPTIONS;
  physicalStatusOptions = REGISTRATION_DATA.PHYSICAL_STATUS_OPTIONS;
  maritalStatusOptions = REGISTRATION_DATA.MARITAL_STATUS_OPTIONS;
  foodPreferenceOptions = REGISTRATION_DATA.FOOD_PREFERENCE_OPTIONS;

  // Dropdown options for professional section
  educationOptions = REGISTRATION_DATA.EDUCATION_OPTIONS;
  employmentTypeOptions = REGISTRATION_DATA.EMPLOYMENT_TYPE_OPTIONS;
  occupationOptions = REGISTRATION_DATA.OCCUPATION_OPTIONS;
  annualIncomeOptions = REGISTRATION_DATA.ANNUAL_INCOME_OPTIONS;
  workLocationOptions = REGISTRATION_DATA.WORK_LOCATION_OPTIONS;

  // Dropdown options for family section
  familyTypeOptions = REGISTRATION_DATA.FAMILY_TYPE_OPTIONS;
  familyStatusOptions = REGISTRATION_DATA.FAMILY_STATUS_OPTIONS;

  // Dropdown options for astrology section
  starOptions = REGISTRATION_DATA.STAR_OPTIONS;
  rasiOptions = REGISTRATION_DATA.RASI_OPTIONS;

  // Dropdown options for preferences section
  educationPreferenceOptions = REGISTRATION_DATA.EDUCATION_OPTIONS;
  occupationPreferenceOptions = REGISTRATION_DATA.OCCUPATION_OPTIONS;
  incomePreferenceOptions = REGISTRATION_DATA.ANNUAL_INCOME_OPTIONS;
  starPreferenceOptions = REGISTRATION_DATA.STAR_OPTIONS;
  rasiPreferenceOptions = REGISTRATION_DATA.RASI_OPTIONS;
  locationPreferenceDropdownOptions: { value: string; label: string }[] = []; // Will be populated from LOCATION_DATA

  // Dropdown options for address section
  countries: string[] = [];
  states: string[] = [];
  cities: string[] = [];

  // Horoscope file upload states
  isUploadingHoroscope = false;
  horoscopeUploadError: string | null = null;
  showHoroscopeViewModal = false;
  horoscopeViewUrl: SafeResourceUrl | null = null;
  horoscopeViewBlobUrl: string = '';
  horoscopeViewFileName: string = '';
  horoscopeViewLoading = false;
  horoscopeViewError: string | null = null;

  constructor(
    private userPageService: UserPageService,
    private userApi: UserApiService,
    private sanitizer: DomSanitizer,
    private globalState: GlobalStateService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadUserProfile();
    this.initializeLocationDropdowns();
    this.initializeBilingualPreferenceOptions();
  }

  /**
   * Initialize bilingual (English + Tamil) display for star and rasi preference options
   */
  initializeBilingualPreferenceOptions(): void {
    // Transform star preference options to show bilingual labels
    this.starPreferenceOptions = REGISTRATION_DATA.STAR_OPTIONS.map(option => ({
      value: option.value,
      label: this.getStarDisplay(option.value)
    }));

    // Transform rasi preference options to show bilingual labels
    this.rasiPreferenceOptions = REGISTRATION_DATA.RASI_OPTIONS.map(option => ({
      value: option.value,
      label: this.getRasiDisplay(option.value)
    }));
  }

  /**
   * Initialize country/state/city dropdowns from LOCATION_DATA
   */
  initializeLocationDropdowns(): void {
    // Extract all countries from LOCATION_DATA
    this.countries = Object.keys(LOCATION_DATA);

    // Extract all unique cities from LOCATION_DATA for location preferences
    const citiesSet = new Set<string>();
    Object.values(LOCATION_DATA).forEach(country => {
      Object.values(country).forEach(cities => {
        if (Array.isArray(cities)) {
          cities.forEach(city => citiesSet.add(city));
        }
      });
    });
    const sortedCities = Array.from(citiesSet).sort();
    this.locationPreferenceDropdownOptions = sortedCities.map(city => ({
      value: city,
      label: city
    }));
  }

  /**
   * Handle country change - update states dropdown
   */
  onCountryChange(country: string): void {
    this.editFormData.country = country;
    this.editFormData.state = '';
    this.editFormData.city = '';
    this.states = [];
    this.cities = [];

    if (LOCATION_DATA[country]) {
      this.states = Object.keys(LOCATION_DATA[country]);
    }
  }

  /**
   * Handle state change - update cities dropdown
   */
  onStateChange(state: string): void {
    this.editFormData.state = state;
    this.editFormData.city = '';
    this.cities = [];

    const country = this.editFormData.country;
    if (LOCATION_DATA[country] && LOCATION_DATA[country][state]) {
      this.cities = LOCATION_DATA[country][state];
    }
  }

  /**
   * Convert string or array to array format
   * Handles both database strings (comma-separated) and already-array values
   */
  ensureArray(value: any): string[] {
    if (!value) {
      return [];
    }
    if (Array.isArray(value)) {
      return value;
    }
    if (typeof value === 'string') {
      // Handle both comma-separated strings and JSON arrays
      if (value.startsWith('[')) {
        try {
          return JSON.parse(value);
        } catch {
          return [value];
        }
      }
      // If it's a comma-separated string, split it
      if (value.includes(',')) {
        return value.split(',').map(v => v.trim()).filter(v => v.length > 0);
      }
      // If it's a single string value, return as single-item array
      return [value];
    }
    return [];
  }

  /**
   * Get bilingual display for star (English + Tamil)
   */
  getStarDisplay(star: string): string {
    if (!star) return '';
    const tamilName = STAR_TAMIL_MAP[star];
    return tamilName ? `${star} (${tamilName})` : star;
  }

  /**
   * Get bilingual display for rasi (English + Tamil)
   */
  getRasiDisplay(rasi: string): string {
    if (!rasi) return '';
    const tamilName = RASI_TAMIL_MAP[rasi];
    return tamilName ? `${rasi} (${tamilName})` : rasi;
  }

  /**
   * Preference selection change handlers
   */
  onEducationPreferenceChanged(selectedValues: string[]): void {
    this.editFormData.education_preference = selectedValues;
  }

  onOccupationPreferenceChanged(selectedValues: string[]): void {
    this.editFormData.occupation_preference = selectedValues;
  }

  onIncomePreferenceChanged(selectedValues: string[]): void {
    this.editFormData.income_preference = selectedValues;
  }

  onStarPreferenceChanged(selectedValues: string[]): void {
    this.editFormData.star_preference = selectedValues;
  }

  onRasiPreferenceChanged(selectedValues: string[]): void {
    this.editFormData.rasi_preference = selectedValues;
  }

  onLocationPreferenceChanged(selectedValues: string[]): void {
    this.editFormData.location_preference = selectedValues;
  }

  /**
   * Handle location preference blur - convert comma-separated string to array
   */
  onLocationBlur(): void {
    // Check if it's already an array (from database or multi-select)
    if (Array.isArray(this.editFormData.location_preference)) {
      return;
    }

    // If it's not an array, it's a string input - convert it
    const locationInput = this.editFormData.location_preference?.trim();
    
    if (!locationInput || locationInput === '') {
      this.editFormData.location_preference = [];
      return;
    }

    // Split by comma, trim spaces, and filter empty values
    const locations = locationInput
      .split(',')
      .map((loc: string) => loc.trim())
      .filter((loc: string) => loc.length > 0);

    // Store as array
    this.editFormData.location_preference = locations;

    console.log('Location preferences:', this.editFormData.location_preference);
  }

  /**
   * Load current user's complete profile
   */
  loadUserProfile(): void {
    const profileId = this.globalState.profileId;
    const isSignedIn = this.globalState.isUserSignedIn;

    if (!isSignedIn || !profileId) {
      this.error = 'User not signed in. Redirecting to login...';
      setTimeout(() => this.router.navigate(['/login']), 2000);
      return;
    }

    this.userPageService.getCompleteUserProfile(profileId).subscribe({
      next: (profile: UserProfileComplete) => {
        this.currentProfile = profile;
        this.isLoading = false;
        this.loadProfilePhoto();
        
        // Only load recommended profiles if membership is active
        if (this.hasActiveMembership()) {
          this.loadRecommendedProfiles(profile.profile_id);
        } else {
          // No active membership - don't load recommendations
          this.recommendedProfiles = [];
          this.isLoadingRecommendations = false;
        }
      },
      error: (err: any) => {
        this.error = `Failed to load profile: ${err.error?.detail || 'Unknown error'}`;
        this.isLoading = false;
        console.error('Profile load error:', err);
      }
    });
  }

  /**
   * Load profile photo thumbnail
   * If photo_file_id_1 exists, get the thumbnail blob and convert to safe URL
   */
  loadProfilePhoto(): void {
    if (!this.currentProfile || (!this.currentProfile.photo_file_id_1 && !this.currentProfile.photo_file_id_2)) {
      console.log('No photo file IDs available');
      return;
    }

    // Prefer photo_file_id_1, fallback to photo_file_id_2
    const fileId = this.currentProfile.photo_file_id_1 || this.currentProfile.photo_file_id_2;

    if (!fileId) {
      console.log('No photo file ID selected');
      return;
    }

    this.userApi.getFileThumbnail(fileId).subscribe({
      next: (blob: Blob) => {
        // Create object URL from blob
        const url = URL.createObjectURL(blob);
        // Sanitize and set as safe URL for display
        this.profilePhotoUrl = this.sanitizer.bypassSecurityTrustUrl(url);
        console.log('Profile photo loaded successfully:', fileId);
      },
      error: (err: any) => {
        console.error('Failed to load profile photo:', err);
        // Fallback to avatar if photo fails to load
        this.profilePhotoUrl = null;
      }
    });
  }

  /**
   * Load recommended profiles based on user's partner preferences
   */
  loadRecommendedProfiles(profileId: number): void {
    this.userPageService.getRecommendedProfiles(profileId, 20).subscribe({
      next: (profiles: RecommendedProfile[]) => {
        // Sort by match score (descending)
        this.recommendedProfiles = profiles.sort((a, b) => {
          return b.match_score - a.match_score;
        });
        this.isLoadingRecommendations = false;
        // Load photos for all recommended profiles
        this.loadRecommendedProfilePhotos();
      },
      error: (err: any) => {
        console.error('Failed to load recommendations:', err);
        this.recommendedProfiles = [];
        this.isLoadingRecommendations = false;
      }
    });
  }

  /**
   * Load thumbnail photos for all recommended profiles
   * Uses photo_file_id_1 if available, fallback to photo_file_id_2
   */
  loadRecommendedProfilePhotos(): void {
    this.recommendedProfiles.forEach((profile: RecommendedProfile) => {
      // Check if profile has valid photo file IDs
      if (!profile.photo_file_id_1 && !profile.photo_file_id_2) {
        this.recommendedProfilePhotos[profile.match_profile_id] = null;
        return;
      }

      // Prefer photo_file_id_1, fallback to photo_file_id_2
      const fileId = profile.photo_file_id_1 || profile.photo_file_id_2;

      if (!fileId) {
        this.recommendedProfilePhotos[profile.match_profile_id] = null;
        return;
      }

      // Fetch thumbnail for this profile
      this.userApi.getFileThumbnail(fileId).subscribe({
        next: (blob: Blob) => {
          // Create object URL from blob and sanitize
          const url = URL.createObjectURL(blob);
          this.recommendedProfilePhotos[profile.match_profile_id] = 
            this.sanitizer.bypassSecurityTrustUrl(url);
          console.log(`Photo loaded for profile ${profile.match_profile_id}:`, fileId);
        },
        error: (err: any) => {
          console.error(`Failed to load photo for profile ${profile.match_profile_id}:`, err);
          // Fallback to null (will show avatar)
          this.recommendedProfilePhotos[profile.match_profile_id] = null;
        }
      });
    });
  }

  /**
   * Calculate age from birth date
   */
  getAge(birthDate: string): number {
    if (!birthDate) return 0;
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const month = today.getMonth() - birth.getMonth();
    if (month < 0 || (month === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  }

  /**
   * Format date for display
   */
  formatDate(date: string | null): string {
    if (!date) return 'N/A';
    return new Date(date).toLocaleDateString('en-GB');
  }

  /**
   * Check if membership has expired
   */
  isExpired(endDate: string | null): boolean {
    if (!endDate) return false;
    try {
      const today = new Date();
      const end = new Date(endDate);
      return end < today;
    } catch {
      return false;
    }
  }

  /**
   * Check if user has active membership
   */
  hasActiveMembership(): boolean {
    if (!this.currentProfile) return false;
    if (!this.currentProfile.plan_name) return false;
    if (!this.currentProfile.end_date) return false;
    
    try {
      const today = new Date();
      const endDate = new Date(this.currentProfile.end_date);
      return endDate >= today;
    } catch {
      return false;
    }
  }

  /**
   * Format timestamp for last updated (relative time)
   */
  formatTimestamp(timestamp: string): string {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return `${Math.floor(diffDays / 365)} years ago`;
  }

  /**
   * Toggle section expansion
   */
  toggleSection(section: string): void {
    this.expandedSections[section as keyof typeof this.expandedSections] = 
      !this.expandedSections[section as keyof typeof this.expandedSections];
  }

  /**
   * Toggle modal section expansion
   */
  toggleModalSection(section: string): void {
    this.modalExpandedSections[section as keyof typeof this.modalExpandedSections] = 
      !this.modalExpandedSections[section as keyof typeof this.modalExpandedSections];
  }

  /**
   * Open edit modal for a section
   */
  openEditModal(section: string): void {
    this.editingSection = section;
    this.showEditModal = true;

    // Initialize form data based on section
    switch (section) {
      case 'personal':
        // Format birth_date to YYYY-MM-DD (Python date.fromisoformat() only accepts this format)
        let formattedBirthDate: string | null = null;
        if (this.currentProfile?.birth_date) {
          // Remove time portion if present (e.g., "2000-05-15T00:00:00" -> "2000-05-15")
          formattedBirthDate = String(this.currentProfile.birth_date).split('T')[0];
        }

        this.editFormData = {
          name: this.currentProfile?.name,
          birth_date: formattedBirthDate, // Must be YYYY-MM-DD or null
          height_cm: Number(this.currentProfile?.height_cm),
          religion: this.currentProfile?.religion,
          caste: this.currentProfile?.caste,
          complexion: this.currentProfile?.complexion,
          mobile_number: this.currentProfile?.mobile,
          gender: this.currentProfile?.gender,
          hobbies: this.currentProfile?.hobbies,
          about_me: this.currentProfile?.about_me,
          physical_status: this.currentProfile?.physical_status,
          marital_status: this.currentProfile?.marital_status,
          food_preference: this.currentProfile?.food_preference,
          address_line1: this.currentProfile?.address_line1,
          address_line2: this.currentProfile?.address_line2,
          city: this.currentProfile?.city,
          state: this.currentProfile?.state,
          country: this.currentProfile?.country,
          postal_code: this.currentProfile?.postal_code
        };
        // Populate states and cities dropdowns based on selected country
        if (this.currentProfile?.country && LOCATION_DATA[this.currentProfile.country]) {
          this.states = Object.keys(LOCATION_DATA[this.currentProfile.country]);
          if (this.currentProfile.state && LOCATION_DATA[this.currentProfile.country][this.currentProfile.state]) {
            this.cities = LOCATION_DATA[this.currentProfile.country][this.currentProfile.state];
          }
        }
        break;

      case 'professional':
        this.editFormData = {
          education: this.currentProfile?.education,
          employment_type: this.currentProfile?.employment_type,
          occupation: this.currentProfile?.occupation,
          company_name: this.currentProfile?.company_name,
          annual_income: this.currentProfile?.annual_income,
          work_location: this.currentProfile?.work_location
        };
        break;

      case 'family':
        this.editFormData = {
          family_type: this.currentProfile?.family_type,
          family_status: this.currentProfile?.family_status,
          brothers: this.currentProfile?.brothers,
          sisters: this.currentProfile?.sisters,
          married_brothers: this.currentProfile?.married_brothers,
          married_sisters: this.currentProfile?.married_sisters,
          father_name: this.currentProfile?.father_name,
          father_occupation: this.currentProfile?.father_occupation,
          mother_name: this.currentProfile?.mother_name,
          mother_occupation: this.currentProfile?.mother_occupation,
          family_description: this.currentProfile?.family_description
        };
        break;

      case 'astrology':
        this.editFormData = {
          star: this.currentProfile?.star,
          rasi: this.currentProfile?.rasi,
          lagnam: this.currentProfile?.lagnam,
          birth_place: this.currentProfile?.birth_place,
          dosham_details: this.currentProfile?.dosham_details
        };
        break;

      case 'preferences':
        this.editFormData = {
          education_preference: this.ensureArray(this.currentProfile?.education_preference),
          occupation_preference: this.ensureArray(this.currentProfile?.occupation_preference),
          income_preference: this.ensureArray(this.currentProfile?.income_preference),
          star_preference: this.ensureArray(this.currentProfile?.star_preference),
          rasi_preference: this.ensureArray(this.currentProfile?.rasi_preference),
          location_preference: this.ensureArray(this.currentProfile?.location_preference),
          age_from: this.currentProfile?.age_from,
          age_to: this.currentProfile?.age_to,
          height_from: this.currentProfile?.height_from,
          height_to: this.currentProfile?.height_to
        };
        break;
    }
  }

  /**
   * Save edited section
   */
  saveSection(): void {
    if (!this.currentProfile || !this.editingSection) return;

    const profileId = this.currentProfile.profile_id;

    let updateObservable: any;
    let successMessage = 'Section updated successfully!';

    switch (this.editingSection) {
      case 'personal':
        // Validate mandatory fields: personal + address
        if (!this.editFormData.name || !this.editFormData.birth_date || !this.editFormData.height_cm || 
            !this.editFormData.complexion || !this.editFormData.physical_status || 
            !this.editFormData.marital_status || !this.editFormData.food_preference ||
            !this.editFormData.address_line1 || !this.editFormData.city || 
            !this.editFormData.state || !this.editFormData.country || !this.editFormData.postal_code) {
          alert('Please fill in all mandatory fields: Name, Birth Date, Height, Complexion, Physical Status, Marital Status, Food Preference, Address Line 1, City, State, Country, and Postal Code');
          return;
        }
        updateObservable = this.userPageService.updateProfile(profileId, this.editFormData);
        successMessage = 'Personal details updated successfully!';
        break;
      case 'professional':
        updateObservable = this.userPageService.updateProfessional(profileId, this.editFormData);
        successMessage = 'Professional details updated successfully!';
        break;
      case 'family':
        updateObservable = this.userPageService.updateFamily(profileId, this.editFormData);
        successMessage = 'Family details updated successfully!';
        break;
      case 'astrology':
        // Validate mandatory fields
        if (!this.editFormData.star || !this.editFormData.rasi) {
          alert('Please fill in all mandatory fields: Star and Rasi');
          return;
        }
        updateObservable = this.userPageService.updateAstrology(profileId, this.editFormData);
        successMessage = 'Astrology details updated successfully!';
        break;
      case 'preferences':
        // Validate mandatory fields: age and height ranges
        if (!this.editFormData.age_from || !this.editFormData.age_to || 
            !this.editFormData.height_from || !this.editFormData.height_to) {
          alert('Please fill in all mandatory fields: Age From, Age To, Height From, and Height To');
          return;
        }
        // Validate ranges
        if (this.editFormData.age_from > this.editFormData.age_to) {
          alert('Age From must be less than or equal to Age To');
          return;
        }
        if (this.editFormData.height_from > this.editFormData.height_to) {
          alert('Height From must be less than or equal to Height To');
          return;
        }
        
        // Convert array preferences to comma-separated strings for backend
        const preferencesData = {
          ...this.editFormData,
          education_preference: Array.isArray(this.editFormData.education_preference) 
            ? this.editFormData.education_preference.join(',') 
            : this.editFormData.education_preference,
          occupation_preference: Array.isArray(this.editFormData.occupation_preference) 
            ? this.editFormData.occupation_preference.join(',') 
            : this.editFormData.occupation_preference,
          income_preference: Array.isArray(this.editFormData.income_preference) 
            ? this.editFormData.income_preference.join(',') 
            : this.editFormData.income_preference,
          star_preference: Array.isArray(this.editFormData.star_preference) 
            ? this.editFormData.star_preference.join(',') 
            : this.editFormData.star_preference,
          rasi_preference: Array.isArray(this.editFormData.rasi_preference) 
            ? this.editFormData.rasi_preference.join(',') 
            : this.editFormData.rasi_preference,
          location_preference: Array.isArray(this.editFormData.location_preference) 
            ? this.editFormData.location_preference.join(',') 
            : this.editFormData.location_preference
        };
        
        updateObservable = this.userPageService.updatePartnerPreferences(profileId, preferencesData);
        successMessage = 'Partner preferences updated successfully!';
        break;
    }

    if (updateObservable) {
      updateObservable.subscribe({
        next: () => {
          alert(successMessage);
          this.closeEditModal();
          this.loadUserProfile(); // Reload profile
        },
        error: (err: any) => {
          const errorMessage = err.error?.detail || err.error?.message || 'Unknown error';
          alert(`Failed to update: ${errorMessage}`);
        }
      });
    }
  }

  /**
   * Close edit modal
   */
  closeEditModal(): void {
    this.showEditModal = false;
    this.editingSection = null;
    this.editFormData = {};
  }

  /**
   * View full profile (navigate to detail page)
   */
  viewProfile(profile: RecommendedProfile): void {
    // Fetch complete profile data
    this.userPageService.getCompleteUserProfile(profile.match_profile_id).subscribe({
      next: (completeProfile: UserProfileComplete) => {
        this.selectedProfile = completeProfile;
        this.selectedProfilePhotoIndex = 0;
        this.selectedProfilePhotos = [];
        this.showProfileModal = true;
        
        // Load photos for the selected profile
        this.loadSelectedProfilePhotos(completeProfile);
      },
      error: (err: any) => {
        console.error('Failed to load complete profile:', err);
        alert(`Failed to load profile: ${err.error?.detail || 'Unknown error'}`);
      }
    });
  }

  /**
   * Load photos for the selected profile in modal
   */
  loadSelectedProfilePhotos(profile: UserProfileComplete): void {
    const photoIds: string[] = [];
    
    // Collect available photo IDs (prefer photo_file_id_1 first)
    if (profile.photo_file_id_1) {
      photoIds.push(profile.photo_file_id_1);
    }
    if (profile.photo_file_id_2) {
      photoIds.push(profile.photo_file_id_2);
    }

    // If no photos, reset the array
    if (photoIds.length === 0) {
      this.selectedProfilePhotos = [];
      return;
    }

    // Fetch thumbnails for each photo
    photoIds.forEach((fileId: string) => {
      this.userApi.getFileThumbnail(fileId).subscribe({
        next: (blob: Blob) => {
          const url = URL.createObjectURL(blob);
          const safeUrl = this.sanitizer.bypassSecurityTrustUrl(url);
          this.selectedProfilePhotos.push(safeUrl);
          console.log(`Photo loaded for modal:`, fileId);
        },
        error: (err: any) => {
          console.error(`Failed to load photo in modal:`, err);
        }
      });
    });
  }

  /**
   * Navigate to next photo in modal
   */
  nextPhoto(): void {
    if (this.selectedProfilePhotos.length > 0) {
      this.selectedProfilePhotoIndex = 
        (this.selectedProfilePhotoIndex + 1) % this.selectedProfilePhotos.length;
    }
  }

  /**
   * Navigate to previous photo in modal
   */
  prevPhoto(): void {
    if (this.selectedProfilePhotos.length > 0) {
      this.selectedProfilePhotoIndex = 
        (this.selectedProfilePhotoIndex - 1 + this.selectedProfilePhotos.length) % this.selectedProfilePhotos.length;
    }
  }

  /**
   * Close profile modal
   */
  closeProfileModal(): void {
    this.showProfileModal = false;
    this.selectedProfile = null;
    this.selectedProfilePhotos = [];
    this.selectedProfilePhotoIndex = 0;
    // Reset modal sections state
    this.modalExpandedSections = {
      personal: false,
      professional: false,
      family: false,
      astrology: false,
      address: false
    };
  }

  /**
   * Send interest to profile (future feature)
   */
  sendInterest(profile: RecommendedProfile | UserProfileComplete): void {
    // TODO: Implement send interest functionality
    alert(`Interest sent to ${profile.name}!`);
  }

  /**
   * Add to favorites (future feature)
   */
  addToFavorites(profile: RecommendedProfile | UserProfileComplete): void {
    // TODO: Implement favorites functionality
    alert(`${profile.name} added to favorites!`);
  }

  /**
   * View community certificate
   */
  viewCommunityCertificate(fileId: string): void {
    if (!fileId) {
      this.communityCertViewError = 'No file ID provided';
      return;
    }

    this.communityCertViewLoading = true;
    this.communityCertViewError = null;
    this.communityCertViewUrl = null;
    this.communityCertViewBlobUrl = '';

    this.userApi.getCommunityCert(fileId).subscribe({
      next: (blob: Blob) => {
        // Create object URL from blob
        const url = URL.createObjectURL(blob);
        // Store both the raw blob URL and sanitized version
        this.communityCertViewBlobUrl = url;
        this.communityCertViewUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
        this.communityCertViewFileName = `Community_Certificate_${this.currentProfile?.serial_number}.pdf`;
        this.showCommunityCertViewModal = true;
        this.communityCertViewLoading = false;
        console.log('Community certificate loaded successfully:', fileId);
      },
      error: (err: any) => {
        console.error('Failed to load community certificate:', err);
        this.communityCertViewError = `Failed to load certificate: ${err.error?.detail || err.statusText || 'Unknown error'}`;
        this.communityCertViewLoading = false;
        this.showCommunityCertViewModal = true;
      }
    });
  }

  /**
   * Close community certificate view modal
   */
  closeCommunityCertViewModal(): void {
    this.showCommunityCertViewModal = false;
    // Clean up blob URL
    if (this.communityCertViewBlobUrl) {
      URL.revokeObjectURL(this.communityCertViewBlobUrl);
    }
    this.communityCertViewUrl = null;
    this.communityCertViewBlobUrl = '';
    this.communityCertViewFileName = '';
    this.communityCertViewError = null;
  }

  /**
   * Download community certificate
   */
  downloadCommunityCert(): void {
    if (!this.communityCertViewBlobUrl || !this.communityCertViewFileName) {
      alert('Certificate not loaded');
      return;
    }

    const link = document.createElement('a');
    link.href = this.communityCertViewBlobUrl;
    link.download = this.communityCertViewFileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  /**
   * View profile photo in modal
   */
  viewProfilePhoto(fileId: string): void {
    if (!fileId) {
      this.profilePhotoViewError = 'No file ID provided';
      return;
    }

    this.profilePhotoViewLoading = true;
    this.profilePhotoViewError = null;
    this.profilePhotoViewUrl = null;
    this.profilePhotoViewBlobUrl = '';
    this.profilePhotoViewFileId = fileId;

    this.userApi.getFileThumbnail(fileId).subscribe({
      next: (blob: Blob) => {
        const url = URL.createObjectURL(blob);
        this.profilePhotoViewBlobUrl = url;
        this.profilePhotoViewUrl = this.sanitizer.bypassSecurityTrustUrl(url);
        this.showProfilePhotoViewModal = true;
        this.profilePhotoViewLoading = false;
        console.log('Profile photo loaded successfully:', fileId);
      },
      error: (err: any) => {
        console.error('Failed to load profile photo:', err);
        this.profilePhotoViewError = `Failed to load photo: ${err.error?.detail || 'Unknown error'}`;
        this.profilePhotoViewLoading = false;
        this.showProfilePhotoViewModal = true;
      }
    });
  }

  /**
   * Close profile photo view modal
   */
  closeProfilePhotoViewModal(): void {
    this.showProfilePhotoViewModal = false;
    if (this.profilePhotoViewBlobUrl) {
      URL.revokeObjectURL(this.profilePhotoViewBlobUrl);
    }
    this.profilePhotoViewUrl = null;
    this.profilePhotoViewBlobUrl = '';
    this.profilePhotoViewError = null;
    this.profilePhotoViewFileId = null;
  }

  /**
   * Delete community certificate
   */
  deleteCommunityCert(fileId: string): void {
    if (!this.currentProfile) return;

    if (!confirm('Are you sure you want to delete this community certificate?')) {
      return;
    }

    this.userApi.deleteCommunityCert(fileId, this.currentProfile.profile_id).subscribe({
      next: () => {
        alert('Community certificate deleted successfully');
        // Clear the file ID from current profile
        if (this.currentProfile) {
          this.currentProfile.community_file_id = null;
        }
        this.loadUserProfile(); // Reload to reflect changes
      },
      error: (err: any) => {
        const errorMsg = err.error?.detail || 'Failed to delete certificate';
        alert(`Error: ${errorMsg}`);
      }
    });
  }

  /**
   * Delete profile photo
   */
  deleteProfilePhoto(fileId: string): void {
    if (!this.currentProfile) return;

    if (!confirm('Are you sure you want to delete this photo?')) {
      return;
    }

    this.userApi.deleteProfilePhoto(fileId, this.currentProfile.profile_id).subscribe({
      next: () => {
        alert('Photo deleted successfully');
        // Clear the file ID from current profile
        if (this.currentProfile) {
          if (this.currentProfile.photo_file_id_1 === fileId) {
            this.currentProfile.photo_file_id_1 = null;
          } else if (this.currentProfile.photo_file_id_2 === fileId) {
            this.currentProfile.photo_file_id_2 = null;
          }
        }
        this.loadUserProfile(); // Reload to reflect changes
      },
      error: (err: any) => {
        const errorMsg = err.error?.detail || 'Failed to delete photo';
        alert(`Error: ${errorMsg}`);
      }
    });
  }

  /**
   * Handle community certificate file selection and upload
   */
  handleCommunityCertUpload(event: any): void {
    this.certificateUploadError = null;
    const selectedFiles = event.target.files as FileList;

    if (!selectedFiles || selectedFiles.length === 0) {
      return;
    }

    const file = selectedFiles[0];

    // Validate file type
    const validMimes = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validMimes.includes(file.type)) {
      this.certificateUploadError = 'Invalid file type. Please upload a PDF or image file (JPG, PNG, GIF, WebP).';
      event.target.value = '';
      return;
    }

    // Upload the file
    this.uploadCommunityCertFile(file);
  }

  /**
   * Upload community certificate file
   */
  private uploadCommunityCertFile(file: File): void {
    if (!this.currentProfile) return;

    this.isUploadingCommunityCert = true;
    this.certificateUploadError = null;

    this.userApi.communityCertupload(file, this.currentProfile.profile_id).subscribe({
      next: (response: any) => {
        if (response.status === 'success' && response.file_id) {
          alert('Community certificate uploaded successfully!');
          // Update the current profile with new file ID
          if (this.currentProfile) {
            this.currentProfile.community_file_id = response.file_id;
          }
          this.isUploadingCommunityCert = false;
        } else {
          this.handleCommunityCertUploadError(response);
        }
      },
      error: (err: any) => {
        this.handleCommunityCertUploadError(err);
      }
    });
  }

  /**
   * Handle community certificate upload errors
   */
  private handleCommunityCertUploadError(error: any): void {
    const errorDetail = error.error?.detail || error.message || 'Unknown error';

    let errorMessage = `Failed to upload certificate: ${errorDetail}`;

    if (error.error?.detail) {
      const detail = error.error.detail.toLowerCase();

      if (detail.includes('size_exceeded') || detail.includes('too large')) {
        errorMessage = 'Certificate file is too large. Please use a file smaller than 10MB.';
      } else if (detail.includes('virus_found') || detail.includes('malicious')) {
        errorMessage = 'Certificate file failed security scan. Please try another file.';
      } else if (detail.includes('duplicate_detected')) {
        errorMessage = 'This certificate file has already been uploaded.';
      } else if (detail.includes('no_free_slot')) {
        errorMessage = 'You\'ve reached the maximum file limit. Please delete a file before uploading another.';
      }
    }

    this.certificateUploadError = errorMessage;
    this.isUploadingCommunityCert = false;
    alert(errorMessage);
  }

  /**
   * Handle profile photo file selection and upload
   */
  handleProfilePhotoUpload(event: any): void {
    this.photoUploadError = null;
    const selectedFiles = event.target.files as FileList;

    if (!selectedFiles || selectedFiles.length === 0) {
      return;
    }

    const file = selectedFiles[0];

    // Validate file type
    const validMimes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validMimes.includes(file.type)) {
      this.photoUploadError = 'Invalid file type. Please upload an image file (JPG, PNG, WebP).';
      event.target.value = '';
      return;
    }

    // Upload the file
    this.uploadProfilePhotoFile(file);
  }

  /**
   * Upload profile photo file
   */
  private uploadProfilePhotoFile(file: File): void {
    if (!this.currentProfile) return;

    this.isUploadingProfilePhoto = true;
    this.photoUploadError = null;

    this.userApi.uploadProfilePhoto(file, this.currentProfile.profile_id).subscribe({
      next: (response: any) => {
        if (response.status === 'success' && response.file_id) {
          alert('Photo uploaded successfully!');
          // Update the current profile with new file ID
          if (this.currentProfile) {
            // Assign to available slot (prefer photo_file_id_1, fallback to photo_file_id_2)
            if (!this.currentProfile.photo_file_id_1) {
              this.currentProfile.photo_file_id_1 = response.file_id;
            } else if (!this.currentProfile.photo_file_id_2) {
              this.currentProfile.photo_file_id_2 = response.file_id;
            }
          }
          this.isUploadingProfilePhoto = false;
        } else {
          this.handleProfilePhotoUploadError(response);
        }
      },
      error: (err: any) => {
        this.handleProfilePhotoUploadError(err);
      }
    });
  }

  /**
   * Handle profile photo upload errors
   */
  private handleProfilePhotoUploadError(error: any): void {
    const errorDetail = error.error?.detail || error.message || 'Unknown error';

    let errorMessage = `Failed to upload photo: ${errorDetail}`;

    if (error.error?.detail) {
      const detail = error.error.detail.toLowerCase();

      if (detail.includes('size_exceeded') || detail.includes('too large')) {
        errorMessage = 'Photo file is too large. Please use a smaller image.';
      } else if (detail.includes('virus_found') || detail.includes('malicious')) {
        errorMessage = 'Photo file failed security scan. Please try another image.';
      } else if (detail.includes('no_free_slot') || detail.includes('max') || detail.includes('limit')) {
        errorMessage = 'You\'ve reached the maximum number of photos. Please delete a photo before uploading another.';
      }
    }

    this.photoUploadError = errorMessage;
    this.isUploadingProfilePhoto = false;
    alert(errorMessage);
  }

  /**
   * View horoscope file
   */
  viewHoroscope(fileId: string): void {
    if (!fileId) {
      this.horoscopeViewError = 'No file ID provided';
      return;
    }

    this.horoscopeViewLoading = true;
    this.horoscopeViewError = null;
    this.horoscopeViewUrl = null;
    this.horoscopeViewBlobUrl = '';

    this.userApi.getHoroscope(fileId).subscribe({
      next: (blob: Blob) => {
        const url = URL.createObjectURL(blob);
        this.horoscopeViewBlobUrl = url;
        this.horoscopeViewUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
        this.horoscopeViewFileName = `Horoscope_${this.currentProfile?.serial_number}.pdf`;
        this.showHoroscopeViewModal = true;
        this.horoscopeViewLoading = false;
        console.log('Horoscope loaded successfully:', fileId);
      },
      error: (err: any) => {
        console.error('Failed to load horoscope:', err);
        this.horoscopeViewError = `Failed to load horoscope: ${err.error?.detail || 'Unknown error'}`;
        this.horoscopeViewLoading = false;
        this.showHoroscopeViewModal = true;
      }
    });
  }

  /**
   * Close horoscope view modal
   */
  closeHoroscopeViewModal(): void {
    this.showHoroscopeViewModal = false;
    if (this.horoscopeViewBlobUrl) {
      URL.revokeObjectURL(this.horoscopeViewBlobUrl);
    }
    this.horoscopeViewUrl = null;
    this.horoscopeViewBlobUrl = '';
    this.horoscopeViewFileName = '';
    this.horoscopeViewError = null;
  }

  /**
   * Download horoscope
   */
  downloadHoroscope(): void {
    if (!this.horoscopeViewBlobUrl || !this.horoscopeViewFileName) {
      alert('Horoscope not loaded');
      return;
    }

    const link = document.createElement('a');
    link.href = this.horoscopeViewBlobUrl;
    link.download = this.horoscopeViewFileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  /**
   * Delete horoscope file
   */
  deleteHoroscope(fileId: string): void {
    if (!this.currentProfile) return;

    if (!confirm('Are you sure you want to delete this horoscope?')) {
      return;
    }

    this.userApi.deleteHoroscope(fileId).subscribe({
      next: () => {
        alert('Horoscope deleted successfully');
        // Clear the file ID from current profile
        if (this.currentProfile) {
          this.currentProfile.astrology_file_id = null;
        }
        this.loadUserProfile(); // Reload to reflect changes
      },
      error: (err: any) => {
        const errorMsg = err.error?.detail || 'Failed to delete horoscope';
        alert(`Error: ${errorMsg}`);
      }
    });
  }

  /**
   * Handle horoscope file selection and upload
   */
  handleHoroscopeUpload(event: any): void {
    this.horoscopeUploadError = null;
    const selectedFiles = event.target.files as FileList;

    if (!selectedFiles || selectedFiles.length === 0) {
      return;
    }

    const file = selectedFiles[0];

    // Validate file type
    const validMimes = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validMimes.includes(file.type)) {
      this.horoscopeUploadError = 'Invalid file type. Please upload a PDF or image file (JPG, PNG, GIF, WebP).';
      event.target.value = '';
      return;
    }

    // Upload the file
    this.uploadHoroscopeFile(file);
  }

  /**
   * Upload horoscope file
   */
  private uploadHoroscopeFile(file: File): void {
    if (!this.currentProfile) return;

    this.isUploadingHoroscope = true;
    this.horoscopeUploadError = null;

    this.userApi.uploadHoroscope(file, this.currentProfile.profile_id).subscribe({
      next: (response: any) => {
        if (response.status === 'success' && response.file_id) {
          alert('Horoscope uploaded successfully!');
          // Update the current profile with new file ID
          if (this.currentProfile) {
            this.currentProfile.astrology_file_id = response.file_id;
          }
          this.isUploadingHoroscope = false;
        } else {
          this.handleHoroscopeUploadError(response);
        }
      },
      error: (err: any) => {
        this.handleHoroscopeUploadError(err);
      }
    });
  }

  /**
   * Handle horoscope upload errors
   */
  private handleHoroscopeUploadError(error: any): void {
    const errorDetail = error.error?.detail || error.message || 'Unknown error';

    let errorMessage = `Failed to upload horoscope: ${errorDetail}`;

    if (error.error?.detail) {
      const detail = error.error.detail.toLowerCase();

      if (detail.includes('size_exceeded') || detail.includes('too large')) {
        errorMessage = 'Horoscope file is too large. Please use a file smaller than 10MB.';
      } else if (detail.includes('virus_found') || detail.includes('malicious')) {
        errorMessage = 'Horoscope file failed security scan. Please try another file.';
      } else if (detail.includes('duplicate_detected')) {
        errorMessage = 'This horoscope file has already been uploaded.';
      } else if (detail.includes('no_free_slot')) {
        errorMessage = 'You\'ve reached the maximum file limit. Please delete a file before uploading another.';
      }
    }

    this.horoscopeUploadError = errorMessage;
    this.isUploadingHoroscope = false;
    alert(errorMessage);
  }
}
