import { Component } from '@angular/core';
import { RouterModule, Router } from '@angular/router'; 
import { CommonModule } from '@angular/common';
import { GlobalStateService } from '../../global-state.service';

@Component({
  selector: 'app-navbar',
  imports: [RouterModule, CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  logo = 'assets/images/gallery/logo.jpg';
  logo1 = 'assets/images/gallery/logo1.jpeg';

  constructor(public globalState: GlobalStateService, public router: Router) {}

  get showLogout(): boolean {
    return this.globalState.isUserSignedIn && this.globalState.profileId !== null && this.globalState.profileId > 0;
  }

  logout() {
    this.globalState.isUserSignedIn = false;
    this.globalState.profileId = null;
    window.location.href = '/login';
  }
}
