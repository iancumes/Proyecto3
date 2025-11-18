
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List, Any, Iterable, Set


Symbol = Optional[str]  # None will be used for the blank symbol on the tape


@dataclass(frozen=True)
class TransitionKey:
    """Key to identify a transition: (current_state, mem_cache_value, tape_input)."""
    state: str
    mem_value: Symbol
    tape_symbol: Symbol


@dataclass
class TransitionResult:
    """Result of a transition: (next_state, new_mem_value, tape_output_symbol, movement)."""
    next_state: str
    new_mem_value: Symbol
    write_symbol: Symbol
    head_move: str  # "L", "R" or "S"


@dataclass
class SimulationResult:
    accepted: bool
    final_state: str
    final_tape: str
    history: List[str]
    halted_by: str  # "no_transition", "max_steps"


class Tape:
    """
    Representa una cinta infinita hacia ambos lados.
    Internamente se usa un diccionario (posicion -> simbolo).
    Si una posicion no existe en el diccionario, se considera blank (None).
    """

    def __init__(self, blank: Symbol = None) -> None:
        self.blank: Symbol = blank
        self._cells: Dict[int, Symbol] = {}
        self.head: int = 0

    @classmethod
    def from_input(cls, input_string: str, blank: Symbol = None) -> "Tape":
        tape = cls(blank=blank)
        for i, ch in enumerate(input_string):
            tape._cells[i] = ch
        tape.head = 0
        return tape

    def read(self) -> Symbol:
        return self._cells.get(self.head, self.blank)

    def write(self, symbol: Symbol) -> None:
        if symbol is None or symbol == self.blank:
            # Borrar la celda si solo contiene blank para mantener cinta finita
            self._cells.pop(self.head, None)
        else:
            self._cells[self.head] = symbol

    def move(self, direction: str) -> None:
        if direction == "L":
            self.head -= 1
        elif direction == "R":
            self.head += 1
        elif direction == "S":
            # Stay
            return
        else:
            raise ValueError(f"Movimiento inválido en la cinta: {direction!r}")

    def _range(self) -> Tuple[int, int]:
        if not self._cells:
            return self.head, self.head
        min_pos = min(self._cells.keys() | {self.head})
        max_pos = max(self._cells.keys() | {self.head})
        return min_pos, max_pos

    def as_string(self, blank_repr: str = "_") -> str:
        """Devuelve el contenido de la cinta (desde la primera hasta la última celda usada)."""
        min_pos, max_pos = self._range()
        chars: List[str] = []
        for i in range(min_pos, max_pos + 1):
            sym = self._cells.get(i, self.blank)
            if sym is None:
                chars.append(blank_repr)
            else:
                chars.append(str(sym))
        return "".join(chars)

    def format_with_head(self, blank_repr: str = "_") -> str:
        """
        Devuelve la cinta como string, marcando la posición del cabezal con corchetes.
        Ejemplo: __[a]b__
        """
        min_pos, max_pos = self._range()
        parts: List[str] = []
        for i in range(min_pos, max_pos + 1):
            sym = self._cells.get(i, self.blank)
            if sym is None:
                ch = blank_repr
            else:
                ch = str(sym)

            if i == self.head:
                parts.append(f"[{ch}]")
            else:
                parts.append(f" {ch} ")
        return "".join(parts)


class TuringMachine:
    """
    Implementación básica de una MT de una sola cinta con un registro de memoria (mem_cache_value).
    Las transiciones se buscan usando (estado_actual, mem_cache_value, simbolo_leido).
    """

    def __init__(
        self,
        states: Iterable[str],
        initial_state: str,
        final_states: Iterable[str],
        alphabet: Iterable[str],
        tape_alphabet: Iterable[Symbol],
        transitions: Dict[TransitionKey, TransitionResult],
        blank_symbol: Symbol = None,
    ) -> None:
        self.states: Set[str] = set(states)
        self.initial_state: str = initial_state
        self.final_states: Set[str] = set(final_states)
        self.alphabet: Set[str] = set(alphabet)
        self.tape_alphabet: Set[Symbol] = set(tape_alphabet)
        self.transitions: Dict[TransitionKey, TransitionResult] = transitions
        self.blank_symbol: Symbol = blank_symbol

        if self.initial_state not in self.states:
            raise ValueError(f"Estado inicial {initial_state!r} no pertenece al conjunto de estados.")
        if not self.final_states.issubset(self.states):
            raise ValueError("Hay estados finales que no pertenecen al conjunto de estados.")

    def run(self, input_string: str, max_steps: int = 1000) -> SimulationResult:
        """
        Simula la MT sobre una cadena de entrada.
        Devuelve un SimulationResult con la historia de IDs, el estado final y si se aceptó o no.
        """
        state = self.initial_state
        mem_cache: Symbol = None
        tape = Tape.from_input(input_string, blank=self.blank_symbol)

        history: List[str] = []
        history.append(self._format_id(step=0, state=state, mem_cache=mem_cache, tape=tape))

        halted_by = "no_transition"
        for step in range(1, max_steps + 1):
            current_symbol = tape.read()
            key = TransitionKey(state=state, mem_value=mem_cache, tape_symbol=current_symbol)

            result = self.transitions.get(key)
            if result is None:
                break

            state = result.next_state
            mem_cache = result.new_mem_value
            tape.write(result.write_symbol)
            tape.move(result.head_move)

            history.append(self._format_id(step=step, state=state, mem_cache=mem_cache, tape=tape))
        else:
            halted_by = "max_steps"

        final_state = state
        final_tape = tape.as_string()
        accepted = final_state in self.final_states

        return SimulationResult(
            accepted=accepted,
            final_state=final_state,
            final_tape=final_tape,
            history=history,
            halted_by=halted_by,
        )

    def _format_id(self, step: int, state: str, mem_cache: Symbol, tape: Tape) -> str:
        mem_repr = "_" if mem_cache is None else str(mem_cache)
        tape_repr = tape.format_with_head()
        return f"Paso {step:03d} | q={state} | mem={mem_repr} | cinta: {tape_repr}"
