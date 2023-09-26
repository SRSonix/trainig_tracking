import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {Skill} from "../Models";

import {HttpClient, HttpHeaders} from "@angular/common/http"

const httpOptions = {
  headers: new HttpHeaders({
    "Content-Type": "application/json"
  })
}

@Injectable({
  providedIn: 'root'
})
export class SkillsService {
  private apiUrl: string = "http://192.168.178.26:8080/skills/";

  constructor(private http:HttpClient) { }

  getSkills(): Observable<Skill[]>{
    return this.http.get<Skill[]>(this.apiUrl);
  }

  deleteSkill(skill: Skill): Observable<Skill>{
    const url = `${this.apiUrl}${skill.id}`;
    return this.http.delete<Skill>(url);
  }
 
  createSkill(skill: Skill): Observable<Skill>{
    return this.http.post<Skill>(this.apiUrl, skill, httpOptions);
  }
}
