import { Component, EventEmitter, Output } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-city-selector',
  templateUrl: './city-selector.component.html',
  styleUrls: ['./city-selector.component.css'],
  standalone: true,
  imports: [CommonModule, MatFormFieldModule, MatSelectModule]
})
export class CitySelectorComponent {
  cities = [
    { name: 'Berlin', value: 'berlin' },
    { name: 'London', value: 'london' },
    { name: 'Paris', value: 'paris' }
  ];

  selectedCity = this.cities[0].value;

  @Output() cityChange = new EventEmitter<string>();

  onCityChange(city: string) {
    this.selectedCity = city;
    this.cityChange.emit(city);
  }
}