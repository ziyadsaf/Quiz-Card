# Quiz-Card

A Python-based educational quiz application that automatically generates flashcards from incorrectly answered questions, helping students learn from their mistakes through spaced repetition.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Creating a Quiz](#creating-a-quiz)
  - [Running the Application](#running-the-application)
  - [Quiz Flow](#quiz-flow)
- [Configuration](#configuration)
  - [CSV Format](#csv-format)
  - [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
  - [Quiz Class](#quiz-class)
  - [Flashcard Class](#flashcard-class)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Overview

### Problem Statement

As a Computer Science teacher, I observed that students often struggle to retain information from their mistakes on quizzes. The process of manually tracking wrong answers was tedious, and students rarely revisited their errors to learn from them.

### Solution

Quiz-Card addresses this by:
1. Allowing educators to create custom quizzes from CSV files
2. Providing an interactive quiz experience with multiple attempts per question
3. Automatically generating flashcards from incorrectly answered questions
4. Persisting flashcards to a database for future review sessions

This creates a feedback loop where mistakes become learning opportunities through targeted flashcard review.

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| CSV Quiz Import | Complete | Load quiz questions from structured CSV files |
| Interactive Quiz Mode | Complete | Answer questions with real-time feedback |
| Multiple Attempts | Complete | 3 attempts per question with scoring adjustments |
| Score Tracking | Complete | Running score with penalties for incorrect answers |
| Reattempt System | Complete | Second chance to answer previously failed questions |
| Flashcard Generation | Complete | Automatic flashcard creation from mistakes |
| SQLite Persistence | Complete | Flashcards saved to database with duplicate prevention |
| CSV Results Export | Planned | Export quiz results and performance data |
| Progress Visualization | Planned | Plot learning progress over time |
| GUI Interface | In Progress | Tkinter-based graphical interface |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Quiz-Card System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐  │
│   │   CSV File  │────▶│  Quiz Class │────▶│ Flashcard Class │  │
│   │  (Input)    │     │             │     │                 │  │
│   └─────────────┘     └──────┬──────┘     └────────┬────────┘  │
│                              │                     │            │
│                              ▼                     ▼            │
│                       ┌─────────────┐      ┌─────────────┐     │
│                       │  User CLI   │      │   SQLite    │     │
│                       │ Interface   │      │  Database   │     │
│                       └─────────────┘      └─────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input Processing**: CSV file is parsed into question and answer dictionaries
2. **Quiz Execution**: Questions are presented sequentially with multiple-choice options
3. **Answer Validation**: User responses are validated (case-insensitive) against correct answers
4. **Reattempt Phase**: Failed questions are offered for a second attempt
5. **Flashcard Creation**: Persistently failed questions are converted to flashcards
6. **Database Storage**: Flashcards are stored in SQLite with duplicate checking

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses Python standard library only)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ziyadsaf/quiz_app.git
cd quiz_app
```

2. Verify Python installation:
```bash
python --version
```

3. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Creating a Quiz

Create a CSV file with your quiz questions following this format:

```csv
QUESTION_NUMBER,QUESTION,CHOICE1,CHOICE2,CHOICE3,CHOICE4,CORRECT_ANSWER
1,What is the capital of France?,London,Paris,Berlin,Madrid,Paris
2,Which planet is known as the Red Planet?,Venus,Mars,Jupiter,Saturn,Mars
3,What is 2 + 2?,3,4,5,6,4
```

**Important Notes:**
- The first row must be a header row (it will be skipped during parsing)
- `CORRECT_ANSWER` must exactly match one of the four choices
- Answer validation is case-insensitive

### Running the Application

```bash
python quiz.py
```

### Quiz Flow

1. **File Selection**: Enter the path to your CSV quiz file
2. **Quiz Start**: Confirm to begin the quiz (Y/N)
3. **Question Phase**:
   - View all questions and their options
   - Answer each question (up to 3 attempts per question)
   - Receive immediate feedback and scoring
4. **Reattempt Phase**: Retry questions you got wrong
5. **Flashcard Generation**: Review and save flashcards for persistent errors

**Scoring System:**
- Correct answer: +1 point
- Incorrect answer: -1 point
- Maximum 3 attempts per question

## Configuration

### CSV Format

| Column | Description | Required |
|--------|-------------|----------|
| QUESTION_NUMBER | Unique identifier for the question | Yes |
| QUESTION | The question text | Yes |
| CHOICE1-4 | Four multiple choice options | Yes |
| CORRECT_ANSWER | Must match one of the four choices exactly | Yes |

### Database Schema

The application uses SQLite for flashcard persistence.

**Table: `flashcard`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| question | VARCHAR | The question text |
| answer | VARCHAR | The correct answer |

```sql
CREATE TABLE IF NOT EXISTS flashcard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question VARCHAR,
    answer VARCHAR
)
```

## Project Structure

```
Quiz-Card/
├── quiz.py              # Main application entry point and core classes
├── data.csv             # Sample quiz data for testing
├── flashcards.sql       # Database schema definition
├── flashcards.db        # SQLite database (generated at runtime)
├── README.md            # Project documentation
├── .gitignore           # Git ignore rules
└── Quiz spec            # Feature specification document
```

## API Reference

### Quiz Class

The main class responsible for quiz management and execution.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `data` | tuple | Parsed question bank and answer bank |
| `file_name` | str | Path to the loaded CSV file |
| `q_bank` | dict | Question text mapped to choices |
| `q_answer` | dict | Question text mapped to correct answer |
| `incorrect_questions` | dict | Questions answered incorrectly |

#### Methods

##### `process_csv()`
Prompts for a CSV file path and validates the file type. Populates `self.data` with parsed question data.

##### `get_file(path: Path) -> csv.reader`
Reads and parses a CSV file at the given path.

**Parameters:**
- `path`: Path object pointing to the CSV file

**Returns:** CSV reader object

##### `get_data(reader: csv.reader) -> tuple[dict, dict]`
Converts CSV data into question and answer dictionaries.

**Parameters:**
- `reader`: CSV reader object

**Returns:** Tuple of (question_bank, question_answer_bank)

##### `show_question(question: str) -> None`
Displays all questions with their multiple-choice options.

**Parameters:**
- `question`: User input ('Y' to display, 'N' to exit)

##### `answer_question() -> dict`
Executes the quiz, tracks scoring, and identifies incorrect answers.

**Returns:** Dictionary of incorrect questions mapped to their correct answers

##### `reattempt_questions(incorrect_questions: dict) -> dict`
Allows users to retry failed questions with up to 3 attempts each.

**Parameters:**
- `incorrect_questions`: Dict of questions the user got wrong

**Returns:** Dictionary of questions still incorrect after reattempts

### Flashcard Class

Manages flashcard creation and database persistence.

#### Constructor

```python
Flashcard(flashcards: dict)
```

**Parameters:**
- `flashcards`: Dictionary mapping questions to correct answers

#### Methods

##### `create_flashcard() -> None`
Displays formatted flashcards to the console.

##### `save_flashcards() -> None`
Persists flashcards to the SQLite database. Performs duplicate checking before insertion.

## Roadmap

### Phase 1: Core Functionality (Complete)
- [x] CSV-based quiz import
- [x] Interactive quiz with scoring
- [x] Multiple attempt system
- [x] Reattempt phase for incorrect questions
- [x] Flashcard generation and display
- [x] SQLite persistence with duplicate prevention

### Phase 2: Data Export and Analytics (In Progress)
- [ ] Export quiz results to CSV
- [ ] Track performance metrics over time
- [ ] Generate progress visualization plots

### Phase 3: GUI Development (In Progress)
- [ ] Main menu interface
- [ ] Quiz selection screen
- [ ] Question display with interactive buttons
- [ ] Shuffled vs. sequential question order option
- [ ] Dedicated flashcard review tab
- [ ] Results summary screen

### Phase 4: Future Enhancements (Planned)
- [ ] Web-based interface (Django/Flask)
- [ ] User authentication and profiles
- [ ] Quiz sharing and collaboration
- [ ] Spaced repetition algorithm for flashcard scheduling
- [ ] Import/export quiz templates

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request

### Code Style Guidelines

- Follow PEP 8 conventions
- Include docstrings for all public methods
- Add type hints where appropriate
- Write descriptive commit messages

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Project Link:** [https://github.com/ziyadsaf/quiz_app](https://github.com/ziyadsaf/quiz_app)
