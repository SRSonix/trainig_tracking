CREATE TABLE skills(
    id VARCHAR(32) NOT NULL PRIMARY KEY,
    description text
);

CREATE TABLE exercises (
    id VARCHAR(32) NOT NULL,
    variation VARCHAR(32) NOT NULL,
    description text,
    PRIMARY KEY(id, variation)
);

CREATE TABLE exercise_skill (
  exercise_id VARCHAR(32) NOT NULL,
  variation VARCHAR(32) NOT NULL,
  skill_id VARCHAR(32) NOT NULL REFERENCES skills (id),
  primary key (exercise_id, variation, skill_id),
  FOREIGN KEY (exercise_id, variation) REFERENCES exercises (id, variation)
);
