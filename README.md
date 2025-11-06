## UW Trivia (Notion-backed)

This Django app is a jQuery + Materialize UI that proxies CRUD to Notion databases, acting as middleware between the web UI and Notion.

### Environment

Create `.env` in the project root with:

```
NOTION_API_KEY=secret_...
NOTION_DATABASE_EVENTS=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_QUESTIONS=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_PRIZES=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_PLACEMENTS=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Notion database schemas

Create four Notion databases with these properties:

- Events (`NOTION_DATABASE_EVENTS`)
  - Title: Title
  - Description: Rich text
  - Location: Rich text
  - Starts At: Date

- Questions (`NOTION_DATABASE_QUESTIONS`)
  - Text: Title
  - EventId: Rich text (stores Event page id)
  - Choice A: Rich text
  - Choice B: Rich text
  - Choice C: Rich text (optional)
  - Choice D: Rich text (optional)
  - Correct: Select (A, B, C, D)

- Prizes (`NOTION_DATABASE_PRIZES`)
  - Name: Title
  - EventId: Rich text
  - Description: Rich text
  - Rank: Number
  - Value: Number

- Placements (`NOTION_DATABASE_PLACEMENTS`)
  - Participant: Title
  - EventId: Rich text
  - Score: Number
  - Rank: Number

You can switch `EventId` to a Relation to the Events DB and adjust `notion_middleware/notion_client.py` accordingly.

### Run

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `/` to list and create events. Inside an event page, add questions, prizes, and placements via AJAX.
