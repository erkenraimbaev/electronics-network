Данное приложение представляет собой онлайн платформу торговой сети электроники.

Сеть представляет собой иерархическую структуру из 3 уровней:

-Завод
-Розничная сеть
-Индивидуальный предприниматель 

Каждое звено сети ссылается только на одного поставщика оборудования (не обязательно предыдущего по иерархии). 
Важно отметить, что уровень иерархии определяется не названием звена, а отношением к остальным элементам сети.
Иерархическая структура сети:
Теоретически у каждого из уровней может быть поставщик - ограничение в уровне иерархии(он может быть равен или ниже, математически выше).
Уровень 0: Поставщик - Производитель
    Поставщиком здесь может быть: производитель уровня 0(Покупает запчати у другого завода доделывает и продает
    посреднику или продавцу для потребителей)
Уровень 1: Поставщик - Розничная сеть, продает другому поставщику или потребителю
    (Посредник или продавец потребителю)
    Поставщиком может быть: уровни 0 или 1
Уровень 2: Поставщик - ИП
    Поставщиком может быть: уровни 0, 1, 2

В приложении Main созданы модели:
Продукт
Звено сети (производитель, розничная сеть, ИП)

В админ-панели звена сети есть:
-ссылка на «Поставщика»,
-«admin action», очищающий задолженность перед поставщиком у выбранных объектов,
-фильтр по названию города.

С помощью DRF создан набор представлений:
-CRUD для модели товар
-CRUD для модели производителя

Запрещено обновление через API поля «Задолженность перед поставщиком».
Добавлена возможность фильтрации объектов по определенной стране.

Права доступа к API настроены так, чтобы только активные сотрудники имели доступ к API.

Создание суперпользователя: выполнить команду python manage.py create_super_user

Для запуска приложения на локальной машине выполнить команду python manage.py runserver

Доступ к админ панели: http://localhost:8000/admin/

Запуск проекта через Docker:
-Cобрать образ командой docker-compose build 
-Запустить контейнер командой docker-compose up