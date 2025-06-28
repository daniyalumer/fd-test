import { Component, OnInit } from '@angular/core';
import { WeatherService } from '../../services/weather.service';
import { CitySelectorComponent } from '../city-selector/city-selector.component';
import { ForecastChartComponent } from '../forecast-chart/forecast-chart.component';
import { UnitToggleComponent } from '../unit-toggle/unit-toggle.component';
import { CurrentWeatherComponent } from '../current-weather/current-weather.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-weather-dashboard',
  templateUrl: './weather-dashboard.component.html',
  styleUrls: ['./weather-dashboard.component.css'],
  standalone: true,
  imports: [
    CommonModule,
    CitySelectorComponent,
    ForecastChartComponent,
    UnitToggleComponent,
    CurrentWeatherComponent
  ]
})
export class WeatherDashboardComponent {
  selectedCity = 'paris';
  currentWeather: any = null;
  forecast: any[] = [];
  unit: 'C' | 'F' = 'C';

  constructor(private weatherService: WeatherService) {}

  ngOnInit() {
    this.fetchWeather();
    this.fetchForecast();
  }

  onCityChange(city: string) {
    this.selectedCity = city;
    this.fetchWeather();
    this.fetchForecast();
  }

  onUnitChange(unit: 'C' | 'F') {
    this.unit = unit;
  }

  fetchWeather() {
    this.weatherService.getCurrentWeather(this.selectedCity).subscribe(data => {
      this.currentWeather = {
        location: data.location,
        temperature: data.current_weather.temperature,
        condition: data.current_weather.condition,
        humidity: data.current_weather.humidity,
        windSpeed: data.current_weather.wind_speed,
        feelsLike: data.current_weather.feels_like
      };
    });
  }

  fetchForecast() {
    this.weatherService.getForecast(this.selectedCity).subscribe(data => {
      console.log('Forecast API response:', data); // Add this line
      this.forecast = data.hourly_forecast.map((slot: any) => ({
        time: slot.time,
        temp: slot.temperature_2m,
        condition: slot.condition,
        precipProbability: slot.precipitation_probability,
        feelsLike: slot.feels_like
      }));
      console.log('Mapped forecast:', this.forecast); // Add this line
    });
  }
}