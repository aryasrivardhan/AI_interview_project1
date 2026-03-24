import sqlite3
import random
import time
from datetime import datetime
from flask import Flask, render_template, request, g, redirect, url_for

app = Flask(__name__)
DB_NAME = 'interview_prep.db'

# Dummy question database logically categorized and expanded
QUESTION_DB = {
    "Data Structures": [
        {"q": "What is an array?", "diff": "Easy", "ans": "An array is a collection of items stored at contiguous memory locations."},
        {"q": "What is a linked list?", "diff": "Easy", "ans": "A sequence of elements where each element points to the next one."},
        {"q": "How does a Stack differ from a Queue?", "diff": "Easy", "ans": "Stack is LIFO, Queue is FIFO."},
        {"q": "What is a hash table?", "diff": "Medium", "ans": "A data structure that implements an associative array abstract data type, mapping keys to values using a hash function."},
        {"q": "How do you detect a cycle in a linked list?", "diff": "Medium", "ans": "Use Floyd's Cycle-Finding Algorithm (Tortoise and Hare)."},
        {"q": "What is the difference between BFS and DFS traversal?", "diff": "Medium", "ans": "BFS explores level by level using a queue. DFS explores as far as possible along each branch using a stack or recursion."},
        {"q": "Describe a Red-Black tree.", "diff": "Hard", "ans": "A self-balancing binary search tree where each node has an extra bit for color to ensure the tree remains balanced."},
        {"q": "What is the time complexity of building a heap?", "diff": "Hard", "ans": "O(N) time complexity."},
        {"q": "How does Dijkstra's algorithm work?", "diff": "Hard", "ans": "Finds the shortest path between nodes in a graph by maintaining a set of unvisited nodes and iteratively picking the node with the lowest distance."},
        {"q": "What is an AVL Tree?", "diff": "Hard", "ans": "A self-balancing binary search tree where the heights of the two child subtrees of any node differ by at most one."}
    ],
    "Python": [
        {"q": "What are lists and tuples?", "diff": "Easy", "ans": "Lists are mutable, tuples are immutable."},
        {"q": "Define PEP 8.", "diff": "Easy", "ans": "PEP 8 is the style guide for Python code."},
        {"q": "What is a dictionary in Python?", "diff": "Easy", "ans": "An unordered, mutable, and indexed collection of key-value pairs."},
        {"q": "What are decorators?", "diff": "Medium", "ans": "A way to modify the behavior of a function or class. It wraps another function."},
        {"q": "Explain list comprehension.", "diff": "Medium", "ans": "A concise syntactic construct to create a new list based on an existing iterable."},
        {"q": "What is `*args` and `**kwargs`?", "diff": "Medium", "ans": "`*args` passes variable number of non-keyworded arguments. `**kwargs` passes variable number of keyword arguments."},
        {"q": "What is the GIL?", "diff": "Hard", "ans": "Global Interpreter Lock. It prevents multiple native threads from executing Python bytecodes at once."},
        {"q": "Explain metaclasses in Python.", "diff": "Hard", "ans": "A metaclass is a class whose instances are classes. It defines the behavior of classes."},
        {"q": "What are generators?", "diff": "Hard", "ans": "Functions that use the `yield` keyword to return an iterator, generating values lazily to save internal memory."},
        {"q": "How does Python handle memory management?", "diff": "Hard", "ans": "Python incorporates a private heap and uses automatic garbage collection (reference counting and cyclic garbage collector)."}
    ],
    "DBMS": [
        {"q": "What is DBMS?", "diff": "Easy", "ans": "Database Management System, software for storing and managing databases."},
        {"q": "What is a primary key?", "diff": "Easy", "ans": "A column or a set of columns that uniquely identifies a row in a table."},
        {"q": "Explain defining a foreign key.", "diff": "Easy", "ans": "A field in a table that uniquely identifies a row of another table, enforcing referential integrity."},
        {"q": "Explain ACID properties.", "diff": "Medium", "ans": "Atomicity, Consistency, Isolation, Durability. Fundamental properties of a transaction."},
        {"q": "What is normalization?", "diff": "Medium", "ans": "Process of organizing data to reduce redundancy and improve data integrity (1NF, 2NF, 3NF)."},
        {"q": "Explain LEFT JOIN vs INNER JOIN.", "diff": "Medium", "ans": "INNER JOIN returns matching rows in both tables. LEFT JOIN returns all rows from the left table and matched rows from the right."},
        {"q": "Explain the difference between clustered and non-clustered index.", "diff": "Hard", "ans": "Clustered index determines the physical order of data. Non-clustered creates a separate structure for the index."},
        {"q": "What is a deadlock and how to prevent it?", "diff": "Hard", "ans": "A situation where two transactions wait for each other's locks forever. Prevent it by ensuring a specific locking order."},
        {"q": "What are database triggers?", "diff": "Hard", "ans": "Stored programs that automatically execute in response to specific events (INSERT, UPDATE, DELETE)."},
        {"q": "Explain what a distributed database is.", "diff": "Hard", "ans": "A database where multiple storage devices are not all attached to a common processor, but exist across multiple computers."}
    ],
    "OS": [
        {"q": "What is an Operating System?", "diff": "Easy", "ans": "Software that manages computer hardware and provides common services for computer programs."},
        {"q": "What is a process vs thread?", "diff": "Easy", "ans": "Process is a program in execution. Thread is light-weight sequence of instructions within a process."},
        {"q": "What is GUI vs CLI?", "diff": "Easy", "ans": "Graphical User Interface (visual interaction) vs Command Line Interface (text-based interaction)."},
        {"q": "What is virtual memory?", "diff": "Medium", "ans": "A memory management capability that provides an idealized abstraction of storage resources, using disk space to simulate extra RAM."},
        {"q": "Explain paging.", "diff": "Medium", "ans": "A memory management scheme to retrieve data from secondary storage in fixed-size blocks (pages)."},
        {"q": "What is a kernel?", "diff": "Medium", "ans": "The central component of an OS that manages system resources and bridges hardware/software interaction."},
        {"q": "What is a semaphore?", "diff": "Hard", "ans": "A synchronization variable used to control access to a common resource by multiple processes."},
        {"q": "Explain context switching.", "diff": "Hard", "ans": "The process of saving the state of a process/thread and restoring the state of another to share a single CPU."},
        {"q": "What is a race condition?", "diff": "Hard", "ans": "An undesirable situation that occurs when a system attempts to perform two or more operations at the same time on shared data."},
        {"q": "Explain Thrashing in memory management.", "diff": "Hard", "ans": "A state where the CPU spends more time swapping pages in and out of memory than executing actual instructions."}
    ]
}

