
from __future__ import annotations

import argparse
from typing import List

from tmsim.parser_yaml import load_machine_from_yaml


def simulate_file(yaml_path: str, only_string: str | None = None, max_steps: int = 1000) -> None:
    mt, simulation_strings = load_machine_from_yaml(yaml_path)

    if only_string is not None:
        inputs: List[str] = [only_string]
    else:
        inputs = simulation_strings

    if not inputs:
        print("No hay cadenas configuradas en 'simulation_strings' y no se proporcionó una cadena manualmente.")
        return

    for idx, s in enumerate(inputs, start=1):
        print("=" * 80)
        print(f"Simulación {idx} | entrada = {s!r}")
        result = mt.run(s, max_steps=max_steps)
        for line in result.history:
            print(line)

        print("-" * 80)
        print(f"Estado final : {result.final_state}")
        print(f"Cinta final  : {result.final_tape}")
        if result.accepted:
            print("Resultado   : CADENA ACEPTADA")
        else:
            print("Resultado   : CADENA RECHAZADA")

        if result.halted_by == "max_steps":
            print(f"[Aviso] Se alcanzó el máximo de pasos ({max_steps}). Posible bucle infinito.")

        print("=" * 80)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulador de Máquina de Turing de una cinta (configurada en YAML)."
    )
    parser.add_argument(
        "yaml_file",
        help="Ruta al archivo .yaml que describe la Máquina de Turing.",
    )
    parser.add_argument(
        "--string",
        help="Cadena a simular manualmente (ignora 'simulation_strings' del YAML).",
        default=None,
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=1000,
        help="Máximo de pasos de simulación para evitar ciclos infinitos (default: 1000).",
    )

    args = parser.parse_args()

    simulate_file(args.yaml_file, only_string=args.string, max_steps=args.max_steps)


if __name__ == "__main__":
    main()
