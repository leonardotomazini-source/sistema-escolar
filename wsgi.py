import os
from app import app, criar_banco

# Garantir que o banco é criado ao iniciar
try:
    criar_banco()
except Exception as e:
    print(f"Aviso ao criar banco: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
