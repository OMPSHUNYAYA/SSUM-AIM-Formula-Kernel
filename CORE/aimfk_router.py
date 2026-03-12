import json
import hashlib
import datetime
import math
import re
import sys
from pathlib import Path

AIMFK_VERSION = "0.2"

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TASK_FILE = BASE_DIR / "TASKS" / "TASK_PAYLOAD.json"
RESULT_FILE = BASE_DIR / "TASKS" / "TASK_RESULT.json"
RECEIPTS_DIR = BASE_DIR / "RECEIPTS"
LOG_FILE = BASE_DIR / "LOGS" / "aimfk_run_log.jsonl"
MANIFEST_FILE = BASE_DIR / "MANIFESTS" / "core_arithmetic_manifest.json"
VERIFY_FILE = BASE_DIR / "release" / "VERIFY_SHA256.txt"

FROZEN_RELATIVE_PATHS = [
    "CORE/aimfk_router.py",
    "MANIFESTS/core_arithmetic_manifest.json",
    "RUN/RUN_AIMFK.cmd",
    "EXAMPLES/example_eval.json",
    "EXAMPLES/example_subst.json",
    "EXAMPLES/example_verify.json",
    "EXAMPLES/example_poly_eval.json",
    "EXAMPLES/example_poly_sum.json",
    "EXAMPLES/example_poly_mul.json",
    "EXAMPLES/example_solve_linear.json",
    "EXAMPLES/example_solve_quadratic.json",
    "EXAMPLES/example_matrix_add.json",
    "EXAMPLES/example_matrix_sub.json",
    "EXAMPLES/example_matrix_mul.json",
    "release/AIMFK_RELEASE_NOTES.txt",
    "release/FREEZE_NOTE.txt"
]

def utc_now():
    return datetime.datetime.now(datetime.UTC).isoformat()

def make_stamp(obj):
    payload = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def write_receipt(result):
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    ts_safe = result["timestamp"].replace(":", "-")
    receipt_file = RECEIPTS_DIR / f"receipt_{ts_safe}.json"
    with open(receipt_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

def append_log(result):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, sort_keys=True) + "\n")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_mode():
    if len(sys.argv) >= 2 and sys.argv[1] == "--verify-release":
        return "verify_release", None, "verify_release"
    if len(sys.argv) >= 2 and sys.argv[1] == "--generate-release-hash":
        return "generate_release_hash", None, "generate_release_hash"
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        candidate = Path(sys.argv[1])
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        return "task", candidate, "cli_path"
    return "task", DEFAULT_TASK_FILE, "default_task_payload"

def load_manifest():
    manifest = load_json(MANIFEST_FILE)
    required_keys = [
        "task_types",
        "allowed_operators",
        "allowed_functions",
        "max_expression_length",
        "verify_mode",
        "polynomial_mode",
        "solve_mode",
        "matrix_mode",
        "simplify_mode",
        "proof_trace_mode"
    ]
    missing = [k for k in required_keys if k not in manifest]
    if missing:
        raise ValueError("manifest missing required fields: " + ", ".join(missing))
    return manifest

def safe_eval(expr):
    expr = expr.replace("^", "**")
    allowed_names = {
        "sqrt": math.sqrt
    }
    return eval(expr, {"__builtins__": None}, allowed_names)

def substitute_expression(expr, values):
    result = expr
    for key, value in values.items():
        pattern = r"\b" + re.escape(str(key)) + r"\b"
        result = re.sub(pattern, str(value), result)
    return result

def approx_equal(a, b, tol=1e-12):
    return abs(a - b) <= tol

def poly_trim(poly):
    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result

def poly_eval(coeffs, x):
    total = 0
    for i, c in enumerate(coeffs):
        total += c * (x ** i)
    return total

def poly_sum(a, b):
    n = max(len(a), len(b))
    result = []
    for i in range(n):
        av = a[i] if i < len(a) else 0
        bv = b[i] if i < len(b) else 0
        result.append(av + bv)
    return poly_trim(result)

