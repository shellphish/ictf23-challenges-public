(define (problem castle_escape_problem)
    (:domain castle_escape)
    (:objects
        whispering_gallery enchanted_hall mirror_chamber dragon_lair wizards_study
        moonlit_grove shadowy_vault sunken_crypt frozen_cell phantom_corridor
        serpents_nest knights_hall golden_sanctum crystal_cove mystic_garden
        starlit_tower silent_tomb echoing_cavern haunted_chamber forbidden_throne - room
        sapphire_key ruby_key emerald_key diamond_key amethyst_key
        topaz_key opal_key pearl_key garnet_key onyx_key
        moonstone_key sunstone_key quartz_key turquoise_key jade_key
        obsidian_key amber_key citrine_key lapis_key agate_key - key
    )
    (:init
        ;at
        In Whispering Gallery begins our tale,

        ;opens_with
        Atop a vault of shadows, silent, steep, topaz, pearl keys awake its sleep.
        Crypt sunken 'neath the time's decree, opal, garnet turn the key.
        Cell of frostbound, age-old hex, yields to pearl and onyx's behest.

        (opens_with phantom_corridor garnet_key moonstone_key)
        (opens_with enchanted_hall sapphire_key emerald_key)
        (opens_with mirror_chamber ruby_key diamond_key)
        (opens_with dragon_lair emerald_key amethyst_key)

        Bow of Wizard's study, knowledge bound, diamond, topaz keys unwound.
        Grove beneath the moonlit sky, amethyst, opal the secrets ply.
        Knight's great hall, strong and tall, with moonstone, quartz, its gates do fall.
        Golden sanctum's hidden trust, unveiled by sunstone, turquoise's thrust.

        (opens_with crystal_cove quartz_key jade_key)
        (opens_with mystic_garden turquoise_key obsidian_key)
        (opens_with starlit_tower jade_key amber_key)
        (opens_with echoing_cavern amber_key lapis_key)

        Haunted chamber's secrets deep, citrine, agate open keep.
        Throne's domain, regal, vast, lapis, agate keys hold fast.
        Serpents' nest, coils tight, onyx, sunstone keys ignite.
        Silent tomb, whispers cease, obsidian, citrine keys release.

        ;has_key
        In the gallery that whispers, sapphire key does rest,
        With emerald key beside, in the very same nest.
        Ruby key in enchanted hall does dwell,
        Sunstone key in the corridor where phantoms tell.

        (has_key quartz_key serpents_nest)
        (has_key opal_key wizards_study)
        (has_key pearl_key moonlit_grove)
        (has_key garnet_key shadowy_vault)

        Onyx key in the crypt, sunken and deep,
        Moonstone key in the frozen cell's keep.
        Jade key in the hall where knights do parade,
        Obsidian key in the crystal cove's shade.

        (has_key amber_key mystic_garden)
        (has_key citrine_key starlit_tower)
        (has_key lapis_key silent_tomb)
        (has_key agate_key echoing_cavern)

        (has_key turquoise_key knights_hall)
        (has_key diamond_key enchanted_hall)
        (has_key diamond_key mirror_chamber)
        (has_key amethyst_key mirror_chamber)
        (has_key topaz_key mirror_chamber)
        (has_key topaz_key wizards_study)

        ;blocks
        In verse, the castle's blockades we now state,
        Each line a path, each path a fate.

        Wizards' study blocks the mirror's gleam,
        Moonlit grove blocks the enchanted hall's dream.
        Mystic garden blocks the moonlit grove,
        Starlit tower blocks the crypt below.

        (blocks silent_tomb shadowy_vault)
        (blocks echoing_cavern moonlit_grove)
        (blocks haunted_chamber wizards_study)
        (blocks forbidden_throne whispering_gallery)

        Whispering gallery, enchanted hall blocks,
        Enchanted hall, whispering gallery locks.
        Mirror chamber, enchanted hall's gate,
        Dragon lair, whispering gallery's fate.

        (blocks knights_hall serpents_nest)
        (blocks crystal_cove serpents_nest)
        (blocks shadowy_vault wizards_study)
        (blocks sunken_crypt enchanted_hall)

        Frozen cell blocks the dragon's lair,
        Phantom corridor, shadowy vault's snare.
        Serpents' nest blocks the moonlit grove,
        Golden sanctum, moonlit grove's trove.
    )
    ;goal
    And so the goal, clear and true,
    To reach the throne, forbidden view
    And claim the crown, the kingdom's due.
)
