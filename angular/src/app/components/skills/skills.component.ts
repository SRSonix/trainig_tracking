import { Component, OnInit } from '@angular/core';
import {Skill} from "../../Models";
import { SkillsService } from 'src/app/services/skills.service';

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.css']
})
export class SkillsComponent implements OnInit{

  skills: Skill[] = [];
  showAdd: boolean = false;

  constructor(private skillService: SkillsService){}

  ngOnInit(): void {
      this.skillService.getSkills().subscribe((skills) => this.skills = skills);
  }

  deleteSkill(skill: Skill){
    this.skillService.deleteSkill(skill).subscribe(() => this.skills = this.skills.filter(t => t.id !== skill.id ) )
  }

  createSkill(skill: Skill){
    this.skillService.createSkill(skill).subscribe((skill: Skill) => this.skills.push(skill));

    this.showAdd = false;
  }

  toggleAdd(){
    console.log("test");
    this.showAdd = !this.showAdd;
  }
}