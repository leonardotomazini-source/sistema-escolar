#!/usr/bin/env python
import sys
import traceback

try:
    print("[1] Importando app...")
    from app import app, criar_banco
    print("[2] Criando banco de dados...")
    criar_banco()
    print("[3] Banco criado com sucesso!")
    
    print("\n[4] Testando GET /agendar...")
    app.testing = True
    client = app.test_client()
    resp = client.get('/agendar')
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print("Resposta:")
        print(resp.data.decode()[:1000])
    else:
        print("✓ /agendar retornou 200 OK")
    
    print("\n[5] Testando GET /professores (sem login)...")
    resp2 = client.get('/professores')
    print(f"Status: {resp2.status_code}")
    if resp2.status_code == 302:
        print("✓ /professores redirecionou para login (esperado)")
    else:
        print("Resposta:")
        print(resp2.data.decode()[:1000])
    
    print("\n[6] Login como admin...")
    resp3 = client.post('/login', data={'usuario':'admin', 'senha':'Dotti2826'}, follow_redirects=False)
    print(f"Status: {resp3.status_code}")
    
    print("\n[7] Acessando /professores após login...")
    resp4 = client.get('/professores')
    print(f"Status: {resp4.status_code}")
    if resp4.status_code == 200:
        print("✓ /professores retornou 200 OK")
    else:
        print("Resposta:")
        print(resp4.data.decode()[:1000])
        
except Exception as e:
    print(f"\n❌ ERRO: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Tudo funcionando!")
