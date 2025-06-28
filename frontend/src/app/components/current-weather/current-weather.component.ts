import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-current-weather',
  templateUrl: './current-weather.component.html',
  styleUrls: ['./current-weather.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class CurrentWeatherComponent {
  @Input() currentWeather: any = null;
  @Input() unit: 'C' | 'F' = 'C';

  toUnit(temp: number): number {
    return this.unit === 'C' ? temp : (temp * 9/5 + 32);
  }
}