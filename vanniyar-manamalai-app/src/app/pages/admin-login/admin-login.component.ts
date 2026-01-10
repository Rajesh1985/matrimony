import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { UserApiService } from '../../user-api.service';
import { GlobalStateService } from '../../global-state.service';

@Component({
  selector: 'admin-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './admin-login.component.html',
  styleUrl: './admin-login.component.scss'
})
export class AdminLoginComponent implements OnInit {
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
      username: ['', [Validators.required]],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const username = this.loginForm.value.username;
      const password = this.loginForm.value.password;
      this.userApi.validateAdminUser(username, password).subscribe(
        (res) => {
          console.log('Validation response:', res);
          if (res.valid) {
            this.globalState.isAdmin = true;
            console.log('Admin Login successful:');
            this.router.navigate(['/admin-user-page']);
          } else {
            console.log('Admin Login failed: Invalid username or password');
            this.loginError = 'Invalid username or password';
          }
        },
        (err) => {
          console.error('Admin Login error:', err);
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
