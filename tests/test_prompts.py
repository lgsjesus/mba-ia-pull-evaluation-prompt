"""
Testes automatizados para validação de prompts.
"""

import sys
from pathlib import Path

import pytest
import yaml

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_latest_prompt_file() -> Path:
    """Retorna o arquivo de prompt com maior versão (vN)."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    candidates = sorted(prompts_dir.glob("bug_to_user_story_v*.yml"))
    candidates = [p for p in candidates if "_old" not in p.stem]

    if not candidates:
        raise FileNotFoundError("Nenhum arquivo de prompt encontrado em /prompts")

    def version_key(path: Path) -> int:
        stem = path.stem  # bug_to_user_story_v2
        return int(stem.rsplit("v", 1)[-1])

    return max(candidates, key=version_key)


def get_prompt_payload() -> dict:
    """Carrega o payload interno do prompt do arquivo YAML mais recente."""
    data = load_prompts(str(get_latest_prompt_file()))
    return next(iter(data.values()))


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = get_prompt_payload()
        _, errors = validate_prompt_structure(prompt)

        system_errors = [
            err
            for err in errors
            if "system_prompt" in err.lower()
            or "campo obrigatório faltando: system_prompt" in err.lower()
        ]

        assert prompt.get("system_prompt") is not None
        assert prompt.get("system_prompt", "").strip() != ""
        assert not system_errors, f"Erros em system_prompt: {system_errors}"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt = get_prompt_payload()
        system_prompt = prompt.get("system_prompt", "")

        role_markers = ["Você é", "Você atua como", "Seu papel é", "Como "]
        assert any(marker in system_prompt for marker in role_markers), (
            "system_prompt deve definir persona explícita (ex: 'Você é um Product Manager')"
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt = get_prompt_payload()
        system_prompt = prompt.get("system_prompt", "")

        format_markers = ["Markdown", "User Story", "Critérios de Aceitação", "Como um"]
        assert any(marker in system_prompt for marker in format_markers), (
            "system_prompt deve exigir formato de saída (Markdown/User Story padrão)"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt = get_prompt_payload()
        system_prompt = prompt.get("system_prompt", "")

        has_examples_section = (
            "EXEMPLOS" in system_prompt or "Exemplos" in system_prompt
        )
        has_input_output_pattern = (
            "Relato:" in system_prompt and "Saída:" in system_prompt
        )

        assert has_examples_section and has_input_output_pattern, (
            "system_prompt deve conter exemplos Few-shot com pares de entrada/saída"
        )

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = get_prompt_payload()
        joined_text = "\n".join(
            str(value) for value in prompt.values() if isinstance(value, str)
        )
        assert "[TODO]" not in joined_text
        assert "TODO" not in joined_text

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt = get_prompt_payload()
        techniques = prompt.get("techniques_applied", [])

        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, (
            f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
