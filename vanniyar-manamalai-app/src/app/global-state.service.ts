import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class GlobalStateService {
  private _profileId: number | null = null;
  private _isUserSignedIn: boolean = false;
  private _isAdmin: boolean = false;

  get profileId(): number | null {
    return this._profileId;
  }
  set profileId(id: number | null) {
    this._profileId = id;
  }

  get isUserSignedIn(): boolean {
    return this._isUserSignedIn;
  }
  set isUserSignedIn(signedIn: boolean) {
    this._isUserSignedIn = signedIn;
  }

  get isAdmin(): boolean {
    return this._isAdmin;
  }
  set isAdmin(val: boolean) {
    this._isAdmin = val;
  }
}
