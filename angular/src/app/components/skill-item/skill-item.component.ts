import { Component, Input, EventEmitter, Output} from '@angular/core';
import { Skill } from 'src/app/Models';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-skill-item',
  templateUrl: './skill-item.component.html',
  styleUrls: ['./skill-item.component.css']
})
export class SkillItemComponent {
  @Input() skill: Skill;
  @Output() onDeleteSkill = new EventEmitter();

  iconClose = faTimes;
  expanded: boolean = false;

  toggleExpand(){
    this.expanded = !this.expanded;
  }

  onDelete(event: any){
    this.onDeleteSkill.emit()

    event.stopPropagation()
  }
}
