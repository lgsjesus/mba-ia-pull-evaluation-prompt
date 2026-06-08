"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from utils import (
    check_env_vars,
    print_section_header,
    save_yaml,
    serialize_chat_prompt_to_yaml,
)

load_dotenv()

PROMPT_NAME = "bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"


def pull_prompts_from_langsmith():
    print_section_header("Iniciando pull de prompts do LangSmith Hub")

    required_env_vars = [
        "LANGSMITH_API_KEY",
        "USERNAME_LANGSMITH_HUB",
        "LANGSMITH_PROJECT",
    ]
    if not check_env_vars(required_env_vars):
        print(
            "❌ Variáveis de ambiente obrigatórias não configuradas. Verifique o .env"
        )
        return False

    try:
        print("🔄 Conectando ao LangSmith Hub...")
        client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        prompt_template = client.pull_prompt(PROMPT_NAME)
        if not isinstance(prompt_template, ChatPromptTemplate):
            raise ValueError(
                "O formato do prompt retornado não é suportado para esta formatação automática."
            )

        print("script pull_prompts_from_langsmith: Prompts puxados com sucesso!")

        jsonl_path = (
            Path(__file__).parent.parent / "datasets" / "bug_to_user_story.jsonl"
        )
        return run_prompt_with_dataset(prompt_template, str(jsonl_path))

    except Exception as e:
        print(f"❌ Erro ao puxar prompts do LangSmith Hub: {e}")
        return False


def load_dataset(jsonl_path: str) -> list:
    examples: List[Dict[str, Any]] = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    examples.append(json.loads(line))
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {jsonl_path}")
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao parsear JSONL: {e}")
    return examples


def get_first_bug_report(examples: List[Dict[str, Any]]) -> Optional[str]:
    if not examples:
        return None

    first_example = examples[0]
    inputs = first_example.get("inputs", {}) if isinstance(first_example, dict) else {}
    bug_report = inputs.get("bug_report")

    return bug_report if isinstance(bug_report, str) and bug_report.strip() else None


def run_prompt_with_dataset(
    prompt_template: ChatPromptTemplate, jsonl_path: str
) -> bool:
    print_section_header("Executando prompt com bug_reports do dataset")

    examples = load_dataset(jsonl_path)
    if not examples:
        print("❌ Nenhum exemplo carregado.")
        return False

    print(f"📦 {len(examples)} exemplos carregados de: {jsonl_path}\n")

    bug_report = get_first_bug_report(examples)
    if bug_report is None:
        print("❌ Campo inputs.bug_report ausente ou inválido no primeiro exemplo.")
        return False

    print(f"Bug Report: {bug_report[:120]}{'...' if len(bug_report) > 120 else ''}")

    messages = prompt_template.invoke({"bug_report": bug_report})
    system_message = next((m for m in messages.messages if m.type == "system"), None)
    if system_message is None:
        print("❌ System message não encontrada.")
        return False

    print(f"Mensagens formatadas:\n{system_message.content}\n")

    yaml_data = serialize_chat_prompt_to_yaml(prompt_template, PROMPT_NAME)
    if save_yaml(yaml_data, OUTPUT_PATH):
        print(f"✅ Prompts salvos em: {OUTPUT_PATH}")
        return True

    print("❌ Falha ao salvar YAML de prompts.")
    return False


def main():
    """Função principal"""
    if pull_prompts_from_langsmith():
        print_section_header("Pull de prompts concluído com sucesso!")
    else:
        print_section_header("Pull de prompts falhou.")


if __name__ == "__main__":
    sys.exit(main())
