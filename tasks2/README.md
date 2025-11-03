# Task Manager - Command-Line Task Management System

A comprehensive command-line task manager that allows you to **create**, **list**, **search**, **update**, **delete**, and **organize** tasks with full status tracking, due dates, and notes.

---

## 🧩 Features
- ✅ Add new tasks with optional due dates and notes
- ✅ List all tasks with status, due dates, and notes
- ✅ Search tasks by keyword
- ✅ Update task status (not started, started, complete)
- ✅ Update task details (due dates and notes)
- ✅ Delete tasks
- ✅ Sort and reorder tasks (alphabetically, by creation time, by due date, or swap positions)
- ✅ Persistent JSON storage (`tasks.json`)
- ✅ Automatic timestamp tracking for task creation

---

## ▶️ How to Use

# Task Manager Command-Line Programs

## 1. Storing a Task
Add a new task to the JSON file. Tasks are automatically assigned a "not started" status and a creation timestamp.

**Basic usage:**
```sh
python store.py "Your task description here"
```

**With due date:**
```sh
python store.py "Your task description" --due YYYY-MM-DD
```

**With note:**
```sh
python store.py "Your task description" --note "Additional details here"
```

**With both due date and note:**
```sh
python store.py "Complete project report" --due 2025-11-15 --note "Submit before midnight"
```

**Examples:**
```sh
python store.py "Take a shower"
python store.py "Finish homework" --due 2025-11-10
python store.py "Call dentist" --note "Ask about appointment availability"
python store.py "Team meeting" --due 2025-11-05 --note "Prepare presentation slides"
```

---

## 2. Listing Tasks
Display all tasks with their status, due dates (if any), and notes (if any).

```sh
python list.py
```

**Example output:**
```
1. [NOT STARTED] Complete project report
   Due: 2025-11-15
   Note: Submit before midnight
2. [STARTED] Take a shower
3. [COMPLETE] Call dentist
   Note: Appointment scheduled
```

---

## 3. Searching Tasks
Search for tasks containing a specific keyword in their description.

```sh
python search.py <search_term>
```

**Examples:**
```sh
python search.py shower
python search.py project
python search.py meeting
```

**Example output:**
```
1. [NOT STARTED] Team meeting
   Due: 2025-11-05
   Note: Prepare presentation slides
```

---

## 4. Updating Task Status
Mark tasks as "not started", "started", or "complete".

```sh
python update_status.py <task_number> <status>
```

**Valid status options:**
- `not started`
- `started`
- `complete`

**Examples:**
```sh
python update_status.py 1 started
python update_status.py 3 complete
python update_status.py 2 not started
```

---

## 5. Updating Task Details
Add or update due dates and notes for existing tasks.

```sh
python update_task.py <task_number> [--due YYYY-MM-DD] [--note "note text"]
```

**Examples:**
```sh
python update_task.py 1 --due 2025-12-01
python update_task.py 2 --note "Remember to bring documents"
python update_task.py 3 --due 2025-11-20 --note "High priority task"
```

---

## 6. Deleting a Task
Remove a task from the list by its number.

```sh
python delete.py <task_number>
```

**Examples:**
```sh
python delete.py 1
python delete.py 5
```

---

## 7. Sorting and Reordering Tasks
Organize your tasks in different ways using the sort_tasks.py script.

### Sort Alphabetically
Sort all tasks alphabetically by their description (case-insensitive).

```sh
python sort_tasks.py alpha
```

### Sort by Most Recently Created
Sort tasks with the most recently created tasks appearing first.

```sh
python sort_tasks.py recent
```

### Sort by Due Date
Sort tasks by due date with the nearest dates first. Tasks without due dates appear at the end.

```sh
python sort_tasks.py due
```

### Swap Two Tasks
Manually swap the positions of two tasks in the list.

```sh
python sort_tasks.py swap <position1> <position2>
```

**Examples:**
```sh
python sort_tasks.py alpha
python sort_tasks.py recent
python sort_tasks.py due
python sort_tasks.py swap 2 5
python sort_tasks.py swap 1 3
```

---

## 📝 Task Data Structure

Each task is stored in `tasks.json` with the following fields:
- **description**: The task description (required)
- **status**: Current status - "not started", "started", or "complete" (default: "not started")
- **creation_time**: ISO timestamp of when the task was created (automatic)
- **due_date**: Optional due date in YYYY-MM-DD format
- **note**: Optional additional note or description

---

## 🚀 Quick Start Examples

```sh
# Create some tasks
python store.py "Buy groceries" --due 2025-11-05
python store.py "Read chapter 5" --note "For history class"
python store.py "Exercise" --due 2025-11-04 --note "30 minutes cardio"

# View all tasks
python list.py

# Mark a task as started
python update_status.py 1 started

# Sort by due date to see what's urgent
python sort_tasks.py due

# Complete a task
python update_status.py 3 complete

# Delete finished tasks
python delete.py 3
```
