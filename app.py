from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave-super-secretar-escola"  # necessário para flash messages

# Credenciais admin
ADMIN_USER = "admin"
ADMIN_PASS = "Dotti2826"

def requer_admin(f):
    """Decorator para proteger rotas admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_logado" not in session:
            flash("Você precisa fazer login para acessar essa página", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def conectar():
    return sqlite3.connect("database.db")

# Criar banco se não existir
def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # tabela de professores pré‑cadastrados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    # tabela de disciplinas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    # agendamentos com turno, período e conteúdo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_id INTEGER NOT NULL,
        disciplina_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        turno TEXT NOT NULL,
        periodo INTEGER NOT NULL,
        conteudo TEXT NOT NULL,
        UNIQUE(data, turno, periodo)
    )
    """)

    # caso a tabela já exista em formato antigo, adicionamos colunas necessárias
    cursor.execute("PRAGMA table_info(agendamentos)")
    existing = [row[1] for row in cursor.fetchall()]
    if "disciplina_id" not in existing:
        cursor.execute("ALTER TABLE agendamentos ADD COLUMN disciplina_id INTEGER NOT NULL DEFAULT 0")
    if "turno" not in existing:
        cursor.execute("ALTER TABLE agendamentos ADD COLUMN turno TEXT NOT NULL DEFAULT 'matutino'")
    if "periodo" not in existing:
        cursor.execute("ALTER TABLE agendamentos ADD COLUMN periodo INTEGER NOT NULL DEFAULT 1")
    if "conteudo" not in existing:
        cursor.execute("ALTER TABLE agendamentos ADD COLUMN conteudo TEXT NOT NULL DEFAULT ''")

    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    """Página de login do admin"""
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        
        if usuario == ADMIN_USER and senha == ADMIN_PASS:
            session["admin_logado"] = True
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha incorretos", "danger")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Fazer logout"""
    session.pop("admin_logado", None)
    flash("Logout realizado", "success")
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        professor_id = request.form.get("professor")
        disciplina_id = request.form.get("disciplina")
        data = request.form.get("data")
        turno = request.form.get("turno")
        periodo = request.form.get("periodo")
        conteudo = request.form.get("conteudo", "").strip()

        if not all([professor_id, disciplina_id, data, turno, periodo, conteudo]):
            flash("Todos os campos são obrigatórios", "danger")
            return redirect(url_for("agendar"))

        try:
            cursor.execute(
                "INSERT INTO agendamentos (professor_id, disciplina_id, data, turno, periodo, conteudo) VALUES (?, ?, ?, ?, ?, ?)",
                (professor_id, disciplina_id, data, turno, periodo, conteudo)
            )
            conn.commit()
            flash("Agendamento realizado com sucesso!", "success")
            return redirect(url_for("agendar"))
        except sqlite3.IntegrityError:
            flash("Já existe um agendamento para esse dia/turno/período", "danger")
        except Exception as e:
            flash(f"Erro ao agendar: {e}", "danger")

    cursor.execute("SELECT id, nome FROM professores ORDER BY nome")
    professores = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM disciplinas ORDER BY nome")
    disciplinas = cursor.fetchall()
    conn.close()
    return render_template("agendar.html", professores=professores, disciplinas=disciplinas)

@app.route("/professores", methods=["GET", "POST"])
@requer_admin
def gerenciar_professores():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if nome:
            try:
                cursor.execute("INSERT INTO professores (nome) VALUES (?)", (nome,))
                conn.commit()
                flash("Professor cadastrado com sucesso", "success")
            except sqlite3.IntegrityError:
                flash("Professor já existe", "warning")
        return redirect(url_for("gerenciar_professores"))

    cursor.execute("SELECT id, nome FROM professores ORDER BY nome")
    professores = cursor.fetchall()
    conn.close()
    return render_template("professores.html", professores=professores)

