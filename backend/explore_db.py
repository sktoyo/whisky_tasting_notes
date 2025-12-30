"""
대화형 SQLite 데이터베이스 탐색 도구
Run: python backend/explore_db.py
"""
import sqlite3
import os
import sys
from tabulate import tabulate
from typing import List, Tuple, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'app', 'tasting_notes.db')


class DatabaseExplorer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """데이터베이스 연결"""
        if not os.path.exists(self.db_path):
            print(f"❌ 데이터베이스 파일이 없습니다: {self.db_path}")
            return False
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # 딕셔너리처럼 접근 가능
            print(f"✅ 데이터베이스 연결됨: {self.db_path}\n")
            return True
        except Exception as e:
            print(f"❌ 연결 실패: {e}")
            return False
    
    def close(self):
        """연결 종료"""
        if self.conn:
            self.conn.close()
    
    def get_tables(self) -> List[str]:
        """모든 테이블 목록 반환"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in cursor.fetchall()]
    
    def get_table_schema(self, table_name: str) -> Optional[str]:
        """테이블 스키마 반환"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_table_info(self, table_name: str) -> List[Tuple]:
        """테이블 컬럼 정보 반환"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return cursor.fetchall()
    
    def get_row_count(self, table_name: str) -> int:
        """테이블 행 개수 반환"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    
    def query(self, sql: str, params: tuple = ()) -> Tuple[List[str], List[Tuple]]:
        """SQL 쿼리 실행"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
            # cursor.description이 None일 수 있음 (SELECT가 아닌 쿼리 또는 결과 없음)
            if cursor.description is None:
                return [], []
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        except Exception as e:
            print(f"❌ 쿼리 실행 오류: {e}")
            import traceback
            traceback.print_exc()
            return [], []
    
    def show_tables(self):
        """모든 테이블 목록 및 통계 표시"""
        tables = self.get_tables()
        if not tables:
            print("테이블이 없습니다.")
            return
        
        print("=" * 80)
        print("📊 데이터베이스 테이블 목록")
        print("=" * 80)
        
        table_data = []
        for table in tables:
            count = self.get_row_count(table)
            table_data.append([table, count])
        
        print(tabulate(table_data, headers=["테이블명", "행 개수"], tablefmt="grid"))
        print()
    
    def show_table_details(self, table_name: str, limit: int = 10):
        """테이블 상세 정보 및 샘플 데이터 표시"""
        if table_name not in self.get_tables():
            print(f"❌ 테이블 '{table_name}'이 존재하지 않습니다.")
            return
        
        print("=" * 80)
        print(f"📋 테이블: {table_name}")
        print("=" * 80)
        
        # 스키마
        schema = self.get_table_schema(table_name)
        if schema:
            print("\n[스키마]")
            print(schema)
        
        # 컬럼 정보
        print("\n[컬럼 정보]")
        info = self.get_table_info(table_name)
        column_data = [[col[1], col[2], "NOT NULL" if col[3] else "NULL", col[4] if col[4] else ""] 
                      for col in info]
        print(tabulate(column_data, headers=["컬럼명", "타입", "NULL", "기본값"], tablefmt="grid"))
        
        # 행 개수
        count = self.get_row_count(table_name)
        print(f"\n[행 개수]: {count}")
        
        # 샘플 데이터
        if count > 0:
            print(f"\n[샘플 데이터 (최대 {limit}개)]")
            columns, rows = self.query(f"SELECT * FROM {table_name} LIMIT {limit}")
            if columns and rows:
                # Row 객체를 튜플로 변환
                row_data = [tuple(row) for row in rows]
                print(tabulate(row_data, headers=columns, tablefmt="grid", maxcolwidths=[30]*len(columns)))
                if count > limit:
                    print(f"\n... 총 {count}개 중 {limit}개만 표시됨")
        print()
    
    def search_keyword(self, keyword: str, scope: Optional[str] = None):
        """키워드 검색"""
        print("=" * 80)
        print(f"🔍 키워드 검색: '{keyword}'")
        if scope:
            print(f"   Scope: {scope}")
        print("=" * 80)
        
        # vocabulary_terms에서 검색
        if scope:
            sql = "SELECT * FROM vocabulary_terms WHERE term LIKE ? AND scope = ?"
            params = (f"%{keyword}%", scope)
        else:
            sql = "SELECT * FROM vocabulary_terms WHERE term LIKE ?"
            params = (f"%{keyword}%",)
        
        columns, rows = self.query(sql, params)
        if columns and rows:
            row_data = [tuple(row) for row in rows]
            print(tabulate(row_data, headers=columns, tablefmt="grid", maxcolwidths=[30]*len(columns)))
            print(f"\n총 {len(rows)}개 결과")
        else:
            print("검색 결과가 없습니다.")
        print()
    
    def show_hierarchy(self, scope: Optional[str] = None):
        """계층 구조 키워드 표시"""
        print("=" * 80)
        print("🌳 키워드 계층 구조")
        if scope:
            print(f"   Scope: {scope}")
        print("=" * 80)
        
        if scope:
            sql = """
                SELECT category, subcategory, term, level, icon_key 
                FROM vocabulary_terms 
                WHERE scope = ? 
                ORDER BY level, category, subcategory, term
            """
            params = (scope,)
        else:
            sql = """
                SELECT scope, category, subcategory, term, level, icon_key 
                FROM vocabulary_terms 
                ORDER BY scope, level, category, subcategory, term
            """
            params = ()
        
        columns, rows = self.query(sql, params)
        if columns and rows:
            row_data = [tuple(row) for row in rows]
            print(tabulate(row_data, headers=columns, tablefmt="grid", maxcolwidths=[15, 20, 20, 30, 5, 10]))
            print(f"\n총 {len(rows)}개 키워드")
        else:
            print("키워드가 없습니다.")
        print()
    
    def interactive_mode(self):
        """대화형 모드"""
        print("\n" + "=" * 80)
        print("🗄️  데이터베이스 탐색 모드")
        print("=" * 80)
        print("\n사용 가능한 명령어:")
        print("  tables          - 모든 테이블 목록 보기")
        print("  show <table>    - 테이블 상세 정보 보기")
        print("  search <keyword> - 키워드 검색")
        print("  hierarchy       - 계층 구조 키워드 보기")
        print("  sql <query>     - SQL 쿼리 실행")
        print("  help            - 도움말")
        print("  exit            - 종료")
        print()
        
        while True:
            try:
                command = input("db> ").strip()
                
                if not command:
                    continue
                
                if command == "exit" or command == "quit":
                    print("👋 종료합니다.")
                    break
                
                elif command == "help":
                    print("\n사용 가능한 명령어:")
                    print("  tables                    - 모든 테이블 목록")
                    print("  show <table>              - 테이블 상세 정보")
                    print("  search <keyword>           - 키워드 검색 (모든 scope)")
                    print("  search <keyword> <scope>   - 특정 scope에서 키워드 검색")
                    print("  hierarchy                 - 모든 scope의 계층 구조")
                    print("  hierarchy <scope>          - 특정 scope의 계층 구조")
                    print("  sql <query>               - SQL 쿼리 실행")
                    print("  exit                      - 종료")
                    print()
                
                elif command == "tables":
                    self.show_tables()
                
                elif command.startswith("show "):
                    table_name = command.split(" ", 1)[1].strip()
                    self.show_table_details(table_name)
                
                elif command.startswith("search "):
                    parts = command.split(" ", 2)
                    if len(parts) == 2:
                        keyword = parts[1]
                        self.search_keyword(keyword)
                    elif len(parts) == 3:
                        keyword, scope = parts[1], parts[2]
                        self.search_keyword(keyword, scope)
                    else:
                        print("❌ 사용법: search <keyword> [scope]")
                
                elif command.startswith("hierarchy"):
                    parts = command.split(" ", 1)
                    scope = parts[1] if len(parts) > 1 else None
                    self.show_hierarchy(scope)
                
                elif command.startswith("sql "):
                    query = command.split(" ", 1)[1].strip()
                    columns, rows = self.query(query)
                    if columns and rows:
                        row_data = [tuple(row) for row in rows]
                        print(tabulate(row_data, headers=columns, tablefmt="grid", maxcolwidths=[30]*len(columns)))
                        print(f"\n총 {len(rows)}개 결과")
                    elif columns:
                        print("✅ 쿼리 실행 완료 (결과 없음)")
                    print()
                
                else:
                    print(f"❌ 알 수 없는 명령어: {command}")
                    print("   'help'를 입력하여 도움말을 확인하세요.")
            
            except KeyboardInterrupt:
                print("\n\n👋 종료합니다.")
                break
            except Exception as e:
                print(f"❌ 오류 발생: {e}\n")


def main():
    """메인 함수"""
    explorer = DatabaseExplorer(DB_PATH)
    
    if not explorer.connect():
        return
    
    try:
        # 초기 정보 표시
        explorer.show_tables()
        
        # 대화형 모드 시작
        explorer.interactive_mode()
    
    finally:
        explorer.close()


if __name__ == "__main__":
    # Windows 인코딩 문제 해결
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    main()