def poly_mul(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            result[i + j] += av * bv
    return poly_trim(result)

def solve_linear(a, b):
    if a == 0:
        if b == 0:
            return {"status": "infinite_solutions"}
        return {"status": "no_solution"}
    return {"status": "unique_solution", "x": (-b / a)}

def solve_quadratic(a, b, c):
    if a == 0:
        linear = solve_linear(b, c)
        linear["reduced_to"] = "linear"
        return linear

    discriminant = b * b - 4 * a * c

    if discriminant > 0:
        sqrt_d = math.sqrt(discriminant)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        roots = sorted([x1, x2])
        return {
            "status": "two_real_roots",
            "discriminant": discriminant,
            "roots": roots
        }

    if discriminant == 0:
        x = (-b) / (2 * a)
        return {
            "status": "one_real_root",
            "discriminant": discriminant,
            "roots": [x]
        }

    real_part = (-b) / (2 * a)
    imag_part = math.sqrt(-discriminant) / (2 * a)
    return {
        "status": "complex_roots",
        "discriminant": discriminant,
        "roots": [
            {"real": real_part, "imag": imag_part},
            {"real": real_part, "imag": -imag_part}
        ]
    }

def matrix_shape(m):
    if not isinstance(m, list) or len(m) == 0:
        raise ValueError("matrix must be a non-empty list")
    cols = len(m[0])
    if cols == 0:
        raise ValueError("matrix rows must be non-empty")
    for row in m:
        if not isinstance(row, list) or len(row) != cols:
            raise ValueError("matrix must be rectangular")
    return (len(m), cols)

def matrix_add(a, b):
    ra, ca = matrix_shape(a)
    rb, cb = matrix_shape(b)
    if (ra, ca) != (rb, cb):
        raise ValueError("matrix shapes must match for addition")
    return [
        [a[i][j] + b[i][j] for j in range(ca)]
        for i in range(ra)
    ]

def matrix_sub(a, b):
    ra, ca = matrix_shape(a)
    rb, cb = matrix_shape(b)
    if (ra, ca) != (rb, cb):
        raise ValueError("matrix shapes must match for subtraction")
    return [
        [a[i][j] - b[i][j] for j in range(ca)]
        for i in range(ra)
    ]

def matrix_mul(a, b):
    ra, ca = matrix_shape(a)
    rb, cb = matrix_shape(b)
    if ca != rb:
        raise ValueError("inner matrix dimensions must match for multiplication")
    result = []
    for i in range(ra):
        row = []
        for j in range(cb):
            total = 0
            for k in range(ca):
                total += a[i][k] * b[k][j]
            row.append(total)
        result.append(row)
    return result

def simplify_expression(expr):
    expr = expr.replace(" ", "")

    if expr == "x+x":
        return "2*x"
    if expr == "x+0":
        return "x"
    if expr == "0+x":
        return "x"
    if expr == "x*1":
        return "x"
    if expr == "1*x":
        return "x"
    if expr == "x*0":
        return "0"
    if expr == "0*x":
        return "0"

    return expr

def enforce_expression_length(expr, manifest):
    if len(expr) > manifest["max_expression_length"]:
        raise ValueError("expression exceeds manifest max_expression_length")

def extract_function_names(expr):
    return set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", expr))

def enforce_functions(expr, manifest):
    names = extract_function_names(expr)
    allowed = set(manifest["allowed_functions"])
    disallowed = sorted(name for name in names if name not in allowed)
    if disallowed:
        raise ValueError("expression uses disallowed functions: " + ", ".join(disallowed))

def enforce_operators(expr, manifest):
    allowed = set(manifest["allowed_operators"])
    normalized = expr.replace(" ", "")
    normalized = normalized.replace("**", "^")
    operators_found = set(ch for ch in normalized if ch in "+-*/^")
    disallowed = sorted(op for op in operators_found if op not in allowed)
    if disallowed:
        raise ValueError("expression uses disallowed operators: " + ", ".join(disallowed))

def enforce_expression_contract(expr, manifest):
    if not isinstance(expr, str):
        raise ValueError("expression must be a string")
    enforce_expression_length(expr, manifest)
    enforce_functions(expr, manifest)
    enforce_operators(expr, manifest)

def enforce_task_contract(task, manifest):
    task_name = task.get("task")
    if task_name not in manifest["task_types"]:
        raise ValueError("task not allowed by manifest")

    if task_name == "EVAL":
        expr = task.get("expression")
        enforce_expression_contract(expr, manifest)

    elif task_name == "SUBST":
        expr = task.get("expression")
        enforce_expression_contract(expr, manifest)

    elif task_name == "SIMPLIFY":
        expr = task.get("expression")
        enforce_expression_contract(expr, manifest)

    elif task_name == "VERIFY":
        left_expr = task.get("left_expression")
        right_expr = task.get("right_expression")
        enforce_expression_contract(left_expr, manifest)
        enforce_expression_contract(right_expr, manifest)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def canonical_relative_path(path):
    return str(path).replace("/", "\\")

def get_frozen_entries():
    entries = []
    for rel_path_text in FROZEN_RELATIVE_PATHS:
        rel_path = Path(rel_path_text)
        file_path = BASE_DIR / rel_path
        entries.append({
            "relative_path": canonical_relative_path(rel_path),
            "file_path": file_path
        })
    return entries

def generate_release_hash():
    entries = get_frozen_entries()

    missing_files = []
    hash_entries = []

    for entry in entries:
        file_path = entry["file_path"]
        relative_path = entry["relative_path"]

        if not file_path.exists():
            missing_files.append(relative_path)
            continue

        hash_entries.append({
            "relative_path": relative_path,
            "sha256": sha256_file(file_path)
        })

    if missing_files:
        raise FileNotFoundError("frozen boundary file(s) missing: " + ", ".join(missing_files))

    VERIFY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VERIFY_FILE, "w", encoding="utf-8", newline="\n") as f:
        for entry in hash_entries:
            f.write(entry["sha256"] + "  " + entry["relative_path"] + "\n")

    return {
        "AIMFK_version": AIMFK_VERSION,
        "task": "GENERATE_RELEASE_HASH",
        "verify_file": str(VERIFY_FILE),
        "entries_written": len(hash_entries),
        "frozen_boundary_file_count": len(entries),
        "missing_file_count": 0,
        "generation_status": "PASS",
        "hash_entries": hash_entries
    }

