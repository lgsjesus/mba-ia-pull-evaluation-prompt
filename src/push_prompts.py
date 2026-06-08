"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from utils import check_env_vars, load_yaml, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
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
        print("🔄 Conectando ao LangSmith Hub para push...")
        client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        messages = [("system", prompt_data["system_prompt"])]
        user_prompt = prompt_data.get("user_prompt", "").strip()
        if user_prompt:
            messages.append(("human", user_prompt))
        prompt_objeto = ChatPromptTemplate.from_messages(messages)
        print(f"🔄 Fazendo push do prompt '{prompt_name}' para o LangSmith Hub...")
        client.push_prompt(
            prompt_identifier=f"luiz-guilherme-jesus/{prompt_name}",
            object=prompt_objeto,
            description=prompt_data.get("description", ""),
            tags=prompt_data.get("tags", []),
            is_public=True,
        )
        print("✅ Push do prompt realizado com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    prompt_name = next(iter(prompt_data.keys()), "unknown_prompt")
    inner = prompt_data.get(prompt_name) or next(
        (v for v in prompt_data.values() if isinstance(v, dict)), prompt_data
    )
    if isinstance(inner, dict):
        if inner.get("description", "").strip() == "":
            errors.append("Campo 'description' é obrigatório e não pode ser vazio.")
        if str(inner.get("version", "")).strip() == "":
            errors.append("Campo 'version' é obrigatório e não pode ser vazio.")
        if str(inner.get("created_at", "")).strip() == "":
            errors.append("Campo 'created_at' é obrigatório e não pode ser vazio.")
        if not inner.get("tags"):
            errors.append("Campo 'tags' é obrigatório e não pode ser vazio.")
            # Se o YAML embutido tiver um system_prompt real, usa-o
        if inner.get("system_prompt", "").strip() == "":
            errors.append("Campo 'system_prompt' é obrigatório e não pode ser vazio.")

    return (len(errors) == 0, errors)


def get_prompt_and_execute_push():
    print_section_header("Iniciando push de prompts otimizados para o LangSmith Hub")

    prompt_path = "prompts/bug_to_user_story_v2.yml"
    prompt_data = load_yaml(prompt_path)
    if not prompt_data:
        print(f"❌ Falha ao carregar o prompt otimizado de {prompt_path}")
        return False

    err, erros = validate_prompt(prompt_data)
    if not err:
        print("❌ Validação do prompt falhou com os seguintes erros:")
        for e in erros:
            print(f"   - {e}")
        return False

    prompt_name = next(iter(prompt_data.keys()))
    return push_prompt_to_langsmith(prompt_name, prompt_data[prompt_name])


def main():
    """Função principal"""
    if get_prompt_and_execute_push():
        print_section_header("Push de prompts concluído com sucesso!")
    else:
        print_section_header("Push de prompts falhou.")


if __name__ == "__main__":
    sys.exit(main())
