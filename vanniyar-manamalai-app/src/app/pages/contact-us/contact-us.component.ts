import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-contact-us',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './contact-us.component.html',
  styleUrls: ['./contact-us.component.scss']
})
export class ContactUsComponent {
  title = 'Contact Us';
  backgroundimg = 'assets/images/gallery/background.png';
  
  // Location coordinates for Google Maps
  mapLocation = {
    lat: 12.7214,  // Chengalpattu coordinates (approximate)
    lng: 79.9821
  };
}
