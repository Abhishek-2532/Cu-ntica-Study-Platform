# ⚛ Cuántica — Quantum Machine Learning Study Platform

> A full-stack interactive web application for learning **Quantum Machine Learning (QML)** — featuring structured courses, live quantum circuit simulations, an AI-powered tutor, a Jupyter-style notebook, and AI-generated quizzes — all in one premium platform.

---

## 📌 What Is This Project?

**Cuántica** is an educational web platform built to teach **Quantum Machine Learning (QML)** in a structured, interactive, and beginner-friendly way.

Quantum Machine Learning sits at the intersection of quantum computing and artificial intelligence. It is a rapidly growing field, but learning it is difficult because:
- There are very few good learning resources.
- The mathematics (Hilbert spaces, qubits, quantum gates) is complex.
- Hands-on practice with quantum circuits is hard to set up.

**Cuántica solves all three problems** by combining:
- **Rich course content** — Well-written, chapter-by-chapter lessons.
- **Live simulations** — Run real quantum circuits in the browser without any setup.
- **AI Tutor** — Ask any question about QML and get an instant, teacher-style answer.
- **Smart notebook** — Write and execute Python/Qiskit code inside the platform.
- **AI-generated quizzes** — Test your knowledge after every course.

---

## 🗺 How the Platform Works (For Someone New)

Here is the full journey a user takes on this platform:

```
[1] User visits the Landing Page
        ↓
[2] User registers an account (Signup)
        ↓
[3] User logs in and reaches their Dashboard
        ↓
[4] User browses all available Courses
        ↓
[5] User opens a Course → reads Chapter-by-Chapter content
        ↓
[6] User tries a live Quantum Simulation (run actual circuits!)
        ↓
[7] User asks a question to the AI Tutor (powered by Gemini)
        ↓
[8] User opens the Notebook → writes and runs Python/Qiskit code
        ↓
[9] User takes an AI-generated Quiz to test their understanding
        ↓
[10] User tracks progress on their Profile (XP, Coins, Streaks, Badges)
```

---

## ✨ Features — Explained in Detail

### 1. User Authentication System
- Users register with their **first name, last name, email, and password**.
- Passwords are **hashed securely** using `werkzeug.security` — the raw password is never stored.
- On registration, the system automatically creates a rich user profile with fields for:
  - **Personal info**: name, phone, gender, date of birth, bio.
  - **Academic info**: college, university, course, branch, semester.
  - **Address**: country, state, city.
  - **Learning data**: XP points, coins, badges, certificates, quiz attempts, simulation history, learning streak, total learning hours.
  - **Preferences**: theme, language, notifications.
- On login, the server verifies the hashed password and returns a user session with key data (name, email, role, XP, coins).
- `last_login` timestamp is updated on every successful login.

---

### 2. Course System
- Courses are stored in **MongoDB** with fields like title, description, difficulty, estimated time, main image, and full HTML content.
- Users can:
  - Browse all available courses.
  - View a course overview page.
  - Read structured course content (chapter by chapter).
  - Track which lessons and courses they've completed.

---

### 3. Course Modules (Quantum Data Encoding Curriculum)

This is the heart of the platform. Cuántica contains a detailed QML curriculum. Here is what the **Module 8: Quantum Data Encoding** curriculum covers:

| Chapter | Topic |
|---|---|
| Chapter 1 | Introduction to Quantum Data Encoding |
| Chapter 2 | What is Quantum Data Encoding? |
| Chapter 3 | Mathematical Background (Hilbert Space, Dirac Notation, Bloch Sphere, Tensor Products) |
| Chapter 4 | Types of Quantum Data Encoding |
| Chapter 5 | Basis Encoding |
| Chapter 6 | Angle Encoding |
| Chapter 7 | Amplitude Encoding |
| Chapter 8 | Feature Maps |
| Chapter 9 | Data Re-Uploading |

Each chapter contains:
- Learning objectives
- Theory explanation with real-world analogies
- Mathematical formulations
- Circuit diagrams
- Code examples in **Qiskit** and **PennyLane**
- Comparison tables
- Key takeaways