@app.route("/disciplinas", methods=["GET", "POST"])
@requer_admin
def gerenciar_disciplinas():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if nome:
            try:
                cursor.execute("INSERT INTO disciplinas (nome) VALUES (?)", (nome,))
                conn.commit()
                flash("Disciplina cadastrada com sucesso", "success")
            except sqlite3.IntegrityError:
                flash("Disciplina já existe", "warning")
        return redirect(url_for("gerenciar_disciplinas"))

    cursor.execute("SELECT id, nome FROM disciplinas ORDER BY nome")
    disciplinas = cursor.fetchall()
    conn.close()
    return render_template("disciplinas.html", disciplinas=disciplinas)

@app.route("/cancelar", methods=["GET", "POST"])
@requer_admin
def cancelar():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        agendamento_id = request.form.get("id")
        if agendamento_id:
            cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
            conn.commit()
            flash("Agendamento cancelado", "success")
        return redirect(url_for("cancelar"))

    cursor.execute(
        """
        SELECT a.id, p.nome, d.nome, a.data, a.turno, a.periodo
        FROM agendamentos a
        JOIN professores p ON a.professor_id = p.id
        JOIN disciplinas d ON a.disciplina_id = d.id
        ORDER BY a.data, a.turno, a.periodo
        """
    )
    agendamentos = cursor.fetchall()
    conn.close()
    return render_template("cancelar.html", agendamentos=agendamentos)

@app.route("/relatorio", methods=["GET", "POST"])
@requer_admin
def relatorio():
    conn = conectar()
    cursor = conn.cursor()

    # determina semana inicial (segunda-feira)
    if request.method == "POST":
        start = request.form.get("start_date")
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
        except:
            start_date = datetime.today().date()
    else:
        today = datetime.today().date()
        start_date = today - timedelta(days=today.weekday())

    end_date = start_date + timedelta(days=4)
    fmt_start = start_date.isoformat()
    fmt_end = end_date.isoformat()

    cursor.execute(
        """
        SELECT a.id, p.nome, d.nome, a.data, a.turno, a.periodo, a.conteudo
        FROM agendamentos a
        JOIN professores p ON a.professor_id = p.id
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE a.data BETWEEN ? AND ?
        ORDER BY a.data, a.turno, a.periodo
        """,
        (fmt_start, fmt_end)
    )
    entries = cursor.fetchall()

    # estatísticas
    cursor.execute(
        """
        SELECT d.nome, COUNT(*)
        FROM agendamentos a
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE a.data BETWEEN ? AND ?
        GROUP BY d.nome
        ORDER BY COUNT(*) DESC
        """,
        (fmt_start, fmt_end)
    )
    disc_stats = cursor.fetchall()

    cursor.execute(
        """
        SELECT turno, COUNT(*)
        FROM agendamentos
        WHERE data BETWEEN ? AND ?
        GROUP BY turno
        """,
        (fmt_start, fmt_end)
    )
    turno_stats = cursor.fetchall()

    cursor.execute(
        """
        SELECT p.nome, COUNT(*)
        FROM agendamentos a
        JOIN professores p ON a.professor_id = p.id
        WHERE a.data BETWEEN ? AND ?
        GROUP BY p.nome
        ORDER BY COUNT(*) DESC
        """,
        (fmt_start, fmt_end)
    )
    prof_stats = cursor.fetchall()

    conn.close()
    return render_template(
        "relatorio.html",
        entries=entries,
        disc_stats=disc_stats,
        turno_stats=turno_stats,
        prof_stats=prof_stats,
        start_date=start_date,
        end_date=end_date,
    )

