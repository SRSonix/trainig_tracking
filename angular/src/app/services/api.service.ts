import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {Skill, Exercise} from "../Models";

import {HttpClient, HttpHeaders} from "@angular/common/http"

const httpOptions = {
  headers: new HttpHeaders({
    "Content-Type": "application/json"
  })
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl: string = "http://192.168.178.26:8080";

  constructor(private http:HttpClient) { }

  getSkills(): Observable<Skill[]>{
    const url = `${this.apiUrl}/skills`;
    return this.http.get<Skill[]>(url);
  }
  deleteSkill(skill: Skill): Observable<Skill>{
    const url = `${this.apiUrl}/skills/${skill.id}`;
    return this.http.delete<Skill>(url);
  }
 
  createSkill(skill: Skill): Observable<Skill>{
    const url = `${this.apiUrl}/skills`;
    return this.http.post<Skill>(url, skill, httpOptions);
  }
  
  getExercises(): Observable<Exercise[]>{
    const url = `${this.apiUrl}/exercises`;
    return this.http.get<Exercise[]>(url);
  }
  
}
