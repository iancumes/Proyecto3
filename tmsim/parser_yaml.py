
from __future__ import annotations

from typing import Tuple, List, Optional, Dict, Any
import yaml

from .turing_machine import (
    TuringMachine,
    TransitionKey,
    TransitionResult,
    Symbol,
)


def _normalize_symbol(value: Any) -> Symbol:
    if value is None:
        return None
    return str(value)


def load_machine_from_yaml(path: str) -> Tuple[TuringMachine, List[str]]:
    with open(path, "r", encoding="utf8") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"El archivo YAML {path} está vacío o no se pudo parsear.")

    q_states = data.get("q_states") or {}
    states = [str(s) for s in q_states.get("q_list", [])]
    initial_state = str(q_states.get("initial"))
    final_raw = q_states.get("final")
    if isinstance(final_raw, list):
        final_states = [str(s) for s in final_raw]
    else:
        final_states = [str(final_raw)] if final_raw is not None else []

    alphabet = [str(s) for s in data.get("alphabet", [])]
    tape_alphabet_raw = data.get("tape_alphabet", [])
    tape_alphabet = [_normalize_symbol(s) for s in tape_alphabet_raw]

    blank_symbol = None
    for s in tape_alphabet:
        if s is None:
            blank_symbol = None
            break

    transitions_raw = data.get("delta", [])
    transitions: Dict[TransitionKey, TransitionResult] = {}

    for entry in transitions_raw:
        params = entry.get("params") or {}
        output = entry.get("output") or {}

        initial_state_t = str(params["initial_state"])
        mem_cache_value_in = _normalize_symbol(params.get("mem_cache_value"))
        tape_input = _normalize_symbol(params.get("tape_input"))

        final_state_t = str(output["final_state"])
        mem_cache_value_out = _normalize_symbol(output.get("mem_cache_value"))
        tape_output = _normalize_symbol(output.get("tape_output"))
        tape_displacement = str(output.get("tape_displacement", "S"))

        key = TransitionKey(
            state=initial_state_t,
            mem_value=mem_cache_value_in,
            tape_symbol=tape_input,
        )
        result = TransitionResult(
            next_state=final_state_t,
            new_mem_value=mem_cache_value_out,
            write_symbol=tape_output,
            head_move=tape_displacement,
        )
        transitions[key] = result

    simulation_strings = [str(s) for s in data.get("simulation_strings", [])]

    mt = TuringMachine(
        states=states,
        initial_state=initial_state,
        final_states=final_states,
        alphabet=alphabet,
        tape_alphabet=tape_alphabet,
        transitions=transitions,
        blank_symbol=blank_symbol,
    )

    return mt, simulation_strings
