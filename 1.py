import os
import shutil
import zipfile

# список дозволених розширень для кожної категорії
images_extensions = ('JPEG', 'PNG', 'JPG', 'SVG')
videos_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
documents_extensions = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
audio_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
archives_extensions = ('ZIP', 'GZ', 'TAR')

# створення папок для кожної категорії
folders = {
    'images': 'Images',
    'videos': 'Videos',
    'documents': 'Documents',
    'audio': 'Audio',
    'archives': 'Archives',
    'unknown': 'Unknown'
}
for folder in folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)


def normalize(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    translit = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia',
    }
    name = ''.join(c if c in valid_chars else '_' for c in name)
    name = ''.join(translit.get(c.lower(), c) for c in name)
    return name

# Функція, яка обробляє папки
def process_folder(path):
    # Створюємо словник для зберігання списку файлів за категоріями
    files_by_category = {
        'images': [],
        'videos': [],
        'documents': [],
        'music': [],
        'archives': [],
        'unknown': []
    }

    # Створюємо список для зберігання розширень файлів
    extensions = set()

    # Проходимо по всіх файлах і папках у даній директорії
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        # Якщо це папка, викликаємо функцію обробки цієї папки рекурсивно
        if os.path.isdir(filepath):
            process_folder(filepath)
        # Якщо це файл, додаємо його до відповідної категорії
        elif os.path.isfile(filepath):
            # Отримуємо розширення файлу
            extension = os.path.splitext(filename)[1][1:].upper()
            # Додаємо розширення до списку розширень
            extensions.add(extension)
            # Додаємо файл до відповідної категорії
            if extension in IMAGE_EXTENSIONS:
                files_by_category['images'].append(filename)
            elif extension in VIDEO_EXTENSIONS:
                files_by_category['videos'].append(filename)
            elif extension in DOCUMENT_EXTENSIONS:
                files_by_category['documents'].append(filename)
            elif extension in MUSIC_EXTENSIONS:
                files_by_category['music'].append(filename)
            elif extension in ARCHIVE_EXTENSIONS:
                files_by_category['archives'].append(filename)
            else:
                files_by_category['unknown'].append(filename)

    # Виводимо результати
    print(f"Files in {path}:")
    print(f"Images: {files_by_category['images']}")
    print(f"Videos: {files_by_category['videos']}")
    print(f"Documents: {files_by_category['documents']}")
    print(f"Music: {files_by_category['music']}")
    print(f"Archives: {files_by_category['archives']}")
    print(f"Unknown: {files_by_category['unknown']}")
    print(f"Extensions in {path}: {', '.join(sorted(extensions))}")
