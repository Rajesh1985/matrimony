import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserApiService {
  //private baseUrl = 'http://89.116.134.253:8000';
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // ============================================================
  // PROFILES - Matrimony Profile Management
  // ============================================================

  /**
   * Create new matrimony profile
   * POST /profiles/
   */
  createNewProfile(profileData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/profiles/`, profileData);
  }

  /**
   * Get profile by ID
   * GET /profiles/{profile_id}
   */
  getProfileById(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/profiles/${profile_id}`);
  }

  /**
   * Get profile_id by mobile number
   * GET /profiles/profile_id_by_mobile/{mobile}
   */
  getProfileIdByMobileRoute(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/profiles/profile_id_by_mobile/${mobile}`);
  }

  /**
   * Update profile (by ID)
   * PATCH /profiles/{profile_id}
   */
  updateProfile(profile_id: number, profileData: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/profiles/${profile_id}`, profileData);
  }

  /**
   * Delete profile
   * DELETE /profiles/{profile_id}
   */
  deleteProfile(profile_id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/profiles/${profile_id}`);
  }

  // ============================================================
  // USERS - User Account Management
  // ============================================================

  /**
   * Check if user exists by mobile
   * GET /users/exists/{mobile}
   */
  isUserExists(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/exists/${mobile}`);
  }

  /**
   * Register new user
   * POST /users/
   */
  registerUser(userData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/`, userData);
  }

  /**
   * Get profile_id by mobile number
   * GET /users/profile_id/{mobile}
   */
  getProfileIdByMobile(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/profile_id/${mobile}`);
  }

  /**
   * Get user by mobile number
   * GET /users/mobile/{mobile}
   */
  getUserByMobile(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/mobile/${mobile}`);
  }

  /**
   * Get user by user ID
   * GET /users/{user_id}
   */
  getUserById(user_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/${user_id}`);
  }

  /**
   * Assign profile_id to user (after profile creation)
   * PUT /users/profile_id/{mobile}?profile_id=...
   */
  updateProfileIdByMobile(mobile: string, profile_id: number): Observable<any> {
    return this.http.put(
      `${this.baseUrl}/users/profile_id/${mobile}?profile_id=${profile_id}`,
      null
    );
  }

  updateIsVerifiedbyProfileID(is_verified: boolean, profile_id: number): Observable<any> {
      return this.http.put(
      `${this.baseUrl}/users/is_verified/profile/${profile_id}?is_verified=${is_verified}`,
      null
    );
  }  

  updateSerialNumberByProfileID(serial_number: string, profile_id: number): Observable<any> {
      return this.http.put(
      `${this.baseUrl}/profiles/serial_number/${profile_id}?serial_number=${serial_number}`,
      null
    );
  } 

  /**
   * Update user details (name, email, gender - excludes profile_id)
   * PATCH /users/{user_id}
   */
  updateUser(user_id: number, userData: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/users/${user_id}`, userData);
  }

  /**
   * Update mobile number by profile_id
   * PATCH /users/mobile/profile/{profile_id}
   * 
   * Allows user to change phone number from profile context.
   * Resets is_verified to False (must re-verify new number)
   */
  updateMobileByProfileId(
    profile_id: number,
    new_mobile: string,
    otp_code?: string
  ): Observable<any> {
    const body: any = { new_mobile };
    if (otp_code) {
      body.otp_code = otp_code;
    }
    return this.http.patch(
      `${this.baseUrl}/users/mobile/profile/${profile_id}`,
      body
    );
  }

  /**
   * Update password
   * PATCH /users/{user_id}/password
   */
  updatePassword(
    user_id: number,
    old_password: string,
    new_password: string
  ): Observable<any> {
    return this.http.patch(`${this.baseUrl}/users/${user_id}/password`, {
      old_password,
      new_password
    });
  }

  /**
   * Generate OTP for mobile verification
   * POST /users/generate_otp
   */
  generateOtp(mobile: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/generate_otp`, { mobile });
  }

  /**
   * Verify OTP
   * POST /users/verify_otp
   */
  verifyOtp(mobile: string, otp_code: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/verify_otp`, {
      mobile,
      otp_code
    });
  }

  /**
   * User login
   * POST /users/login
   */
  validateUser(mobile: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/login`, {
      mobile,
      password
    });
  }

  /**
   * Delete user account
   * DELETE /users/{user_id}
   */
  deleteUser(user_id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/users/${user_id}`);
  }

  // ============================================================
  // ASTROLOGY DETAILS - Astrological Information
  // ============================================================

  /**
   * Create astrology details
   * POST /astrology/
   */
  createAstrology(astrologyData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/astrology/`, astrologyData);
  }

  /**
   * Get astrology by ID
   * GET /astrology/{astrology_id}
   */
  getAstrologyById(astrology_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/astrology/${astrology_id}`);
  }

  /**
   * Get astrology by profile ID
   * GET /astrology/profile/{profile_id}
   */
  getAstrologyByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/astrology/profile/${profile_id}`);
  }

  /**
   * Update astrology by ID
   * PATCH /astrology/{astrology_id}
   */
  updateAstrology(astrology_id: number, data: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/astrology/${astrology_id}`, data);
  }

  /**
   * Update astrology by profile ID
   * PATCH /astrology/profile/{profile_id}
   * 
   * Simpler API: Update using profile_id instead of astrology_id
   */
  updateAstrologyByProfileId(profile_id: number, data: any): Observable<any> {
    return this.http.patch(
      `${this.baseUrl}/astrology/profile/${profile_id}`,
      data
    );
  }

  /**
   * Delete astrology by ID
   * DELETE /astrology/{astrology_id}
   */
  deleteAstrology(astrology_id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/astrology/${astrology_id}`);
  }

  /**
   * Delete astrology by profile ID
   * DELETE /astrology/profile/{profile_id}
   */
  deleteAstrologyByProfileId(profile_id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/astrology/profile/${profile_id}`
    );
  }

  // ============================================================
  // FAMILY DETAILS - Family Background Information
  // ============================================================

  /**
   * Create family details
   * POST /family/
   */
  createFamily(familyData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/family/`, familyData);
  }

  /**
   * Get family by ID
   * GET /family/{family_id}
   */
  getFamilyById(family_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/family/${family_id}`);
  }

  /**
   * Get family by profile ID
   * GET /family/profile/{profile_id}
   */
  getFamilyByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/family/profile/${profile_id}`);
  }

  /**
   * Update family by ID
   * PATCH /family/{family_id}
   */
  updateFamily(family_id: number, data: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/family/${family_id}`, data);
  }

  /**
   * Update family by profile ID
   * PATCH /family/profile/{profile_id}
   * 
   * Simpler API: Update using profile_id instead of family_id
   * Use cases: Parent occupation change, sibling marriage update
   */
  updateFamilyByProfileId(profile_id: number, data: any): Observable<any> {
    return this.http.patch(
      `${this.baseUrl}/family/profile/${profile_id}`,
      data
    );
  }

  /**
   * Delete family by ID
   * DELETE /family/{family_id}
   */
  deleteFamily(family_id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/family/${family_id}`);
  }

  /**
   * Delete family by profile ID
   * DELETE /family/profile/{profile_id}
   */
  deleteFamilyByProfileId(profile_id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/family/profile/${profile_id}`);
  }

  /**
   * Get family summary (computed properties)
   * GET /family/profile/{profile_id}/summary
   * 
   * Returns: total_siblings, married_siblings, unmarried counts
   */
  getFamilySummary(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/family/profile/${profile_id}/summary`);
  }

  // ============================================================
  // PARTNER PREFERENCES - What Partner You're Looking For
  // ============================================================

  /**
   * Create partner preferences
   * POST /partner-preferences/
   */
  createPartnerPreferences(preferencesData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/partner-preferences/`, preferencesData);
  }

  /**
   * Get partner preferences by ID
   * GET /partner-preferences/{preferences_id}
   */
  getPartnerPreferencesById(preferences_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/partner-preferences/${preferences_id}`);
  }

  /**
   * Get partner preferences by profile ID
   * GET /partner-preferences/profile/{profile_id}
   */
  getPartnerPreferencesByProfileId(profile_id: number): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/partner-preferences/profile/${profile_id}`
    );
  }

  /**
   * Update partner preferences by ID
   * PATCH /partner-preferences/{preferences_id}
   */
  updatePartnerPreferences(preferences_id: number, data: any): Observable<any> {
    return this.http.patch(
      `${this.baseUrl}/partner-preferences/${preferences_id}`,
      data
    );
  }

  /**
   * Update partner preferences by profile ID
   * PATCH /partner-preferences/profile/{profile_id}
   * 
   * Simpler API: Update using profile_id instead of preferences_id
   * Use cases: Age adjustment, location change, income update
   */
  updatePartnerPreferencesByProfileId(
    profile_id: number,
    data: any
  ): Observable<any> {
    return this.http.patch(
      `${this.baseUrl}/partner-preferences/profile/${profile_id}`,
      data
    );
  }

  /**
   * Delete partner preferences by ID
   * DELETE /partner-preferences/{preferences_id}
   */
  deletePartnerPreferences(preferences_id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/partner-preferences/${preferences_id}`
    );
  }

  /**
   * Delete partner preferences by profile ID
   * DELETE /partner-preferences/profile/{profile_id}
   */
  deletePartnerPreferencesByProfileId(profile_id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/partner-preferences/profile/${profile_id}`
    );
  }

  /**
   * Get preference options for dropdowns
   * GET /partner-preferences/options/list
   */
  getPartnerPreferenceOptions(): Observable<any> {
    return this.http.get(`${this.baseUrl}/partner-preferences/options/list`);
  }

  /**
   * Find matching profiles
   * GET /partner-preferences/matches/{profile_id}
   */
  getMatchingProfiles(
    profile_id: number,
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(
      `${this.baseUrl}/partner-preferences/matches/${profile_id}`,
      { params }
    );
  }

  // ============================================================
  // PROFESSIONAL DETAILS - Career and Education Information
  // ============================================================

  /**
   * Create professional details
   * POST /professional/
   */
  createProfessional(professionalData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/professional/`, professionalData);
  }

  /**
   * Get professional by ID
   * GET /professional/{professional_id}
   */
  getProfessionalById(professional_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/professional/${professional_id}`);
  }

  /**
   * Get professional by profile ID
   * GET /professional/profile/{profile_id}
   */
  getProfessionalByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/professional/profile/${profile_id}`);
  }

  /**
   * Update professional by ID
   * PATCH /professional/{professional_id}
   */
  updateProfessional(professional_id: number, data: any): Observable<any> {
    return this.http.patch(
      `${this.baseUrl}/professional/${professional_id}`,
      data
    );
  }

  /**
   * Update professional by profile ID
   * PATCH /professional/profile/{profile_id}
   * 
   * Simpler API: Update using profile_id instead of professional_id
   * Use cases: Job change, salary increase, MBA completion, relocation
   */
  updateProfessionalByProfileId(profile_id: number, data: any): Observable<any> {
    return this.http.patch(
      `${this.baseUrl}/professional/profile/${profile_id}`,
      data
    );
  }

  /**
   * Delete professional by ID
   * DELETE /professional/{professional_id}
   */
  deleteProfessional(professional_id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/professional/${professional_id}`
    );
  }

  /**
   * Delete professional by profile ID
   * DELETE /professional/profile/{profile_id}
   */
  deleteProfessionalByProfileId(profile_id: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/professional/profile/${profile_id}`
    );
  }

  /**
   * Get professional summary (computed/formatted)
   * GET /professional/profile/{profile_id}/summary
   * 
   * Returns: education_summary, employment_summary, income_summary, flags
   */
  getProfessionalSummary(profile_id: number): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/professional/profile/${profile_id}/summary`
    );
  }

  /**
   * Get professional options for dropdowns
   * GET /professional/options/list
   */
  getProfessionalOptions(): Observable<any> {
    return this.http.get(`${this.baseUrl}/professional/options/list`);
  }

  /**
   * Search professionals by education
   * GET /professional/search/by-education/{education}
   */
  searchProfessionalsByEducation(
    education: string,
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(
      `${this.baseUrl}/professional/search/by-education/${education}`,
      { params }
    );
  }

  /**
   * Search professionals by occupation
   * GET /professional/search/by-occupation/{occupation}
   */
  searchProfessionalsByOccupation(
    occupation: string,
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(
      `${this.baseUrl}/professional/search/by-occupation/${occupation}`,
      { params }
    );
  }

  /**
   * Search professionals by work location
   * GET /professional/search/by-location/{work_location}
   */
  searchProfessionalsByLocation(
    work_location: string,
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(
      `${this.baseUrl}/professional/search/by-location/${work_location}`,
      { params }
    );
  }

  // ============================================================
  // FILES - File Management (Profile Photos, Documents, PDFs)
  // ============================================================

  /**
   * Upload profile photo
   * POST /files/upload/profile-photo
   * 
   * Upload and process family photo with validation, virus scanning, and WebP conversion
   * 
   * Workflow:
   * 1. Validate file size (max 10MB)
   * 2. Validate MIME type (JPEG, PNG, WebP only)
   * 3. Calculate SHA256 checksum for duplicate detection
   * 4. Check for existing duplicate file
   * 5. Save to quarantine directory
   * 6. Scan for viruses with ClamAV
   * 7. Convert to WebP with EXIF preservation
   * 8. Generate thumbnail (150x150 WebP)
   * 9. Determine available photo slot (1 or 2)
   * 10. Move file to permanent storage
   * 11. Create database record
   * 12. Assign to family_details photo slot
   * 
   * @param file - Image file (JPEG, PNG, WebP)
   * @param profileId - Profile ID to assign photo to
   * @returns Observable with response: { status, file_id, thumbnail_url, profile_id, message } or error
   */
  uploadProfilePhoto(file: File, profileId: number): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(
      `${this.baseUrl}/files/upload/profile-photo?profile_id=${profileId}`,
      formData
    );
  }



  /**
   * Delete profile photo
   * DELETE /files/{file_id}
   * 
   * Delete photo from profile and remove from disk
   * 
   * @param fileId - File ID to delete
   * @param profileId - Profile ID (for verification)
   * @returns Observable with response: { status, file_id, message } or error
   */
  deleteProfilePhoto(fileId: string, profileId: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/files/${fileId}?profile_id=${profileId}`
    );
  }

  /**
   * Get file thumbnail
   * GET /files/{file_id}/thumbnail
   * 
   * Purpose: Serve thumbnail for image preview
   * 
   * Returns the thumbnail image blob (WebP format) for preview purposes.
   * Backend returns FileResponse with thumbnail file from disk.
   * 
   * Response Type:
   * - Media Type: image/webp (WebP thumbnail format)
   * - Size: 150x150 pixels
   * - Format: WebP (optimized for web)
   * 
   * Error Handling:
   * - 404 File not found: Invalid file_id
   * - 404 Thumbnail not available: File exists but has no thumbnail
   * - 404 Thumbnail not found on disk: Thumbnail file missing from storage
   * 
   * Use Cases:
   * - Gallery thumbnails (150x150 WebP)
   * - Profile photo preview
   * - PDF first page preview
   * 
   * @param file_id - File ID to get thumbnail for
   * @returns Observable<Blob> - Thumbnail image blob (WebP format)
   * 
   * Example Usage:
   * ```typescript
   * this.userApi.getFileThumbnail('uuid-string').subscribe(
   *   (blob: Blob) => {
   *     const url = URL.createObjectURL(blob);
   *     this.thumbnailUrl = this.sanitizer.bypassSecurityTrustUrl(url);
   *   },
   *   (error) => console.error('Failed to load thumbnail:', error)
   * );
   * ```
   */
  getFileThumbnail(file_id: string): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/files/${file_id}/thumbnail`, {
      responseType: 'blob'
    });
  }


  /**
   * Get file system statistics (admin)
   * GET /files/admin/statistics
   * 
   * Returns: total files, storage used, files by kind/status
   */
  getFileStatistics(): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/admin/statistics`);
  }

  /**
   * Upload community certificate (PDF or image)
   * POST /files/upload/comm-cert
   * 
   * Uploads a community certificate file (PDF or image).
   * Backend processes:
   * 1. Validate file size < 10MB
   * 2. Validate file type (PDF, JPEG, PNG, GIF, WebP)
   * 3. Scan for viruses with ClamAV
   * 4. Convert images to PDF (if needed)
   * 5. Check for duplicates
   * 6. Store file with UUID
   * 7. Auto-link to family_details.community_file_id
   * 
   * @param file - File to upload (PDF or image)
   * @param profileId - Profile ID to associate file with
   * @returns Observable with response: { status, file_id, filename, profile_id } or error
   */
  communityCertupload(file: File, profileId: number): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(
      `${this.baseUrl}/files/upload/comm-cert?profile_id=${profileId}`,
      formData
    );
  }

  /**
   * Get community certificate file
   * GET /files/{file_id}/comm-cert
   * 
   * Purpose: Retrieve and serve community certificate file
   * 
   * Returns the community certificate file (PDF or converted image format).
   * Backend returns FileResponse with certificate file from disk.
   * 
   * Response Type:
   * - Media Type: application/pdf or image/* (based on file type)
   * - Format: PDF or image format as stored
   * 
   * Error Handling:
   * - 404 File not found: Invalid file_id
   * - 404 Certificate not found: File exists but not a certificate
   * - 403 Forbidden: Profile ID mismatch or no permission
   * 
   * Use Cases:
   * - Download community certificate
   * - View/preview certificate
   * - Verify certificate authenticity
   * 
   * @param fileId - File ID to retrieve certificate for
   * @returns Observable<Blob> - Certificate file blob
   * 
   * Example Usage:
   * ```typescript
   * this.userApi.getCommunityCert('uuid-string').subscribe(
   *   (blob: Blob) => {
   *     const url = URL.createObjectURL(blob);
   *     // Download or preview the file
   *   },
   *   (error) => console.error('Failed to load certificate:', error)
   * );
   * ```
   */
  getCommunityCert(fileId: string): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/files/${fileId}/comm-cert`, {
      responseType: 'blob'
    });
  }

  /**
   * Delete community certificate
   * DELETE /files/delete/comm-cert/{file_id}
   * 
   * Delete community certificate file and auto-unlink from family_details.community_file_id
   * 
   * @param fileId - File ID to delete
   * @param profileId - Profile ID (for verification)
   * @returns Observable with response: { status, message } or error
   */
  deleteCommunityCert(fileId: string, profileId: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/files/delete/comm-cert/${fileId}?profile_id=${profileId}`
    );
  }

  /**
   * Upload horoscope file (PDF or image)
   * POST /files/upload/horoscope
   * 
   * Uploads a horoscope file (PDF or image).
   * Backend processes:
   * 1. Validate file size < 10MB
   * 2. Validate file type (PDF, JPEG, PNG, GIF, WebP)
   * 3. Scan for viruses with ClamAV
   * 4. Convert images to PDF (if needed)
   * 5. Check for duplicates
   * 6. Store file with UUID
   * 7. Auto-link to astrology_details.file_id
   * 
   * @param file - File to upload (PDF or image)
   * @param profileId - Profile ID to associate file with
   * @returns Observable with response: { status, file_id, filename, profile_id } or error
   */
  uploadHoroscope(file: File, profileId: number): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(
      `${this.baseUrl}/files/upload/horoscope?profile_id=${profileId}`,
      formData
    );
  }

  /**
   * Get horoscope file
   * GET /files/{file_id}/horoscope
   * 
   * Purpose: Retrieve and serve horoscope file
   * 
   * Returns the horoscope file (PDF) for download/preview.
   * 
   * @param fileId - File ID to retrieve horoscope for
   * @returns Observable<Blob> - Horoscope file blob
   */
  getHoroscope(fileId: string): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/files/${fileId}/horoscope`, {
      responseType: 'blob'
    });
  }

  /**
   * Delete horoscope file
   * DELETE /files/delete/horoscope/{file_id}
   * 
   * Delete horoscope file and auto-unlink from astrology_details.file_id
   * 
   * @param fileId - File ID to delete
   * @returns Observable with response: { status, message } or error
   */
  deleteHoroscope(fileId: string): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/files/delete/horoscope/${fileId}`
    );
  }
}