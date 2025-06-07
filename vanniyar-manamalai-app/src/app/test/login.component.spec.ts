import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginComponent } from '../pages/login/login.component';
import { RouterTestingModule } from '@angular/router/testing';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        LoginComponent,
        RouterTestingModule,
        ReactiveFormsModule,
        FormsModule
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    component.ngOnInit(); // Initialize the form
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have a login form', () => {
    expect(component.loginForm).toBeTruthy();
  });

  describe('Form Validation', () => {
    it('should mark form as invalid when empty', () => {
      expect(component.loginForm.valid).toBeFalsy();
    });

    it('should validate email format', () => {
      const emailControl = component.loginForm.get('email');
      emailControl?.setValue('invalid-email');
      expect(emailControl?.errors?.['email']).toBeTruthy();

      emailControl?.setValue('valid@email.com');
      expect(emailControl?.errors).toBeNull();
    });

    it('should validate password minimum length', () => {
      const passwordControl = component.loginForm.get('password');
      passwordControl?.setValue('12345');
      expect(passwordControl?.errors?.['minlength']).toBeTruthy();

      passwordControl?.setValue('123456');
      expect(passwordControl?.errors).toBeNull();
    });

    it('should mark form as valid with proper data', () => {
      const form = component.loginForm;
      form.get('email')?.setValue('test@example.com');
      form.get('password')?.setValue('password123');
      expect(form.valid).toBeTruthy();
    });
  });

  describe('Form Submission', () => {
    it('should call onSubmit when form is submitted', () => {
      const form = component.loginForm;
      const submitSpy = jest.spyOn(component, 'onSubmit');
      
      form.get('email')?.setValue('test@example.com');
      form.get('password')?.setValue('password123');
      
      const button = fixture.nativeElement.querySelector('button[type="submit"]');
      button.click();
      
      expect(submitSpy).toHaveBeenCalled();
    });

    it('should mark all fields as touched on invalid submission', () => {
      component.onSubmit();
      
      expect(component.loginForm.get('email')?.touched).toBeTruthy();
      expect(component.loginForm.get('password')?.touched).toBeTruthy();
    });
  });

  describe('UI Elements', () => {
    it('should have login form elements', () => {
      const compiled = fixture.nativeElement;
      expect(compiled.querySelector('form')).toBeTruthy();
      expect(compiled.querySelector('input[type="email"]')).toBeTruthy();
      expect(compiled.querySelector('input[type="password"]')).toBeTruthy();
      expect(compiled.querySelector('button[type="submit"]')).toBeTruthy();
    });

    it('should show validation errors when fields are touched', () => {
      const form = component.loginForm;
      const emailControl = form.get('email');
      const passwordControl = form.get('password');

      emailControl?.setValue('');
      emailControl?.markAsTouched();
      passwordControl?.setValue('');
      passwordControl?.markAsTouched();

      fixture.detectChanges();
      
      expect(form.get('email')?.errors?.['required']).toBeTruthy();
      expect(form.get('password')?.errors?.['required']).toBeTruthy();
    });
  });
});
