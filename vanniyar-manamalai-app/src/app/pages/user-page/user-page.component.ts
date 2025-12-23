// src/app/pages/user-page/user-page.component.ts (UPDATED - Address in profiles table)
import '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { FooterComponent } from '../../layout/footer/footer.component';
import { GlobalStateService } from '../../global-state.service';
import { UserPageService, UserProfileComplete, RecommendedProfile } from '../../shared/services/user-page.service';
import { UserApiService } from '../../user-api.service';
import { AvatarComponent } from '../../shared/components/avatar/avatar.component';

@Component({
  selector: 'app-user-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    NavbarComponent,
    FooterComponent,
    AvatarComponent
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

  constructor(
    private userPageService: UserPageService,
    private userApi: UserApiService,
    private sanitizer: DomSanitizer,
    private globalState: GlobalStateService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadUserProfile();
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
        this.loadRecommendedProfiles(profile.profile_id);
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
  formatDate(date: string): string {
    if (!date) return 'N/A';
    return new Date(date).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
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
        this.editFormData = {
          height_cm: this.currentProfile?.height_cm,
          physical_status: this.currentProfile?.physical_status,
          complexion: this.currentProfile?.complexion,
          hobbies: this.currentProfile?.hobbies,
          about_me: this.currentProfile?.about_me
        };
        break;

      case 'professional':
        this.editFormData = {
          education: this.currentProfile?.education,
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
          birth_place: this.currentProfile?.birth_place
        };
        break;

      case 'address':
        this.editFormData = {
          address_line1: this.currentProfile?.address_line1,
          address_line2: this.currentProfile?.address_line2,
          city: this.currentProfile?.city,
          state: this.currentProfile?.state,
          country: this.currentProfile?.country,
          postal_code: this.currentProfile?.postal_code
        };
        break;

      case 'preferences':
        this.editFormData = {
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

    switch (this.editingSection) {
      case 'personal':
      case 'address':
        // Both personal and address are in profiles table
        updateObservable = this.userPageService.updateProfile(profileId, this.editFormData);
        break;
      case 'professional':
        updateObservable = this.userPageService.updateProfessional(profileId, this.editFormData);
        break;
      case 'family':
        updateObservable = this.userPageService.updateFamily(profileId, this.editFormData);
        break;
      case 'astrology':
        updateObservable = this.userPageService.updateAstrology(profileId, this.editFormData);
        break;
      case 'preferences':
        updateObservable = this.userPageService.updatePartnerPreferences(profileId, this.editFormData);
        break;
    }

    if (updateObservable) {
      updateObservable.subscribe({
        next: () => {
          alert('Section updated successfully!');
          this.closeEditModal();
          this.loadUserProfile(); // Reload profile
        },
        error: (err: any) => {
          alert(`Failed to update: ${err.error?.detail || 'Unknown error'}`);
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
}
