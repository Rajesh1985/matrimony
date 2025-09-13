import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserApiService } from '../../user-api.service';
import { GlobalStateService } from '../../global-state.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-page.component.html',
  styleUrl: './user-page.component.scss'
})
export class UserPageComponent implements OnInit {
  userData: any = null;
  error: string | null = null;

  constructor(
    private userApi: UserApiService,
    private globalState: GlobalStateService,
    private router: Router
  ) {}

  ngOnInit() {
    const profileId = this.globalState.profileId;
    const isSignedIn = this.globalState.isUserSignedIn;
    if (isSignedIn && profileId) {
      this.userApi.getProfileById(profileId).subscribe(
        (res) => {
          this.userData = {
            name: res.name,
            birth_date: res.birth_date,
            height_cm: res.height_cm,
            caste: res.caste,
            sub_caste: res.sub_caste,
            mobile_number: res.mobile_number
          };
        },
        (err) => {
          this.globalState.isUserSignedIn = false;
          this.globalState.profileId = null;
          this.error = 'Failed to load user data.';
          this.router.navigate(['/login']);
        }
      );
      this.userApi.getAddressByProfileId(profileId).subscribe(address => {
        this.userData.address = address[0];
      });
      this.userApi.getAstrologyByProfileId(profileId).subscribe(astrology => {
        this.userData.astrology = astrology[0];
      });
      this.userApi.getFamilyByProfileId(profileId).subscribe(family => {
        this.userData.family = family[0];
      });
      this.userApi.getEducationsByProfileId(profileId).subscribe(education => {
        this.userData.education = education[0];
      });
      this.userApi.getProfessionalByProfileId(profileId).subscribe(professional => {
        this.userData.professional = professional[0];
      });
      this.userApi.getPartnerPreferencesByProfileId(profileId).subscribe(partner_preferences => {
        this.userData.partner_preferences = partner_preferences[0];
      });
    } else {
      this.globalState.isUserSignedIn = false;
      this.globalState.profileId = null;
      this.error = 'User not signed in or profile ID missing.';
      this.router.navigate(['/login']);
    }
  }
}
