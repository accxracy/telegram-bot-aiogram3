CREATE TABLE IF NOT EXISTS neuro_history (
  id SERIAL PRIMARY KEY,
  telegram_id BIGINT NOT NULL,
  username VARCHAR(50),
  prompt TEXT NOT NULL,
  answer TEXT NOT NULL,
  model VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS neuro_usage (
  id SERIAL PRIMARY KEY,
  telegram_id BIGINT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ege_tasks (
  id SERIAL PRIMARY KEY,
  subject VARCHAR(20) NOT NULL,
  task_num INTEGER NOT NULL,
  condition TEXT NOT NULL,
  solution TEXT NOT NULL,
  answer VARCHAR(255) NOT NULL,
  photo_id VARCHAR(255),

  CONSTRAINT unique_task UNIQUE (subject, condition)
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  telegram_id BIGINT UNIQUE NOT NULL,
  username VARCHAR(50),
  solved INT DEFAULT 0,
  unsolved INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_solved_tasks (
  user_id INT NOT NULL,
  task_id INT NOT NULL,

  CONSTRAINT fk_user
    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_task
    FOREIGN KEY(task_id)
    REFERENCES ege_tasks(id)
    ON DELETE CASCADE,

  PRIMARY KEY (user_id, task_id)
);


