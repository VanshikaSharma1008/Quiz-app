# Quiz Application

A professional Python quiz application that demonstrates software engineering best practices and design patterns.

## 🎯 Features

- **Multiple Question Types**: Support for Multiple Choice and True/False questions
- **Design Patterns**: Implementation of Factory, Singleton, and Observer patterns
- **Professional Structure**: Clean, modular code following software engineering principles
- **Comprehensive Testing**: Unit tests for all major components
- **Thread-Safe Operations**: Thread-safe quiz management with proper locking
- **Documentation**: Google-style docstrings throughout the codebase

## 📁 Project Structure

```
Quiz_app/
│
├── main.py                          # Application entry point
├── demo_quiz.py                     # Demo quiz implementation
├── README.md                        # Project documentation
├── reflection.md                    # Project reflection and insights
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore patterns
│
├── models/                          # Data models layer
│   ├── __init__.py
│   ├── question.py                  # Question base class and types
│   └── user.py                      # User model
│
├── patterns/                        # Design patterns implementation
│   ├── __init__.py
│   ├── factory.py                   # Factory pattern for question creation
│   ├── observer.py                  # Observer pattern interfaces
│   └── singleton.py                 # Singleton pattern utilities
│
├── services/                        # Business logic layer
│   ├── __init__.py
│   ├── quiz_manager.py              # Quiz state management (Singleton)
│   └── ui.py                        # User interface service
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   └── timer.py                     # Timer implementation (Subject)
│
├── quiz/                            # Legacy quiz package
│   ├── __init__.py
│   ├── questions.py                 # Question factory implementation
│   ├── quiz_manager.py              # Quiz manager implementation
│   ├── ui.py                        # UI implementation
│   ├── observer.py                  # Observer implementations
│   └── console_observer.py          # Console notification observer
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_question_pytest.py      # Pytest tests for Question model
│   ├── test_quiz_manager_pytest.py  # Pytest tests for QuizManager
│   ├── test_observer_pytest.py      # Pytest tests for Observer pattern
│   ├── test_timer_pytest.py         # Pytest tests for Timer utility
│   ├── test_questions.py            # Unittest tests for questions
│   ├── test_quiz_manager.py         # Unittest tests for quiz manager
│   └── test_quiz.py                 # Integration tests
│
└── demos/                           # Demo and example scripts
    └── demo_quiz_run.py             # Manual testing script
```

## 🏛️ Architecture

### Clean Architecture Layers

**Models Layer (`models/`)**

- **question.py**: Question base class and concrete implementations (MCQ, True/False, Short Answer)
- **user.py**: User model with score tracking and quiz history

**Patterns Layer (`patterns/`)**

- **factory.py**: Factory pattern for creating different question types
- **observer.py**: Observer pattern interfaces (Subject, Observer)
- **singleton.py**: Singleton pattern utilities and decorators

**Services Layer (`services/`)**

- **quiz_manager.py**: Core quiz state management (Singleton, Subject, Observer)
- **ui.py**: User interface service for quiz interaction

**Utils Layer (`utils/`)**

- **timer.py**: Thread-safe timer implementation (Subject)

### Legacy Package (`quiz/`)

- **questions.py**: Question factory implementation
- **quiz_manager.py**: Quiz manager implementation
- **ui.py**: UI implementation
- **observer.py**: Observer implementations (ScoreObserver, TimeObserver, QuizCompletionObserver)
- **console_observer.py**: Console notification observer

### Tests Package (`tests/`)

- **test_question_pytest.py**: Pytest tests for Question model
- **test_quiz_manager_pytest.py**: Pytest tests for QuizManager
- **test_observer_pytest.py**: Pytest tests for Observer pattern
- **test_timer_pytest.py**: Pytest tests for Timer utility
- **test_questions.py**: Unittest tests for questions
- **test_quiz_manager.py**: Unittest tests for quiz manager
- **test_quiz.py**: Integration tests

## 📝 Coding Standards

- **Indentation**: 4 spaces, no tabs
- **Naming**: snake_case for functions/variables, CamelCase for classes
- **Documentation**: Google-style docstrings for all public functions/classes
- **Error Handling**: Proper exception handling with clear error messages
- **Type Hints**: Comprehensive type annotations throughout
- **Thread Safety**: Thread-safe operations where needed

## 🎓 Learning Objectives

This project demonstrates:

- **Software Design Patterns**: Factory, Singleton, Observer
- **Clean Architecture**: Separation of concerns, modular design
- **Professional Practices**: Error handling, testing, documentation
- **Python Best Practices**: Type hints, docstrings, code organization
- **Thread Safety**: Proper concurrent access handling

Perfect for learning advanced Python concepts and software engineering principles!

## 🏗️ Design Patterns Implemented

### 1. Factory Pattern (`patterns/factory.py`)

- **Purpose**: Create different types of questions (MCQ, True/False, Short Answer)
- **Benefits**: Encapsulates object creation logic, easy to extend with new question types
- **Usage**: `QuestionFactory().create_question(question_type, text, correct_answer, ...)`

### 2. Singleton Pattern (`services/quiz_manager.py`)

- **Purpose**: Global quiz state management across the application
- **Benefits**: Ensures single instance, thread-safe operations
- **Class**: `QuizManager`

### 3. Observer Pattern (`patterns/observer.py`)

- **Purpose**: Handle notifications for quiz events (completion, time updates, etc.)
- **Benefits**: Loose coupling between components, extensible notification system
- **Usage**: Attach observers to subjects for real-time updates

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pytest (for running pytest-style tests)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd quiz_app
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

### Running Tests

**Unittest tests:**

```bash
python -m unittest discover tests
```

**Pytest tests:**

```bash
pytest tests/
```

**Run all tests with coverage:**

```bash
pytest tests/ --cov=. --cov-report=html
```

## 📖 Usage

1. **Start the Application**: Run `python main.py`
2. **Enter Your Name**: Provide your name when prompted
3. **Answer Questions**:
   - Multiple Choice: Enter the number (1, 2, 3, 4)
   - True/False: Enter 1 for True, 2 for False
4. **View Results**: See your score and completion time

## 🧪 Testing

The application includes comprehensive unit tests covering:

- **Question Objects**: Creation, validation, answer checking
- **Factory Pattern**: Question creation, error handling
- **Quiz Manager**: Singleton behavior, quiz flow, state management
- **Observer Pattern**: Notification system
- **Thread Safety**: Concurrent access handling
- **Timer Utility**: Thread-safe timer operations

### Test Coverage

**Unittest Tests:**

- `test_questions.py`: Question factory and validation tests
- `test_quiz_manager.py`: Quiz manager functionality tests
- `test_quiz.py`: Integration tests

**Pytest Tests:**

- `test_question_pytest.py`: Question model tests with fixtures
- `test_quiz_manager_pytest.py`: QuizManager service tests
- `test_observer_pytest.py`: Observer pattern tests
- `test_timer_pytest.py`: Timer utility tests

### Running Tests

**Unittest tests:**

```bash
python -m unittest discover tests
```

**Pytest tests:**

```bash
pytest tests/
```

**Run all tests with coverage:**

```bash
pytest tests/ --cov=. --cov-report=html
```
