import { Component } from '@angular/core';
import { NgForOf } from '@angular/common';
import { UserApiService } from '../../user-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NgForOf],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  imagemainPath = ['assets/images/gallery/1.jpg',
    'assets/images/gallery/2.jpg',
    'assets/images/gallery/3.jpg',
    'assets/images/gallery/4.jpg'];
  video1Path = 'assets/videos/wedding-intro.mp4';
  backgroundimg = 'assets/images/gallery/background.png';
  message: string = '';
  constructor(private userApi: UserApiService, private router: Router) {}

  onRegister() {
    const nameInput = (document.getElementById('name') as HTMLInputElement)?.value?.trim();
    const mobileInput = (document.getElementById('phone') as HTMLInputElement)?.value?.trim();

    // Validate mobile: 10 digits
    if (!/^\d{10}$/.test(mobileInput)) {
      alert('Please enter a valid 10-digit mobile number.');
      return;
    }

    // Validate name: alphabets and spaces only
    if (!/^[A-Za-z ]+$/.test(nameInput)) {
      alert('Name should contain only alphabets and spaces.');
      return;
    }

    this.userApi.isUserExists(mobileInput).subscribe(
      res => {
        console.log('GET:', res);
        if (res.exists) {
          alert('User already exists with this mobile number.');
        } else {
          // Route to registration page
          this.router.navigate(['/registration']);
        }
      });
  }
}
