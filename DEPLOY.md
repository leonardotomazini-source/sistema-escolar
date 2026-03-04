# 🚀 Guia de Deploy - Sistema de Agendamento Escolar

Existem várias opções para colocar a aplicação online. Aqui estão as melhores:

---

## **Opção 1: RENDER (Recomendado) ✅**

A forma mais simples e gratuita. Perfeita para esse projeto.

### Passo a Passo:

1. **Criar conta no Render**
   - Acesse: https://render.com
   - Clique em "Sign Up"
   - Use GitHub ou email

2. **Conectar seu repositório GitHub**
   - Se o projeto está no GitHub, conecte
   - Se não está, siga as instruções para conectar

3. **Criar um novo Web Service**
   - Clique em "New +"
   - Selecione "Web Service"
   - Conecte seu repositório
   - Configure:
     - **Name:** sistema-escolar (ou seu nome)
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn wsgi:app`
     - **Instance Type:** Free (ou pago se quiser mais performance)

4. **Deploy**
   - Clique "Create Web Service"
   - O Render fará o deploy automaticamente
   - Você receberá um link tipo: `https://sistema-escolar-xxxx.onrender.com`

**Vantagens:**
- Grátis
- Deploy automático (conecta ao GitHub)
- SSL/HTTPS incluído
- Banco de dados SQLite funciona

---

## **Opção 2: RAILWAY**

Bem fácil e também gratuito com créditos.

### Passo a Passo:

1. **Criar conta no Railway**
   - Acesse: https://railway.app
   - Sign up com GitHub ou email

2. **Deploy rápido**
   - Clique "Start New Project"
   - Selecione "Deploy from GitHub Repo"
   - Autorize e selecione seu repositório

3. **Configurar**
   - Railway detecta automaticamente que é Python
   - Você receberá um e URL pública

**Vantagens:**
- Super fácil
- Free tier com $5/mês

---

## **Opção 3: REPLIT**

Grátis e muito rápido de configurar (menos profissional).

### Passo a Passo:

1. **Ir para https://replit.com**
2. **Clique "Upload folder"**
3. **Upload toda a pasta `sistema_escolar`**
4. **Crie um arquivo `.replit`** com:
   ```
   run = "python app.py"
   ```
5. **Clique "Run"**
6. Replit vai gerar uma URL pública

---

## **Opção 4: PYTHONANYWHERE**

Específico para Python, muito confiável.

### Passo a Passo:

1. **Acesse https://www.pythonanywhere.com**
2. **Crie conta gratuita**
3. **Upload os arquivos via Web**
4. **Configure Web App → Flask → Python 3.x**
5. **PythonAnywhere gera URL automática**

---

## **⚡ FORMA MAIS RÁPIDA (Recomendado):**

Se você quer fazer em 5 minutos:

### 1️⃣ **Crie um repositório GitHub**
```bash
cd c:\Users\Professor\sistema_escolar
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU_USUARIO/sistema_escolar.git
git branch -M main
git push -u origin main
```

### 2️⃣ **Vá para Render.com**
- Sign up com GitHub
- Clique "New +" → "Web Service"
- Conecte seu repositório GitHub
- Configure como descrito acima
- **Pronto! Seu site está online!**

---

## **Arquivos Necessários ✅**

Seu projeto já tem:
- ✅ `requirements.txt` - Dependências
- ✅ `wsgi.py` - Entry point para web servers
- ✅ `app.py` - Aplicação principal
- ✅ `database.db` - Banco de dados SQLite

---

## **URL de Acesso para Professores**

Após deploy, você compartilha algo como:
```
https://sistema-escolar-xxxx.onrender.com
```

Os professores abrem no navegador e podem:
- ✅ Agendar aulas
- ✅ Ver agenda semanal
- ✅ Sem necessidade de login

Admin pode entrar em:
```
https://sistema-escolar-xxxx.onrender.com/login
```

---

## **Troubleshooting**

### "ModuleNotFoundError"
- Certifique-se que `requirements.txt` está atualizado
- Rode: `pip install -r requirements.txt` localmente

### "Application failed to start"
- Verifique `wsgi.py`
- Certifique-se que `app.py` existe

### Banco de dados não persiste
- No Render/Railway, o SQLite funciona mas dados podem ser perdidos em redeploy
- Para produção real, considere usar PostgreSQL (add do Render/Railway)

---

## **Próximos Passos (opcional)**

Para melhor escalabilidade (+ usuários), considere:
1. Migrar para PostgreSQL (em vez de SQLite)
2. Adicionar autenticação de professores
3. Implementar backup automático

Mas por enquanto, a solução atual é perfeita! 🎉
