(define (domain castle_escape)
    (:requirements :strips :typing :negative-preconditions)
    (:types
        room
        key
    )
    (:predicates
        (at ?r - room)
        (opens_with ?r - room ?k1 - key ?k2 - key)
        (opened_with ?r - room ?k1 - key ?k2 - key)
        (has_key ?k - key ?r - room)
        (got_key ?k - key)
        (blocks ?r1 - room ?r2 - room)
        (blocked ?r - room)
    )

    (:action move
        :parameters (?from - room ?to - room ?bl - room ?k1 - key ?k2 - key)
        :precondition (and (at ?from) (not (blocked ?to))
                           (opens_with ?to ?k1 ?k2) (got_key ?k1) (got_key ?k2) (blocks ?to ?bl))
        :effect (and (blocked ?bl) (not (at ?from)) (at ?to) (opened_with ?to ?k1 ?k2)
        )
    )

    (:action pickup_key
        :parameters (?r - room ?k - key)
        :precondition (and (at ?r) (has_key ?k ?r))
        :effect (got_key ?k)
    )
)
