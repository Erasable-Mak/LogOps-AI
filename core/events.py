import sqlite3
from datetime import datetime
from threading import Lock

class EventStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.lock = Lock()
        # Don't create connection here - create it per request
        
    def _get_conn(self):
        """Create a new connection for each request (thread-safe)"""
        return sqlite3.connect(self.db_path)
    
    def write(self, **kwargs):
        with self.lock:
            conn = self._get_conn()
            try:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS anomalies (
                        id INTEGER PRIMARY KEY,
                        ts TEXT,
                        service TEXT,
                        score REAL,
                        severity TEXT,
                        reason TEXT,
                        context_path TEXT,
                        start_offset INTEGER,
                        end_offset INTEGER
                    )
                """)
                
                cursor = conn.execute("""
                    INSERT INTO anomalies (ts, service, score, severity, reason, context_path, start_offset, end_offset)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (kwargs['ts'], kwargs['service'], kwargs['score'], kwargs['severity'], 
                      kwargs['reason'], kwargs['context_path'], kwargs['start_offset'], kwargs['end_offset']))
                result = cursor.lastrowid
                conn.commit()
                return result
            finally:
                conn.close()
    
    def get(self, anomaly_id: int):
        conn = self._get_conn()
        try:
            cursor = conn.execute("SELECT * FROM anomalies WHERE id = ?", [anomaly_id])
            row = cursor.fetchone()
            if row:
                return dict(zip([col[0] for col in cursor.description], row))
            return None
        finally:
            conn.close()
    
    def list(self, since: str = None, service: str = None):
        query = "SELECT * FROM anomalies WHERE 1=1"
        params = []
        if since:
            query += " AND ts >= ?"
            params.append(since)
        if service:
            query += " AND service = ?"
            params.append(service)
        query += " ORDER BY ts DESC"
        
        conn = self._get_conn()
        try:
            cursor = conn.execute(query, params)
            return [dict(zip([col[0] for col in cursor.description], row)) 
                    for row in cursor.fetchall()]
        finally:
            conn.close()
