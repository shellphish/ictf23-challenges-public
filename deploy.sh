challenges=(
    ai_calc
    ai_cryptic_game
    ai_lock
    aimazing
    ai_mystical_castle
    aipi_escape
    brokenwords
    bugdget
    bytes_in_pairs
    ci_ninja
    ci_ninja2
    deepfakes
    escape_from_markov
    evilmodel
    ghostinthestack
    guesstimate
    islandparty
    lost_album
    max_64
    parakeet
    parakeet_v2
    pixel_mirage
    pixel_mirage2
    printbof
    rockpaperscissors
    rustyneurone
    snake
    stopthemodelthief
    stopthespammer
    supermart
    tensormania
    translation
    trendy
    who_is_waldo
)

for c in "${challenges[@]}"; do
    ctf challenge install "ictf23-challenges-public/$c"
    ctf challenge deploy "ictf23-challenges-public/$c"
done
