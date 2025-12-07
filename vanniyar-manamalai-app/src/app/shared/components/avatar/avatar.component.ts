// src/app/shared/components/avatar/avatar.component.ts

import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-avatar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="avatar" [class]="sizeClass" [ngStyle]="avatarStyle">
      <span class="avatar-text">{{ initials }}</span>
    </div>
  `,
  styles: [`
    .avatar {
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      font-weight: bold;
      color: white;
      overflow: hidden;
    }

    .avatar-text {
      font-size: inherit;
    }

    .avatar.sm {
      width: 32px;
      height: 32px;
      font-size: 12px;
    }

    .avatar.md {
      width: 48px;
      height: 48px;
      font-size: 14px;
    }

    .avatar.lg {
      width: 64px;
      height: 64px;
      font-size: 18px;
    }

    .avatar.xl {
      width: 120px;
      height: 120px;
      font-size: 32px;
    }
  `]
})
export class AvatarComponent implements OnInit {
  @Input() name: string = '';
  @Input() size: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  @Input() photoUrl?: string;

  initials: string = '';
  sizeClass: string = '';
  avatarStyle: any = {};

  ngOnInit(): void {
    this.sizeClass = `avatar ${this.size}`;
    this.generateInitials();
    this.generateColor();
  }

  /**
   * Generate initials from name
   */
  private generateInitials(): void {
    if (!this.name) {
      this.initials = '?';
      return;
    }

    const parts = this.name.trim().split(/\s+/);
    if (parts.length === 1) {
      this.initials = parts[0].substring(0, 1).toUpperCase();
    } else {
      this.initials = (parts[0].substring(0, 1) + parts[parts.length - 1].substring(0, 1)).toUpperCase();
    }
  }

  /**
   * Generate consistent color based on name
   */
  private generateColor(): void {
    if (this.photoUrl) {
      this.avatarStyle = {
        backgroundImage: `url(${this.photoUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      };
      return;
    }

    // Generate color from name hash
    const hash = this.hashCode(this.name);
    const colors = [
      '#667eea', // Purple
      '#764ba2', // Deep Purple
      '#f093fb', // Pink
      '#4facfe', // Blue
      '#00f2fe', // Cyan
      '#43e97b', // Green
      '#fa709a', // Red
      '#fee140', // Yellow
      '#ff6b6b', // Coral
      '#ee5a6f'  // Rose
    ];
    
    const color = colors[Math.abs(hash) % colors.length];
    this.avatarStyle = {
      background: color
    };
  }

  /**
   * Simple hash function for consistent colors
   */
  private hashCode(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return hash;
  }
}
