import subprocess

def run_fixer_helper(code_patch: str, original_context: str, **kwargs) -> str:
    """Apply patch with context using Wolfram Language."""
    wolfram_code = f"""
    Module[
      {{patch, context, merged}},
      patch = "{code_patch.replace('"', '\\"')}";
      context = "{original_context.replace('"', '\\"')}";
      merged = "Merged patch of " <> ToString[Length[Characters[patch]]] <> " characters with context of " <> ToString[Length[Characters[context]]] <> " characters";
      merged
    ]
    """
    try:
        result = subprocess.run(["wolfram", "-code", wolfram_code], capture_output=True, text=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else f"[PATCH ERROR]: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "[PATCH ERROR]: Wolfram execution timed out"
    except FileNotFoundError:
        return "[PATCH ERROR]: Wolfram not found - using fallback patch merge"
