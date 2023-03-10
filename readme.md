# Игра 2048
***Проект по pygame для Яндекс.Лицея***

**Авторы:**
- Исламов Владимир [GitHub](https://github.com/Pixelaze) [VK](https://vk.com/pixelaze)
- Сироткин Игорь [GitHub](https://github.com/seerigorsss) [VK](https://vk.com/seerigorsss)

## Описание идеи

Реализовать классическую игру **[2048](https://2048.org)**, используя графический интерфейс ***(но и с возможностью играть в версии для терминала)***. Следующие элементы игры реализованы:
- **Основная игра**: правила, ходы, движение клеток
- **Сохранение данных**: поле сохраняется для возможности продолжения игры
- **Подсчет счета**: ради соревновательного элемента введен подсчет счета игрока

## Описание реализации

Основная реализация делится на 3 основных файла: **field.py**, **gui.py** и **console.py**.

### field.py

Этот файл включает в себя основную логику игры, основанную на 3 классах:
- **Status**: класс определяет 3 возможных сценария игры: проигрыш, выигрыш и продолжающаюся игру
- **Directions**: класс определяет 4 возможных направления движения: вверх, вниз, вправо и влево, а также словарь для перевода их в строки
- **GameField**: класс определяет игровое поле и взаимодействие с ним: совершение ходов, счет, сохранение и загрузку

Используется встроенная библиотека **random** для генерации случайных чисел в ходе создания новой клетки, а также **csv** ***(с одноименным форматом файлов .csv)*** для сохранения поля.

### gui.py

Этот файл включает в себя графическую версию игры, реализованную на главном классе **GraphicsField**, содержащем все методы для работы с графическим полем и связи с классами из **field.py**.

Используется библиотека **pygame** для обработки нажатий, событий и отрисовки экрана.

### console.py

Максимально простой файл, представляющий собой примитивную версию игры в терминал, используя для этого **field.py**.

## Технологический стэк

- Python 3
  - Встроенная библиотека csv
  - Встроенная библиотека random
- pygame

## Скриншоты

***тут будут скриншоты***
