// frontend/src/app.spec.ts

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';

import { AppComponent } from './app';
import { ApiService, CurrencyRate } from './services/api.service';

// Feature: Główny komponent aplikacji
describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let mockApiService: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    mockApiService = jasmine.createSpyObj('ApiService', ['getRatesByDate', 'getRatesForDateRange']);

    await TestBed.configureTestingModule({
      imports: [ AppComponent, FormsModule, HttpClientTestingModule ],
      providers: [
        { provide: ApiService, useValue: mockApiService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

  // Scenario: Wyświetlenie tabeli z kursami, gdy dane istnieją
  it('powinien wyświetlić tabelę z kursami, gdy API zwróci poprawne dane', () => {
    // Given: Serwis API jest gotowy zwrócić listę kursów dla wybranej daty
    const mockData: CurrencyRate[] = [
      { id: 1, currency_code: 'TEST', currency_name: 'Testcoin', rate: 5.0, effective_date: '2025-06-06' }
    ];
    mockApiService.getRatesByDate.and.returnValue(of(mockData));

    // When: Użytkownik wybiera datę i inicjuje ładowanie danych
    component.viewMode.set('day');
    component.selectedDate = '2025-06-06';
    component.loadData();

    // Then: Metoda serwisu API zostaje wywołana
    expect(mockApiService.getRatesByDate).toHaveBeenCalledWith('2025-06-06');
    // And: Stan komponentu (sygnał `rates`) zostaje poprawnie zaktualizowany
    expect(component.rates().length).toBe(1);
    expect(component.rates()[0].currency_code).toBe('TEST');
    // And: Stan błędu jest pusty
    expect(component.error()).toBeNull();
  });

  // Scenario: Wyświetlenie komunikatu o błędzie, gdy pobieranie danych się nie powiedzie
  it('powinien wyświetlić komunikat o błędzie, gdy API zwróci błąd', () => {
    // Given: Serwis API jest skonfigurowany, aby zwrócić błąd
    const errorResponse = { status: 500, statusText: 'Server Error' };
    mockApiService.getRatesByDate.and.returnValue(throwError(() => errorResponse));

    // When: Użytkownik inicjuje ładowanie danych
    component.viewMode.set('day');
    component.selectedDate = '2025-06-06';
    component.loadData();

    // Then: Stan błędu w komponencie zostaje ustawiony
    expect(component.error()).not.toBeNull();
    expect(component.error()).toContain('Nie udało się pobrać kursów');
    // And: Lista kursów pozostaje pusta
    expect(component.rates().length).toBe(0);
  });
});