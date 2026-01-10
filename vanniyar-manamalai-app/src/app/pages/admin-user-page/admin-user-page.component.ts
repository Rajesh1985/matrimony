import { Component } from '@angular/core';
// import { MatDialog } from '@angular/material/dialog';
// import { SetMembershipDialogComponent, PlanNameEnum } from './set-membership-dialog.component';
import { CommonModule } from '@angular/common';
import { UserApiService } from '../../user-api.service';
import { UserPageService } from '../../shared/services/user-page.service';

const PAGE_LIMIT = 10;

@Component({
  selector: 'app-admin-user-page',
  templateUrl: './admin-user-page.component.html',
  styleUrls: ['./admin-user-page.component.scss'],
  imports: [CommonModule]
})

export class AdminUserPageComponent {
  readonly PAGE_LIMIT = PAGE_LIMIT;

  activeTab: 'approved' | 'unapproved' | 'expired' = 'approved';
  counts = { approved: 0, unapproved: 0, expired: 0 };
  pages = {
    approved: { offset: 0, page: 1 },
    unapproved: { offset: 0, page: 1 },
    expired: { offset: 0, page: 1 }
  };
  tableData: any[] = [];
  loading = false;
  error = '';

  constructor(
    private userApi: UserApiService,
    private userPageService: UserPageService,
    // private dialog: MatDialog
  ) {}

  setTab(tab: 'approved' | 'unapproved' | 'expired') {
    this.activeTab = tab;
    this.pages[tab] = { offset: 0, page: 1 };
    this.error = '';
    this.tableData = [];
    this.loadCountAndList(tab);
  }

  loadCountAndList(tab: 'approved' | 'unapproved' | 'expired') {
    this.loading = true;
    this.error = '';
    let countApi, listApi;
    if (tab === 'approved') {
      countApi = this.userApi.getApprovedUsersCount();
      listApi = (offset: number) => this.userApi.getApprovedUsers(this.PAGE_LIMIT, offset);
    } else if (tab === 'unapproved') {
      countApi = this.userApi.getUnapprovedUsersCount();
      listApi = (offset: number) => this.userApi.getUnapprovedUsers(this.PAGE_LIMIT, offset);
    } else {
      countApi = this.userApi.getExpiredUsersCount();
      listApi = (offset: number) => this.userApi.getExpiredUsers(this.PAGE_LIMIT, offset);
    }
    countApi.subscribe({
      next: (res) => {
        this.counts[tab] = res.count || 0;
        if (this.counts[tab] > 0) {
          listApi(0).subscribe({
            next: (listRes) => {
              if (Array.isArray(listRes)) {
                this.tableData = listRes;
              } else if (listRes && typeof listRes === 'object' && 'profiles' in listRes && Array.isArray((listRes as any).profiles)) {
                this.tableData = (listRes as any).profiles;
              } else {
                this.tableData = [];
              }
              this.loading = false;
            },
            error: () => {
              this.error = 'Backend error';
              this.loading = false;
            }
          });
        } else {
          this.tableData = [];
          this.error = tab === 'unapproved' ? 'No unapproved users found' : (tab === 'expired' ? 'No expired users found' : 'No approved users found');
          this.loading = false;
        }
      },
      error: () => {
        this.error = 'Backend error';
        this.loading = false;
      }
    });
  }

  nextPage() {
    const tab = this.activeTab;
    if ((this.pages[tab].page * this.PAGE_LIMIT) < this.counts[tab]) {
      this.pages[tab].page++;
      this.pages[tab].offset = (this.pages[tab].page - 1) * this.PAGE_LIMIT;
      this.loadList(tab);
    }
  }

  prevPage() {
    const tab = this.activeTab;
    if (this.pages[tab].page > 1) {
      this.pages[tab].page--;
      this.pages[tab].offset = (this.pages[tab].page - 1) * this.PAGE_LIMIT;
      this.loadList(tab);
    }
  }

  loadList(tab: 'approved' | 'unapproved' | 'expired') {
    this.loading = true;
    this.error = '';
    let listApi;
    if (tab === 'approved') {
      listApi = this.userApi.getApprovedUsers(this.PAGE_LIMIT, this.pages[tab].offset);
    } else if (tab === 'unapproved') {
      listApi = this.userApi.getUnapprovedUsers(this.PAGE_LIMIT, this.pages[tab].offset);
    } else {
      listApi = this.userApi.getExpiredUsers(this.PAGE_LIMIT, this.pages[tab].offset);
    }
    listApi.subscribe({
      next: (listRes) => {
        if (Array.isArray(listRes)) {
          this.tableData = listRes;
        } else if (listRes && typeof listRes === 'object' && 'profiles' in listRes && Array.isArray((listRes as any).profiles)) {
          this.tableData = (listRes as any).profiles;
        } else {
          this.tableData = [];
        }
        this.loading = false;
      },
      error: () => {
        this.error = 'Backend error';
        this.loading = false;
      }
    });
  }

  viewCommunityCert(profile: any) {
    this.userPageService.getCompleteUserProfile(profile.profile_id).subscribe({
      next: (data) => {
        const fileId = data?.community_file_id;
        if (fileId) {
          this.userApi.getCommunityCert(fileId).subscribe({
            next: (blob) => {
              // Open PDF in Angular Material dialog (pseudo-code)
              // this.dialog.open(PdfViewDialog, { data: { blob } });
              const url = URL.createObjectURL(blob);
              window.open(url, '_blank');
            },
            error: () => window.alert('Backend error')
          });
        } else {
          window.alert('No community certificate found');
        }
      },
      error: () => window.alert('Backend error')
    });
  }

  approveProfile(profile: any) {
    this.userApi.updateIsVerifiedbyProfileID(true, profile.profile_id).subscribe({
      next: () => {
        window.alert('Profile approved successfully');
        this.setTab('unapproved');
      },
      error: () => {
        window.alert('Approval failed');
        this.setTab('unapproved');
      }
    });
  }

  openSetMembershipDialog(profile: any) {
    // Fallback to prompt
    const plan = window.prompt('Select membership plan: Silver, Gold, Platinum');
    if (!plan) return;
    this.userApi.getMembership(profile.profile_id).subscribe({
      next: () => {
        this.userApi.updateMembership(profile.profile_id, plan).subscribe({
          next: () => {
            window.alert('Membership updated successfully');
            this.setTab('expired');
          },
          error: () => {
            window.alert('Membership update failed');
            this.setTab('expired');
          }
        });
      },
      error: (err) => {
        if (err.status === 404) {
          this.userApi.createMembership(profile.profile_id, plan).subscribe({
            next: () => {
              window.alert('Membership updated successfully');
              this.setTab('expired');
            },
            error: () => {
              window.alert('Membership update failed');
              this.setTab('expired');
            }
          });
        } else {
          window.alert('Backend error');
        }
      }
    });
  }

  get totalPages(): number {
    return Math.ceil(this.counts[this.activeTab] / this.PAGE_LIMIT);
  }
}
