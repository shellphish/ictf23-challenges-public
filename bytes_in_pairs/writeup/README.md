Challenge bytes_in_pairs
=================

This challenge uses byte-pair-encoding on the user-input together with some other text containing the flag. By
injecting the right bytes, the flag can be extracted piece by piece via the resulting tokens. If a matching flag piece
is injected, the resulting text will be counted as appearing multiple times and will be added as a separate token.
This can be used to extract the flag.
