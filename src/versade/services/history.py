"""
Versade History Service - Query and response history management.
"""

import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

from rich.console import Console

console = Console()


@dataclass
class HistoryEntry:
    """Represents a history entry with query and response."""
    id: int
    query: str
    query_type: str
    timestamp: datetime
    response: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class HistoryService:
    """Service for managing query/response history with caching."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize history service with database path."""
        if db_path is None:
            config_dir = Path.home() / ".versade"
            config_dir.mkdir(exist_ok=True)
            db_path = config_dir / "history.db"
        
        self.db_path = db_path
        self._init_database()
        self._cache_size = 100  # LRU cache size
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    query_type TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT  -- JSON string
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    response TEXT,
                    success BOOLEAN DEFAULT TRUE,
                    error_message TEXT,
                    metadata TEXT,  -- JSON string
                    FOREIGN KEY (query_id) REFERENCES queries (id)
                )
            """)
            
            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_queries_timestamp ON queries(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_queries_type ON queries(query_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_responses_query_id ON responses(query_id)")
            
            conn.commit()
    
    def save_query(
        self,
        query: str,
        query_type: str,
        response: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Save a query and its response to history."""
        with sqlite3.connect(self.db_path) as conn:
            # Insert query
            cursor = conn.execute(
                "INSERT INTO queries (query, query_type, metadata) VALUES (?, ?, ?)",
                (query, query_type, json.dumps(metadata) if metadata else None)
            )
            query_id = cursor.lastrowid
            
            # Insert response if provided
            if response is not None or error_message is not None:
                conn.execute(
                    "INSERT INTO responses (query_id, response, success, error_message, metadata) VALUES (?, ?, ?, ?, ?)",
                    (query_id, response, success, error_message, json.dumps(metadata) if metadata else None)
                )
            
            conn.commit()
            return query_id
    
    def get_history(
        self,
        limit: int = 50,
        offset: int = 0,
        query_type: Optional[str] = None,
        since: Optional[datetime] = None
    ) -> List[HistoryEntry]:
        """Get history entries with optional filtering."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = """
                SELECT 
                    q.id, q.query, q.query_type, q.timestamp, q.metadata as q_metadata,
                    r.response, r.success, r.error_message, r.metadata as r_metadata
                FROM queries q
                LEFT JOIN responses r ON q.id = r.query_id
                WHERE 1=1
            """
            params = []
            
            if query_type:
                query += " AND q.query_type = ?"
                params.append(query_type)
            
            if since:
                query += " AND q.timestamp >= ?"
                params.append(since.isoformat())
            
            query += " ORDER BY q.timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            entries = []
            for row in rows:
                metadata = {}
                if row['q_metadata']:
                    metadata.update(json.loads(row['q_metadata']))
                if row['r_metadata']:
                    metadata.update(json.loads(row['r_metadata']))
                
                entries.append(HistoryEntry(
                    id=row['id'],
                    query=row['query'],
                    query_type=row['query_type'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    response=row['response'],
                    success=bool(row['success']) if row['success'] is not None else True,
                    error_message=row['error_message'],
                    metadata=metadata if metadata else None
                ))
            
            return entries
    
    def search_history(
        self,
        search_term: str,
        limit: int = 50,
        query_type: Optional[str] = None
    ) -> List[HistoryEntry]:
        """Search history entries by query or response content."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = """
                SELECT 
                    q.id, q.query, q.query_type, q.timestamp, q.metadata as q_metadata,
                    r.response, r.success, r.error_message, r.metadata as r_metadata
                FROM queries q
                LEFT JOIN responses r ON q.id = r.query_id
                WHERE (q.query LIKE ? OR r.response LIKE ?)
            """
            params = [f"%{search_term}%", f"%{search_term}%"]
            
            if query_type:
                query += " AND q.query_type = ?"
                params.append(query_type)
            
            query += " ORDER BY q.timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            entries = []
            for row in rows:
                metadata = {}
                if row['q_metadata']:
                    metadata.update(json.loads(row['q_metadata']))
                if row['r_metadata']:
                    metadata.update(json.loads(row['r_metadata']))
                
                entries.append(HistoryEntry(
                    id=row['id'],
                    query=row['query'],
                    query_type=row['query_type'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    response=row['response'],
                    success=bool(row['success']) if row['success'] is not None else True,
                    error_message=row['error_message'],
                    metadata=metadata if metadata else None
                ))
            
            return entries
    
    def get_entry_by_id(self, entry_id: int) -> Optional[HistoryEntry]:
        """Get a specific history entry by ID."""
        entries = self.get_history(limit=1, offset=0)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            cursor = conn.execute("""
                SELECT 
                    q.id, q.query, q.query_type, q.timestamp, q.metadata as q_metadata,
                    r.response, r.success, r.error_message, r.metadata as r_metadata
                FROM queries q
                LEFT JOIN responses r ON q.id = r.query_id
                WHERE q.id = ?
            """, (entry_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            metadata = {}
            if row['q_metadata']:
                metadata.update(json.loads(row['q_metadata']))
            if row['r_metadata']:
                metadata.update(json.loads(row['r_metadata']))
            
            return HistoryEntry(
                id=row['id'],
                query=row['query'],
                query_type=row['query_type'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                response=row['response'],
                success=bool(row['success']) if row['success'] is not None else True,
                error_message=row['error_message'],
                metadata=metadata if metadata else None
            )
    
    def clear_history(self, older_than: Optional[datetime] = None) -> int:
        """Clear history entries, optionally only older than specified date."""
        with sqlite3.connect(self.db_path) as conn:
            if older_than:
                cursor = conn.execute(
                    "DELETE FROM responses WHERE query_id IN (SELECT id FROM queries WHERE timestamp < ?)",
                    (older_than.isoformat(),)
                )
                cursor = conn.execute(
                    "DELETE FROM queries WHERE timestamp < ?",
                    (older_than.isoformat(),)
                )
            else:
                cursor = conn.execute("DELETE FROM responses")
                cursor = conn.execute("DELETE FROM queries")
            
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get history statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM queries")
            total_queries = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT query_type, COUNT(*) FROM queries GROUP BY query_type")
            by_type = dict(cursor.fetchall())
            
            cursor = conn.execute("SELECT COUNT(*) FROM responses WHERE success = 1")
            successful_responses = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT MIN(timestamp), MAX(timestamp) FROM queries")
            date_range = cursor.fetchone()
            
            return {
                "total_queries": total_queries,
                "by_type": by_type,
                "successful_responses": successful_responses,
                "date_range": date_range,
                "database_size": self.db_path.stat().st_size if self.db_path.exists() else 0
            }
    
    @lru_cache(maxsize=100)
    def _cached_search(self, search_term: str, query_type: Optional[str] = None) -> Tuple[HistoryEntry, ...]:
        """Cached search for better performance."""
        return tuple(self.search_history(search_term, query_type=query_type))


# Global history service instance
history_service = HistoryService() 