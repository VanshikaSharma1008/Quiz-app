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
quiz_app/
│
├── main.py                          # Entry point for the app
├── README.md                        # Project description
├── .gitignore                       # Ignore .pyc, __pycache__, env folders etc.
│
├── quiz/                            # Core quiz package
│   ├── __init__.py                  # Package initialization
│   ├── questions.py                 # Question objects (Factory pattern)
│   ├── quiz_manager.py              # Quiz state, timer, score (Singleton)
│   ├── ui.py                        # Display questions and collect answers
│   └── observer.py                  # Observer pattern for notifications
│
└── tests/                           # Unit tests
    ├── test_questions.py           # Tests for question objects and factory
    └── test_quiz_manager.py        # Tests for quiz manager and singleton
```

## 🏗️ Design Patterns Implemented

### 1. Factory Pattern (`quiz/questions.py`)

- **Purpose**: Create different types of questions (MCQ, True/False)
- **Benefits**: Encapsulates object creation logic, easy to extend with new question types
- **Usage**: `QuestionFactory().create_question(question_type, text, correct_answer, ...)`

### 2. Singleton Pattern (`quiz/quiz_manager.py`)

- **Purpose**: Global quiz state management across the application
- **Benefits**: Ensures single instance, thread-safe operations
- **Class**: `QuizManager`

### 3. Observer Pattern (`quiz/observer.py`)

- **Purpose**: Handle notifications for quiz events (completion, time updates, etc.)
- **Benefits**: Loose coupling between components, extensible notification system
- **Usage**: Attach observers to subjects for real-time updates

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

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

3. Run the application:

```bash
python main.py
```

### Running Tests

```bash
python -m unittest discover tests
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

Run tests with:

```bash
python -m unittest discover tests
```

## 🏛️ Architecture

### Quiz Package (`quiz/`)

- **questions.py**: Question objects with Factory pattern
- **quiz_manager.py**: Singleton for quiz state management
- **ui.py**: User interface and interaction handling
- **observer.py**: Observer pattern implementation

### Tests Package (`tests/`)

- **test_questions.py**: Tests for question objects and factory
- **test_quiz_manager.py**: Tests for quiz manager and singleton

## 📝 Coding Standards

- **Indentation**: 4 spaces, no tabs
- **Naming**: snake_case for functions/variables, CamelCase for classes
- **Documentation**: Google-style docstrings for all public functions/classes
- **Error Handling**: Proper exception handling with clear error messages
- **Type Hints**: Comprehensive type annotations throughout
- **Thread Safety**: Thread-safe operations where needed

## 🔧 Extending the Application

### Adding New Question Types

1. Create a new question class inheriting from `Question`
2. Implement required abstract methods
3. Add creation logic to `QuestionFactory`
4. Update the factory's supported types list
5. Add corresponding tests

### Adding New Features

1. Follow the existing modular structure
2. Implement appropriate design patterns
3. Add comprehensive tests
4. Update documentation

## 🤝 Contributing

1. Follow the established coding standards
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass before submitting

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎓 Learning Objectives

This project demonstrates:

- **Software Design Patterns**: Factory, Singleton, Observer
- **Clean Architecture**: Separation of concerns, modular design
- **Professional Practices**: Error handling, testing, documentation
- **Python Best Practices**: Type hints, docstrings, code organization
- **Thread Safety**: Proper concurrent access handling

Perfect for learning advanced Python concepts and software engineering principles!

## 📊 Class Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              QUIZ APP CLASS DIAGRAM                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐         ⬆ inherits         ┌─────────────────┐
│   Question      │◄────────────────────────────│ QuestionFactory │
│  (Abstract)     │                             │                 │
├─────────────────┤                             ├─────────────────┤
│ + text: str     │                             │ + create_question() │
│ + points: int   │                             │ + get_supported_types() │
│ + check_answer()│                             └─────────────────┘
│ + get_correct_  │                                         │
│   answer()      │                                         │ creates
│ + display_      │                                         │
│   question()    │                                         ▼
└─────────────────┘                             ┌─────────────────┐
         ▲                                      │ MultipleChoice  │
         │                                      │   Question      │
         │                                      ├─────────────────┤
         │                                      │ + options: List │
         │                                      │ + correct_answer│
         │                                      └─────────────────┘
         │
         │                                      ┌─────────────────┐
         │                                      │ TrueFalseQuestion│
         │                                      ├─────────────────┤
         │                                      │ + correct_answer│
         │                                      │   (bool)        │
         │                                      └─────────────────┘
         │
         │
┌─────────────────┐         ⬆ inherits         ┌─────────────────┐
│    Subject      │◄────────────────────────────│  QuizManager    │
│  (Abstract)     │                             │   (Singleton)   │
├─────────────────┤                             ├─────────────────┤
│ + _observers    │                             │ + _instance     │
│ + attach()      │                             │ + score         │
│ + detach()      │                             │ + timer         │
│ + notify_       │                             │ + submit_answer()│
│   observers()   │                             │ + end_quiz()    │
└─────────────────┘                             └─────────────────┘
         │                                               │
         │                                               │ notifies
         │                                               │
         ▼                                               ▼
┌─────────────────┐         ⬆ inherits         ┌─────────────────┐
│    Observer     │◄────────────────────────────│ ScoreObserver   │
│  (Abstract)     │                             ├─────────────────┤
├─────────────────┤                             │ + update()      │
│ + update()      │                             │ (score events)  │
└─────────────────┘                             └─────────────────┘
         ▲
         │
         │                                      ┌─────────────────┐
         │                                      │ TimeObserver    │
         │                                      ├─────────────────┤
         │                                      │ + update()      │
         │                                      │ (time events)   │
         │                                      └─────────────────┘
         │
         │                                      ┌─────────────────┐
         │                                      │ QuizCompletion  │
         │                                      │   Observer      │
         │                                      ├─────────────────┤
         │                                      │ + update()      │
         │                                      │ (completion)    │
         │                                      └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              DESIGN PATTERNS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🏭 FACTORY PATTERN: QuestionFactory creates different Question types        │
│  SINGLETON PATTERN: QuizManager ensures single instance                   │
│ ️ OBSERVER PATTERN: QuizManager notifies Observers on events              │
└─────────────────────────────────────────────────────────────────────────────┘
```
