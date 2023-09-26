import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { Skill, Exercise, ExerciseId } from 'src/app/Models';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-add-skill',
  templateUrl: './add-skill.component.html',
  styleUrls: ['./add-skill.component.css']
})
export class AddSkillComponent implements OnInit{
  id: string;
  description: string;
  exercises: Map<Exercise, boolean> = new Map<Exercise, boolean>();

  @Output() onCreateSkill: EventEmitter<Skill> = new EventEmitter()

  constructor(private apiService: ApiService){};

  ngOnInit(): void {
      this.refresh()
  }

  refresh() {
    this.exercises.clear()
    this.apiService.getExercises().subscribe((exercieses) => {

      exercieses.forEach((exerciese) => this.exercises.set(exerciese, false))
    });

    this.id = "";
    this.description = "";
  }

  toggleExercise(exercise: Exercise){
    this.exercises.set(exercise, !this.exercises.get(exercise))
  }

  onSubmit() {
    if (!this.id){
      alert("add id")
      return
    }

    let exercise_ids: ExerciseId[] = []
    this.exercises.forEach((isactive, exercise) => {
      if (isactive){
        exercise_ids.push({"id":exercise.id, "variation":exercise.variation})
      }
    });

    const newSkill: Skill = {
      id: this.id,
      description: this.description,
      excercise_ids: exercise_ids
    }

    this.onCreateSkill.emit(newSkill);

    this.refresh()
  }
}