def init_db():
    """Create the SQLite database table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                num_questions INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

init_db()

def get_db():
    """Retrieve or create a database connection in the app context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)
        # Use row factory to return dict-like rows
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of every request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('topic')
    difficulty = request.form.get('difficulty')
    
    # Validation fallback on server
    if not topic or not difficulty:
        return redirect(url_for('index'))
        
    try:
        num_questions = int(request.form.get('num_questions', 1))
        num_questions = max(1, min(10, num_questions))
    except (ValueError, TypeError):
        num_questions = 1

    # Simulate AI loading time for realism
    time.sleep(1.0)
    
    # Log user inputs to the database
    db = get_db()
    db.execute('''
        INSERT INTO search_history (topic, difficulty, num_questions)
        VALUES (?, ?, ?)
    ''', (topic, difficulty, num_questions))
    db.commit()
    
    # Advanced logic: Randomization & difficulty supplement
    all_topic_questions = QUESTION_DB.get(topic, [])
    # Find matching difficulty exactly
    available_questions = [q for q in all_topic_questions if q['diff'] == difficulty]
    
    # If not enough exact matches, supplement with other difficulties
    if len(available_questions) < num_questions:
        supplemental = [q for q in all_topic_questions if q not in available_questions]
        random.shuffle(supplemental)
        available_questions.extend(supplemental)
        
    # Final random shuffle so outputs are distinct on each run
    random.shuffle(available_questions)
    generated = available_questions[:num_questions]
        
    return render_template('result.html', questions=generated, topic=topic, difficulty=difficulty)

@app.route('/history')
def history():
    """Route displaying previous generation histories."""
    db = get_db()
    cur = db.execute('''
        SELECT id, topic, difficulty, num_questions, created_at
        FROM search_history
        ORDER BY created_at DESC
        LIMIT 50
    ''')
    records = cur.fetchall()
    return render_template('history.html', history=records)

if __name__ == '__main__':
    app.run(debug=True)
