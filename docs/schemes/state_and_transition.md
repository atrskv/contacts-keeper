
``` mermaid
graph TB

    classDef Status fill:#000000, fill:#ffffff, stroke:#000000;

    Created("Создан"):::Status

    Edited("Отредактирован"):::Status
    Deleted("Удалён"):::Status

    Start@{ shape: sm-circ, label: "Small start" }

    Start -->|Создать| Created
    Created -->|Отредактировать| Edited
    Created -->|Удалить| Deleted
    Edited -->|Удалить| Deleted
    Deleted --> Start
```
