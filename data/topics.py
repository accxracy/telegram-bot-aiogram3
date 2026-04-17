

TOPICS = {
  '🏃 Кинематика': {
    'description': 'Кинематика: движение тел',
    'theory': """
- <b>Механическое движение. СО. Траектория, путь и перемещение</b>
https://videouroki.net/video/1-miekhanichieskoie-dvizhieniie-so-traiektoriia-put-i-pieriemieshchieniie.html \n
- <b>Скорость при РПД</b>
https://videouroki.net/video/2-skorost-pri-rpd.html \n
- <b>Прямолинейное равноускоренное движение. Ускорение</b>
https://videouroki.net/video/3-priamolinieinoie-ravnouskoriennoie-dvizhieniie-uskorieniie.html \n
- <b>Скорость при прямолинейном равноускоренном движении</b>
https://videouroki.net/video/4-skorost-pri-priamolinieinom-ravnouskoriennom-dvizhienii.html \n
- <b>Перемещение тела при равноускоренном движении</b>
https://videouroki.net/video/5-pieriemieshchieniie-tiela-pri-ravnouskoriennom-dvizhienii.html \n
- <b>Решение задач по теме Основы кинематики</b>
https://videouroki.net/video/9-rieshieniie-zadach-po-tiemie-osnovy-kiniematiki.html""",
    'formulas': (
      "<b>🏃 Формулы: Кинематика</b>\n\n"
      "Скорость при равноускоренном движении:\n"
      "<code>v = v₀ ± a·t</code>\n\n"
      "Уравнение координаты:\n"
      "<code>x = x₀ + v₀·t ± (a·t²) / 2</code>\n\n"
      "Перемещение без времени:\n"
      "<code>S = (v² - v₀²) / (2·a)</code>"
    ),
    'hints': {
      'Подсказка 1.1': 'Как определить среднюю скорость?',
      'Подсказка 1.2': 'Как найти ускорение по графику?'
    }
  },

  '🌀 Вращение': {
    'description': 'Вращательное движение тел',
    'theory':
"""- <b>Равномерное движение точки по окружности</b>
https://videouroki.net/video/07-ravnomernoe-dvizhenie-tochki-po-okruzhnosti.html""",
    'formulas': (
      "<b>🌀 Формулы: Вращение</b>\n\n"
      "Угловая скорость:\n"
      "<code>ω = φ / t = 2·π / T = 2·π·ν</code>\n\n"
      "Связь линейной и угловой скорости:\n"
      "<code>v = ω·R</code>\n\n"
      "Центростремительное ускорение:\n"
      "<code>a_ц = v² / R = ω²·R</code>"
    ),
    'hints': {
      'Подсказка 2.1': 'Как связаны линейная и угловая скорости?',
      'Подсказка 2.2': 'Как рассчитать центростремительное ускорение?'
    }
  },

  '🎢 Колебания': {
    'description': 'Механические и электромагнитные колебания',
    'theory': """
- <b> Измерение частоты и периода колебаний математического маятника </b>
https://videouroki.net/video/24-izmerenie-chastoty-i-perioda-kolebanij-matematicheskogo-mayatnika-241.html
- <b> Исследование периода (частоты) колебаний нитяного маятника </b>
https://videouroki.net/video/25-issledovanie-perioda-chastoty-kolebanij-nityanogo-mayatnika-241.html
- <b> Измерение частоты и периода колебаний пружинного маятника </b>
https://videouroki.net/video/26-izmerenie-chastoty-i-perioda-kolebanij-pruzhinnogo-mayatnika-241.html
    """,
    'formulas': (
      "<b>🎢 Формулы: Колебания</b>\n\n"
      "Период математического маятника:\n"
      "<code>T = 2·π·√(l / g)</code>\n\n"
      "Период пружинного маятника:\n"
      "<code>T = 2·π·√(m / k)</code>\n\n"
      "Уравнение гармонических колебаний:\n"
      "<code>x = A·cos(ω·t + φ₀)</code>"
    ),
    'hints': {
      'Подсказка 3.1': 'Как определить период колебаний пружинного маятника?',
      'Подсказка 3.2': 'Что такое резонанс?'
    }
  },  '🏋️ Динамика': {
    'description': 'Динамика: силы в природе',
    'theory':
"""- <b> Законы Ньютона </b>
https://videouroki.net/video/08-zakony-nyutona-229.html""",
    'formulas': (
      "<b>🏋️ Формулы: Динамика</b>\n\n"
      "Второй закон Ньютона:\n"
      "<code>F = m·a</code>\n\n"
      "Закон всемирного тяготения:\n"
      "<code>F = G·(m₁·m₂) / R²</code>\n\n"
      "Сила трения скольжения:\n"
      "<code>F_тр = μ·N</code>\n\n"
      "Закон Гука (сила упругости):\n"
      "<code>F_упр = -k·x</code>"
    ),
    'hints': {
      'Подсказка 4.1': 'Как определить равнодействующую силу?',
      'Подсказка 4.2': 'Когда применяется закон Гука?'
    }
  },

  '⚖️ Статика': {
    'description': 'Равновесие тел',
    'theory': '''
- <b> Измерение момента силы, действующего на рычаг </b> 
https://videouroki.net/video/28-izmerenie-momenta-sily-dejstvuyushchego-na-rychag-241.html
- <b> Проверка условия равновесия рычага </b> 
https://videouroki.net/video/29-proverka-usloviya-ravnovesiya-rychaga-241.html
    ''',
    'formulas': (
      "<b>⚖️ Формулы: Статика</b>\n\n"
      "Момент силы:\n"
      "<code>M = F·d</code>\n\n"
      "Условие равновесия рычага:\n"
      "<code>F₁·d₁ = F₂·d₂</code> (или ΣM = 0)\n\n"
      "Давление твердого тела:\n"
      "<code>p = F / S</code>"
    ),
    'hints': {
      'Подсказка 5.1': 'Как определить центр тяжести тела?',
      'Подсказка 5.2': 'Когда выполняется правило рычага?'
    }
  },

  '♻️ Законы сохранения': {
    'description': 'Законы сохранения в механике',
    'theory': '''
- <b> Импульс. Закон сохранения импульса </b>
https://videouroki.net/video/12-impuls-zakon-sohraneniya-impulsa-229.html
- <b> Кинетическая и потенциальная энергия. Закон сохранения энергии </b>
https://videouroki.net/video/14-kineticheskaya-i-potencialnaya-ehnergiya-zsmeh-229.html
    ''',
    'formulas': (
      "<b>♻️ Формулы: Законы сохранения</b>\n\n"
      "Импульс тела:\n"
      "<code>p = m·v</code>\n\n"
      "Механическая работа:\n"
      "<code>A = F·S·cos(α)</code>\n\n"
      "Кинетическая энергия:\n"
      "<code>E_к = (m·v²) / 2</code>\n\n"
      "Потенциальная энергия в поле тяжести:\n"
      "<code>E_п = m·g·h</code>\n\n"
      "Мощность:\n"
      "<code>N = A / t = F·v</code>"
    ),
    'hints': {
      'Подсказка 6.1': 'Когда сохраняется механическая энергия?',
      'Подсказка 6.2': 'Как применять закон сохранения импульса?'
    }
  },

  '🌊 + 💨 Гидроаэростатика': {
    'description': 'Механика жидкостей и газов',
    'theory': '''
- <b> Закон Паскаля. Закон Архимеда </b>
https://videouroki.net/video/17-zakon-paskalya-zakon-arhimeda-229.html
    ''',
    'formulas': (
      "<b>🌊 Формулы: Гидростатика</b>\n\n"
      "Гидростатическое давление:\n"
      "<code>p = ρ_ж·g·h</code>\n\n"
      "Сила Архимеда:\n"
      "<code>F_А = ρ_ж·g·V_погр</code>\n\n"
      "Гидравлический пресс:\n"
      "<code>F₁ / S₁ = F₂ / S₂</code>"
    ),
    'hints': {
      'Подсказка 7.1': 'Как рассчитать давление жидкости на глубине?',
      'Подсказка 7.2': 'Когда тело плавает на поверхности?'
    }
  },

  '🌩️ Электростатика': {
    'description': 'Электрические заряды и поля',
    'theory': '''
- <b> Работа и мощность электрического тока. Закон Джоуля — Ленца </b>
https://videouroki.net/video/07-rabota-i-moshchnost-ehlektricheskogo-toka-zakon-dzhoulya-lenca-235.html
          ''',
    'formulas': (
      "<b>🌩️ Формулы: Электростатика</b>\n\n"
      "Закон Кулона:\n"
      "<code>F = k·(|q₁|·|q₂|) / r²</code>\n\n"
      "Напряженность поля точечного заряда:\n"
      "<code>E = F / q = k·|q| / r²</code>\n\n"
      "Емкость плоского конденсатора:\n"
      "<code>C = q / U = (ε·ε₀·S) / d</code>\n\n"
      "Энергия конденсатора:\n"
      "<code>W = (C·U²) / 2 = q² / (2·C)</code>"
    ),
    'hints': {
      'Подсказка 8.1': 'Как направлена сила Кулона?',
      'Подсказка 8.2': 'Как рассчитать напряженность точечного заряда?'
    }
  },

  '➡️ Постоянный электр. ток': {
    'description': 'Электрический ток в проводниках',
    'theory': '''
- <b> Постоянный электрический ток. Сила тока. Напряжение </b>
https://videouroki.net/video/03-postoyannyj-ehlektricheskij-tok-sila-toka-napryazhenie-235.html
    ''',
    'formulas': (
      "<b>➡️ Формулы: Постоянный ток</b>\n\n"
      "Закон Ома для участка цепи:\n"
      "<code>I = U / R</code>\n\n"
      "Сопротивление проводника:\n"
      "<code>R = ρ·(l / S)</code>\n\n"
      "Закон Ома для полной цепи:\n"
      "<code>I = ε / (R + r)</code>\n\n"
      "Закон Джоуля-Ленца:\n"
      "<code>Q = I²·R·t = (U² / R)·t = I·U·t</code>"
    ),
    'hints': {
      'Подсказка 9.1': 'Как рассчитать сопротивление проводника?',
      'Подсказка 9.2': 'Когда применяется закон Ома для полной цепи?'
    }
  },

  '🧲 Магнетизм': {
    'description': 'Магнитные поля и их взаимодействия',
    'theory': '''
- <b> Сила Лоренца </b>
https://videouroki.net/video/17-sila-lorientsa.html
    ''',
    'formulas': (
      "<b>🧲 Формулы: Магнетизм</b>\n\n"
      "Сила Ампера (на проводник):\n"
      "<code>F_А = I·B·l·sin(α)</code>\n\n"
      "Сила Лоренца (на заряд):\n"
      "<code>F_л = |q|·v·B·sin(α)</code>\n\n"
      "Магнитный поток:\n"
      "<code>Φ = B·S·cos(α)</code>"
    ),
    'hints': {
      'Подсказка 10.1': 'Как определить направление силы Ампера?',
      'Подсказка 10.2': 'Как движется заряженная частица в магнитном поле?'
    }
  },

  '↔️ Переменный электр. ток': {
    'description': 'Колебания в электрических цепях',
    'theory': '''
- <b> Переменный электрический ток. Резистор в цепи переменного тока </b>
https://videouroki.net/video/12-peremennyj-ehlektricheskij-tok-rezistor-v-cepi-peremennogo-toka.html
    ''',
    'formulas': (
      "<b>↔️ Формулы: ЭМ Идукция и Колебания</b>\n\n"
      "Закон электромагнитной индукции (Фарадей):\n"
      "<code>ε_i = -ΔΦ / Δt</code>\n\n"
      "ЭДС самоиндукции:\n"
      "<code>ε_is = -L·(ΔI / Δt)</code>\n\n"
      "Формула Томсона (идеальный колебательный контур):\n"
      "<code>T = 2·π·√(L·C)</code>\n\n"
      "Энергия магнитного поля катушки:\n"
      "<code>W = (L·I²) / 2</code>"
    ),
    'hints': {
      'Подсказка 11.1': 'Как рассчитать реактивное сопротивление?',
      'Подсказка 11.2': 'Что такое коэффициент мощности?'
    }
  },

  '🔍 Оптика геометрическая': {
    'description': 'Распространение света как лучей',
    'theory': '''
- <b> Оптическая сила линзы. Формула линзы. Линейное увеличение линзы </b>
https://videouroki.net/video/22-optichieskaia-sila-linzy-formula-linzy-linieinoie-uvielichieniie-linzy.html
    ''',
    'formulas': (
      "<b>🔍 Формулы: Геометрическая оптика</b>\n\n"
      "Закон преломления Снеллиуса:\n"
      "<code>n₁·sin(α) = n₂·sin(γ)</code>\n\n"
      "Формула тонкой линзы:\n"
      "<code>±1/F = ±1/d ± 1/f</code>\n\n"
      "Оптическая сила линзы:\n"
      "<code>D = 1 / F</code> (в диоптриях)"
    ),
    'hints': {
      'Подсказка 12.1': 'Как построить изображение в линзе?',
      'Подсказка 12.2': 'Когда возникает полное внутреннее отражение?'
    }
  },

  '🌈 Оптика волновая': {
    'description': 'Волновая природа света',
    'theory': '''
- <b> Длина волны. Связь длины волны со скоростью её распространения </b>
https://videouroki.net/video/36-dlina-volny-sviaz-dliny-volny-so-skorost-iu-ieio-rasprostranieniia-uravnieniie-volny.html 
    ''',
    'formulas': (
      "<b>🌈 Формулы: Волновая оптика</b>\n\n"
      "Связь скорости, длины волны и частоты:\n"
      "<code>v = λ·ν = λ / T</code>\n\n"
      "Формула дифракционной решетки (максимумы):\n"
      "<code>d·sin(φ) = k·λ</code>"
    ),
    'hints': {
      'Подсказка 13.1': 'Как рассчитать длину волны по интерференционной картине?',
      'Подсказка 13.2': 'Что такое условие максимума дифракционной решетки?'
    }

  },

  '⚛️ Атомная физика': {
    'description': 'Строение атома и квантовые явления',
    'theory': '''
- <b>Опыты Резерфорда. Планетарная модель атома </b>
https://videouroki.net/video/16-opyty-rezerforda-planetarnaya-model-atoma-235.html
    ''',
    'formulas': (
      "<b>⚛️ Формулы: Квантовая физика</b>\n\n"
      "Энергия фотона:\n"
      "<code>E = h·ν = (h·c) / λ</code>\n\n"
      "Уравнение Эйнштейна для фотоэффекта:\n"
      "<code>h·ν = A_вых + (m·v²_max) / 2</code>\n\n"
      "Дефект масс ядра:\n"
      "<code>ΔM = (Z·m_p + N·m_n) - M_ядра</code>\n\n"
      "Энергия связи ядра:\n"
      "<code>E_св = ΔM·c²</code>"
    ),
    'hints': {
      'Подсказка 14.1': 'Как рассчитать энергию фотона?',
      'Подсказка 14.2': 'Что такое работа выхода в фотоэффекте?'
    }
  },

  '🔥 Термодинамика': {
    'description': 'Тепловые явления и законы',
    'theory': '''
- <b>Первый закон термодинамики. Необратимость процессов в природе </b>
https://videouroki.net/video/55-piervyi-zakon-tiermodinamiki-nieobratimost-protsiessov-v-prirodie.html
    ''',
    'formulas': (
      "<b>🔥 Формулы: МКТ и Термодинамика</b>\n\n"
      "Уравнение Менделеева-Клапейрона:\n"
      "<code>p·V = (m / M)·R·T = ν·R·T</code>\n\n"
      "Основное уравнение МКТ:\n"
      "<code>p = (1/3)·m₀·n·v² = n·k·T</code>\n\n"
      "Внутренняя энергия идеального одноатомного газа:\n"
      "<code>U = (3/2)·ν·R·T</code>\n\n"
      "Первый закон термодинамики:\n"
      "<code>Q = ΔU + A_газа</code>\n\n"
      "КПД идеальной тепловой машины (Цикл Карно):\n"
      "<code>η = (T_н - T_х) / T_н</code>"
    ),
    'hints': {
      'Подсказка 15.1': 'Как рассчитать КПД тепловой машины?',
      'Подсказка 15.2': 'Когда применяется уравнение Менделеева-Клапейрона?'
    }
  },

}

