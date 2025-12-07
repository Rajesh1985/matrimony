import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserApiService {
  // private baseUrl = 'http://89.116.134.253:8000';
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
   * Upload file
   * POST /files/upload
   * 
   * Multipart form upload for images and PDFs
   */
  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/files/upload`, formData);
  }

  /**
   * Get file by ID
   * GET /files/{file_id}
   */
  getFileById(file_id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/${file_id}`);
  }

  /**
   * Download file
   * GET /files/{file_id}/download
   * 
   * Returns file blob for download
   */
  downloadFile(file_id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/${file_id}/download`, {
      responseType: 'blob'
    });
  }

  /**
   * Get file thumbnail
   * GET /files/{file_id}/thumbnail
   * 
   * Returns thumbnail image for preview
   */
  getFileThumbnail(file_id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/${file_id}/thumbnail`, {
      responseType: 'blob'
    });
  }

  /**
   * Update file metadata
   * PATCH /files/{file_id}
   * 
   * Update processing status, paths, etc.
   */
  updateFile(file_id: string, fileData: any): Observable<any> {
    return this.http.patch(`${this.baseUrl}/files/${file_id}`, fileData);
  }

  /**
   * Delete file
   * DELETE /files/{file_id}
   */
  deleteFile(file_id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/files/${file_id}`);
  }

  /**
   * Get files by kind (image or pdf)
   * GET /files/kind/{file_kind}
   */
  getFilesByKind(
    file_kind: 'image' | 'pdf',
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(`${this.baseUrl}/files/kind/${file_kind}`, { params });
  }

  /**
   * Get files by processing status
   * GET /files/status/{status}
   * 
   * Status: pending, quarantined, scanning, ready, rejected
   */
  getFilesByStatus(
    status: 'pending' | 'quarantined' | 'scanning' | 'ready' | 'rejected',
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(`${this.baseUrl}/files/status/${status}`, { params });
  }

  /**
   * Get ready (approved) files
   * GET /files/ready/list
   * 
   * Only returns approved files
   */
  getReadyFiles(
    file_kind?: 'image' | 'pdf',
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (file_kind) {
      params = params.set('file_kind', file_kind);
    }

    return this.http.get(`${this.baseUrl}/files/ready/list`, { params });
  }

  /**
   * Get file versions
   * GET /files/{file_id}/versions
   * 
   * Show revision history of file
   */
  getFileVersions(file_id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/${file_id}/versions`);
  }

  /**
   * Approve file (mark as ready)
   * POST /files/{file_id}/approve
   * 
   * Admin operation: Make file visible to users
   */
  approveFile(file_id: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/files/${file_id}/approve`, {});
  }

  /**
   * Reject file
   * POST /files/{file_id}/reject
   * 
   * Admin operation: Block inappropriate file
   */
  rejectFile(file_id: string, reason?: string): Observable<any> {
    const body: any = {};
    if (reason) {
      body.reason = reason;
    }
    return this.http.post(`${this.baseUrl}/files/${file_id}/reject`, body);
  }

  /**
   * Quarantine file for manual review
   * POST /files/{file_id}/quarantine
   */
  quarantineFile(file_id: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/files/${file_id}/quarantine`, {});
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
   * Get large files (admin)
   * GET /files/admin/large-files
   * 
   * Find files consuming storage
   */
  getLargeFiles(
    min_size_mb: number = 10,
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    const params = new HttpParams()
      .set('min_size_mb', min_size_mb.toString())
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get(`${this.baseUrl}/files/admin/large-files`, { params });
  }

  /**
   * Get images by dimensions
   * GET /files/images/dimensions
   * 
   * Filter images by width/height constraints
   */
  getImagesByDimensions(
    min_width?: number,
    max_width?: number,
    min_height?: number,
    max_height?: number,
    skip: number = 0,
    limit: number = 20
  ): Observable<any> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (min_width !== undefined) {
      params = params.set('min_width', min_width.toString());
    }
    if (max_width !== undefined) {
      params = params.set('max_width', max_width.toString());
    }
    if (min_height !== undefined) {
      params = params.set('min_height', min_height.toString());
    }
    if (max_height !== undefined) {
      params = params.set('max_height', max_height.toString());
    }

    return this.http.get(`${this.baseUrl}/files/images/dimensions`, { params });
  }
}
