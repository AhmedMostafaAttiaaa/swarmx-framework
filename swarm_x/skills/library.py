from .base import Skill

summarizer_skill = Skill(
    name="summarizer",
    instructions=(
        "Condense the given text into a short summary. Preserve key facts, numbers, "
        "and names. Drop filler and repetition. Default to 3-5 sentences unless the "
        "caller specifies a different length."
    ),
)

code_reviewer_skill = Skill(
    name="code_reviewer",
    instructions=(
        "Review the given code for correctness, security, and clarity. Point out real "
        "bugs, unsafe patterns, and missing edge-case handling; do not nitpick style. "
        "For each issue, state the concrete failure scenario, not just a general concern."
    ),
)
