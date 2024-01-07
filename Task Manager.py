from datetime import datetime
import json

class Task:
    def __init__(self, name, status, duedate, folder="main"):
        self.name = name
        self.status = status
        self.duedate = duedate
        self.folder = folder

class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M')
        return json.JSONEncoder.default(self, obj)


def create_new_task(tasklist):
    new_task_name = input("Enter a new task: ")
    new_due_date_str = input("Enter the duedate and time for the task (fomat YYYY/MM/DD HH:MM): ")
    try:
        new_due_date = datetime.strptime(new_due_date_str, '%Y/%m/%d %H:%M')
    except ValueError:
        print("Invalid date and time format, please use the format (YYYY/MM/DD HH:MM)")
        return

    new_task = Task(name=new_task_name, status="incomplete", duedate=new_due_date)
    tasklist.append(new_task)
    print(f'Task {new_task_name} created successfully')
    save_tasks(tasklist)

def save_tasks(tasklist):
    all_tasks = [task.__dict__ for task in tasklist]
    with open('tasks.json', 'w') as file:
        json.dump(all_tasks, file, cls=TaskEncoder)

def save_completed_tasks(completed_tasklist):
    all_completed_tasks = [task.__dict__ for task in completed_tasklist]
    with open('completed_tasks.json', 'w') as file:
        json.dump(all_completed_tasks, file, cls=TaskEncoder)

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            file_content = file.read()
            if not file_content:
                print("Tasks file is empty. Creating a new one.")
                return []
            data = json.loads(file_content)
            return [Task(task['name'], task['status'], datetime.strptime(task['duedate'], '%Y/%m/%d %H:%M')) for task in data]
    except FileNotFoundError:
        print("Tasks file not found. Creating a new one.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for tasks: {e}")
        print("File may contain invalid JSON. Creating a new one.")
        return []

def load_completed_tasks():
    try:
        with open('completed_tasks.json', 'r') as file:
            file_content = file.read()
            if not file_content:
                print("Completed tasks file is empty. Creating a new one.")
                return []
            data = json.loads(file_content)
            return [Task(task['name'], task['status'], datetime.strptime(task['duedate'], '%Y/%m/%d %H:%M'), folder="completed") for task in data]
    except FileNotFoundError:
        print("Completed tasks file not found. Creating a new one.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for completed tasks: {e}")
        print("File may contain invalid JSON. Creating a new one.")
        return []

def view_task_list(tasklist):
    print("Main Folder:")
    for idx, task in enumerate(tasklist, start=1):
        if task.folder == "main":
            print(f'{idx}- {task.name} - on {task.duedate} is {task.status}')

def view_completed_tasks(completed_tasklist):
    print("Completed Tasks:")
    for idx, task in enumerate(completed_tasklist, start=1):
        print(f'{idx}- {task.name} - on {task.duedate} is {task.status} (Completed)')

def mark_as_completed(tasklist, completed_tasklist):
    view_task_list(tasklist)
    task_number = int(input("Please enter the number of the completed task: "))
    try:
        selected_task = tasklist[task_number - 1]
        selected_task.status = "complete"
        selected_task.folder = "completed"
        completed_tasklist.append(selected_task)
        tasklist.remove(selected_task)
        print(f'Task {selected_task.name} is marked as completed and moved to the completed task list')
        save_tasks(tasklist)
        save_completed_tasks(completed_tasklist)
    except (IndexError, ValueError):
        print("Please enter a valid task number ")

def edit_task(tasklist):
    view_task_list(tasklist)
    try:
        edited_task_number = int(input("Please Enter the number of the task you would like to edit "))
        if 1 <= edited_task_number <= len(tasklist):
            edited_task = tasklist[edited_task_number - 1]

            new_edited_name = input("Enter the new task name: ")
            new_due_date_str = input("Enter the new duedate (format YYYY/MM/DD HH:MM): ")
            try:
                new_due_date = datetime.strptime(new_due_date_str, '%Y/%m/%d %H:%M')
            except ValueError:
                print("Invalid date and time format, please use the format (YYYY/MM/DD HH:MM) ")
                return

            edited_task.name = new_edited_name
            edited_task.duedate = new_due_date

            print(f'Task {edited_task.name} was changed successfully')
            print("Updated task list:", tasklist)
            save_tasks(tasklist)
        else:
            print("Please enter a valid task number ")
    except (ValueError, IndexError) as e:
        print(f"Error editing task: {e}")
        print("Please enter a valid task number ")

def delete_task(tasklist):
    view_task_list(tasklist)
    try:
        deleted_task_number = int(input("Please enter the number of the task you would like to delete: "))
        if 1 <= deleted_task_number <= len(tasklist):
            deleted_task = tasklist.pop(deleted_task_number - 1)
            print(f'Task {deleted_task.name} deleted successfully')
            print("Updated task list:", tasklist)
            save_tasks(tasklist)
        else:
            print("Please enter a valid task number ")
    except (ValueError, IndexError) as e:
        print(f"Error deleting task: {e}")
        print("Please enter a valid task number ")


tasklist = load_tasks()
completed_tasklist = load_completed_tasks()

while True:
    print("""
    Options:
    
    1- Add a new task
    
    2- Mark a task as completed
    
    3- Edit a task
    
    4- Delete a task
    
    5- View task list
    
    6- View completed tasks
    
    7- Exit
    """)
    choice = input("Please choose an option (1/2/3/4/5/6/7): ")
    if choice == "1":
        create_new_task(tasklist)
    elif choice == "2":
        mark_as_completed(tasklist, completed_tasklist)
    elif choice == "3":
        edit_task(tasklist)
    elif choice == "4":
        delete_task(tasklist)
    elif choice == "5":
        view_task_list(tasklist)
    elif choice == "6":
        view_completed_tasks(completed_tasklist)
    elif choice == "7":
        print("Goodbye")
        save_tasks(tasklist)
        save_completed_tasks(completed_tasklist)
        break
    else:
        print("Please enter a valid choice")