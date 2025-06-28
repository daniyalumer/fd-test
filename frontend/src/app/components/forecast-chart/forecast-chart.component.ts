import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration } from 'chart.js';

@Component({
  selector: 'app-forecast-chart',
  templateUrl: './forecast-chart.component.html',
  styleUrls: ['./forecast-chart.component.css'],
  standalone: true,
  imports: [CommonModule, BaseChartDirective]
})
export class ForecastChartComponent {
  @Input() forecast: any[] = [];
  @Input() unit: 'C' | 'F' = 'C';

  get chartData(): ChartConfiguration<'line'>['data'] {
    const temps = this.forecast.map(slot =>
      this.unit === 'C'
        ? slot.temp
        : (slot.temp * 9/5 + 32)
    );
    return {
      labels: this.forecast.map(slot => slot.time),
      datasets: [
        {
          data: temps,
          label: `Temperature (${this.unit === 'C' ? '°C' : '°F'})`,
          fill: false,
          borderColor: '#1976d2',
          tension: 0.3
        }
      ]
    };
  }
}