# Tasks1 Prototype

This is a simple command-line task manager prototype.  
It allows you to **store**, **list**, and **search** tasks saved in a JSON file.

---

## 🧩 Features
- Add new tasks
- List all tasks
- Search tasks by keyword
- Persistent JSON storage (`tasks.json`)

---

## ▶️ How to Run

# Task Manager Command-Line Programs

## 1. Storing a Task
Add a new task to the JSON file:

```sh
python store.py "Your task description here"
```
Example:
```sh
python store.py "Take a shower"
```

## 2. Listing Tasks
List all tasks:

```sh
python list.py
```

List tasks containing a search term:

```sh
python list.py search_term
```
Example:
```sh
python list.py shower
```

## 3. Searching Tasks
Search for tasks containing a term:

```sh
python search.py search_term
```
Example:
```sh
python search.py shower
```
