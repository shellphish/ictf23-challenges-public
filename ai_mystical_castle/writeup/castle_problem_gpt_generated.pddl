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
        (at whispering_gallery)
        (opens_with shadowy_vault topaz_key pearl_key)
        (opens_with sunken_crypt opal_key garnet_key)
        (opens_with frozen_cell pearl_key onyx_key)
        (opens_with phantom_corridor garnet_key moonstone_key)
        (opens_with enchanted_hall sapphire_key emerald_key)
        (opens_with mirror_chamber ruby_key diamond_key)
        (opens_with dragon_lair emerald_key amethyst_key)
        (opens_with wizards_study diamond_key topaz_key)
        (opens_with moonlit_grove amethyst_key opal_key)
        (opens_with knights_hall moonstone_key quartz_key)
        (opens_with golden_sanctum sunstone_key turquoise_key)
        (opens_with crystal_cove quartz_key jade_key)
        (opens_with mystic_garden turquoise_key obsidian_key)
        (opens_with starlit_tower jade_key amber_key)
        (opens_with echoing_cavern amber_key lapis_key)
        (opens_with haunted_chamber citrine_key agate_key)
        (opens_with forbidden_throne lapis_key agate_key)
        (opens_with serpents_nest onyx_key sunstone_key)
        (opens_with silent_tomb obsidian_key citrine_key)
        (has_key sapphire_key whispering_gallery)
        (has_key emerald_key whispering_gallery)
        (has_key ruby_key enchanted_hall)
        (has_key sunstone_key phantom_corridor)
        (has_key quartz_key serpents_nest)
        (has_key opal_key wizards_study)
        (has_key pearl_key moonlit_grove)
        (has_key garnet_key shadowy_vault)
        (has_key onyx_key sunken_crypt)
        (has_key moonstone_key frozen_cell)
        (has_key jade_key knights_hall)
        (has_key obsidian_key crystal_cove)
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
        (blocks wizards_study mirror_chamber)
        (blocks moonlit_grove enchanted_hall)
        (blocks mystic_garden moonlit_grove)
        (blocks starlit_tower sunken_crypt)
        (blocks silent_tomb shadowy_vault)
        (blocks echoing_cavern moonlit_grove)
        (blocks haunted_chamber wizards_study)
        (blocks forbidden_throne whispering_gallery)
        (blocks whispering_gallery enchanted_hall)
        (blocks enchanted_hall whispering_gallery)
        (blocks mirror_chamber enchanted_hall)
        (blocks dragon_lair whispering_gallery)
        (blocks knights_hall serpents_nest)
        (blocks crystal_cove serpents_nest)
        (blocks shadowy_vault wizards_study)
        (blocks sunken_crypt enchanted_hall)
        (blocks frozen_cell dragon_lair)
        (blocks phantom_corridor shadowy_vault)
        (blocks serpents_nest moonlit_grove)
        (blocks golden_sanctum moonlit_grove)
    )
    (:goal (at forbidden_throne))
)
