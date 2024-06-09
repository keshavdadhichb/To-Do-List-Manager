

import json
import os

class TaskItem:
    def __init__(self, details, is_done=False):
        self.details = details
        self.is_done = is_done

    def to_dict(self):
        return {
            'details': self.details,
            'is_done': self.is_done
        }

    @staticmethod
    def from_dict(task_dict):
        return TaskItem(
            details=task_dict['details'],
            is_done=task_dict['is_done']
        )

TASKS_STORAGE = 'task_items.json'

def fetch_tasks():
    if not os.path.exists(TASKS_STORAGE):
        return []
    with open(TASKS_STORAGE, 'r') as file:
        tasks_data = json.load(file)
        return [TaskItem.from_dict(task) for task in tasks_data]

def store_tasks(task_items):
    with open(TASKS_STORAGE, 'w') as file:
        json.dump([task.to_dict() for task in task_items], file, indent=4)

def add_task_item(details):
    task_items = fetch_tasks()
    task_items.append(TaskItem(details=details))
    store_tasks(task_items)
    print(f"Added task: {details}")

def display_tasks():
    task_items = fetch_tasks()
    if not task_items:
        print("No tasks to show.")
        return
    for index, task in enumerate(task_items, start=1):
        status = "✓" if task.is_done else "✗"
        print(f"{index}. [{status}] {task.details}")

def mark_task_done(index):
    task_items = fetch_tasks()
    if 0 <= index < len(task_items):
        task_items[index].is_done = True
        store_tasks(task_items)
        print(f"Marked task {index + 1} as completed.")
    else:
        print(f"No task at index {index + 1}.")

def delete_task_item(index):
    task_items = fetch_tasks()
    if 0 <= index < len(task_items):
        removed_task = task_items.pop(index)
        store_tasks(task_items)
        print(f"Removed task: {removed_task.details}")
    else:
        print(f"No task at index {index + 1}.")

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python todo.py [add|list|complete|remove] [task details|task index]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python todo.py add [task details]")
            return
        details = " ".join(sys.argv[2:])
        add_task_item(details)

    elif command == "list":
        display_tasks()

    elif command == "complete":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Usage: python todo.py complete [task index]")
            return
        index = int(sys.argv[2]) - 1
        mark_task_done(index)

    elif command == "remove":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Usage: python todo.py remove [task index]")
            return
        index = int(sys.argv[2]) - 1
        delete_task_item(index)

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
