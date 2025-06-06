import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { ApiService, CurrencyRate } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class AppComponent {
  private apiService = inject(ApiService);

  public rates = signal<CurrencyRate[]>([]);
  public isLoading = signal(false);
  public error = signal<string | null>(null);

  
  public viewMode = signal<'day' | 'month' | 'quarter' | 'year'>('day');

  
  public selectedDate: string = new Date().toISOString().split('T')[0];
  public selectedMonth: string = new Date().toISOString().substring(0, 7);
  public selectedYear: number = new Date().getFullYear();
  public selectedQuarter: 1 | 2 | 3 | 4 = 1;

  
  loadData(): void {
    this.isLoading.set(true);
    this.error.set(null);
    this.rates.set([]);

    
    switch(this.viewMode()) {
      case 'day':
        this.loadRatesForDay();
        break;
      case 'month':
        this.loadRatesForMonth();
        break;
      case 'quarter':
        this.loadRatesForQuarter();
        break;
      case 'year':
        this.loadRatesForYear();
        break;
    }
  }

  private loadRatesForDay(): void {
    this.apiService.getRatesByDate(this.selectedDate).subscribe({
      next: (data) => this.handleSuccess(data),
      error: (err) => this.handleError(`dla daty ${this.selectedDate}`, err)
    });
  }

  private loadRatesForMonth(): void {
    const [year, month] = this.selectedMonth.split('-').map(Number);
    const startDate = new Date(year, month - 1, 1);
    const endDate = new Date(year, month, 0);
    this.fetchDataForRange(startDate, endDate, `dla miesiąca ${this.selectedMonth}`);
  }

  // === NOWE METODY ===
  private loadRatesForQuarter(): void {
    const year = this.selectedYear;
    const startMonth = (this.selectedQuarter - 1) * 3; // Q1->0, Q2->3, Q3->6, Q4->9
    const startDate = new Date(year, startMonth, 1);
    const endDate = new Date(year, startMonth + 3, 0);
    this.fetchDataForRange(startDate, endDate, `dla Q${this.selectedQuarter} ${year}`);
  }

  private loadRatesForYear(): void {
    const year = this.selectedYear;
    const startDate = new Date(year, 0, 1);  
    const endDate = new Date(year, 11, 31); 
    this.fetchDataForRange(startDate, endDate, `dla roku ${year}`);
  }

  
  private fetchDataForRange(startDate: Date, endDate: Date, periodLabel: string): void {
    const formattedStartDate = startDate.toLocaleDateString('en-CA');
    const formattedEndDate = endDate.toLocaleDateString('en-CA');

    this.apiService.getRatesForDateRange(formattedStartDate, formattedEndDate).subscribe({
      next: (data) => this.handleSuccess(data),
      error: (err) => this.handleError(periodLabel, err)
    });
  }

  private handleSuccess(data: CurrencyRate[]): void {
    this.rates.set(data);
    this.isLoading.set(false);
    if (data.length === 0) {
      this.error.set("Brak danych dla wybranego okresu.");
    }
  }

  private handleError(period: string, error: any): void {
    console.error(`Wystąpił błąd:`, error);
    this.error.set(`Nie udało się pobrać kursów ${period}. Sprawdź, czy dane dla tego okresu istnieją.`);
    this.isLoading.set(false);
  }
}