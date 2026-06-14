# Визначення класу Teacher
class Teacher:
    def __init__(self, first_name: str, last_name: str, age: int, email: str, can_teach_subjects: set):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        # Список предметів, які фактично призначені викладачу в розкладі
        self.assigned_subjects = set()

def create_schedule(subjects, teachers):
    uncovered = set(subjects)
    schedule = []
    available_teachers = list(teachers)

    while uncovered:
        best_teacher = None
        best_intersection = set()

        for teacher in available_teachers:
            # Знаходимо предмети, які викладач може закрити із тих, що ще не покриті
            intersection = teacher.can_teach_subjects & uncovered
            if not intersection:
                continue

            if best_teacher is None:
                best_teacher = teacher
                best_intersection = intersection
            else:
                # Критерій 1: Найбільша кількість непокритих предметів
                if len(intersection) > len(best_intersection):
                    best_teacher = teacher
                    best_intersection = intersection
                # Критерій 2: Якщо кількість однакова, обираємо наймолодшого
                elif len(intersection) == len(best_intersection):
                    if teacher.age < best_teacher.age:
                        best_teacher = teacher
                        best_intersection = intersection

        # Якщо пройшли всіх викладачів і ніхто не може покрити залишок предметів
        if best_teacher is None:
            return None

        # Призначаємо викладачу знайдені предмети
        best_teacher.assigned_subjects = best_intersection
        schedule.append(best_teacher)

        # Оновлюємо множину непокритих предметів та вилучаємо використаного викладача
        uncovered -= best_intersection
        available_teachers.remove(best_teacher)

    return schedule

if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    
    # Створення списку викладачів
    teachers = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'})
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")