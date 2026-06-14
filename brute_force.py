from itertools import combinations

# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name: str, last_name: str, age: int, email: str, can_teach_subjects: set):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()

def create_schedule_brute_force(subjects, teachers):
    target_subjects = set(subjects)
    n = len(teachers)
    valid_combinations = []

    # Шукаємо комбінації, починаючи з розміру 1 до n
    for k in range(1, n + 1):
        for combo in combinations(teachers, k):
            # Об'єднуємо всі предмети, які може викладати ця група
            covered_by_combo = set()
            for teacher in combo:
                covered_by_combo.update(teacher.can_teach_subjects)
            
            # Якщо комбінація покриває всі необхідні предмети
            if target_subjects.issubset(covered_by_combo):
                valid_combinations.append(combo)
        
        # Якщо ми знайшли хоча б одну робочу комбінацію розміру k,
        # далі шукати (розміри k+1, k+2...) немає сенсу, бо ми шукаємо МІНІМУМ викладачів
        if valid_combinations:
            break

    if not valid_combinations:
        return None

    # Серед усіх знайдених оптимальних комбінацій обираємо ту, де сумарний вік найменший
    best_combo = min(valid_combinations, key=lambda combo: sum(t.age for t in combo))

    # Розподіляємо предмети між обраними викладачами
    uncovered = set(subjects)
   
    for t in teachers:
        t.assigned_subjects = set()

    # Розподіляємо предмети (пріоритет молодшим та більш завантаженим)
    for teacher in sorted(best_combo, key=lambda x: (len(x.can_teach_subjects & uncovered), -x.age), reverse=True):
        intersection = teacher.can_teach_subjects & uncovered
        teacher.assigned_subjects = intersection
        uncovered -= intersection

    return list(best_combo)

if __name__ == '__main__':
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    
    teachers = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'})
    ]

    schedule = create_schedule_brute_force(subjects, teachers)

    if schedule:
        print("Розклад занять (Метод повного перебору):")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")