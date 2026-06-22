# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.9: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Helpfulness >= 0.9
- Correctness >= 0.9
- F1-Score >= 0.9
- Clarity >= 0.9
- Precision >= 0.9

MÉDIA das 5 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
│
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

    - persona-definition : Definir claramente a persona (ex: "Você é um Senior Product Owner com 10+ anos de experiência em times ágeis B2B e B2C.")
    - chain-of-thought-guardrails: Instruir o modelo a "pensar passo a passo" e fornecer raciocínio detalhado antes da resposta final.
    - structured-output-template: Fornecer um template claro para a resposta, como "User Story: [formato específico]" ou "Resposta em Markdown com seções claras".
    - few-shot-examples: Fornecer exemplos claros de entrada/saída no prompt para guiar o modelo.
    - self-checklist: Instruir o modelo a revisar sua resposta antes de finalizar, usando uma checklist de critérios (ex: "Revise sua resposta e verifique se atende aos seguintes critérios: [lista de critérios]").

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

  ### Como Executar

  Esta seção descreve o fluxo completo para instalar dependências, configurar variáveis de ambiente, publicar prompt otimizado no LangSmith e rodar validações locais.

  **Pré-requisitos**

  - Python 3.9 ou superior instalado
  - `pip` disponível no terminal
  - Conta no LangSmith
  - Chave de API do LangSmith configurada no arquivo `.env`
  - Chave de API de um provider de LLM para avaliação (`OPENAI_API_KEY` ou `GOOGLE_API_KEY`)

  **Dependências do projeto**

  Instale as dependências definidas em `requirements.txt`:

  - `langchain`
  - `langchain-core`
  - `langchain-community`
  - `langsmith`
  - `langchain-openai`
  - `langchain-google-genai`
  - `python-dotenv`
  - `pyyaml`
  - `pydantic`
  - `pytest`

  **1. Criar e ativar ambiente virtual**

  No Windows:

  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

  No Linux/macOS:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

  **2. Instalar dependências**

  ```bash
  pip install -r requirements.txt
  ```

  **3. Configurar variáveis de ambiente**

  Crie arquivo `.env` na raiz do projeto com credenciais necessárias. Exemplo mínimo:

  ```env
  LANGSMITH_API_KEY=sua_chave_langsmith
  USERNAME_LANGSMITH_HUB=seu_usuario
  LANGSMITH_PROJECT=nome_do_projeto
  LLM_PROVIDER=openai
  OPENAI_API_KEY=sua_chave_openai
  ```

  Se preferir Gemini, ajuste provider e chave correspondente:

  ```env
  LLM_PROVIDER=google
  GOOGLE_API_KEY=sua_chave_google
  ```

  **4. Fazer pull do prompt base**

  Esse comando baixa prompt inicial do LangSmith Hub e salva versão local em `prompts/bug_to_user_story_v1.yml`.

  ```bash
  python src/pull_prompts.py
  ```

  **5. Editar prompt otimizado**

  Atualize arquivo `prompts/bug_to_user_story_v2.yml` com técnicas de otimização exigidas no desafio, incluindo Few-shot Learning e pelo menos mais uma técnica complementar.

  **6. Fazer push do prompt otimizado**

  Esse comando lê `prompts/bug_to_user_story_v2.yml`, valida estrutura básica e publica prompt no LangSmith Hub como público.

  ```bash
  python src/push_prompts.py
  ```

  **7. Executar avaliação automática**

  Esse comando usa dataset `datasets/bug_to_user_story.jsonl`, busca prompt publicado no LangSmith Hub e calcula métricas de avaliação.

  ```bash
  python src/evaluate.py
  ```

  **8. Executar testes de validação do prompt**

  Esse comando roda testes automatizados que verificam presença de `system_prompt`, persona, formato de saída, exemplos few-shot, ausência de `TODO` e quantidade mínima de técnicas.

  ```bash
  pytest tests/test_prompts.py
  ```

  **Sequência recomendada de execução**

  ```bash
  python src/pull_prompts.py
  python src/push_prompts.py
  python src/evaluate.py
  pytest tests/test_prompts.py
  ```

  **Fluxo de iteração**

  Se alguma métrica ficar abaixo de `0.9`, ajuste `prompts/bug_to_user_story_v2.yml`, publique novamente e reavalie:

  ```bash
  python src/push_prompts.py
  python src/evaluate.py
  pytest tests/test_prompts.py
  ```

