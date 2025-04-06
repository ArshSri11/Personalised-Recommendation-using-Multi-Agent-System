import sqlite3
import json

class UserItemDB:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_user_profile(self, user_id):
        """Retrieve the user profile from the info database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return {
                'user_id': user_data[0],
                'age': user_data[1],
                'gender': user_data[2],
                'occupation': user_data[3]
            }
        return None
    
    def get_item_attributes(self, item_id):
        """Retrieve item attributes from the info database."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Items WHERE item_id = ?', (item_id,))
        item_data = cursor.fetchone()
        conn.close()
        if item_data:
            return {
                'item_id': item_data[0],
                'title': item_data[1],
                'genres': list(map(str.strip, item_data[3].split('|'))),  # genres are stored as a pipe-separated string
            }
        return None
    
    def get_user_item_history(self, user_id):
        """Retrieve user item history from the info database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, history_item_id, history_rating FROM History WHERE user_id = ?', (user_id,))
        history_data = cursor.fetchone()
        conn.close()
        if history_data:
            return {
                'user_id': history_data[0],
                'history_item_ids': json.loads(history_data[1]),
                'history_ratings': json.loads(history_data[2])
            }
        return None