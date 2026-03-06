# 🚀 Deploy no Render com PostgreSQL

## ✅ O que foi configurado:
- ✅ Código compatível com PostgreSQL e SQLite
- ✅ `render.yaml` para deploy automático
- ✅ `requirements.txt` com psycopg2-binary
- ✅ `.gitignore` atualizado

## 📋 Próximos passos para deploy:

### 1. **Subir código para GitHub**
```bash
git add .
git commit -m "Configurado para PostgreSQL no Render"
git push origin main
```

### 2. **Criar conta no Render**
- Acesse: https://render.com
- Conecte sua conta GitHub

### 3. **Deploy no Render**
- Clique em "New +" → "Blueprint"
- Conecte seu repositório GitHub
- O `render.yaml` será detectado automaticamente
- Configure:
  - **Service Group Name:** sistema-escolar
  - **Branch:** main (ou sua branch)

### 4. **Aguardar deploy**
- O Render criará automaticamente:
  - Web Service (sua app Flask)
  - PostgreSQL database
- Você receberá uma URL tipo: `https://sistema-escolar-xxxx.onrender.com`

### 5. **Primeiro acesso**
- Acesse a URL
- Faça login com admin/Dotti2826
- O banco será criado automaticamente na primeira requisição

## 🔧 Configuração técnica:

### Variáveis de ambiente (automáticas):
- `DATABASE_URL`: String de conexão PostgreSQL (criada automaticamente)
- `PYTHON_VERSION`: 3.11

### Banco de dados:
- PostgreSQL gerenciado pelo Render
- Dados persistem entre deploys
- Backup automático incluído

## 🐛 Troubleshooting:

### Se der erro no deploy:
1. Verifique os logs no Render Dashboard
2. Certifique-se que `requirements.txt` tem `psycopg2-binary==2.9.10`
3. Verifique se `render.yaml` está na raiz do projeto

### Se o banco não for criado:
- Acesse qualquer página da app (isso dispara `init_db()`)
- Ou acesse diretamente `/login` para forçar inicialização

## 🎉 Resultado final:
- App rodando 24/7 gratuitamente
- Banco PostgreSQL persistente
- Deploy automático a cada push no GitHub
- SSL/HTTPS incluído