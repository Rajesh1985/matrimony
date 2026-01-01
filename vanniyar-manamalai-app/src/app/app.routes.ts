import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { AboutUsComponent } from './pages/about-us/about-us.component';
import { SuccessStoriesComponent } from './pages/success-stories/success-stories.component';
import { ContactUsComponent } from './pages/contact-us/contact-us.component';
import { MembershipComponent } from './pages/membership/membership.component';
import { RegistrationComponent } from './pages/registration/registration.component';
import { UserPageComponent } from './pages/user-page/user-page.component';
import { AdminLoginComponent } from './pages/admin-login/admin-login.component';
import { AdminUserPageComponent } from './pages/admin-user-page/admin-user-page.component';  

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'registration', component: RegistrationComponent },
  { path: 'login', component: LoginComponent },
  { path: 'admin-login', component: AdminLoginComponent },
  { path: 'admin-user-page', component: AdminUserPageComponent },
  { path: 'about-us', component: AboutUsComponent },
  { path: 'success-stories', component: SuccessStoriesComponent },
  { path: 'contact-us', component: ContactUsComponent },
  { path: 'membership', component: MembershipComponent },
  { path: 'user-page', component: UserPageComponent },
  { path: '**', redirectTo: '' }
];
