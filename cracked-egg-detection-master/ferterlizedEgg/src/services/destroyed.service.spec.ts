import { TestBed } from '@angular/core/testing';

import { DestroyedService } from './destroyed.service';

describe('DestroyedService', () => {
  let service: DestroyedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DestroyedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
