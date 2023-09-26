import { Component, OnInit, ViewChild } from '@angular/core';
import {Skill} from "../../Models";
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.css']
})
export class SkillsComponent implements OnInit{
  skills: Skill[] = [];
  showAdd: boolean = false;

  constructor(private apiService: ApiService){}

  ngOnInit(): void {
      this.apiService.getSkills().subscribe((skills) => this.skills = skills);
  }

  deleteSkill(skill: Skill){
    this.apiService.deleteSkill(skill).subscribe(() => this.skills = this.skills.filter(t => t.id !== skill.id ) )
  }

  createSkill(skill: Skill){
    this.apiService.createSkill(skill).subscribe((skill: Skill) => this.skills.push(skill));

    this.showAdd = false;
  }

  toggleAdd(){
    this.showAdd = !this.showAdd;
  }
}