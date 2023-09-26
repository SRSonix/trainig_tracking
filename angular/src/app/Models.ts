export interface ExerciseId{
    id: string;
    variation: string;
}

export interface Skill{
    id: string;
    description: string;
    excercise_ids: ExerciseId[];
}

export interface Exercise{
    id: string;
    variation: string;
    description: string;
    skill_ids: string[];
}
