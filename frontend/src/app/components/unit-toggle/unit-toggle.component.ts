import { Component, EventEmitter, Output, Input } from '@angular/core';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

@Component({
  selector: 'app-unit-toggle',
  templateUrl: './unit-toggle.component.html',
  styleUrls: ['./unit-toggle.component.css'],
  standalone: true,
  imports: [MatButtonToggleModule]
})
export class UnitToggleComponent {
  @Input() unit: 'C' | 'F' = 'C';
  @Output() unitChange = new EventEmitter<'C' | 'F'>();

  onToggle(unit: 'C' | 'F') {
    this.unit = unit;
    this.unitChange.emit(unit);
  }
}