// src/app/shared/services/user-page.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UserProfileComplete {
  user_id: number;
  profile_id: number;
  serial_number: string;
  name: string;
  email_id: string;
  mobile: string;
  gender: string;
  age: number;
  height_cm: number;
  caste: string;
  religion: string;
  star: string;
  rasi: string;
  lagnam: string;
  birth_place: string;
  occupation: string;
  company_name: string;
  annual_income: string;
  city: string;
  state: string;
  country: string;
  postal_code: string;
  address_line1: string;
  address_line2: string;
  about_me: string;
  hobbies: string;
  physical_status: string;
  marital_status: string;
  food_preference: string;
  complexion: string;
  family_type: string;
  family_status: string;
  brothers: number;
  sisters: number;
  married_brothers: number;
  married_sisters: number;
  father_name: string;
  father_occupation: string;
  mother_name: string;
  mother_occupation: string;
  family_description: string;
  education: string;
  employment_type: string;
  work_location: string;
  education_preference: string;
  occupation_preference: string;
  income_preference: string;
  location_preference: string;
  star_preference: string;
  rasi_preference: string;
  age_from: number;
  age_to: number;
  height_from: number;
  height_to: number;
  preferences_updated_at: string;
  profile_updated_at: string;
  
  // File IDs for photos and documents
  astrology_file_id: string | null;
  community_file_id: string | null;
  photo_file_id_1: string | null;
  photo_file_id_2: string | null;
}

export interface RecommendedProfile {
  match_profile_id: number;
  match_user_id: number;
  serial_number: string;
  name: string;
  age: number;
  height_cm: number;
  gender: string;
  occupation: string;
  star: string;
  rasi: string;
  city: string;
  state: string;
  country: string;
  about_me: string;
  match_score: number;
  photo_file_id_1: string | null;
  photo_file_id_2: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class UserPageService {
  private apiUrl = 'http://89.116.134.253:8000';
  //private apiUrl =  'http://localhost:8000';

  constructor(private http: HttpClient) {}

  /**
   * Get complete user profile from vw_user_profiles_complete view
   */
  getCompleteUserProfile(profileId: number): Observable<UserProfileComplete> {
    return this.http.get<UserProfileComplete>(
      `${this.apiUrl}/profiles/complete/${profileId}`
    );
  }

  /**
   * Get complete user profile by user ID
   */
  getCompleteUserProfileByUserId(userId: number): Observable<UserProfileComplete> {
    return this.http.get<UserProfileComplete>(
      `${this.apiUrl}/profiles/complete-by-user/${userId}`
    );
  }

  /**
   * Get recommended profiles for user based on partner preferences
   */
  getRecommendedProfiles(
    profileId: number,
    limit: number = 20
  ): Observable<RecommendedProfile[]> {
    return this.http.get<RecommendedProfile[]>(
      `${this.apiUrl}/profiles/recommendations/${profileId}?limit=${limit}`
    );
  }

  /**
   * Search profiles with custom criteria
   */
  searchProfiles(criteria: any): Observable<RecommendedProfile[]> {
    return this.http.post<RecommendedProfile[]>(
      `${this.apiUrl}/profiles/search`,
      criteria
    );
  }

  /**
   * Update profile details (personal, address)
   */
  updateProfile(profileId: number, data: any): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/profiles/${profileId}`,
      data
    );
  }

  /**
   * Update professional details
   */
  updateProfessional(profileId: number, data: any): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/profiles/${profileId}/professional`,
      data
    );
  }

  /**
   * Update partner preferences
   */
  updatePartnerPreferences(profileId: number, data: any): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/profiles/${profileId}/partner-preferences`,
      data
    );
  }

  /**
   * Update family details
   */
  updateFamily(profileId: number, data: any): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/profiles/${profileId}/family`,
      data
    );
  }

  /**
   * Update astrology details
   */
  updateAstrology(profileId: number, data: any): Observable<any> {
    return this.http.put(
      `${this.apiUrl}/profiles/${profileId}/astrology`,
      data
    );
  }
}
