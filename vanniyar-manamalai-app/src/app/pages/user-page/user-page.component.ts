// src/app/pages/user-page/user-page.component.ts (UPDATED - Address in profiles table)
import '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { FooterComponent } from '../../layout/footer/footer.component';
import { GlobalStateService } from '../../global-state.service';
import { UserPageService, UserProfileComplete, RecommendedProfile } from '../../shared/services/user-page.service';
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

  // Edit modal state
  showEditModal = false;
  editingSection: string | null = null;
  editFormData: any = {};

  constructor(
    private userPageService: UserPageService,
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
        this.loadRecommendedProfiles(profile.user_id);
      },
      error: (err: any) => {
        this.error = `Failed to load profile: ${err.error?.detail || 'Unknown error'}`;
        this.isLoading = false;
        console.error('Profile load error:', err);
      }
    });
  }

  /**
   * Load recommended profiles based on user's partner preferences
   */
  loadRecommendedProfiles(userId: number): void {
    this.userPageService.getRecommendedProfiles(userId, 20).subscribe({
      next: (profiles: RecommendedProfile[]) => {
        // Sort by match score (descending) and then by last updated (descending)
        this.recommendedProfiles = profiles.sort((a, b) => {
          if (b.match_score !== a.match_score) {
            return b.match_score - a.match_score;
          }
          return new Date(b.preferences_updated_at).getTime() - 
                 new Date(a.preferences_updated_at).getTime();
        });
        this.isLoadingRecommendations = false;
      },
      error: (err: any) => {
        console.error('Failed to load recommendations:', err);
        this.recommendedProfiles = [];
        this.isLoadingRecommendations = false;
      }
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
    // TODO: Navigate to profile detail page
    console.log('View profile:', profile);
    // this.router.navigate(['/profile', profile.match_profile_id]);
  }

  /**
   * Send interest to profile (future feature)
   */
  sendInterest(profile: RecommendedProfile): void {
    // TODO: Implement send interest functionality
    alert(`Interest sent to ${profile.name}!`);
  }

  /**
   * Add to favorites (future feature)
   */
  addToFavorites(profile: RecommendedProfile): void {
    // TODO: Implement favorites functionality
    alert(`${profile.name} added to favorites!`);
  }
}
