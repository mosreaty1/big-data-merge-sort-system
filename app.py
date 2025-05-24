from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import pymongo
import os
import json
import time
import random
import heapq
import tempfile
import shutil
import csv
import io
import threading
from datetime import datetime, timedelta
from bson import ObjectId
import statistics
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = "mongodb://mo123:mo123@ac-w97brco-shard-00-00.davqq8d.mongodb.net:27017,ac-w97brco-shard-00-01.davqq8d.mongodb.net:27017,ac-w97brco-shard-00-02.davqq8d.mongodb.net:27017/?replicaSet=atlas-14cu20-shard-0&ssl=true&authSource=admin"
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client['employee_db']
    employees_collection = db['employees']
    operations_collection = db['operations']
    analytics_collection = db['analytics']
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")

class Employee:
    def __init__(self, emp_id, first_name, last_name, department, salary, hire_date=None, position=None, email=None):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.salary = salary
        self.hire_date = hire_date or datetime.now().strftime('%Y-%m-%d')
        self.position = position or "Employee"
        self.email = email or f"{first_name.lower()}.{last_name.lower()}@company.com"
    
    def to_dict(self):
        return {
            'emp_id': self.emp_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'department': self.department,
            'salary': self.salary,
            'hire_date': self.hire_date,
            'position': self.position,
            'email': self.email,
            'full_name': f"{self.first_name} {self.last_name}"
        }
    
    def __str__(self):
        return f"{self.emp_id},{self.first_name},{self.last_name},{self.department},{self.salary},{self.hire_date},{self.position},{self.email}"

