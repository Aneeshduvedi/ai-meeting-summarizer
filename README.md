# AI Meeting Summarizer

An AI-powered web application that transforms meeting transcripts into structured, easy-to-understand reports using Django, PostgreSQL, and the Groq API.

## Features

- **User Authentication:** Register, log in, and log out securely.
- **Meeting Summarization:** Convert pasted meeting transcripts into concise summaries.
- **Meeting Analysis Agent:** Identify key topics, important decisions, and unresolved questions.
- **Action Item Agent:** Extract tasks, assigned owners, and deadlines from meeting discussions.
- **Meeting Reports:** View structured reports containing summaries, topics, decisions, action items, and unresolved questions.
- **PDF Export:** Download meeting reports as PDF files.
- **Dashboard:** View meeting statistics, search meetings, filter by date, sort results, and navigate through pages.
- **PostgreSQL Database:** Store meeting information and reports.
- **User-Specific History:** Keep each user's meetings separate.
- **Interactive Interface:** Responsive layouts, sidebar navigation, loading feedback, and notifications.

## Technology Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **AI Integration:** Groq API
- **AI Model:** `openai/gpt-oss-20b`
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Version Control:** Git and GitHub

## Project Structure

```text
ai_meeting_summarizer/
├── accounts/           # User authentication
├── config/             # Django project configuration
├── meetings/           # Meeting and report functionality
├── static/
│   ├── css/             # Stylesheets
│   └── js/              # Frontend JavaScript
├── templates/           # Shared HTML templates
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/broski62026-prog/ai-meeting-summarizer.git
cd ai-meeting-summarizer
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root and configure the Groq API key and Django settings required by your application.

Example:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Use the variable names expected by your Django settings and application code. Obtain your API key from the [Groq Console](https://console.groq.com/).

**Important:** Never commit `.env` or expose API keys in source code or GitHub.

### 5. Configure PostgreSQL

Install PostgreSQL and create a database for the application. Configure the database name, username, password, host, and port according to your Django settings.

Ensure the database exists and PostgreSQL is running before continuing.

### 6. Apply database migrations

```powershell
python manage.py migrate
```

### 7. Start the development server

```powershell
python manage.py runserver
```

Open the local address displayed in the terminal, usually:

http://127.0.0.1:8000/

## How It Works

1. Register or log in to the application.
2. Enter a meeting transcript.
3. Generate a report using the AI-powered meeting analysis and action item agents.
4. Review the summary, topics, decisions, action items, and unresolved questions.
5. Download the report as a PDF or access it later from the dashboard.

The application is designed to avoid inventing meeting details. When an owner or deadline is not stated in the transcript, the report should indicate that it was not specified.

## Security and Configuration Notes

- Keep API keys and database passwords in local environment configuration.
- Do not upload `.env` or virtual environment files.
- Configure Django settings and database credentials before running the application.

## Future Improvements

Potential enhancements include improved report formatting, additional meeting analytics, and further user-interface improvements.

## Author

**Aneesh Duvedi**

GitHub: [broski62026-prog](https://github.com/broski62026-prog)

## License

No license has been specified yet.
