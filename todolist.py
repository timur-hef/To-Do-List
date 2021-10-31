from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# First, you need to create your database file. To create it, you should use the create_engine() method, where file_name
# is the database file name
# check_same_thread=False argument allows connecting to the database from another thread. It's required for the test
# purpose, otherwise, you will get an exception.
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# Once you've created your database file, you need to create a table in it. First, create a model class that describes
# the table in the database. All model classes should inherit from the DeclarativeMeta class that is returned by
# declarative_base():
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return f"{self.task};{self.deadline.day} {self.deadline.strftime('%b')}"


# After we've described our table, it's time to create it in our database. All we need is to call the create_all()
# method and pass engine to it. This method creates a table in our database by generating SQL queries according to
# the models we described.
Base.metadata.create_all(engine)

# Now we can access the database and store data in it. To access the database, we need to create a session.
# The session object is the only thing you need to manage the database.
Session = sessionmaker(bind=engine)
session = Session()


def print_tasks(list_of_tasks):
    if not list_of_tasks:
        print("Nothing to do!")
    else:
        i = 1
        for task in list_of_tasks:
            print(f"{i}.", task.task)
            i += 1


weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

today = datetime.today().date()
while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    choice = int(input())
    if choice == 1:
        today_tasks = session.query(Table).filter(Table.deadline == today).all()
        print(f"\nToday {today.day} {today.strftime('%b')}:")
        print_tasks(today_tasks)
    elif choice == 2:
        day = today
        day_tasks = session.query(Table).filter(Table.deadline == day).all()
        print(f"\n{weekdays[day.weekday()]} {day.day} {day.strftime('%b')}:")
        print_tasks(day_tasks)
        for i in range(6):
            day = day + timedelta(days=1)
            print(f"\n{weekdays[day.weekday()]} {day.day} {day.strftime('%b')}:")
            day_tasks = session.query(Table).filter(Table.deadline == day).all()
            print_tasks(day_tasks)
    elif choice == 3:
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        if not all_tasks:
            print("Nothing to do!")
        else:
            i = 1
            for task in all_tasks:
                print(f"{i}.", f"{task.task}.", task.deadline.day, task.deadline.strftime('%b'))
                i += 1
    elif choice == 4:
        missed_tasks = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        print("Missed tasks:")
        if not missed_tasks:
            print("Nothing is missed!")
        else:
            i = 1
            for task in missed_tasks:
                print(f"{i}.", f"{task.task}.", task.deadline.day, task.deadline.strftime('%b'))
                i += 1
    elif choice == 5:
        row = Table(task=input("\nEnter task\n"), deadline=datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d').date())
        session.add(row)
        session.commit()
        print("The task has been added!")
    elif choice == 6:
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        if not all_tasks:
            print("Nothing to delete!")
        else:
            print("Choose the number of the task you want to delete:")
            i = 1
            for task in all_tasks:
                print(f"{i}.", f"{task.task}.", task.deadline.day, task.deadline.strftime('%b'))
                i += 1
            deleting_choice = int(input())
            session.delete(all_tasks[deleting_choice - 1])
            session.commit()
            print("The task has been deleted!")
    else:
        print("\nBye!")
        break
    print()