import os
import csv
from collections import defaultdict
from tabulate import tabulate


class PriceAnalyzer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.data = []
        self.load_prices()

    def load_prices(self):
        """
        Сканирует папку и загружает данные из файлов прайс-листов.
        """
        for filename in os.listdir(self.folder_path):
            if "price" in filename:
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=',')
                    for row in reader:
                        # Определение колонок
                        name = self._get_column_value(row, ["название", "продукт", "товар", "наименование"])
                        price = self._get_column_value(row, ["цена", "розница"])
                        weight = self._get_column_value(row, ["фасовка", "масса", "вес"])

                        if name and price and weight:
                            try:
                                price = float(price)
                                weight = float(weight)
                                price_per_kg = price / weight
                                self.data.append({
                                    "name": name,
                                    "file_path": price,
                                    "weight": weight,
                                    "file": filename,
                                    "price_per_kg": price_per_kg
                                })
                            except ValueError:
                                continue  # Пропускаем строки с некорректными данными

    def _get_column_value(self, row, column_names):
        """
        Возвращает значение из строки по одному из возможных названий колонок.
        """
        for column in column_names:
            if column in row:
                return row[column]
        return None

    def find_text(self, search_text):
        """
        Возвращает список позиций, содержащих указанный текст в названии товара.
        """
        results = [item for item in self.data if search_text.lower() in item["name"].lower()]
        results.sort(key=lambda x: x["price_per_kg"])  # Сортировка по цене за кг
        return results

    def export_to_html(self, filename="output.html"):
        """
        Экспортирует все данные в HTML-файл.
        """
        headers = ["№", "Наименование", "цена", "вес", "файл", "цена за кг."]
        rows = []
        for idx, item in enumerate(self.data, start=1):
            rows.append([
                idx,
                item["name"],
                item["file_path"],
                item["weight"],
                item["file"],
                item["price_per_kg"]
            ])

        html_content = tabulate(rows, headers, tablefmt="html")
        with open(filename, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

    def run_console_interface(self):
        """
        Запускает консольный интерфейс для поиска товаров.
        """
        while True:
            search_text = input("Введите текст для поиска (или 'exit' для выхода): ").strip()
            if search_text.lower() == "exit":
                print("Работа программы завершена.")
                break

            results = self.find_text(search_text)
            if results:
                headers = ["№", "Наименование", "цена", "вес", "файл", "цена за кг."]
                rows = []
                for idx, item in enumerate(results, start=1):
                    rows.append([
                        idx,
                        item["name"],
                        item["file_path"],
                        item["weight"],
                        item["file"],
                        item["price_per_kg"]
                    ])
                print(tabulate(rows, headers, tablefmt="grid"))
            else:
                print("По вашему запросу ничего не найдено.")


if __name__ == "__main__":
    analyzer = PriceAnalyzer(".")  # Укажите путь к папке с файлами
    analyzer.run_console_interface()
    analyzer.export_to_html()