---

### 4. Live Quantum Circuit Simulations

Users can run real quantum computations inside the platform. There are **3 simulation types**:

#### Basis Encoding Simulation
- User provides a **binary string** (e.g., `1101`).
- The backend builds a **Qiskit quantum circuit** where `X` gates are applied to qubits corresponding to `1` bits.
- The circuit is simulated using **Qiskit Aer** (a quantum simulator).
- The platform returns:
  - A rendered **circuit diagram image** (PNG).
  - **Measurement counts** — how many times each basis state was observed.

#### Angle Encoding Simulation
- User provides a **list of numerical values** (e.g., `[0.5, 1.2, 2.4]`).
- Each value becomes the rotation angle for an `RY` gate applied to a qubit.
- The circuit is built and simulated, then a circuit diagram and measurement counts are returned.

#### Amplitude Encoding Simulation
- User provides a **numerical vector** (must have length that is a power of 2, e.g., 2, 4, 8).
- The vector is **automatically normalized** (`L2 norm`).
- The normalized vector is loaded into the amplitudes of a quantum state using Qiskit's `initialize()`.
- The circuit is simulated and the result (counts + circuit diagram) is returned.

> All simulations use **Qiskit** for circuit construction, **Qiskit Aer** for simulation, and **Matplotlib** (Agg backend) for rendering circuit images on the server.

---

### 5. AI Tutor (Powered by Google Gemini 2.5 Flash)

The AI Tutor is a conversational assistant that answers student questions about QML.

**How it works:**
1. Student types a question in the chat interface.
2. The frontend sends the question to the `/tutor/ask` API endpoint.
3. The backend wraps the question in a structured prompt:
   - Sets the AI as a "QML Learning Platform Tutor".
   - Instructs it to answer clearly, in max 200 words, using bullet points.
   - Focuses the AI on: Quantum Computing, QML, Python, Qiskit, and AI topics.
   - Ends every answer with a learning tip.
4. The answer from **Gemini 2.5 Flash** is returned to the student.

---

### 6. AI-Generated Quiz System (Powered by Google Gemini 2.5 Flash)

After completing a course, students can take a quiz to test their understanding.

**How it works:**
1. The quiz system fetches the course title and description from MongoDB.
2. It sends a structured prompt to **Gemini 2.5 Flash** asking it to generate:
   - Exactly **10 multiple-choice questions**.
   - Each question with exactly **4 options**.
   - **Only one correct answer** per question.
   - Pure JSON output (no extra text).
3. The JSON quiz is parsed and returned to the frontend for display.

Every quiz generation call produces a **completely new, unique quiz** — questions are never repeated.

---

### 7. Smart Notebook (Jupyter-Style Code Editor)

The notebook feature gives students a full **Python code execution environment** inside the platform — similar to a Jupyter Notebook.

**Features:**
- **Execute Python code** in real-time (including Qiskit, NumPy, Matplotlib, etc.).
- **Restart the kernel** — clears all variables and state.
- **Interrupt the kernel** — stop a long-running computation.
- **Install packages** — install any Python package directly from the notebook.
- **List installed packages** — see what is available.
- **Save notebooks** — save cells as `.ipynb` files on the server.
- **Load notebooks** — reload previously saved notebooks.
- **Export notebooks** — download as `.ipynb` (standard Jupyter format).
- **Import notebooks** — upload an existing `.ipynb` file and continue working.

This is powered by a custom `NotebookKernel` and `NotebookManager` that manage the kernel lifecycle and file I/O.

---

### 8. User Profile & Progress Tracking

Every user has a rich profile page showing:

| Field | Description |
|---|---|
| `xp` | Experience points earned by studying and taking quizzes |
| `coins` | Virtual coins earned on the platform |
| `badges` | Achievement badges |
| `certificates` | Course completion certificates |
| `learning_streak` | Consecutive days of learning |
| `total_learning_hours` | Total time spent on the platform |
| `completed_courses` | List of courses the user has fully completed |
| `completed_lessons` | Individual lessons completed with progress % |
| `favorite_courses` | Courses marked as favourite |
| `bookmarked_lessons` | Individual lessons bookmarked for later |
| `simulation_history` | Record of all simulations the user has run |
| `quiz_attempts` | Record of all quiz attempts and scores |
| `learning_level` | Beginner / Intermediate / Advanced |
| `last_login` | Timestamp of the most recent login |

