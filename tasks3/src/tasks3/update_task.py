import json
import sys
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def save_tasks(tasks):
	with open(DATA_FILE, "w") as f:
		json.dump(tasks, f, indent=2)

def main():
	if len(sys.argv) < 2:
		print("Usage: python update_task.py <task_number> [--due YYYY-MM-DD] [--note \"note text\"]")
		return
	
	try:
		task_num = int(sys.argv[1])
	except ValueError:
		print("Error: Task number must be an integer")
		return
	
	# Parse arguments
	args = sys.argv[2:]
	due_date = None
	note = None
	
	i = 0
	while i < len(args):
		if args[i] == "--due" and i + 1 < len(args):
			due_date = args[i + 1]
			i += 2
		elif args[i] == "--note" and i + 1 < len(args):
			note = args[i + 1]
			i += 2
		else:
			print(f"Warning: Ignoring unknown argument: {args[i]}")
			i += 1
	
	if due_date is None and note is None:
		print("Error: You must specify at least --due or --note")
		return
	
	tasks = load_tasks()
	
	if not tasks:
		print("No tasks found.")
		return
	
	if task_num < 1 or task_num > len(tasks):
		print(f"Error: Task number must be between 1 and {len(tasks)}")
		return
	
	task = tasks[task_num - 1]
	
	if due_date:
		task["due_date"] = due_date
		print(f"Due date updated to: {due_date}")
	if note:
		task["note"] = note
		print(f"Note updated to: {note}")
	
	save_tasks(tasks)
	print(f"Task {task_num} updated: {task['description']}")

if __name__ == "__main__":
	main()
