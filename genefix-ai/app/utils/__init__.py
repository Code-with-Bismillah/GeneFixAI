import json
import pandas as pd

class DataBase:
    def __init__(self, json_path=None, excel_path=None):
        self.json_path = json_path
        self.excel_path = excel_path

    def load_json(self):
        if not self.json_path:
            raise ValueError("No JSON path provided.")
        with open(self.json_path, 'r') as f:
            return json.load(f)

    def save_json(self, data):
        if not self.json_path:
            raise ValueError("No JSON path provided.")
        with open(self.json_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_excel(self):
        if not self.excel_path:
            raise ValueError("No Excel path provided.")
        return pd.read_csv(self.excel_path)

    def save_excel(self, df):
        if not self.excel_path:
            raise ValueError("No Excel path provided.")
        df.to_csv(self.excel_path, index=False)
