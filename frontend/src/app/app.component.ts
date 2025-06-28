import { Component } from '@angular/core';
import { WeatherDashboardComponent } from './components/weather-dashboard/weather-dashboard.component';

@Component({
  selector: 'app-root',
  template: `<app-weather-dashboard></app-weather-dashboard>`,
  standalone: true,
  imports: [WeatherDashboardComponent]
})
export class AppComponent {}