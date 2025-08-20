import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserApiService } from '../../user-api.service';

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss']
})
export class UserPageComponent implements OnInit {
  mobile: string = '';
  userProfile: any = {};
  profileId: number | null = null;
  isLoading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private userApi: UserApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.mobile = this.route.snapshot.paramMap.get('mobile') || '';
    if (!this.mobile) {
      this.router.navigate(['/login']);
      return;
    }
    // Get profile id
    this.userApi.getProfileIdByMobileRoute(this.mobile).subscribe(
      (resp: any) => {
        this.profileId = resp?.profile_id;
        if (this.profileId) {
          this.userApi.getProfileById(this.profileId).subscribe(
            (profile: any) => {
              this.userProfile = profile;
              this.isLoading = false;
            },
            () => { this.isLoading = false; }
          );
        } else {
          this.isLoading = false;
        }
      },
      () => { this.isLoading = false; }
    );
  }

  editProfile() {
    // Implement navigation to edit profile page
    alert('Edit Profile feature coming soon!');
  }
}
