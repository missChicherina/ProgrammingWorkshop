# Лабораторная работа №2 "Файловый менеджер"

## Задания для выполнения:

Необходимо создать примитивный файловый менеджер. Программа должна работать в определенной папке (рабочей папки менеджера) и позволять пользователю выполнять следующие простые действия в пределах рабочей папки:

* Создание папки (с указанием имени);
* Удаление папки по имени;
* Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх;
* Создание пустых файлов с указанием имени;
* Запись текста в файл; 
* Просмотр содержимого текстового файла;
* Удаление файлов по имени;
* Копирование файлов из одной папки в другую;
* Перемещение файлов;
* Переименование файлов.

## Дополнительные задания:
* Разработайте псевдографический интерфейс для разработанного в основном задании файлового менеджера по аналогии с программами Far или Midnight Commander. 
* Сделайте файловый менеджер многопользовательским. Добавьте возможность регистрации пользователей. При регистрации каждому пользователю создается своя домашняя папка, в пределах которой он может работать.
* Придумайте и добавьте дополнительные функциональные возможности для файлового менеджера. Как пример можно взять:
    * Архивация и разархивация файлов и папок;
    * Квотирование дискового пространства и отображение занятого оставшегося места;

## Требования к работе:
* Расположение рабочей папки должно указываться в настройках файлового менеджера. Настройки должны располагаться в отдельном от основного исходного кода файле.
* Файловый менеджер должен блокировать пользователя от выхода за пределы рабочей папки. Пользователь должен воспринимать рабочую папку как корневую и все действия файлового менеджера должны локализоваться только в пределах этой папки.
* Программный проект должен быть оформлен как код на языке программирования Python и располагаться в определенной папке. Проект должен состоять из нескольких файлов. Расположение рабочей папки не должно быть связано с физическим расположением файлов исходного кода. 
Файловый менеджер по умолчанию должен иметь текстовый интерфейс по аналогии с интерфейсом командной строки. Действия пользователя осуществляются вводом с клавиатуры соответствующей команды (по необходимости с параметрами).
* Код должен быть организован в виде набора функций или классов, каждая операция файлового менеджера должна быть реализована в отдельной функции или методе класса.
* Файловый менеджер должен быть кроссплатформенным и работать как в среде Windows, так и в UNIX системах. Необходимо протестировать работоспособность программы в разных ОС. Для кроссплатформенности рекомендуется использовать стандартную библиотеку Python для осуществления файловых операций.
* Разработка программы должна вестись с использованием СКВ Git. Код должен публиковаться в репозитории на GitHub.
* Перед разработкой программист должен продумать названия и структуру команд для пользователя. Команды не должны повторять команды существующих программных оболочек.
