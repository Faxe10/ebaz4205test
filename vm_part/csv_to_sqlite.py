import ast, re
from numbers import Number
import pandas as pd

BIT_LENGTHS = {8, 16, 24, 32, 64}

def parse_binary_string(s: str):
    s = s.strip()
    if set(s) <= {"0", "1"} and len(s) in BIT_LENGTHS:
        try:
            return int(s, 2)
        except Exception:
            return None
    return None

def to_number(x):
    """Konvertiert Messwerte robust in float.
    Spezialfall: Listen/Tupel mit [dezimal, binärstring] -> binärstring wird bevorzugt.
    """
    # leere/nicht vorhandene Werte
    if x is None or (isinstance(x, float) and pd.isna(x)) or (isinstance(x, str) and x.strip() == ""):
        return None

    # schon numerisch
    if isinstance(x, Number):
        return float(x)

    # Liste/Tupel – bevorzugt 2. Element (typisch: [dezimal, binär])
    if isinstance(x, (list, tuple)):
        if len(x) == 2:
            _, b = x[0], x[1]
            if isinstance(b, str):
                nb = parse_binary_string(b)
                if nb is not None:
                    return float(nb)
            nb = to_number(b)
            if nb is not None:
                return float(nb)
            # Fallback: notfalls erstes Element (aber hier willst du es ja loswerden)
            return None
        # sonst: erstes sinnvolles Element
        for el in x:
            n = to_number(el)
            if n is not None:
                return float(n)
        return None

    # Dict – bevorzugt Felder, die Binärstrings enthalten könnten
    if isinstance(x, dict):
        for k in ("bin", "binary", "bits", "bitstring"):
            if k in x:
                nb = to_number(x[k])
                if nb is not None:
                    return float(nb)
        for k in ("value", "val", "y", "data", "measurement"):
            if k in x:
                nb = to_number(x[k])
                if nb is not None:
                    return float(nb)
        for v in x.values():
            n = to_number(v)
            if n is not None:
                return float(n)
        return None

    # String
    if isinstance(x, str):
        # erst prüfen, ob es wie ein Binärstring aussieht (z. B. 32 Bit f'032b')
        nb = parse_binary_string(x)
        if nb is not None:
            return float(nb)

        # JSON-/Python-Literal? (z. B. "[0, '00001010']")
        s = x.strip()
        if (s.startswith("[") and s.endswith("]")) or (s.startswith("{") and s.endswith("}")):
            try:
                obj = ast.literal_eval(s)
                return to_number(obj)
            except Exception:
                pass

        # normale Zahl mit Punkt/Komma
        try:
            return float(s.replace(",", "."))
        except Exception:
            pass

        # eingebettete Zahl
        m = re.search(r'[-+]?\d*\.?\d+(?:[eE][+-]?\d+)?', s.replace(",", "."))
        if m:
            try:
                return float(m.group(0))
            except Exception:
                pass
        return None

    return None
