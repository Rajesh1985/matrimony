import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface MembershipPlan {
  name: string;
  cost: number;
  views: number;
  validity: string;
  features: string[];
  recommended?: boolean;
}

@Component({
  selector: 'app-membership',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './membership.component.html',
  styleUrls: ['./membership.component.scss']
})
export class MembershipComponent {
  backgroundimg = 'assets/images/gallery/background.png';
  
  plans: MembershipPlan[] = [
    {
      name: 'Basic',
      cost: 1000,
      views: 25,
      validity: '1 month',
      features: [
        '25 Profile Views',
        '1 Month Validity',
        'Basic Support',
        'Access to Basic Search'
      ]
    },
    {
      name: 'Elite',
      cost: 2500,
      views: 100,
      validity: '6 months',
      recommended: true,
      features: [
        '100 Profile Views',
        '6 Months Validity',
        'Priority Support',
        'Advanced Search Features',
        'Featured Profile Listing'
      ]
    },
    {
      name: 'Premium',
      cost: 5000,
      views: 500,
      validity: '12 months',
      features: [
        '500 Profile Views',
        '12 Months Validity',
        'On Call Support 24/7',
        'Premium Search Features',
        'Featured Profile Listing',
        'Priority Match Alerts',
        'Personal Relationship Manager'
      ]
    }
  ];
}
