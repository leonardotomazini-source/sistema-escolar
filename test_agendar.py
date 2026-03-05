#!/usr/bin/env python3
"""
Script para testar especificamente a rota de agendamento
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from flask import url_for

def test_agendar_route():
    """Testa a rota de agendamento"""
    try:
        with app.test_client() as client:
            print("🔄 Testando rota GET /agendar...")
            response = client.get('/agendar')
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                print("✅ Rota funciona")
                content = response.get_data(as_text=True)

                # Verificar se tem options nos selects
                professor_options = content.count('<option value="')
                print(f"Total de options encontradas: {professor_options}")

                # Verificar conteúdo específico
                if 'Professor Exemplo' in content:
                    print("✅ Professor Exemplo encontrado")
                else:
                    print("❌ Professor Exemplo NÃO encontrado")

                if 'Disciplina Exemplo' in content:
                    print("✅ Disciplina Exemplo encontrada")
                else:
                    print("❌ Disciplina Exemplo NÃO encontrada")

                if '101 EF' in content:
                    print("✅ Turma 101 EF encontrada")
                else:
                    print("❌ Turma 101 EF NÃO encontrada")

                # Mostrar um trecho onde deveria estar as turmas
                lines = content.split('\n')
                found_turma_select = False
                for i, line in enumerate(lines):
                    if 'name="turma"' in line:
                        found_turma_select = True
                        print(f"✅ Select de turma encontrado na linha {i}")
                        # Mostrar as próximas linhas
                        for j in range(max(0, i-2), min(len(lines), i+10)):
                            marker = ">>>" if j == i else "   "
                            print(f"{marker} {j}: {lines[j].strip()}")
                        break

                if not found_turma_select:
                    print("❌ Select de turma NÃO encontrado")

            else:
                print(f"❌ Erro na rota: {response.status_code}")
                print(f"Resposta: {response.get_data(as_text=True)}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agendar_route()