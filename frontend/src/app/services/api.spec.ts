import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';

import { AppComponent } from '../app'
import { ApiService, CurrencyRate } from './api.service'


describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let mockApiService: jasmine.SpyObj<ApiService>; 


  beforeEach(async () => {

    mockApiService = jasmine.createSpyObj('ApiService', ['getRatesByDate', 'getRatesForDateRange']);


    await TestBed.configureTestingModule({
      imports: [
        FormsModule,
        HttpClientTestingModule 
      ],
      providers: [
       
        { provide: ApiService, useValue: mockApiService }
      ]
    }).compileComponents();

   
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

 
  it('powinien poprawnie załadować dane i zaktualizować sygnał `rates`', () => {
    
    const mockData: CurrencyRate[] = [
      { id: 1, currency_code: 'TEST', currency_name: 'Testcoin', rate: 5.0, effective_date: '2025-06-06' }
    ];
   
    mockApiService.getRatesByDate.and.returnValue(of(mockData));

   
    component.viewMode.set('day'); 
    component.selectedDate = '2025-06-06';
    component.loadData();

    
    expect(mockApiService.getRatesByDate).toHaveBeenCalledWith('2025-06-06');
   
    expect(component.rates().length).toBe(1);
    expect(component.rates()[0].currency_code).toBe('TEST');
    
    expect(component.error()).toBeNull();
  });

  it('powinien ustawić sygnał `error`, gdy API zwróci błąd', () => {
    
    const errorResponse = { status: 500, statusText: 'Server Error' };
    mockApiService.getRatesByDate.and.returnValue(throwError(() => errorResponse));

    
    component.viewMode.set('day');
    component.selectedDate = '2025-06-06';
    component.loadData();

    
    expect(component.error()).not.toBeNull();
    expect(component.error()).toContain('Nie udało się pobrać kursów');
   
    expect(component.rates().length).toBe(0);
  });
});