import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { NavbarComponent } from '../../layout/navbar/navbar.component';
import { FooterComponent } from '../../layout/footer/footer.component';
import { CommonModule } from '@angular/common';
import { register } from 'swiper/element/bundle';

register();

interface Story {
  img: string;
  couple: string;
  testimonial: string;
  link: string;
}

@Component({
  selector: 'app-success-stories',
  standalone: true,
  imports: [NavbarComponent, FooterComponent, CommonModule],
  templateUrl: './success-stories.component.html',
  styleUrl: './success-stories.component.scss',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class SuccessStoriesComponent {
  title = 'Success Stories';
  backgroundimg = 'assets/images/gallery/background.png';

  stories: Story[] = [
    {
      img: 'assets/images/gallery/1.jpg',
      couple: 'Ramesh & Priya',
      testimonial: 'We are extremely happy with the match we found through this platform. Our families connected instantly, and we knew it was meant to be. The traditional values and modern approach of this platform made our journey special.',
      link: '#'
    },
    {
      img: 'assets/images/gallery/2.jpg',
      couple: 'Karthik & Deepa',
      testimonial: 'As parents, we were looking for a platform that understands our community values. Through Chengai Vanniyar Manamalai, we found the perfect match for our daughter. The verification process gave us great confidence.',
      link: '#'
    },
    {
      img: 'assets/images/gallery/3.jpg',
      couple: 'Suresh & Kavitha',
      testimonial: 'Finding a life partner who shares the same cultural values was important to us. This platform helped us connect with the right family. The journey from matching to marriage was smooth and memorable.',
      link: '#'
    },
    {
      img: 'assets/images/gallery/4.jpg',
      couple: 'Kumar & Lakshmi',
      testimonial: 'We are grateful to have found each other through this platform. The authentic profiles and easy communication process made our search for a life partner much simpler. Thank you for helping us start our journey together.',
      link: '#'
    }
  ];  swiperConfig = {
    slidesPerView: 1,
    spaceBetween: 30,
    navigation: {
      enabled: true,
      prevEl: '.swiper-button-prev',
      nextEl: '.swiper-button-next',
      hideOnClick: false
    },
    pagination: {
      enabled: true,
      el: '.swiper-pagination',
      clickable: true,
      type: 'bullets',
      bulletClass: 'swiper-pagination-bullet',
      bulletActiveClass: 'swiper-pagination-bullet-active'
    },
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
      pauseOnMouseEnter: true
    },
    loop: true,
    effect: 'fade',
    fadeEffect: {
      crossFade: true
    },
    initialSlide: 0
  };
}
