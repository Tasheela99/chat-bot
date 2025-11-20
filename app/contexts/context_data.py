
import importlib
import os

def get_context(context_name: str, language: str = "en") -> dict:
    """
    Retrieve context information by dynamically importing the context module for the specified language.
    Language options: 'en' (default), 'si', 'ta'
    """
    context_key = context_name.lower()
    lang_suffix = ""
    if language == "si":
        lang_suffix = "_si"
    elif language == "ta":
        lang_suffix = "_ta"
    context_module = None
    available_contexts = [
        f[:-3] for f in os.listdir(os.path.dirname(__file__))
        if f.endswith('.py') and f not in ('__init__.py', 'context_data.py')
    ]
    context_with_lang = f"{context_key}{lang_suffix}"
    if context_with_lang in available_contexts:
        context_module = f"app.contexts.{context_with_lang}"
    elif context_key in available_contexts:
        context_module = f"app.contexts.{context_key}"
    else:
        context_module = "app.contexts.default"
    mod = importlib.import_module(context_module)
    return getattr(mod, "CONTEXT")