3. **Evidências no LangSmith**:
  - Screenshot do dashboard: [images/dash.png](images/dash.png)
  - Avalições retornadas:
  ``` bash
  Prompt: {seu_username}/bug_to_user_story_v2

  Como um vendedor em campo, eu quero que o app de produtividade sincronize corretamente minhas tarefas offline, para que eu não perca dados importantes e possa gerenciar meus compromissos de forma eficaz.

=== CRITÉRIOS DE ACEITAÇÃO ===
A. Conflito de Dados
- Dado que o Usuário A edita a tarefa #123 para "Ligar para cliente X às 14h" enquanto está offline
- E o Usuário B edita a mesma tarefa para "Ligar para cliente X às 15h (reagendado)" enquanto também está offline
- Quando ambos sincronizam
- Então o sistema deve preservar as edições de ambos os usuários
- E o Usuário A deve ser notificado se seu agendamento foi sobrescrito

B. Sincronização de Anexos
- Dado que o usuário anexa um PDF de 50MB em uma tarefa
- Quando inicia o upload via 4G e a conexão cai
- Então o app deve retomar o upload do ponto onde parou
- E o usuário deve ser notificado se o upload falhar após 5 tentativas

C. Ordenação de Operações
- Dado que o usuário cria uma tarefa "Tarefa A" às 10:00, edita para "Tarefa A - Urgente" às 10:15 e deleta às 10:30 enquanto está offline
- Quando o usuário sincroniza
- Então o servidor deve aplicar as operações na ordem correta
- E a tarefa deve ser deletada conforme esperado, sem gerar erro 404

D. Gerenciamento de Memória
- Dado que o usuário acumula 1.500 operações pendentes após 1 semana offline
- Quando o usuário volta para uma área com WiFi e tenta sincronizar
- Então o app não deve crashar devido a limite de memória
- E deve gerenciar a sincronização de forma eficiente sem exceder 700MB de memória no iOS

=== CONTEXTO DO BUG ===
- Severidade: Crítica
- Impacto: 250+ usuários afetados, perda de R$ 200k em oportunidades

=== TASKS TÉCNICAS SUGERIDAS ===
- Revisar lógica de merge de dados para evitar perda de informações
- Implementar lógica de retomar uploads de anexos
- Garantir que as operações sejam aplicadas na ordem correta no servidor
- Otimizar o gerenciamento de memória durante a sincronização de múltiplos itens pendentes
  ```
---
Impacto apos otimização:

```bash
 [1/15] F1:0.75 Clarity:0.85 Precision:0.90
      [2/15] F1:0.75 Clarity:0.90 Precision:0.90
      [3/15] F1:0.85 Clarity:0.90 Precision:0.90
      [4/15] F1:0.69 Clarity:0.85 Precision:0.67
      [5/15] F1:0.58 Clarity:0.90 Precision:0.67
      [6/15] F1:0.75 Clarity:0.85 Precision:0.80
      [7/15] F1:1.00 Clarity:1.00 Precision:1.00
      [8/15] F1:0.75 Clarity:0.90 Precision:0.90
      [9/15] F1:0.55 Clarity:0.80 Precision:0.67
      [10/15] F1:0.75 Clarity:0.80 Precision:0.67
      [11/15] F1:1.00 Clarity:1.00 Precision:1.00
      [12/15] F1:1.00 Clarity:1.00 Precision:1.00
      [13/15] F1:0.90 Clarity:0.95 Precision:1.00
      [14/15] F1:1.00 Clarity:1.00 Precision:1.00
      [15/15] F1:1.00 Clarity:0.90 Precision:0.67

==================================================
Prompt: luiz-guilherme-jesus/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.88 ✗
  - Correctness: 0.83 ✗

Métricas Base:
  - F1-Score: 0.82 ✗
  - Clarity: 0.91 ✓
  - Precision: 0.85 ✗

--------------------------------------------------
📊 MÉDIA GERAL: 0.8579
```

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final
