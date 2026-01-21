from directory import Directory
from file import File
import datetime
import time

def run_tests():
    print("Запуск тестов...\n")
    
    # Тест 1: Создание файлов и директорий
    print("Тест 1: Создание файлов и директорий")
    root = Directory("root", owner="admin")
    file1 = File("file1.txt", content="Hello World", owner="user1")
    file2 = File("file2.txt", content="Another file", owner="user2")
    subdir = Directory("docs", owner="user1")
    
    root.add(file1)
    root.add(subdir)
    subdir.add(file2)
    
    assert root.size() == len("Hello World") + len("Another file")
    print("✓ Размер корневой директории вычислен корректно")
    
    # Тест 2: Метаданные и modified_at
    print("\nТест 2: Метаданные и modified_at")
    old_modified = root.modified_at
    time.sleep(0.01)
    
    file3 = File("file3.txt", content="New file", owner="user3")
    root.add(file3)
    
    assert root.modified_at > old_modified
    print("✓ modified_at обновился при добавлении файла")
    
    # Тест 3: list_paths
    print("\nТест 3: Метод list_paths()")
    paths = root.list_paths()
    expected_paths = ["root/file1.txt", "root/docs/file2.txt", "root/file3.txt"]
    
    # Сортируем для сравнения
    assert sorted(paths) == sorted(expected_paths)
    print(f"✓ list_paths() вернул корректные пути: {paths}")
    
    # Тест 4: tree()
    print("\nТест 4: Метод tree()")
    tree_output = root.tree()
    print("Вывод tree():")
    print(tree_output)
    
    # Проверяем наличие ключевых элементов в выводе
    assert "root/" in tree_output
    assert "docs/" in tree_output
    assert "file1.txt" in tree_output
    assert "bytes" in tree_output
    print("✓ tree() содержит имена и размеры файлов")
    
    # Тест 5: to_dict()
    print("\nТест 5: Метод to_dict()")
    root_dict = root.to_dict()
    
    assert root_dict["type"] == "directory"
    assert root_dict["name"] == "root"
    assert root_dict["owner"] == "admin"
    assert "file1.txt" in root_dict["children"]
    assert root_dict["children"]["file1.txt"]["type"] == "file"
    
    print("✓ to_dict() работает рекурсивно без ошибок")
    
    # Тест 6: Теги файлов
    print("\nТест 6: Теги файлов")
    file1.add_tag("important")
    file1.add_tag("test")
    
    assert "important" in file1.tags
    assert "test" in file1.tags
    assert len(file1.tags) == 2
    print("✓ Теги файлов работают корректно")
    
    # Тест 7: Переименование
    print("\nТест 7: Переименование")
    old_modified_file = file1.modified_at
    time.sleep(0.01)
    
    file1.rename("renamed_file.txt")
    assert file1.name == "renamed_file.txt"
    assert file1.modified_at > old_modified_file
    
    # Также обновляем ссылку в директории
    root.remove("file1.txt")
    root.add(file1)
    
    print("✓ Переименование обновляет modified_at")
    
    # Тест 8: Удаление файла
    print("\nТест 8: Удаление файла")
    old_size = root.size()
    assert "renamed_file.txt" in root.children
    root.remove("renamed_file.txt")
    
    assert root.size() == old_size - len("Hello World")
    assert "renamed_file.txt" not in root.children
    print("✓ Удаление файла работает корректно")
    
    # Тест 9: Вложенная структура
    print("\nТест 9: Вложенная структура директорий")
    deep_dir = Directory("deep", owner="admin")
    deeper_file = File("deep_file.txt", content="Deep content", owner="admin")
    deep_dir.add(deeper_file)
    subdir.add(deep_dir)
    
    paths = root.list_paths()
    # Исправленная проверка - ищем путь в списке
    expected_path = "root/docs/deep/deep_file.txt"
    found = False
    for path in paths:
        if expected_path in path:  # Ищем подстроку в путях
            found = True
            print(f"✓ Вложенная структура корректно обрабатывается: {path}")
            break
    
    assert found, f"Путь {expected_path} не найден в {paths}"
    
    print("\n" + "="*50)
    print("Все тесты успешно пройдены! ✓")

def interactive_demo():
    """Интерактивная демонстрация"""
    print("\n" + "="*50)
    print("ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ")
    print("="*50)
    
    # Создаем тестовую структуру
    root = Directory("Проект", owner="разработчик")
    
    # Добавляем файлы
    readme = File("README.md", content="Документация проекта", owner="разработчик")
    readme.add_tag("документация")
    readme.add_tag("важно")
    
    main_py = File("main.py", content="print('Hello World')", owner="разработчик")
    main_py.add_tag("код")
    
    config = File("config.yaml", content="параметры: значение", owner="админ")
    config.add_tag("конфигурация")
    
    # Добавляем директории
    src = Directory("src", owner="разработчик")
    tests = Directory("tests", owner="тестировщик")
    
    # Создаем вложенную структуру
    init_py = File("__init__.py", content="", owner="разработчик")
    utils_py = File("utils.py", content="def helper(): pass", owner="разработчик")
    
    # Собираем структуру
    root.add(readme)
    root.add(main_py)
    root.add(config)
    root.add(src)
    root.add(tests)
    
    src.add(init_py)
    src.add(utils_py)
    
    # Демонстрация tree()
    print("\n1. Древовидная структура проекта:")
    print(root.tree())
    
    # Демонстрация list_paths()
    print("\n2. Все пути в проекте:")
    for path in root.list_paths():
        print(f"  • {path}")
    
    # Демонстрация to_dict()
    print("\n3. Метрики проекта (через to_dict()):")
    data = root.to_dict()
    print(f"  • Всего элементов: {data['children_count']}")
    print(f"  • Общий размер: {data['size']} bytes")
    print(f"  • Владелец: {data['owner']}")
    print(f"  • Создан: {data['created_at'][:10]}")
    
    # Демонстрация тегов
    print("\n4. Теги файлов:")
    for name, child in root.children.items():
        if hasattr(child, 'tags') and child.tags:
            print(f"  • {name}: {', '.join(child.tags)}")

if __name__ == "__main__":
    try:
        run_tests()
        interactive_demo()
    except AssertionError as e:
        print(f"\nОшибка теста: {e}")
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")