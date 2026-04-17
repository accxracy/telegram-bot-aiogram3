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


INSERT INTO ege_tasks (subject, task_num, condition, solution, answer)
VALUES
 (
 'math',
 1,
 'Какова вероятность того, что случайно выбранный телефонный номер оканчивается двумя чётными цифрами?',
 'Вероятность четной цифры 0.5. Две цифры подряд: 0.5 * 0.5 = 0.25.',
 '0.25'
 ),
 (
 'math',
 2,
 'В понедельник акции компании подорожали на некоторое количество процентов, а во вторник подешевели на то же самое количество процентов. В результате они стали стоить на 4 % дешевле, чем при открытии торгов в понедельник. На сколько процентов подорожали акции компании в понедельник?',
 'Обозначим первоначальную стоимость акций за 1. Пусть в понедельник акции компании подорожали на c * 100 % и их стоимость стала составлять 1 + c * 1. Во вторник акции подешевели на c * 100 % и их стоимость стала составлять 1 + c - c (1 + c) . В результате они стали стоить на 4 % дешевле, чем при открытии торгов в понедельник, то есть 0,96. Таким образом, 1 + c - c(1+c) = 0,96 <=> 1 - c^2 = 0,96 <=> c^2 = 0,04 <=> c = 0.2',
 '20'
 ),
 (
  'math',
  3,
  'В магазине стоят два платёжных терминала. Каждый из них может быть неисправен с вероятностью 0,1 независимо от другого. Найдите вероятность того, что ровно один терминал из двух оказался неисправен, а другой работает.',
  '1. Вероятность неисправности P(A_fail) = 0,1. 2. Вероятность исправности P(A_ok) = 1 - 0,1 = 0,9. 3. Событие "ровно один неисправен" состоит из двух взаимоисключающих исходов: а) Первый неисправен, второй исправен: P1 = P(A_fail) * P(B_ok) = 0,1 * 0,9 = 0,09. б) Первый исправен, второй неисправен: P2 = P(A_ok) * P(B_fail) = 0,9 * 0,1 = 0,09. 4. Искомая вероятность - сумма этих вероятностей: P = P1 + P2 = 0,09 + 0,09 = 0,18.',
  '0.18'
 ),
 (
 'math',
 4,
 'Найдите наибольшее значение функции y = 16 - 8x + ln(4x) + ln(2) на отрезке [1/9; 2/15]',
 $$1. y' = -8 + (1/(4x))*4 = -8 + 1/x = (1-8x)/x.
2. y' = 0 при x = 1/8.
3. Точка 1/8 (0.125) принадлежит отрезку [1/9; 2/15] (примерно [0.111; 0.133]).
4. При x < 1/8 производная положительная, при x > 1/8 - отрицательная. Значит, x=1/8 - точка максимума.
5. Наибольшее значение будет в этой точке:
 y(1/8) = 16 - 8*(1/8) + ln(4*1/8) + ln(2) = 16 - 1 + ln(1/2) + ln(2) = 15 - ln(2) + ln(2) = 15.$$,
 '15'
 ),
 (

  'physics',
  5,
  'Танк движется со скоростью v1 = 18 км/ч, а грузовик — со скоростью v2 = 72 км/ч. Масса танка m = 36000 кг. Отношение величины импульса танка к величине импульса грузовика равно 2,25. Чему равна масса грузовика? Ответ дайте в килограммах.',
  'Импульс танка: p1 = m * v1. Импульс грузовика: p2 = M * v2, где M — масса грузовика. По условию p1 / p2 = 2,25. Подставим выражения для импульсов: (m * v1) / (M * v2) = 2,25. Отсюда M = (m * v1) / (2,25 * v2). Подставим значения: M = (36000 * 18) / (2,25 * 72) = 4000 кг.',
  '4000'
 )
ON CONFLICT (subject, condition) DO NOTHING;