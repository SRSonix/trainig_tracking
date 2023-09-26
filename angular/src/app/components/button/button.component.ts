import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.css']
})
export class ButtonComponent{
  @Input() text: string = "I am a Button";
  @Input() color: string = "gray";
  @Output() btnClick = new EventEmitter()

  onClick(){
    this.btnClick.emit()
  }
}
