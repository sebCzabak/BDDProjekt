import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface CurrencyRate {
  id: number;
  currency_name: string;
  currency_code: string;
  rate: number;
  effective_date: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  private http = inject(HttpClient);

  
  private readonly apiUrl = '/api';


  getRatesByDate(date: string): Observable<CurrencyRate[]> {
  
    return this.http.get<CurrencyRate[]>(`${this.apiUrl}/currencies/${date}`);
  }

  
  getRatesForDateRange(startDate: string, endDate: string): Observable<CurrencyRate[]> {
    
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
    });
 
    return this.http.get<CurrencyRate[]>(`${this.apiUrl}/currencies?${params.toString()}`);
  }
}