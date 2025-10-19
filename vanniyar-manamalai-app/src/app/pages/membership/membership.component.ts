import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface MembershipPlan {
  name: string;
  cost: string;
  views: string;
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
      cost: 'TBD',
      views: 'TBD',
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
      cost: 'TBD',
      views: 'TBD',
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
      cost: 'TBD',
      views: 'TBD',
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