def parse_verify_file(path):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            match = re.match(r"^([0-9a-fA-F]{64})\s+(.+)$", line)
            if match:
                expected_hash = match.group(1).lower()
                relative_path = canonical_relative_path(match.group(2).strip())
                entries.append({
                    "expected_hash": expected_hash,
                    "relative_path": relative_path
                })
    return entries

def verify_release():
    if not VERIFY_FILE.exists():
        raise FileNotFoundError(f"verify file not found: {VERIFY_FILE}")

    entries = parse_verify_file(VERIFY_FILE)

    checked_files = []
    missing_files = []
    mismatched_files = []

    for entry in entries:
        rel_path_text = entry["relative_path"]
        rel_path = Path(rel_path_text)
        file_path = BASE_DIR / rel_path

        if not file_path.exists():
            missing_files.append(rel_path_text)
            continue

        actual_hash = sha256_file(file_path)
        expected_hash = entry["expected_hash"]

        checked_files.append({
            "file": rel_path_text,
            "expected_hash": expected_hash,
            "actual_hash": actual_hash,
            "match": actual_hash == expected_hash
        })

        if actual_hash != expected_hash:
            mismatched_files.append({
                "file": rel_path_text,
                "expected_hash": expected_hash,
                "actual_hash": actual_hash
            })

    verification_status = "PASS"
    if len(entries) == 0 or missing_files or mismatched_files:
        verification_status = "FAIL"

    result = {
        "AIMFK_version": AIMFK_VERSION,
        "task": "VERIFY_RELEASE",
        "verify_file": str(VERIFY_FILE),
        "entries_declared": len(entries),
        "checked_file_count": len(checked_files),
        "missing_file_count": len(missing_files),
        "mismatch_count": len(mismatched_files),
        "verification_status": verification_status,
        "checked_files": checked_files,
        "missing_files": missing_files,
        "mismatched_files": mismatched_files
    }

    return result