@app.route("/agenda")
@requer_admin
def agenda():
    """Visualização administrativa - todas as aulas por semana"""
    conn = conectar()
    cursor = conn.cursor()
    today = datetime.today().date()
    
    # Calcula início e fim do mês
    primeiro_dia = today.replace(day=1)
    if today.month == 12:
        ultimo_dia = primeiro_dia.replace(year=primeiro_dia.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        ultimo_dia = primeiro_dia.replace(month=primeiro_dia.month + 1, day=1) - timedelta(days=1)
    
    fmt_start = primeiro_dia.isoformat()
    fmt_end = ultimo_dia.isoformat()
    
    # Busca agendamentos do mês
    cursor.execute(
        """
        SELECT a.data, a.turno, a.periodo, p.nome, d.nome, a.conteudo
        FROM agendamentos a
        JOIN professores p ON a.professor_id = p.id
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE a.data BETWEEN ? AND ?
        ORDER BY a.data, a.turno, a.periodo
        """,
        (fmt_start, fmt_end)
    )
    agendamentos = cursor.fetchall()
    conn.close()
    
    # Organiza por semana
    semanas = {}
    for data, turno, periodo, prof, disc, conteudo in agendamentos:
        date_obj = datetime.strptime(data, "%Y-%m-%d").date()
        weekday = date_obj.weekday()
        
        # Calcula segunda-feira da semana
        segunda = date_obj - timedelta(days=weekday)
        sexta = segunda + timedelta(days=4)
        chave = f"{segunda.isoformat()} a {sexta.isoformat()}"
        
        if chave not in semanas:
            semanas[chave] = {"segunda": segunda, "sexta": sexta, "aulas": []}
        
        # Determina cor: verde se hoje, azul se futuro
        if date_obj == today:
            cor = "success"  # verde
        elif date_obj > today:
            cor = "info"  # azul
        else:
            cor = None
        
        semanas[chave]["aulas"].append({
            "data": data,
            "turno": turno,
            "periodo": periodo,
            "prof": prof,
            "disc": disc,
            "conteudo": conteudo,
            "cor": cor
        })
    
    return render_template("agenda.html", semanas=semanas, hoje=today)

@app.route("/professores-agenda")
def professores_agenda():
    """Visualização para professores - apenas visualiza os agendamentos, sem edição"""
    conn = conectar()
    cursor = conn.cursor()
    today = datetime.today().date()
    
    # Calcula próximas 4 semanas
    primeiro_dia = today.replace(day=1)
    if today.month == 12:
        ultimo_dia = primeiro_dia.replace(year=primeiro_dia.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        ultimo_dia = primeiro_dia.replace(month=primeiro_dia.month + 1, day=1) - timedelta(days=1)
    
    fmt_start = primeiro_dia.isoformat()
    fmt_end = ultimo_dia.isoformat()
    
    # Busca agendamentos do mês
    cursor.execute(
        """
        SELECT a.data, a.turno, a.periodo, p.nome, d.nome, a.conteudo
        FROM agendamentos a
        JOIN professores p ON a.professor_id = p.id
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE a.data BETWEEN ? AND ?
        ORDER BY a.data, a.turno, a.periodo
        """,
        (fmt_start, fmt_end)
    )
    agendamentos = cursor.fetchall()
    conn.close()
    
    # Organiza por semana
    semanas = {}
    for data, turno, periodo, prof, disc, conteudo in agendamentos:
        date_obj = datetime.strptime(data, "%Y-%m-%d").date()
        weekday = date_obj.weekday()
        
        # Calcula segunda-feira da semana
        segunda = date_obj - timedelta(days=weekday)
        sexta = segunda + timedelta(days=4)
        chave = f"{segunda.isoformat()} a {sexta.isoformat()}"
        
        if chave not in semanas:
            semanas[chave] = {"segunda": segunda, "sexta": sexta, "aulas": []}
        
        # Determina cor: verde se hoje, azul se futuro
        if date_obj == today:
            cor = "success"  # verde
        elif date_obj > today:
            cor = "info"  # azul
        else:
            cor = None
        
        semanas[chave]["aulas"].append({
            "data": data,
            "turno": turno,
            "periodo": periodo,
            "prof": prof,
            "disc": disc,
            "conteudo": conteudo,
            "cor": cor
        })
    
    return render_template("professores_agenda.html", semanas=semanas, hoje=today)

if __name__ == "__main__":
    criar_banco()
    import os
    debug_mode = os.environ.get("DEBUG", "False") == "True"
    app.run(debug=debug_mode)