---

### 9. Complaints / Feedback Page

Users can submit complaints or feedback through a dedicated `/complaints` page. This provides a channel for users to report issues or suggest improvements.

---

## 🛠 Tech Stack — Full Breakdown

### Backend (Server-Side)

| Technology | Role |
|---|---|
| **Python 3** | Core programming language |
| **Flask** | Lightweight web framework — handles routing, requests, and responses |
| **Flask Blueprints** | Modular routing — each feature has its own Blueprint (home, simulation, user, profile, etc.) |
| **MongoDB** (via `pymongo`) | NoSQL database — stores users, courses, and notebooks |
| **Werkzeug** | Password hashing (`generate_password_hash`, `check_password_hash`) |
| **Google Gemini API** (`google-generativeai`) | Powers both the AI Tutor and AI Quiz Generator |
| **Qiskit** | Quantum circuit construction and definition |
| **Qiskit Aer** | Quantum circuit simulation (runs circuits on a classical computer) |
| **Matplotlib** | Renders quantum circuit diagrams as PNG images (Agg backend for server-side rendering) |
| **NumPy** | Numerical operations (vector normalization in amplitude encoding) |
| **python-dotenv** | Loads environment variables from `.env` file |
| **Jinja2** | Server-side HTML templating (built into Flask) |

### Frontend (Client-Side)

| Technology | Role |
|---|---|
| **HTML5** | Page structure and semantic markup |
| **CSS3** | Styling — custom design system with an Arctic White light theme |
| **JavaScript (Vanilla)** | Interactivity — API calls, DOM manipulation, animations |
| **Font Awesome** | Icons throughout the interface |
| **Jinja2 Templates** | Dynamic HTML rendering from the Flask backend |

### Database (MongoDB)

| Collection | Description |
|---|---|
| `users` | All user accounts — personal info, academic info, progress, XP, coins, etc. |
| `courses` | Course catalog — title, description, difficulty, estimated time, full HTML content |

---

## 📁 Project Structure — Every File Explained