def main():
    mode, task_file, input_mode = get_mode()
    manifest = load_manifest()

    result = {
        "AIMFK_version": AIMFK_VERSION,
        "manifest_name": manifest.get("manifest_name"),
        "manifest_version": manifest.get("version")
    }

    try:
        if mode == "verify_release":
            result["input_mode"] = input_mode
            result.update(verify_release())

        elif mode == "generate_release_hash":
            result["input_mode"] = input_mode
            result.update(generate_release_hash())

        else:
            result["input_mode"] = input_mode
            result["task_file"] = str(task_file)

            if not task_file.exists():
                raise FileNotFoundError(f"task file not found: {task_file}")

            task = load_json(task_file)
            enforce_task_contract(task, manifest)

            result["task"] = task.get("task")

            if task.get("task") == "EVAL":
                expr = task["expression"]
                value = safe_eval(expr)

                result["expression"] = expr
                result["result"] = value
                result["proof_trace"] = [
                    {"step": 1, "action": "evaluate_expression", "input": expr, "output": value}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "SUBST":
                expr = task["expression"]
                values = task["values"]
                substituted = substitute_expression(expr, values)
                enforce_expression_contract(substituted, manifest)
                value = safe_eval(substituted)

                result["expression"] = expr
                result["values"] = values
                result["substituted_expression"] = substituted
                result["result"] = value
                result["proof_trace"] = [
                    {"step": 1, "action": "read_expression", "output": expr},
                    {"step": 2, "action": "substitute_values", "values": values, "output": substituted},
                    {"step": 3, "action": "evaluate_substituted_expression", "output": value}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "VERIFY":
                left_expr = task["left_expression"]
                right_expr = task["right_expression"]
                values = task.get("values", {})

                left_sub = substitute_expression(left_expr, values)
                right_sub = substitute_expression(right_expr, values)

                enforce_expression_contract(left_sub, manifest)
                enforce_expression_contract(right_sub, manifest)

                left_value = safe_eval(left_sub)
                right_value = safe_eval(right_sub)

                verified = approx_equal(left_value, right_value)

                result["left_expression"] = left_expr
                result["right_expression"] = right_expr
                result["values"] = values
                result["left_substituted"] = left_sub
                result["right_substituted"] = right_sub
                result["left_result"] = left_value
                result["right_result"] = right_value
                result["verified"] = verified
                result["verification_mode"] = manifest["verify_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_left_expression", "output": left_expr},
                    {"step": 2, "action": "read_right_expression", "output": right_expr},
                    {"step": 3, "action": "substitute_left_expression", "values": values, "output": left_sub},
                    {"step": 4, "action": "substitute_right_expression", "values": values, "output": right_sub},
                    {"step": 5, "action": "evaluate_left_expression", "output": left_value},
                    {"step": 6, "action": "evaluate_right_expression", "output": right_value},
                    {"step": 7, "action": "compare_results", "output": verified}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "POLY_EVAL":
                coeffs = task["coefficients"]
                x = task["x"]
                value = poly_eval(coeffs, x)

                result["coefficients"] = coeffs
                result["x"] = x
                result["result"] = value
                result["polynomial_mode"] = manifest["polynomial_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_coefficients", "output": coeffs},
                    {"step": 2, "action": "read_x", "output": x},
                    {"step": 3, "action": "evaluate_polynomial", "output": value}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "POLY_SUM":
                poly_a = task["poly_a"]
                poly_b = task["poly_b"]
                summed = poly_sum(poly_a, poly_b)

                result["poly_a"] = poly_a
                result["poly_b"] = poly_b
                result["result_poly"] = summed
                result["polynomial_mode"] = manifest["polynomial_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_poly_a", "output": poly_a},
                    {"step": 2, "action": "read_poly_b", "output": poly_b},
                    {"step": 3, "action": "sum_polynomials", "output": summed}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "POLY_MUL":
                poly_a = task["poly_a"]
                poly_b = task["poly_b"]
                product = poly_mul(poly_a, poly_b)

                result["poly_a"] = poly_a
                result["poly_b"] = poly_b
                result["result_poly"] = product
                result["polynomial_mode"] = manifest["polynomial_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_poly_a", "output": poly_a},
                    {"step": 2, "action": "read_poly_b", "output": poly_b},
                    {"step": 3, "action": "multiply_polynomials", "output": product}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "SOLVE_LINEAR":
                a = task["a"]
                b = task["b"]
                solved = solve_linear(a, b)

                result["equation_form"] = "a*x + b = 0"
                result["a"] = a
                result["b"] = b
                result.update(solved)
                result["solve_mode"] = manifest["solve_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_linear_coefficients", "output": {"a": a, "b": b}},
                    {"step": 2, "action": "solve_linear_equation", "output": solved}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "SOLVE_QUADRATIC":
                a = task["a"]
                b = task["b"]
                c = task["c"]
                solved = solve_quadratic(a, b, c)

                result["equation_form"] = "a*x^2 + b*x + c = 0"
                result["a"] = a
                result["b"] = b
                result["c"] = c
                result.update(solved)
                result["solve_mode"] = manifest["solve_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_quadratic_coefficients", "output": {"a": a, "b": b, "c": c}},
                    {"step": 2, "action": "solve_quadratic_equation", "output": solved}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "MATRIX_ADD":
                matrix_a = task["matrix_a"]
                matrix_b = task["matrix_b"]
                matrix_result = matrix_add(matrix_a, matrix_b)

                result["matrix_a"] = matrix_a
                result["matrix_b"] = matrix_b
                result["result_matrix"] = matrix_result
                result["matrix_mode"] = manifest["matrix_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_matrix_a", "output": matrix_a},
                    {"step": 2, "action": "read_matrix_b", "output": matrix_b},
                    {"step": 3, "action": "add_matrices", "output": matrix_result}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "MATRIX_SUB":
                matrix_a = task["matrix_a"]
                matrix_b = task["matrix_b"]
                matrix_result = matrix_sub(matrix_a, matrix_b)

                result["matrix_a"] = matrix_a
                result["matrix_b"] = matrix_b
                result["result_matrix"] = matrix_result
                result["matrix_mode"] = manifest["matrix_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_matrix_a", "output": matrix_a},
                    {"step": 2, "action": "read_matrix_b", "output": matrix_b},
                    {"step": 3, "action": "subtract_matrices", "output": matrix_result}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "MATRIX_MUL":
                matrix_a = task["matrix_a"]
                matrix_b = task["matrix_b"]
                matrix_result = matrix_mul(matrix_a, matrix_b)

                result["matrix_a"] = matrix_a
                result["matrix_b"] = matrix_b
                result["result_matrix"] = matrix_result
                result["matrix_mode"] = manifest["matrix_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_matrix_a", "output": matrix_a},
                    {"step": 2, "action": "read_matrix_b", "output": matrix_b},
                    {"step": 3, "action": "multiply_matrices", "output": matrix_result}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            elif task.get("task") == "SIMPLIFY":
                expr = task["expression"]
                simplified = simplify_expression(expr)

                result["expression"] = expr
                result["simplified_expression"] = simplified
                result["simplify_mode"] = manifest["simplify_mode"]
                result["proof_trace"] = [
                    {"step": 1, "action": "read_expression", "output": expr},
                    {"step": 2, "action": "apply_deterministic_simplification_rules", "output": simplified}
                ]
                result["proof_trace_mode"] = manifest["proof_trace_mode"]

            else:
                result["error"] = "unsupported task"

    except Exception as e:
        result["error"] = str(e)

    result["timestamp"] = utc_now()
    result["stamp"] = make_stamp(result)

    write_json(RESULT_FILE, result)
    write_receipt(result)
    append_log(result)

if __name__ == "__main__":
    main()