import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EggsInfoComponent } from './eggs-info.component';

describe('EggsInfoComponent', () => {
  let component: EggsInfoComponent;
  let fixture: ComponentFixture<EggsInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EggsInfoComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EggsInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
