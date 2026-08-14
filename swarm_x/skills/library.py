from .base import Skill

summarizer_skill = Skill(
    name="summarizer",
    instructions=(
        "Condense the given text into a short summary. Preserve key facts, numbers, "
        "and names. Drop filler and repetition. Default to 3-5 sentences unless the "
        "caller specifies a different length."
    ),
)
