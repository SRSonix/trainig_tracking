import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs'; 
import { UiService } from 'src/app/services/ui.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent{
  title: string = "Training-Tracker"
  showAddTask: boolean;
  subscription: Subscription;
  
  constructor(private uiService: UiService, private router: Router){
    this.subscription = this.uiService.onToggle().subscribe( (showAddTask) => this.showAddTask = showAddTask)
    this.showAddTask = this.uiService.getShowAddTask();
  }

  toggleAddSkill(){
    this.uiService.toggelAddTask();
  }

  hasRoute(route: string){
    return this.router.url === route;
  }
}
