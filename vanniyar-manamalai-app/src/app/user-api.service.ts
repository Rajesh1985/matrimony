import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  createNewProfile(profileData: any): Observable<any> {
    // Calls backend /profiles endpoint to create a new profile
    return this.http.post(`${this.baseUrl}/profiles/`, profileData);
  }

  updateProfileIdByMobile(mobile: string, profile_id: number): Observable<any> {
    // Calls backend endpoint to update profile_id by mobile
    // Assuming endpoint: /users/update-profile-id/{mobile}
    // Pass profile_id in body
    return this.http.put(`${this.baseUrl}/users/profile_id/${mobile}?profile_id=${profile_id}`, null);
  }
  isUserExists(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/exists/${mobile}`);
  }
  
  registerUser(userData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/`, userData);
  }
  getProfileIdByMobile(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/profile_id/${mobile}`);
  }

  getUserByMobile(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/${mobile}`);
  }

  getProfileById(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/profiles/${profile_id}`);
  }

  createAddress(addressData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/addresses/`, addressData);
  }

  getAddressByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/addresses/profile/${profile_id}`);
  }

  createEducations(educationData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/education/`, educationData);
  }

  getEducationsByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/education/profile/${profile_id}`);
  }

  createAstrology(astrologyData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/astrology/`, astrologyData);
  }

  getAstrologyByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/astrology/profile/${profile_id}`);
  }

  createFamily(familyData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/family/`, familyData);
  }

  getFamilyByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/family/profile/${profile_id}`);
  }

  createPartnerPreferences(preferencesData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/partner-preferences/`, preferencesData);
  }

  getPartnerPreferencesByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/partner-preferences/profile/${profile_id}`);
  }

  createProfessional(professionalData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/professional/`, professionalData);
  }

  getProfessionalByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/professional/profile/${profile_id}`);
  }

  createProfilePhoto(photoData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/profile-photos/`, photoData);
  }

  getProfilePhotoByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/profile-photos/profile/${profile_id}`);
  }

  createProperty(propertyData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/properties/`, propertyData);
  }

  getPropertyByProfileId(profile_id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/properties/profile/${profile_id}`);
  }

  getProfileIdByMobileRoute(mobile: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/profiles/profile_id_by_mobile/${mobile}`);
  }
}
