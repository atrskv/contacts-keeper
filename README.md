<p align="center">
  <picture>
<img alt="Logo" src="/docs/resources/logo.png" width="70" height="70">
    </picture>
  </a>
</p>
<h1 align="center">
  Contacts Keeper
</h1>

<p align="center">
Минималистичное приложение для управления контактами
</p>

<img src="docs/resources/index.png" width="1000" height="1000" />

## Запуск

1. Склонировать репозиторий:

```
git clone https://github.com/atrskv/contacts-keeper.git
```

2. Установить зависимости:

```
uv sync
```

3. Подготовить `.env` файлы:

```
cp .env.example.dev .env.dev
```

```
cp .env.example.prod .env.prod
```

4. Запустить приложение:

```
make dev-up
```

Или:

```
make prod-up
```

В случае запуска на `dev` приложение будет доступно по адресу: `http://localhost:8080/`, в случае `prod` — `http://localhost:80/`

5. Запустить сервис документации:

```
make docs-up
```

Доступ — `http://localhost:8081/`:

<img src="docs/resources/docs.png" width="1000" height="1000" />








