import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
//import { ContactUsComponent } from './pages/contact-us/contact-us.component';

export const routes: Routes = [ // ✅ <-- add 'export' here
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
//  { path: 'contact-us', component: ContactUsComponent },
  { path: '**', redirectTo: '' }
];
