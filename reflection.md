# 🧠 Reflection: Quiz App (Design Patterns in Python)

## Why I Chose These Patterns

I specifically chose Factory, Singleton, and Observer patterns because they naturally fit the structure of a quiz system and each of them solves a unique problem.

### 1. Factory Pattern

I used the Factory Pattern as it helped me handle multiple question types (like MCQ and True/False) without hardcoding logic all over the place. It made the system super flexible — I can easily add more types like fill-in-the-blank in future without touching the rest of the code.

### 2. Singleton Pattern

The `QuizManager` was designed as a Singleton to ensure there's only one place controlling quiz state timer, score, current question, and so on. This helped maintain consistency across the app, especially since everything revolves around this central controller.

### 3. Observer Pattern

I used the Observer Pattern to keep parts of the app loosely connected. Instead of tightly coupling the quiz logic and the output messages, I attached separate observers (like ScoreObserver, TimeObserver, and CompletionObserver) to get updates. This made the app more modular and clean.

---

## How These Patterns Work Together

Each pattern here works really well together.

- The **Factory Pattern** handled the creation of questions. Whether it’s MCQ or True/False, I didn’t have to write separate logic every time. I could just plug in the question type, and the rest stayed clean. That saved me from messy if-else structures and made adding new question types later so easy.

- Then comes the **Singleton Pattern** — the QuizManager. This was the one place where everything about the quiz lived: score, current question, timer, user. I didn’t have to pass data around everywhere, because this one instance was shared across the app. It gave a lot of control and made sure things didn’t break just because I called something twice.

- The best integration was the **Observer Pattern**. I attached different observers — one for score updates, one for timing, and one for completion. So instead of writing print() calls all over my logic, I could just notify observers and let them handle the messages. It felt like the logic and the reactions were nicely separated.

This separation made the project feel like a real, scalable system. Adding or removing functionality didn’t break other parts of the app.

---

## What I Learned

- I finally _understood_ how these design patterns help in real code, not just theory.
- I learned the value of **clean architecture** — separating logic into proper modules and thinking in terms of “responsibility.”
- I became more confident in using **thread locks and type hints**, and organizing code like a professional project.
- I also practiced **writing unit tests**, which helped me debug and trust my code better.

---

## Challenges I Faced

- The biggest challenge was understanding how to **connect observers** in the main flow. I had them mocked in tests but didn’t integrate them properly until later.
- At first, **the folder structure** and file naming were confusing — I kept changing them to find what felt most organized.
- Lastly, staying consistent with **coding standards** like docstrings, type hints, and error handling across all files took extra effort — but it was worth it.

---

## Final Thoughts

This project helped me think like a software engineer. I didn’t just code — I designed. I made sure the system was modular, scalable, and easy to test. It gave me confidence and a strong foundation in Python, software patterns, and professional coding practices.
