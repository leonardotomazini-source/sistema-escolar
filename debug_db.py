#!/usr/bin/env python3
"""
Script de debug para testar a inicialização do banco no Render
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import criar_banco, conectar

def test_db():
    """Testa se o banco pode ser criado e acessado"""
    try:
        print("Testando criação do banco...")
        criar_banco()
        print("✅ Banco criado com sucesso")

        print("Testando conexão...")
        conn = conectar()
        cursor = conn.cursor()

        print("Testando tabelas...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tabelas encontradas: {[t[0] for t in tables]}")

        print("Testando dados...")
        cursor.execute("SELECT COUNT(*) FROM professores")
        prof_count = cursor.fetchone()[0]
        print(f"Professores: {prof_count}")

        cursor.execute("SELECT COUNT(*) FROM disciplinas")
        disc_count = cursor.fetchone()[0]
        print(f"Disciplinas: {disc_count}")

        conn.close()
        print("✅ Teste completo - tudo funcionando!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db()