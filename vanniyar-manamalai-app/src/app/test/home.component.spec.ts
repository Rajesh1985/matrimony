import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { HomeComponent } from '../pages/home/home.component';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: ComponentFixture<HomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Hero Section', () => {
    it('should display hero section with title', () => {
      const heroSection = fixture.debugElement.query(By.css('.hero-section'));
      const title = heroSection.query(By.css('h1')).nativeElement;

      expect(heroSection).toBeTruthy();
      expect(title.textContent).toContain('Chengai Vanniyar Manamalai');
    });

    it('should have background image with correct path', () => {
      const heroImage = fixture.debugElement.query(By.css('.hero-image')).nativeElement;
      expect(heroImage.src).toContain(component.backgroundimg);
    });
  });

  describe('Video Section', () => {
    it('should have video element with correct attributes', () => {
      const video = fixture.debugElement.query(By.css('video')).nativeElement;

      expect(video).toBeTruthy();
      // Check for presence of attributes using hasAttribute
      expect(video.hasAttribute('autoplay')).toBeTruthy();
      expect(video.hasAttribute('muted')).toBeTruthy();
      expect(video.hasAttribute('loop')).toBeTruthy();
    });

    it('should have correct video source', () => {
      const source = fixture.debugElement.query(By.css('video source')).nativeElement;
      expect(source.src).toContain(component.video1Path);
      expect(source.type).toBe('video/mp4');
    });
  });

  describe('Image Carousel', () => {
    it('should have carousel container', () => {
      const carousel = fixture.debugElement.query(By.css('#imageCarousel'));
      expect(carousel).toBeTruthy();
      expect(carousel.classes['carousel']).toBeTruthy();
      expect(carousel.attributes['data-bs-ride']).toBe('carousel');
    });

    it('should have correct number of carousel items', () => {
      const carouselItems = fixture.debugElement.queryAll(By.css('.carousel-item'));
      expect(carouselItems.length).toBe(component.imagemainPath.length);
    });

    it('should have first carousel item active', () => {
      const firstCarouselItem = fixture.debugElement.query(By.css('.carousel-item'));
      expect(firstCarouselItem.classes['active']).toBeTruthy();
    });

    it('should have navigation controls', () => {
      const prevButton = fixture.debugElement.query(By.css('.carousel-control-prev'));
      const nextButton = fixture.debugElement.query(By.css('.carousel-control-next'));

      expect(prevButton).toBeTruthy();
      expect(nextButton).toBeTruthy();
    });
  });

  describe('Registration Form', () => {
    it('should have registration form with required fields', () => {
      const form = fixture.debugElement.query(By.css('form'));
      const nameInput = form.query(By.css('#name')).nativeElement;
      const phoneInput = form.query(By.css('#phone')).nativeElement;

      expect(form).toBeTruthy();
      expect(nameInput.required).toBeTruthy();
      expect(phoneInput.required).toBeTruthy();
    });

    it('should have profile_for select with correct options', () => {
      const select = fixture.debugElement.query(By.css('#profile_for')).nativeElement as HTMLSelectElement;
      const options = Array.from(select.options).map((option: HTMLOptionElement) => option.text);
      const expectedOptions = ['Self', 'Son', 'Daughter', 'Brother', 'Sister', 'Relative', 'Friend'];

      expect(options).toEqual(expectedOptions);
    });

    it('should have register button', () => {
      const button = fixture.debugElement.query(By.css('button[type="submit"]')).nativeElement;
      expect(button.textContent).toContain('REGISTER');
    });
  });
});
