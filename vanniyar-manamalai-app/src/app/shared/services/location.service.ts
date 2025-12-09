// src/app/shared/services/location.service.ts

import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { LOCATION_DATA } from '../constants/registration-data.constants';

export interface CountryCode {
  code: string;
  country: string;
}

@Injectable({
  providedIn: 'root'
})
export class LocationService {
  private countryCodes: CountryCode[] = [
    { code: '+91', country: 'India' },
    { code: '+1', country: 'USA' },
    { code: '+44', country: 'UK' },
    { code: '+1-CA', country: 'Canada' },
    { code: '+61', country: 'Australia' },
    { code: '+33', country: 'France' },
    { code: '+49', country: 'Germany' },
    { code: '+39', country: 'Italy' },
    { code: '+34', country: 'Spain' },
    { code: '+81', country: 'Japan' },
    { code: '+86', country: 'China' },
    { code: '+65', country: 'Singapore' },
    { code: '+971', country: 'UAE' },
    { code: '+60', country: 'Malaysia' },
    { code: '+66', country: 'Thailand' },
    { code: '+63', country: 'Philippines' }
  ];

  constructor() {}

  /**
   * Get all available country codes
   */
  getCountryCodes(): Observable<CountryCode[]> {
    return of(this.countryCodes);
  }

  /**
   * Get countries (from location data)
   */
  getCountries(): Observable<string[]> {
    return of(Object.keys(LOCATION_DATA).sort());
  }

  /**
   * Get states for a country
   */
  getStates(country: string): Observable<string[]> {
    const states = LOCATION_DATA[country] ? Object.keys(LOCATION_DATA[country]).sort() : [];
    return of(states);
  }

  /**
   * Get cities for a state and country
   */
  getCities(country: string, state: string): Observable<string[]> {
    const cities = LOCATION_DATA[country]?.[state] || [];
    return of(cities.sort());
  }
}
