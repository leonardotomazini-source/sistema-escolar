# Sistema de Agendamento de Aulas

Um programa Python com Flask para reserva de horários de aulas, sem login/senha.

## Funcionalidades

✅ **Sem autenticação** - Apenas selecione o professor pré-cadastrado
✅ **Horários** - De segunda a sexta, dividido em:
   - 5 períodos matutinos (1ª à 5ª aula)
   - 5 períodos vespertinos (1ª à 5ª aula)

✅ **Agendamento com bloqueio** - Impossível agendar o mesmo horário 2 vezes
✅ **Cancelamento** - Desbloqueia automaticamente o horário
✅ **Campos obrigatórios:**
   1. Nome do professor
   2. Disciplina
   3. Data
   4. Turno (matutino/vespertino)
   5. Período (1-5)
   6. Conteúdo (habilidades e competências)

✅ **Relatório semanal** com:
   - Disciplinas mais usadas
   - Comparativo entre turnos
   - Professores mais agendados

✅ **Interface amigável** - Simples e clara com Bootstrap

## Instalação

1. Certifique-se que Python está instalado
2. Navegue até a pasta do projeto
3. Execute: `pip install flask`
4. Inicie: `python app.py`
5. Abra http://localhost:5000 no navegador

## Banco de Dados

- Usa SQLite (arquivo `database.db`)
- Armazena: Professores, Disciplinas, Agendamentos
- Criado automaticamente na primeira execução

## Como usar

### 1. Cadastrar Professores
- Menu "Professores" → Digite nome → Clique "Adicionar"

### 2. Cadastrar Disciplinas
- Menu "Disciplinas" → Digite nome → Clique "Adicionar"

### 3. Agendar Aula
- Menu "Agendar"
- Selecione professor, disciplina, data, turno e período
- Escreva conteúdo/habilidades
- Clique "Agendar"
- Se horário estiver ocupado, receberá aviso

### 4. Cancelar Aula
- Menu "Cancelar"
- Clique "Cancelar" ao lado da aula desejada
- Horário fica livre novamente

### 5. Relatório Semanal
- Menu "Relatório"
- Escolha a segunda-feira da semana
- Veja: agendamentos, disciplinas mais usadas, comparativo de turnos, professores tops