class AdvancedExternalMergeSort:
    def __init__(self, chunk_size=1000):
        self.chunk_size = chunk_size
        self.temp_dir = tempfile.mkdtemp()
        self.operations_log = []
        self.sorting_progress = {'current': 0, 'total': 0, 'status': 'idle'}
        
    def log_operation(self, operation, time_taken, details=None):
        log_entry = {
            'operation': operation,
            'time_taken': time_taken,
            'timestamp': datetime.now(),
            'details': details or {}
        }
        self.operations_log.append(log_entry)
        operations_collection.insert_one(log_entry)
    
    def update_progress(self, current, total, status):
        self.sorting_progress = {
            'current': current,
            'total': total,
            'status': status,
            'percentage': round((current / total) * 100, 2) if total > 0 else 0
        }
    
    def generate_advanced_employees(self, num_employees=16000, num_files=16):
        """Generate advanced employee data with more realistic fields"""
        start_time = time.time()
        
        departments = [
            'Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'IT', 
            'Operations', 'Legal', 'Research', 'Customer Service'
        ]
        
        positions = {
            'Engineering': ['Software Engineer', 'Senior Engineer', 'Lead Engineer', 'Architect'],
            'Sales': ['Sales Rep', 'Account Manager', 'Sales Director', 'VP Sales'],
            'Marketing': ['Marketing Specialist', 'Content Manager', 'CMO', 'Brand Manager'],
            'HR': ['HR Generalist', 'Recruiter', 'HR Director', 'CHRO'],
            'Finance': ['Financial Analyst', 'Accountant', 'CFO', 'Controller'],
            'IT': ['IT Support', 'System Admin', 'DevOps Engineer', 'CTO'],
            'Operations': ['Operations Manager', 'Process Analyst', 'COO', 'Operations Director'],
            'Legal': ['Legal Counsel', 'Paralegal', 'General Counsel', 'Compliance Officer'],
            'Research': ['Research Scientist', 'Lab Technician', 'Research Director', 'Principal Scientist'],
            'Customer Service': ['Support Rep', 'Customer Success', 'Support Manager', 'VP Customer Success']
        }
        
        first_names = [
            'John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Anna', 
            'Tom', 'Emma', 'Alex', 'Maria', 'James', 'Jennifer', 'Robert', 'Michelle',
            'William', 'Elizabeth', 'Joseph', 'Patricia', 'Thomas', 'Linda', 'Charles', 'Barbara'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
            'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White'
        ]
        
        employees_per_file = num_employees // num_files
        file_paths = []
        
        # Clear existing employees from MongoDB
        employees_collection.delete_many({})
        
        self.update_progress(0, num_files, 'Generating employee data...')
        
        for file_idx in range(num_files):
            file_path = os.path.join(self.temp_dir, f'employees_{file_idx}.txt')
            file_paths.append(file_path)
            
            with open(file_path, 'w') as f:
                employees_batch = []
                for i in range(employees_per_file):
                    emp_id = file_idx * employees_per_file + i + 1
                    department = random.choice(departments)
                    hire_date = (datetime.now() - timedelta(days=random.randint(30, 3650))).strftime('%Y-%m-%d')
                    
                    employee = Employee(
                        emp_id=emp_id,
                        first_name=random.choice(first_names),
                        last_name=random.choice(last_names),
                        department=department,
                        salary=round(random.uniform(35000, 150000), 2),
                        hire_date=hire_date,
                        position=random.choice(positions[department])
                    )
                    f.write(str(employee) + '\n')
                    employees_batch.append(employee.to_dict())
                
                # Insert batch into MongoDB
                employees_collection.insert_many(employees_batch)
            
            self.update_progress(file_idx + 1, num_files, f'Generated file {file_idx + 1}/{num_files}')
        
        time_taken = time.time() - start_time
        self.log_operation('generate_advanced_data', time_taken, {
            'num_files': num_files, 
            'num_employees': num_employees,
            'fields': ['emp_id', 'name', 'department', 'salary', 'hire_date', 'position', 'email']
        })
        
        return file_paths
    
    def read_employees_from_file(self, file_path):
        """Read employees from a file with enhanced format"""
        employees = []
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    employee = Employee(
                        emp_id=int(parts[0]),
                        first_name=parts[1],
                        last_name=parts[2],
                        department=parts[3],
                        salary=float(parts[4]),
                        hire_date=parts[5] if len(parts) > 5 else None,
                        position=parts[6] if len(parts) > 6 else None,
                        email=parts[7] if len(parts) > 7 else None
                    )
                    employees.append(employee)
        return employees
    
    def write_employees_to_file(self, employees, file_path):
        """Write employees to a file"""
        with open(file_path, 'w') as f:
            for employee in employees:
                f.write(str(employee) + '\n')
    
    def quick_sort_employees(self, employees, sort_by='emp_id'):
        """Quick sort implementation for comparison"""
        if len(employees) <= 1:
            return employees
        
        pivot = employees[len(employees) // 2]
        
        if sort_by == 'emp_id':
            left = [emp for emp in employees if emp.emp_id < pivot.emp_id]
            middle = [emp for emp in employees if emp.emp_id == pivot.emp_id]
            right = [emp for emp in employees if emp.emp_id > pivot.emp_id]
        elif sort_by == 'last_name':
            left = [emp for emp in employees if emp.last_name.lower() < pivot.last_name.lower()]
            middle = [emp for emp in employees if emp.last_name.lower() == pivot.last_name.lower()]
            right = [emp for emp in employees if emp.last_name.lower() > pivot.last_name.lower()]
        elif sort_by == 'salary':
            left = [emp for emp in employees if emp.salary < pivot.salary]
            middle = [emp for emp in employees if emp.salary == pivot.salary]
            right = [emp for emp in employees if emp.salary > pivot.salary]
        
        return self.quick_sort_employees(left, sort_by) + middle + self.quick_sort_employees(right, sort_by)
    
    def heap_sort_employees(self, employees, sort_by='emp_id'):
        """Heap sort implementation for comparison"""
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n:
                if sort_by == 'emp_id' and arr[left].emp_id > arr[largest].emp_id:
                    largest = left
                elif sort_by == 'last_name' and arr[left].last_name.lower() > arr[largest].last_name.lower():
                    largest = left
                elif sort_by == 'salary' and arr[left].salary > arr[largest].salary:
                    largest = left
            
            if right < n:
                if sort_by == 'emp_id' and arr[right].emp_id > arr[largest].emp_id:
                    largest = right
                elif sort_by == 'last_name' and arr[right].last_name.lower() > arr[largest].last_name.lower():
                    largest = right
                elif sort_by == 'salary' and arr[right].salary > arr[largest].salary:
                    largest = right
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)
        
        n = len(employees)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(employees, n, i)
        
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            employees[0], employees[i] = employees[i], employees[0]
            heapify(employees, i, 0)
        
        return employees
    
    def sort_individual_files(self, file_paths, sort_by='emp_id', algorithm='merge'):
        """Sort individual files using specified algorithm"""
        start_time = time.time()
        sorted_files = []
        
        self.update_progress(0, len(file_paths), f'Sorting files with {algorithm} sort...')
        
        for idx, file_path in enumerate(file_paths):
            employees = self.read_employees_from_file(file_path)
            
            # Choose sorting algorithm
            if algorithm == 'merge':
                if sort_by == 'emp_id':
                    employees.sort(key=lambda x: x.emp_id)
                elif sort_by == 'last_name':
                    employees.sort(key=lambda x: x.last_name.lower())
                elif sort_by == 'salary':
                    employees.sort(key=lambda x: x.salary)
                elif sort_by == 'hire_date':
                    employees.sort(key=lambda x: x.hire_date)
            elif algorithm == 'quick':
                employees = self.quick_sort_employees(employees, sort_by)
            elif algorithm == 'heap':
                employees = self.heap_sort_employees(employees, sort_by)
            
            # Write sorted employees back
            sorted_file_path = file_path.replace('.txt', '_sorted.txt')
            self.write_employees_to_file(employees, sorted_file_path)
            sorted_files.append(sorted_file_path)
            
            self.update_progress(idx + 1, len(file_paths), f'Sorted file {idx + 1}/{len(file_paths)}')
        
        time_taken = time.time() - start_time
        self.log_operation('sort_individual_files', time_taken, {
            'sort_by': sort_by, 
            'algorithm': algorithm,
            'num_files': len(file_paths)
        })
        
        return sorted_files
    
    def merge_files(self, sorted_files, output_file, sort_by='emp_id'):
        """Enhanced merge with progress tracking"""
        start_time = time.time()
        
        file_handles = []
        heap = []
        total_records = 0
        processed_records = 0
        
        try:
            # Count total records for progress tracking
            for file_path in sorted_files:
                with open(file_path, 'r') as f:
                    total_records += sum(1 for _ in f)
            
            self.update_progress(0, total_records, 'Merging sorted files...')
            
            # Open all files and create file iterators
            for i, file_path in enumerate(sorted_files):
                f = open(file_path, 'r')
                file_handles.append(f)
                
                line = f.readline().strip()
                if line:
                    parts = line.split(',')
                    employee = Employee(
                        emp_id=int(parts[0]),
                        first_name=parts[1],
                        last_name=parts[2],
                        department=parts[3],
                        salary=float(parts[4]),
                        hire_date=parts[5] if len(parts) > 5 else None,
                        position=parts[6] if len(parts) > 6 else None,
                        email=parts[7] if len(parts) > 7 else None
                    )
                    
                    # Push to heap with appropriate key
                    if sort_by == 'emp_id':
                        heapq.heappush(heap, (employee.emp_id, i, employee))
                    elif sort_by == 'last_name':
                        heapq.heappush(heap, (employee.last_name.lower(), i, employee))
                    elif sort_by == 'salary':
                        heapq.heappush(heap, (employee.salary, i, employee))
                    elif sort_by == 'hire_date':
                        heapq.heappush(heap, (employee.hire_date, i, employee))
            
            # Merge process with progress tracking
            with open(output_file, 'w') as output:
                while heap:
                    key, file_idx, employee = heapq.heappop(heap)
                    output.write(str(employee) + '\n')
                    processed_records += 1
                    
                    if processed_records % 100 == 0:  # Update progress every 100 records
                        self.update_progress(processed_records, total_records, 'Merging files...')
                    
                    # Read next line from the same file
                    line = file_handles[file_idx].readline().strip()
                    if line:
                        parts = line.split(',')
                        next_employee = Employee(
                            emp_id=int(parts[0]),
                            first_name=parts[1],
                            last_name=parts[2],
                            department=parts[3],
                            salary=float(parts[4]),
                            hire_date=parts[5] if len(parts) > 5 else None,
                            position=parts[6] if len(parts) > 6 else None,
                            email=parts[7] if len(parts) > 7 else None
                        )
                        
                        if sort_by == 'emp_id':
                            heapq.heappush(heap, (next_employee.emp_id, file_idx, next_employee))
                        elif sort_by == 'last_name':
                            heapq.heappush(heap, (next_employee.last_name.lower(), file_idx, next_employee))
                        elif sort_by == 'salary':
                            heapq.heappush(heap, (next_employee.salary, file_idx, next_employee))
                        elif sort_by == 'hire_date':
                            heapq.heappush(heap, (next_employee.hire_date, file_idx, next_employee))
        
        finally:
            for f in file_handles:
                f.close()
        
        time_taken = time.time() - start_time
        self.log_operation('merge_files', time_taken, {
            'sort_by': sort_by, 
            'num_files': len(sorted_files),
            'total_records': total_records
        })
        
        return time_taken
    
    def compare_sorting_algorithms(self, sort_by='emp_id'):
        """Compare different sorting algorithms"""
        algorithms = ['merge', 'quick', 'heap']
        results = {}
        
        for algorithm in algorithms:
            start_time = time.time()
            
            # Generate data
            file_paths = self.generate_advanced_employees(num_employees=4000, num_files=4)  # Smaller for comparison
            
            # Sort files
            sorted_files = self.sort_individual_files(file_paths, sort_by, algorithm)
            
            # Merge (only for external merge sort)
            if algorithm == 'merge':
                output_file = os.path.join(self.temp_dir, f'final_sorted_{algorithm}.txt')
                self.merge_files(sorted_files, output_file, sort_by)
            
            total_time = time.time() - start_time
            results[algorithm] = {
                'time': total_time,
                'algorithm': algorithm.title() + ' Sort'
            }
        
        return results
    
    def generate_analytics_chart(self, data, chart_type='performance'):
        """Generate analytics charts"""
        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == 'performance':
            algorithms = list(data.keys())
            times = [data[alg]['time'] for alg in algorithms]
            
            bars = ax.bar(algorithms, times, color=['#3498db', '#e74c3c', '#2ecc71'])
            ax.set_ylabel('Time (seconds)')
            ax.set_title('Algorithm Performance Comparison')
            
            # Add value labels on bars
            for bar, time in zip(bars, times):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{time:.3f}s', ha='center', va='bottom')
        
        elif chart_type == 'operations':
            operations = [op['operation'].replace('_', ' ').title() for op in data]
            times = [op['time_taken'] for op in data]
            
            ax.pie(times, labels=operations, autopct='%1.1f%%', startangle=90)
            ax.set_title('Time Distribution by Operation')
        
        # Convert plot to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def get_analytics_data(self):
        """Get comprehensive analytics data"""
        try:
            # Basic statistics
            total_employees = employees_collection.count_documents({})
            
            # Department distribution
            dept_pipeline = [
                {"$group": {"_id": "$department", "count": {"$sum": 1}, "avg_salary": {"$avg": "$salary"}}},
                {"$sort": {"count": -1}}
            ]
            dept_stats = list(employees_collection.aggregate(dept_pipeline))
            
            # Salary statistics
            salary_pipeline = [
                {"$group": {
                    "_id": None,
                    "avg_salary": {"$avg": "$salary"},
                    "min_salary": {"$min": "$salary"},
                    "max_salary": {"$max": "$salary"}
                }}
            ]
            salary_stats = list(employees_collection.aggregate(salary_pipeline))
            
            # Recent operations
            recent_ops = list(operations_collection.find({}).sort('timestamp', -1).limit(10))
            
            return {
                'total_employees': total_employees,
                'department_stats': dept_stats,
                'salary_stats': salary_stats[0] if salary_stats else {},
                'recent_operations': recent_ops
            }
        except Exception as e:
            return {'error': str(e)}
    
    def export_to_csv(self, output_file, limit=None):
        """Export sorted data to CSV"""
        csv_path = os.path.join(self.temp_dir, 'employees_export.csv')
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['emp_id', 'first_name', 'last_name', 'full_name', 'department', 
                         'position', 'salary', 'hire_date', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            count = 0
            with open(output_file, 'r') as f:
                for line in f:
                    if limit and count >= limit:
                        break
                    
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        employee_data = {
                            'emp_id': parts[0],
                            'first_name': parts[1],
                            'last_name': parts[2],
                            'full_name': f"{parts[1]} {parts[2]}",
                            'department': parts[3],
                            'salary': parts[4],
                            'hire_date': parts[5] if len(parts) > 5 else '',
                            'position': parts[6] if len(parts) > 6 else '',
                            'email': parts[7] if len(parts) > 7 else ''
                        }
                        writer.writerow(employee_data)
                        count += 1
        
        return csv_path
    
    def external_merge_sort(self, sort_by='emp_id', algorithm='merge'):
        """Enhanced external merge sort with analytics"""
        total_start_time = time.time()
        
        # Step 1: Generate data
        file_paths = self.generate_advanced_employees()
        
        # Step 2: Sort individual files
        sorted_files = self.sort_individual_files(file_paths, sort_by, algorithm)
        
        # Step 3: Merge all sorted files (only for merge sort)
        output_file = os.path.join(self.temp_dir, 'final_sorted.txt')
        if algorithm == 'merge':
            merge_time = self.merge_files(sorted_files, output_file, sort_by)
        else:
            # For other algorithms, just concatenate the sorted files
            with open(output_file, 'w') as outf:
                for sorted_file in sorted_files:
                    with open(sorted_file, 'r') as inf:
                        outf.write(inf.read())
        
        total_time = time.time() - total_start_time
        self.log_operation('external_merge_sort_complete', total_time, {
            'sort_by': sort_by,
            'algorithm': algorithm,
            'total_records': 16000
        })
        
        # Store analytics
        analytics_data = {
            'timestamp': datetime.now(),
            'sort_by': sort_by,
            'algorithm': algorithm,
            'total_time': total_time,
            'total_records': 16000,
            'operations_log': self.operations_log
        }
        analytics_collection.insert_one(analytics_data)
        
        self.update_progress(16000, 16000, 'Sorting completed!')
        
        return output_file, self.operations_log
    
    def get_sorted_results(self, output_file, limit=100, page=1):
        """Get paginated sorted results"""
        employees = []
        skip = (page - 1) * limit
        current = 0
        
        with open(output_file, 'r') as f:
            for line in f:
                if current < skip:
                    current += 1
                    continue
                if len(employees) >= limit:
                    break
                    
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    employee = {
                        'emp_id': int(parts[0]),
                        'first_name': parts[1],
                        'last_name': parts[2],
                        'full_name': f"{parts[1]} {parts[2]}",
                        'department': parts[3],
                        'salary': float(parts[4]),
                        'hire_date': parts[5] if len(parts) > 5 else '',
                        'position': parts[6] if len(parts) > 6 else '',
                        'email': parts[7] if len(parts) > 7 else ''
                    }
                    employees.append(employee)
                current += 1
        
        # Count total records
        total_records = 0
        with open(output_file, 'r') as f:
            total_records = sum(1 for _ in f)
        
        return employees, total_records
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

# Global sorter instance for progress tracking
current_sorter = None

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-data', methods=['POST'])
def generate_data():
    global current_sorter
    try:
        data = request.get_json() or {}
        num_employees = data.get('num_employees', 16000)
        num_files = data.get('num_files', 16)
        
        current_sorter = AdvancedExternalMergeSort()
        file_paths = current_sorter.generate_advanced_employees(num_employees, num_files)
        
        return jsonify({
            'success': True,
            'message': f'Generated {num_employees} employee records in {len(file_paths)} files',
            'file_count': len(file_paths),
            'records_per_file': num_employees // num_files
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sort', methods=['POST'])
def sort_employees():
    global current_sorter
    try:
        data = request.get_json()
        sort_by = data.get('sort_by', 'emp_id')
        algorithm = data.get('algorithm', 'merge')
        
        current_sorter = AdvancedExternalMergeSort()
        output_file, operations_log = current_sorter.external_merge_sort(sort_by, algorithm)
        
        # Get sample results
        results, total_records = current_sorter.get_sorted_results(output_file, limit=50)
        
        return jsonify({
            'success': True,
            'results': results,
            'operations_log': [
                {
                    'operation': op['operation'],
                    'time_taken': round(op['time_taken'], 4),
                    'details': op['details']
                } for op in operations_log
            ],
            'total_records': total_records,
            'algorithm_used': algorithm,
            'sort_criteria': sort_by
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/compare-algorithms', methods=['POST'])
def compare_algorithms():
    try:
        data = request.get_json()
        sort_by = data.get('sort_by', 'emp_id')
        
        sorter = AdvancedExternalMergeSort()
        results = sorter.compare_sorting_algorithms(sort_by)
        
        # Generate performance chart
        chart_data = sorter.generate_analytics_chart(results, 'performance')
        
        sorter.cleanup()
        
        return jsonify({
            'success': True,
            'comparison_results': results,
            'chart_data': chart_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    global current_sorter
    if current_sorter:
        return jsonify({
            'success': True,
            'progress': current_sorter.sorting_progress
        })
    return jsonify({
        'success': True,
        'progress': {'current': 0, 'total': 0, 'status': 'idle', 'percentage': 0}
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    try:
        sorter = AdvancedExternalMergeSort()
        analytics_data = sorter.get_analytics_data()
        
        return jsonify({
            'success': True,
            'analytics': analytics_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/employees/search', methods=['GET'])
def search_employees():
    try:
        query = request.args.get('q', '')
        department = request.args.get('department', '')
        min_salary = request.args.get('min_salary', type=float)
        max_salary = request.args.get('max_salary', type=float)
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        
        # Build MongoDB query
        mongo_query = {}
        
        if query:
            mongo_query['$or'] = [
                {'first_name': {'$regex': query, '$options': 'i'}},
                {'last_name': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}}
            ]
        
        if department:
            mongo_query['department'] = department
        
        if min_salary is not None or max_salary is not None:
            salary_query = {}
            if min_salary is not None:
                salary_query['$gte'] = min_salary
            if max_salary is not None:
                salary_query['$lte'] = max_salary
            mongo_query['salary'] = salary_query
        
        skip = (page - 1) * limit
        
        employees = list(employees_collection.find(mongo_query, {'_id': 0})
                        .skip(skip).limit(limit))
        total_count = employees_collection.count_documents(mongo_query)
        
        return jsonify({
            'success': True,
            'employees': employees,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        sort_by = request.args.get('sort_by', 'emp_id')
        sort_order = int(request.args.get('sort_order', 1))
        
        skip = (page - 1) * limit
        
        employees = list(employees_collection.find({}, {'_id': 0})
                        .sort(sort_by, sort_order).skip(skip).limit(limit))
        
        total_count = employees_collection.count_documents({})
        
        return jsonify({
            'success': True,
            'employees': employees,
            'total_count': total_count,
            'page': page,
            'total_pages': (total_count + limit - 1) // limit
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_data():
    global current_sorter
    try:
        if not current_sorter:
            return jsonify({'success': False, 'error': 'No sorting operation in progress'}), 400
        
        data = request.get_json()
        format_type = data.get('format', 'csv')
        limit = data.get('limit', 1000)
        
        # Assume we have a sorted output file
        output_file = os.path.join(current_sorter.temp_dir, 'final_sorted.txt')
        
        if format_type == 'csv':
            csv_path = current_sorter.export_to_csv(output_file, limit)
            return send_file(csv_path, as_attachment=True, download_name='employees_sorted.csv')
        
        return jsonify({'success': False, 'error': 'Unsupported format'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/operations', methods=['GET'])
def get_operations():
    try:
        limit = int(request.args.get('limit', 20))
        operations = list(operations_collection.find({}, {'_id': 0})
                         .sort('timestamp', -1).limit(limit))
        
        return jsonify({
            'success': True,
            'operations': operations
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clear-data', methods=['DELETE'])
def clear_data():
    global current_sorter
    try:
        employees_collection.delete_many({})
        operations_collection.delete_many({})
        analytics_collection.delete_many({})
        
        if current_sorter:
            current_sorter.cleanup()
            current_sorter = None
        
        return jsonify({
            'success': True,
            'message': 'All data cleared successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)