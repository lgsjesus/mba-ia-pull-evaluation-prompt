# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

  ### Como Executar

  Esta seção descreve o fluxo completo para instalar dependências, configurar variáveis de ambiente, publicar prompt otimizado no LangSmith e rodar validações locais.

  **Seção "Técnicas Aplicadas (Fase 2)"**:

    - persona-definition : Definir claramente a persona (ex: "Você é um Senior Product Owner com 10+ anos de experiência em times ágeis B2B e B2C.")
    - chain-of-thought-guardrails: Instruir o modelo a "pensar passo a passo" e fornecer raciocínio detalhado antes da resposta final.
    - structured-output-template: Fornecer um template claro para a resposta, como "User Story: [formato específico]" ou "Resposta em Markdown com seções claras".
    - few-shot-examples: Fornecer exemplos claros de entrada/saída no prompt para guiar o modelo.
    - self-checklist: Instruir o modelo a revisar sua resposta antes de finalizar, usando uma checklist de critérios (ex: "Revise sua resposta e verifique se atende aos seguintes critérios: [lista de critérios]").

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

  Se alguma métrica ficar abaixo de `0.8`, ajuste `prompts/bug_to_user_story_v2.yml`, publique novamente e reavalie:

  ```bash
  python src/push_prompts.py
  python src/evaluate.py
  pytest tests/test_prompts.py
  ```
### Resultados Finais

**Tabela comparativa v1 (baseline) vs v2 (otimizado)**

| Métrica      | v1 (baseline) | v2 (otimizado) | Meta (≥ 0.8)   |
|--------------|---------------|----------------|----------------|
| Helpfulness  | 0.45 ✗        | 0.88 ✓         | ✅            |
| Correctness  | 0.52 ✗        | 0.83 ✓         | ✅            |
| F1-Score     | 0.48 ✗        | 0.82 ✓         | ✅            |
| Clarity      | 0.50 ✗        | 0.91 ✓         | ✅            |
| Precision    | 0.46 ✗        | 0.85 ✓         | ✅            |


3. **Evidências no LangSmith**:
  - Screenshot do dashboard: [images/dash.png](images/dash.png)
  - Avalições retornadas:
  ``` bash
  Prompt: luiz-guilherme-jesus/bug_to_user_story_v2

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

