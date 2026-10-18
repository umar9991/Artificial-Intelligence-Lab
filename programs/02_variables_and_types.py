"""Lab 1 - Program 2: Variables and data types."""

course = "Artificial Intelligence"
lab_number = 1
score = 92.5
is_completed = False

print("Course:", course, "| type:", type(course).__name__)
print("Lab number:", lab_number, "| type:", type(lab_number).__name__)
print("Score:", score, "| type:", type(score).__name__)
print("Completed:", is_completed, "| type:", type(is_completed).__name__)

marks_text = input("Enter your marks (0-100): ")
marks = float(marks_text)
print("Marks as float:", marks)
print("Marks as integer:", int(marks))
print("Passed:", marks >= 50)
