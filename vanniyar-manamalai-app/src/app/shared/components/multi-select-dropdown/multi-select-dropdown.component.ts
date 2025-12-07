// src/app/shared/components/multi-select-dropdown/multi-select-dropdown.component.ts

import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface DropdownOption {
  value: string;
  label: string;
}

@Component({
  selector: 'app-multi-select-dropdown',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="multi-select-container">
      <div class="multi-select-header" (click)="toggleDropdown()">
        <span class="selected-label">
          {{ selectedCount === 0 ? placeholder : selectedCount + ' selected' }}
        </span>
        <span class="dropdown-icon" [class.open]="isOpen">▼</span>
      </div>

      <div class="multi-select-dropdown" *ngIf="isOpen">
        <div class="select-all-option" *ngIf="showSelectAll">
          <label class="checkbox-label">
            <input
              type="checkbox"
              [checked]="isAllSelected()"
              (change)="toggleSelectAll()"
              class="checkbox-input"
            />
            <span>Select All</span>
          </label>
        </div>

        <div class="dropdown-item" *ngFor="let option of options">
          <label class="checkbox-label">
            <input
              type="checkbox"
              [checked]="isSelected(option.value)"
              (change)="toggleOption(option.value)"
              class="checkbox-input"
            />
            <span>{{ option.label }}</span>
          </label>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .multi-select-container {
      position: relative;
      width: 100%;
    }

    .multi-select-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      padding: 12px 14px;
      font-size: 14px;
      border: 2px solid #e0e0e0;
      border-radius: 6px;
      background: white;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        border-color: #667eea;
      }

      &:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
      }
    }

    .selected-label {
      color: #333;
      font-weight: 500;
    }

    .dropdown-icon {
      color: #667eea;
      transition: transform 0.3s ease;

      &.open {
        transform: rotate(180deg);
      }
    }

    .multi-select-dropdown {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: white;
      border: 2px solid #667eea;
      border-top: none;
      border-radius: 0 0 6px 6px;
      max-height: 300px;
      overflow-y: auto;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .select-all-option {
      padding: 10px 14px;
      border-bottom: 1px solid #e0e0e0;
      background: #f9f9f9;
    }

    .dropdown-item {
      padding: 10px 14px;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }
    }

    .checkbox-label {
      display: flex;
      align-items: center;
      cursor: pointer;
      font-size: 14px;
      margin: 0;

      .checkbox-input {
        margin-right: 8px;
        width: 16px;
        height: 16px;
        cursor: pointer;
      }

      span {
        color: #333;
      }
    }
  `]
})
export class MultiSelectDropdownComponent implements OnInit {
  @Input() options: DropdownOption[] = [];
  @Input() selectedValues: string[] = [];
  @Input() placeholder: string = 'Select options';
  @Input() showSelectAll: boolean = false;
  @Output() selectionChanged = new EventEmitter<string[]>();

  isOpen: boolean = false;

  ngOnInit(): void {
    if (!this.selectedValues) {
      this.selectedValues = [];
    }
  }

  toggleDropdown(): void {
    this.isOpen = !this.isOpen;
  }

  toggleOption(value: string): void {
    const index = this.selectedValues.indexOf(value);
    if (index > -1) {
      this.selectedValues.splice(index, 1);
    } else {
      this.selectedValues.push(value);
    }
    this.selectionChanged.emit([...this.selectedValues]);
  }

  isSelected(value: string): boolean {
    return this.selectedValues.includes(value);
  }

  isAllSelected(): boolean {
    return this.options.length > 0 && this.selectedValues.length === this.options.length;
  }

  toggleSelectAll(): void {
    if (this.isAllSelected()) {
      this.selectedValues = [];
    } else {
      this.selectedValues = this.options.map(opt => opt.value);
    }
    this.selectionChanged.emit([...this.selectedValues]);
  }

  get selectedCount(): number {
    return this.selectedValues.length;
  }
}
