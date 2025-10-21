import sqlite3
from model.testModel import Userinputs


class testDAO:
    def __init__(self, db_name="website.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Userinputs (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT)
                            ''')
        self.connection.commit()

    def add_Userinputs(self, Userinputs):
        self.cursor.execute(
            '''INSERT INTO Userinputs (text)
            VALUES (?)''',
            (Userinputs.text,)
        )
        self.connection.commit()

    def get_all_Userinputs(self):
        self.cursor.execute("SELECT * FROM Userinputs")
        rows = self.cursor.fetchall()
        return [Userinputs(row['ID'], row['text']) for row in rows]
    
    def get_Userinputs_by_id(self, ID):
        self.cursor.execute("SELECT* FROM Userinputs WHERE ID = ?", (ID,))
        row = self.cursor.fetchone()
        if row:
            return Userinputs(row[0], row[1])
        else:
            return None

    def update_Userinputs(self, Userinputs):
        self.cursor.execute('''
                            UPDATE Userinputs
                            SET text = ? WHERE ID = ?
                            ''', (Userinputs.text, Userinputs.ID))
        self.connection.commit()

    def delete_Userinputs(self, ID):
        self.cursor.execute("Delete FROM Userinputs WHERE ID = ?", (ID,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()