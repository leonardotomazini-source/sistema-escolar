#!/usr/bin/env python3
"""
Script de debug específico para testar turmas no Render
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import conectar, criar_banco

def test_turmas():
    """Testa especificamente se as turmas estão funcionando"""
    try:
        print("🔄 Testando criação do banco...")
        criar_banco()
        print("✅ Banco criado")

        print("🔄 Testando conexão...")
        conn = conectar()
        cursor = conn.cursor()

        print("🔄 Verificando tabelas...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tabelas: {tables}")

        if 'turmas' not in tables:
            print("❌ Tabela 'turmas' não existe!")
            return

        print("🔄 Verificando turmas...")
        cursor.execute("SELECT COUNT(*) FROM turmas")
        count = cursor.fetchone()[0]
        print(f"Total de turmas: {count}")

        if count == 0:
            print("❌ Nenhuma turma encontrada!")
            return

        print("🔄 Listando primeiras 10 turmas...")
        cursor.execute("SELECT nome FROM turmas ORDER BY nome LIMIT 10")
        turmas = [row[0] for row in cursor.fetchall()]
        print(f"Turmas encontradas: {turmas}")

        print("🔄 Testando JOIN com agendamentos...")
        cursor.execute("""
            SELECT COUNT(*) FROM agendamentos a
            JOIN turmas t ON a.turma_id = t.id
        """)
        join_count = cursor.fetchone()[0]
        print(f"Agendamentos com turmas: {join_count}")

        conn.close()
        print("✅ Teste de turmas completo!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_turmas()