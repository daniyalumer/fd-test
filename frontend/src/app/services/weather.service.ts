import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class WeatherService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getCurrentWeather(city: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/weather/${city}`);
  }

  getForecast(city: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/forecast/${city}`);
  }
}