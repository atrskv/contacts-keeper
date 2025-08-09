
``` mermaid
graph LR
    
    root([Contacts Keeper]):::root_style


    subgraph actions_group [Действия]
    
    create
    read
    show_all_the_cs
    random_contact
    update
    delete
    paginate
    reset_search
    search

    end


    root --> create([Добавлять]):::actions_style
    root --> read([Просматривать]):::actions_style
    root --> update([Редактировать]):::actions_style
    root --> delete([Удалять]):::actions_style
    root --> search([Искать]):::actions_style
    root --> reset_search([Сбрасывать поиск]):::actions_style

    create --> using_navbar([Используя кнопку в нав. меню]):::params_style
    create --> using_creating_button([Используя кнопку в строке поиска]):::params_style

    read --> show_all_the_cs([Показывать всех]):::actions_style
    read --> random_contact([Открывать случайный]):::actions_style
    read --> paginate([Переключать отображение в пагинаторе]):::actions_style

    read -->|Те же| params_group
    random_contact -->|Те же| params_group
    update -->|Те же| params_group
    using_navbar -->|Те же| params_group


    subgraph params_group [Параметры]

    first_name
    last_name
    phone
    email
    gender
    date_of_birth
    priority
    category
    channels
    current_address

    end


    using_creating_button --> first_name([Имя*]):::params_style
    using_creating_button --> last_name([Фамилия]):::params_style
    using_creating_button --> phone([Телефон]):::params_style
    using_creating_button --> email([Эл. почта]):::params_style
    using_creating_button --> gender([Пол]):::params_style
    using_creating_button --> date_of_birth([Дата рождения]):::params_style
    using_creating_button --> priority([Приоритет]):::params_style
    using_creating_button --> category([Категория]):::params_style
    using_creating_button --> channels([Каналы связи]):::params_style
    using_creating_button --> current_address([Адрес]):::params_style
    

    subgraph values_group [Значения]
    uppercase_first_name
    uppercase_last_name

    male
    female
    other

    datetime_format 

    priority_regular
    priority_high

    not_selected
    friends
    family
    work
    clients

    can_call
    can_message
    email_preferred

    end


    first_name --> uppercase_first_name([С заглавной буквы]):::values_style
    last_name --> uppercase_last_name([С заглавной буквы]):::values_style

    gender --> male([Мужчина]):::values_style
    gender --> female([Женщина]):::values_style
    gender --> other([...]):::values_style

    date_of_birth --> datetime_format([дд.мм.гггг]):::values_style
    priority --> priority_regular([Обычный]):::values_style
    priority --> priority_high([Особой важности]):::values_style

    category --> not_selected([Не выбрана]):::values_style
    category --> friends([Друзья]):::values_style
    category --> family([Семья]):::values_style
    category --> work([Работа]):::values_style
    category --> clients([Клиенты]):::values_style

    channels --> can_call([Можно звонить]):::values_style
    channels --> can_message([Можно писать сообщения]):::values_style
    channels --> email_preferred([Предпочтительно по эл. почте]):::values_style


    actions_group:::root_style
    params_group:::root_style
    values_group:::root_style


    classDef root_style fill:#000000, fill:#ffffff, stroke:#000000,font-weight:bold;
    classDef actions_style fill:#000000, fill:#ffffff, stroke:#000000;
    classDef params_style fill:#000000, fill:#ffffff, stroke:#000000;
    classDef values_style fill:#000000, fill:#ffffff, stroke:#000000,font-style:italic;
```
