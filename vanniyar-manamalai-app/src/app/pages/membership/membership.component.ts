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
      name: 'Silver',
      cost: '3500',
      views: 'TBD',
      validity: '3 Months',
      features: [
        '3 Months Validity'
      ]
    },
    {
      name: 'Gold',
      cost: '5000',
      views: 'TBD',
      validity: '6 months',
      recommended: true,
      features: [
        '6 Months Validity'
      ]
    },
    {
      name: 'Platinum',
      cost: '7500',
      views: 'TBD',
      validity: '12 months',
      features: [
        '12 Months Validity'
      ]
    }
  ];
}
