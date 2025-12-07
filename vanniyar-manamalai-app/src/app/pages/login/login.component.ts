import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { UserApiService } from '../../user-api.service';
import { GlobalStateService } from '../../global-state.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loginError: string | null = null;
  constructor(
    private formBuilder: FormBuilder,
    private userApi: UserApiService,
    private globalState: GlobalStateService,
    private router: Router
  ) {}
  backgroundimg='assets/images/gallery/background.png';
  video1Path='assets/videos/wedding-intro.mp4';

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      country_code: ['+91', Validators.required],
      mobile: ['', [Validators.required, Validators.pattern('[0-9]{10}')]],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const mobile = this.loginForm.value.mobile;
      const password = this.loginForm.value.password;
      this.userApi.validateUser(mobile, password).subscribe(
        (res) => {
          console.log('Validation response:', res);
          if (res.success) {
            this.globalState.profileId = res.profile_id;
            this.globalState.isUserSignedIn = true;
            console.log('Login successful, profileId:', res.profile_id);
            this.router.navigate(['/user-page']);
          } else {
            console.log('Login failed: Invalid mobile or password');
            this.loginError = 'Invalid mobile or password';
          }
        },
        (err) => {
          console.error('Login error:', err);
          this.loginError = 'Login failed. Please try again.';
        }
      );
    } else {
      Object.keys(this.loginForm.controls).forEach(key => {
        const control = this.loginForm.get(key);
        control?.markAsTouched();
      });
    }
  }
}