```
Cu-ntica-Study-Platform/
│
├── app.py                          ← Main entry point. Creates the Flask app,
│                                     registers all Blueprints, and starts the server.
│
├── .env                            ← Secret configuration (not committed to Git):
│                                     MONGO_URI, DATABASE_NAME, SECRET_KEY, GEMINI_API_KEY
│
├── .gitignore                      ← Files ignored by Git (e.g., .env, __pycache__)
│
├── requirements.txt                ← All Python dependencies — install with pip
│
├── website-design.txt              ← Design specification: color palette, UI/UX guidelines
│
├── readme.txt                      ← Raw HTML content of the full QML curriculum
│
│
├── Controllers/                    ← Business Logic Layer
│   │                                 (Each file handles the logic for one feature area)
│   │
│   ├── homeController.py           ← Renders all static HTML pages (home, login,
│   │                                 signup, courses, dashboard, tutor, notebook, quiz)
│   │
│   ├── userController.py           ← User registration (register_user) and
│   │                                 login (login_user) with password hashing
│   │
│   ├── profileController.py        ← Get user profile, get completed courses,
│   │                                 get completed lessons with progress
│   │
│   ├── courseController.py         ← Fetch all courses, fetch single course by ID
│   │
│   ├── userCourseController.py     ← Handle user ↔ course enrollment relationships
│   │
│   ├── simulationController.py     ← Run quantum simulations:
│   │                                 - Basis Encoding (/simulation/basis_encoding)
│   │                                 - Angle Encoding (/simulation/angle_encoding)
│   │                                 - Amplitude Encoding (/simulation/amplitude_encoding)
│   │
│   ├── notebookController.py       ← Full notebook lifecycle:
│   │                                 execute code, restart/interrupt kernel,
│   │                                 save/load/export/import .ipynb notebooks,
│   │                                 install packages
│   │
│   ├── tutorController.py          ← AI Tutor: sends student questions to
│   │                                 Gemini 2.5 Flash and returns answers
│   │
│   └── quizCreatorController.py    ← AI Quiz Generator: fetches course data,
│                                     prompts Gemini to generate a 10-question MCQ quiz,
│                                     returns structured JSON
│
│
├── Routes/                         ← URL Routing Layer
│   │                                 (Each file maps URLs to controller functions)
│   │
│   ├── userRoutes.py               ← POST /user/register, POST /user/login
│   ├── profileRoutes.py            ← POST /profile/get, POST /profile/courses
│   ├── courseRoutes.py             ← GET /api/courses, GET /api/course/<id>
│   ├── userCourseRoutes.py         ← Routes for enrollment management
│   ├── notebookRoutes.py           ← POST /notebook/execute, /save, /load, /export, /import
│   ├── tutorRoutes.py              ← POST /tutor/ask
│   └── quizCreatorRoutes.py        ← POST /quiz/generate
│
│
├── Models/                         ← Database Layer
│   │                                 (Each file is a class that talks to MongoDB)
│   │
│   ├── userModel.py                ← UserModel class:
│   │                                 create_user, get_user_by_email, get_user_by_id,
│   │                                 update_user, delete_user, update_last_login, get_profile
│   │
│   ├── courseModel.py              ← CourseModel class:
│   │                                 get_all_courses, get_course, get_completed_courses
│   │
│   └── userCourseModel.py          ← UserCourseModel class: manages enrollment & progress
│
│
├── simulation/                     ← Quantum Simulation Scripts
│   │
│   ├── angle_encoding.py           ← run_angle_encoding(data, shots, image_path)
│   │                                 Builds a Qiskit circuit with RY gates,
│   │                                 simulates it, saves circuit image, returns counts
│   │
│   ├── amplitude_encoding.py       ← run_amplitude_encoding(data, shots, image_path)
│   │                                 Normalizes the input vector, initializes quantum state,
│   │                                 simulates it, saves circuit image, returns counts
│   │
│   └── basic_coding.py             ← run_basis_encoding(binary, shots, image_path)
│                                     Applies X gates for binary 1s,
│                                     simulates it, saves circuit image, returns counts
│
│
├── templates/                      ← HTML Templates (rendered by Flask/Jinja2)
│   ├── home.html                   ← Landing page
│   ├── login.html                  ← Login form
│   ├── signup.html                 ← Registration form
│   ├── dashboard.html              ← User dashboard
│   ├── profile.html                ← User profile page
│   ├── allCourses.html             ← Course catalogue
│   ├── getCourse.html              ← Single course overview
│   ├── courseContent.html          ← Chapter content viewer
│   ├── aiTutor.html                ← AI Tutor chat interface
│   ├── notebook.html               ← Jupyter-style code notebook
│   ├── quiz.html                   ← Quiz interface
│   ├── complaints.html             ← Feedback and complaints form
│   ├── Modules/                    ← HTML files for each course module
│   └── Simulation/                 ← HTML files for simulation result pages
│
│
├── static/                         ← Static assets served to the browser
│                                     (CSS stylesheets, JS files, images, videos,
│                                      generated circuit diagram PNGs)
│
├── assets/                         ← Additional media assets
├── config/                         ← App configuration files (DB connection, settings)
├── database/                       ← Database connection utilities
├── execution/                      ← Code execution engine for the notebook
├── kernel/                         ← Jupyter kernel manager for the notebook
└── notebookManager/                ← Notebook file save/load/export/import utilities
```

---

## 🚀 Getting Started

Follow these steps exactly to run the project on your local machine.

### Step 1 — Prerequisites

Make sure the following are installed:

- **Python 3.9+** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/)
- **A MongoDB Atlas account** (free) — [Create here](https://www.mongodb.com/cloud/atlas) _(or use a local MongoDB instance)_
- **A Google Gemini API Key** (free) — [Get here](https://aistudio.google.com/app/apikey)

---

### Step 2 — Clone the Repository

```bash
git clone https://github.com/your-username/Cu-ntica-Study-Platform.git
cd Cu-ntica-Study-Platform
```

---

### Step 3 — Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your system Python.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, PyMongo, Qiskit, Qiskit-Aer, Matplotlib, Google Generative AI, and all other required packages.

---

### Step 5 — Set Up Environment Variables

Create a file named `.env` in the project root folder. Copy and fill in the following:

```env
# MongoDB — your Atlas connection string
MONGO_URI=mongodb+srv://<db_username>:<db_password>@cluster0.xxxxx.mongodb.net/

# Database name inside MongoDB
DATABASE_NAME=CUNITICA

# A random secret string used by Flask for sessions
SECRET_KEY=your_random_secret_key_here

# Your Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here
```

> ⚠️ **Never share or commit your `.env` file.** It contains secret credentials. It is already listed in `.gitignore`.

---

### Step 6 — Run the Application

```bash
python app.py
```

Flask will start in **debug mode**. Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🌐 All Application Routes

### Page Routes (HTML Pages)

| URL | Page | Description |
|---|---|---|
| `/` | Home | Landing page with platform overview |
| `/signup` | Signup | New user registration form |
| `/login` | Login | User login form |
| `/dashboard` | Dashboard | Personalized student dashboard |
| `/profile` | Profile | User profile and progress stats |
| `/courses` | All Courses | Browse the full course catalogue |
| `/course/<id>` | Course Detail | Overview of a specific course |
| `/course/content` | Course Content | Chapter-by-chapter lesson reader |
| `/tutor` | AI Tutor | Chat interface with the Gemini AI tutor |
| `/notebook` | Notebook | Jupyter-style Python code notebook |
| `/quiz` | Quiz | AI-generated quiz for a course |
| `/complaints` | Complaints | Feedback and complaint submission form |

### API Routes (JSON Endpoints)

| Method | URL | Description |
|---|---|---|
| `POST` | `/user/register` | Register a new user |
| `POST` | `/user/login` | Login and get user data |
| `POST` | `/profile/get` | Get full user profile |
| `POST` | `/profile/courses` | Get user's completed courses & lessons |
| `GET` | `/api/courses` | Fetch all courses |
| `GET` | `/api/course/<id>` | Fetch a single course |
| `POST` | `/simulation/basis_encoding` | Run Basis Encoding simulation |
| `POST` | `/simulation/angle_encoding` | Run Angle Encoding simulation |
| `POST` | `/simulation/amplitude_encoding` | Run Amplitude Encoding simulation |
| `POST` | `/notebook/execute` | Execute Python code in the notebook kernel |
| `POST` | `/notebook/restart` | Restart the notebook kernel |
| `POST` | `/notebook/interrupt` | Interrupt the notebook kernel |
| `POST` | `/notebook/install` | Install a Python package |
| `GET` | `/notebook/packages` | List installed packages |
| `GET` | `/notebook/list` | List saved notebooks |
| `POST` | `/notebook/save` | Save notebook cells to file |
| `POST` | `/notebook/load` | Load a saved notebook |
| `POST` | `/notebook/export` | Export notebook as `.ipynb` |
| `POST` | `/notebook/import` | Import an `.ipynb` file |
| `POST` | `/tutor/ask` | Ask the AI Tutor a question |
| `POST` | `/quiz/generate` | Generate a 10-question AI quiz for a course |

---

## 🧠 User Data Model — What Gets Stored Per User

When a user registers, MongoDB stores all of the following in the `users` collection:

```
Personal:      first_name, last_name, full_name, email, phone, gender, dob, bio, profile_image
Academic:      college, university, course, branch, semester
Location:      country, state, city
Learning:      learning_level, current_course, completed_courses[], completed_lessons[],
               favorite_courses[], bookmarked_lessons[], learning_streak,
               total_learning_hours, xp, coins, badges[], certificates[],
               quiz_attempts[], simulation_history[]
Preferences:   theme, language, notifications
Account:       role, is_verified, email_verified, phone_verified, is_active, is_banned,
               login_provider, last_login, password_reset_token, otp, otp_expiry
Timestamps:    created_at, updated_at
```

---

## 🔬 How Quantum Simulations Work — Step by Step

Here is exactly what happens when you run the **Angle Encoding** simulation as an example:

1. **Frontend**: User enters values like `0.5, 1.2, 2.4` and clicks **"Run Simulation"**.
2. **Request**: The browser sends `POST /simulation/angle_encoding` with `{ "data": [0.5, 1.2, 2.4], "shots": 1024 }`.
3. **Backend validates**: Checks that all values are numeric.
4. **Circuit built**: A 3-qubit `QuantumCircuit` is created. `RY(0.5)` is applied to qubit 0, `RY(1.2)` to qubit 1, `RY(2.4)` to qubit 2.
5. **Measurement added**: `measure_all()` is added to the circuit.
6. **Simulation runs**: `AerSimulator` runs the circuit for 1024 shots.
7. **Results collected**: The simulator returns measurement counts (e.g., `{"000": 512, "111": 512}`).
8. **Image rendered**: The circuit is drawn using `qc.draw(output="mpl")` and saved as a PNG using Matplotlib.
9. **Response sent**: The backend sends back `{ "counts": {...}, "image": "/static/angle_encoding.png" }`.
10. **Frontend displays**: The circuit diagram image and measurement bar chart are shown to the user.

The same flow applies to **Basis Encoding** and **Amplitude Encoding** with different circuit logic.

---

## 🎨 Design System

The platform uses a custom **Arctic White light theme** with the following color palette:

```css
:root {
  --bg:           #F7FEFF;   /* Arctic White — main background */
  --surface:      #FFFFFF;   /* Card backgrounds */
  --surface-alt:  #E0FAF4;   /* Section backgrounds */

  --primary:      #6CE5BF;   /* Main brand color */
  --primary-light:#83E9CA;
  --primary-soft: #ADF1DD;

  --secondary:    #E3EDFE;

  --text:         #1E293B;   /* Primary text */
  --text-muted:   #64748B;   /* Secondary / helper text */

  --border:       #DCEEF2;   /* Border color */
}
```

The UI is designed to be **responsive** — it works correctly on mobile, tablet, and desktop screens. It includes:
- Smooth animations and hover effects
- Premium card layouts
- Clean typography hierarchy
- Font Awesome icons (no emoji)

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork** this repository on GitHub.
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** — follow the existing project structure.
4. **Commit** your changes with a clear message:
   ```bash
   git commit -m "Add: brief description of what you added"
   ```
5. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** on GitHub and describe what you changed and why.

### Contribution Ideas
- Add new quantum simulation types (e.g., Grover's algorithm, VQC circuits)
- Add more course modules (quantum gates, quantum circuits, QSVM, QNN)
- Add a leaderboard for XP/coins
- Add email verification on signup
- Add a video lecture player inside course content
- Improve mobile responsiveness

---

## ⚙️ Common Issues & Fixes

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: qiskit_aer` | Run `pip install qiskit-aer` |
| `ModuleNotFoundError: google.generativeai` | Run `pip install google-generativeai` |
| `pymongo.errors.ServerSelectionTimeoutError` | Check that your `MONGO_URI` in `.env` is correct and your IP is whitelisted in MongoDB Atlas |
| `GEMINI_API_KEY not working` | Make sure the key is correct and the Gemini API is enabled in your Google Cloud project |
| Matplotlib crashes on server | Already handled — the project uses `matplotlib.use("Agg")` (non-interactive backend) |
| Port 5000 already in use | On macOS, AirPlay uses port 5000. Run `python app.py --port=5001` or disable AirPlay |

---

## 📄 License

This project is currently **unlicensed** — all rights are reserved by the author. Contact the author before using this code in any commercial or public project.

---

<div align="center">
  <strong>Cuántica</strong> — Where Classical Data Meets Quantum Intelligence.<br/>
  Built with Flask · MongoDB · Qiskit · Google Gemini
</div>
