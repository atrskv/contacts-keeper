
``` mermaid


graph LR
    root([Contacts Keeper]):::root_style

    root --> create([Добавлять]):::actions_style
    root --> read([Просматривать]):::actions_style
    root --> update([Обновлять]):::actions_style
    root --> delete([Удалять]):::actions_style

    subgraph actions_group [Действия]
    create
    read
    update
    delete
    random_contact
    paginate
    reset_search
    search
    end
    actions_group:::root_style


    create --> using_navbar([Используя кнопку в нав. меню]):::params_style
    create --> using_creating_button([Используя кнопку в строке поиска]):::params_style

    using_navbar -->|Те же| params_group

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

    subgraph params_group [Параметры при добавлении]
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
    params_group:::root_style

    update -->|Те же| params_group
    read -->|Те же| params_group
    random_contact -->|Те же| params_group
    
    read --> random_contact([Открывать случайный]):::actions_style


    root --> search([Искать]):::actions_style
    root --> reset_search([Сбрасывать поиск]):::actions_style
    read --> paginate([Переключать отображение]):::actions_style

    













    classDef root_style fill:#000000, fill:#ffffff, stroke:#000000,font-weight:bold;
    classDef actions_style fill:#000000, fill:#ffffff, stroke:#000000;
    classDef params_style fill:#000000, fill:#ffffff, stroke:#000000;
    classDef values_style fill:#000000, fill:#ffffff, stroke:#000000,font-style:italic;
```
