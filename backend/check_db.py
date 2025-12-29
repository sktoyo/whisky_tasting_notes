"""
Database schema checker and query tool
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app', 'tasting_notes.db')

def check_schema():
    """Check and display database schema"""
    if not os.path.exists(DB_PATH):
        print(f"[X] Database file does not exist: {DB_PATH}")
        return
    
    print(f"[OK] Database file found: {DB_PATH}\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("=" * 80)
    print("DATABASE TABLES")
    print("=" * 80)
    for (table_name,) in tables:
        print(f"\n[TABLE] {table_name}")
        print("-" * 80)
        
        # Get schema
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        schema = cursor.fetchone()[0]
        print(schema)
        print()
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   Rows: {count}")
    
    conn.close()

def query_vocabulary_terms():
    """Query vocabulary terms by scope"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database file does not exist: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("VOCABULARY TERMS BY SCOPE")
    print("=" * 80)
    
    for scope in ['nose', 'palate', 'finish']:
        cursor.execute("SELECT COUNT(*) FROM vocabulary_terms WHERE scope=?", (scope,))
        count = cursor.fetchone()[0]
        print(f"\n{scope.upper()}: {count} terms")
        
        cursor.execute("SELECT term, icon_key FROM vocabulary_terms WHERE scope=? LIMIT 10", (scope,))
        terms = cursor.fetchall()
        for term, icon in terms:
            print(f"  - {term} ({icon})")
        
        if count > 10:
            print(f"  ... and {count - 10} more")
    
    # Check for duplicate terms
    print("\n" + "=" * 80)
    print("CHECKING FOR ISSUES")
    print("=" * 80)
    
    cursor.execute("""
        SELECT term, COUNT(*) as cnt 
        FROM vocabulary_terms 
        GROUP BY term 
        HAVING cnt > 1
    """)
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"\n[WARNING] Found {len(duplicates)} terms with duplicates:")
        for term, cnt in duplicates[:10]:
            cursor.execute("SELECT scope FROM vocabulary_terms WHERE term=?", (term,))
            scopes = [s[0] for s in cursor.fetchall()]
            print(f"  - '{term}': {cnt} occurrences in {', '.join(scopes)}")
    else:
        print("\n[OK] No duplicate terms found (good!)")
    
    conn.close()

if __name__ == "__main__":
    check_schema()
    query_vocabulary_terms()

