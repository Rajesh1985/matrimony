import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  
  constructor(private formBuilder: FormBuilder) {}  backgroundimg='assets/images/gallery/background.png';
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
      // Handle login logic here
      const mobile = this.loginForm.value.mobile;
      // Navigate to user page with mobile
      window.location.href = `/user/${mobile}`;
    } else {
      // Mark all fields as touched to trigger validation display
      Object.keys(this.loginForm.controls).forEach(key => {
        const control = this.loginForm.get(key);
        control?.markAsTouched();
      });
    }
  }
}
