import random

MAIN_LORE = [
    "You are Kael Ashwalker, betrayed by the Seven Thrones and cast into Hell.",
    "Each victory tears one chain from your soul; defeat each Sin to see dawn again.",
]


def ai_rusher(enemy, player):
    return "dash" if abs(enemy.rect.centerx - player.rect.centerx) < 150 else "stalk"


def ai_skirmisher(enemy, player):
    if enemy.hp < enemy.max_hp * 0.35:
        return "retreat"
    return "hop" if enemy.pattern_timer % 90 < 15 else "stalk"


def ai_trickster(enemy, player):
    roll = random.random()
    if roll < 0.3:
        return "hop"
    if roll < 0.55:
        return "retreat"
    return "stalk"


def ai_sentinel(enemy, player):
    return "dash" if enemy.pattern_timer % 120 < 30 else "stalk"


ENEMY_ARCHETYPES = {
    "ember_ghoul": {
        "name": "Ember Ghoul",
        "hp": 38,
        "damage": 9,
        "speed": 2.1,
        "moveset": ["claw_combo", "ember_spit", "lunging_bite"],
        "ai": ai_rusher,
    },
    "chain_wretch": {
        "name": "Chain Wretch",
        "hp": 44,
        "damage": 10,
        "speed": 1.9,
        "moveset": ["chain_whip", "hook_drag", "ankle_snare"],
        "ai": ai_skirmisher,
    },
    "cinder_hunter": {
        "name": "Cinder Hunter",
        "hp": 34,
        "damage": 11,
        "speed": 2.7,
        "moveset": ["bolt_shot", "sidestep_slash", "dust_burst"],
        "ai": ai_trickster,
    },
    "iron_penitent": {
        "name": "Iron Penitent",
        "hp": 52,
        "damage": 8,
        "speed": 1.6,
        "moveset": ["shield_crush", "ground_stomp", "guard_counter"],
        "ai": ai_sentinel,
    },
    "hollow_vesper": {
        "name": "Hollow Vesper",
        "hp": 36,
        "damage": 10,
        "speed": 2.5,
        "moveset": ["wail_pulse", "soul_drain", "phase_lunge"],
        "ai": ai_trickster,
    },
}

MINIBOSSES = {
    "warden_malgor": {
        "name": "Warden Malgor",
        "hp": 190,
        "damage": 14,
        "speed": 2.2,
        "moveset": ["brand_slam", "prison_chain", "searing_roar", "iron_charge"],
        "ai": ai_sentinel,
    },
    "vexa_bloodscribe": {
        "name": "Vexa the Bloodscribe",
        "hp": 170,
        "damage": 16,
        "speed": 2.8,
        "moveset": ["hemorrhage_sigil", "blood_step", "scarlet_orb", "siphon_veil"],
        "ai": ai_trickster,
    },
    "the_hungering_judge": {
        "name": "The Hungering Judge",
        "hp": 210,
        "damage": 15,
        "speed": 2.0,
        "moveset": ["gavel_drop", "verdict_wave", "debt_collector", "maw_unbound"],
        "ai": ai_rusher,
    },
}

BOSSES = {
    "wrath": {
        "name": "Agramon, Sin of Wrath",
        "hp": 320,
        "damage": 21,
        "speed": 2.9,
        "moveset": ["hellcleave", "rage_storm", "meteor_rush", "berserker_howl", "ashfall_breaker"],
        "ai": ai_rusher,
    },
    "pride": {
        "name": "Seraphyx, Sin of Pride",
        "hp": 300,
        "damage": 20,
        "speed": 2.7,
        "moveset": ["mirror_lance", "commanding_gaze", "golden_fall", "imperial_feint", "throne_shatter"],
        "ai": ai_sentinel,
    },
    "envy": {
        "name": "Nhalia, Sin of Envy",
        "hp": 290,
        "damage": 19,
        "speed": 3.2,
        "moveset": ["stolen_edge", "echo_clone", "covetous_bind", "jealous_flurry", "identity_rupture"],
        "ai": ai_trickster,
    },
    "greed": {
        "name": "Midas Rex, Sin of Greed",
        "hp": 340,
        "damage": 18,
        "speed": 2.4,
        "moveset": ["coin_hail", "gilded_maw", "vault_crash", "taxation_aura", "debt_explosion"],
        "ai": ai_sentinel,
    },
    "lust": {
        "name": "Vespera, Sin of Lust",
        "hp": 280,
        "damage": 20,
        "speed": 3.4,
        "moveset": ["charm_lash", "velvet_step", "heartbreak_arc", "kiss_of_agony", "devour_desire"],
        "ai": ai_skirmisher,
    },
    "gluttony": {
        "name": "Gorath, Sin of Gluttony",
        "hp": 360,
        "damage": 22,
        "speed": 2.0,
        "moveset": ["feast_slam", "acid_belch", "hunger_pull", "gorge_roll", "insatiable_nova"],
        "ai": ai_rusher,
    },
    "sloth": {
        "name": "Moros, Sin of Sloth",
        "hp": 350,
        "damage": 19,
        "speed": 1.6,
        "moveset": ["time_mire", "drowsy_wave", "gravity_well", "dream_crush", "inevitable_fall"],
        "ai": ai_sentinel,
    },
}

SKILL_TREE = {
    "embers_of_will": {
        "name": "Embers of Will",
        "cost": 0,
        "requires": [],
        "effects": {"atk": 2},
    },
    "iron_resolve": {
        "name": "Iron Resolve",
        "cost": 1,
        "requires": ["embers_of_will"],
        "effects": {"defense": 1, "max_hp": 10, "hp": 10},
    },
    "executioners_oath": {
        "name": "Executioner's Oath",
        "cost": 1,
        "requires": ["embers_of_will"],
        "effects": {"atk": 4},
    },
    "wings_of_ash": {
        "name": "Wings of Ash",
        "cost": 2,
        "requires": ["iron_resolve"],
        "effects": {"max_jumps": 1, "speed": 0.8},
    },
    "bloodclock_focus": {
        "name": "Bloodclock Focus",
        "cost": 2,
        "requires": ["executioners_oath"],
        "effects": {"crit": 0.07},
    },
    "hellrunner_instinct": {
        "name": "Hellrunner Instinct",
        "cost": 2,
        "requires": ["iron_resolve", "executioners_oath"],
        "effects": {"speed": 1.2, "atk": 2},
    },
}


RANDOM_EVENTS = [
    {
        "name": "Soul Fountain",
        "text": "A cracked shrine floods you with stolen vitality.",
        "effect": lambda game: setattr(game.player.stats, "hp", min(game.player.stats.max_hp, game.player.stats.hp + 25)),
    },
    {
        "name": "Infernal Gambit",
        "text": "Trade blood for strength: +4 attack, -12 HP.",
        "effect": lambda game: (
            setattr(game.player.stats, "atk", game.player.stats.atk + 4),
            setattr(game.player.stats, "hp", max(1, game.player.stats.hp - 12)),
        ),
    },
    {
        "name": "Echo Market",
        "text": "A ghost merchant gifts an extra relic slot this descent.",
        "effect": lambda game: setattr(game.player.inventory, "capacity", game.player.inventory.capacity + 2),
    },
    {
        "name": "Chainstorm",
        "text": "The room writhes with chains; enemies on next wave are sturdier.",
        "effect": lambda game: [setattr(e, "hp", e.hp + 10) for e in game.enemies],
    },
]


UNIQUE_ITEMS = [
    {"name": "Emberfang Dagger", "rarity": "Common", "type": "Weapon", "effect": {"atk": 1}},
    {"name": "Coalguard Buckler", "rarity": "Common", "type": "Armor", "effect": {"defense": 1}},
    {"name": "Pilgrim's Jerkin", "rarity": "Common", "type": "Armor", "effect": {"max_hp": 6}},
    {"name": "Sootrunner Boots", "rarity": "Common", "type": "Charm", "effect": {"speed": 0.3}},
    {"name": "Cauter Salt", "rarity": "Common", "type": "Consumable", "effect": {"heal": 18}},
    {"name": "Ashen Band", "rarity": "Common", "type": "Charm", "effect": {"crit": 0.01}},
    {"name": "Mercy Flask", "rarity": "Common", "type": "Consumable", "effect": {"heal": 15}},
    {"name": "Scoria Charm", "rarity": "Common", "type": "Charm", "effect": {"atk": 1}},
    {"name": "Worn Sigil Plate", "rarity": "Common", "type": "Armor", "effect": {"defense": 1}},
    {"name": "Sinner's Thread", "rarity": "Common", "type": "Charm", "effect": {"max_hp": 4}},
    {"name": "Vessel of Cinders", "rarity": "Uncommon", "type": "Consumable", "effect": {"heal": 24}},
    {"name": "Torchbearer Axe", "rarity": "Uncommon", "type": "Weapon", "effect": {"atk": 2}},
    {"name": "Lava-vein Cuirass", "rarity": "Uncommon", "type": "Armor", "effect": {"defense": 2}},
    {"name": "Riftstep Sandals", "rarity": "Uncommon", "type": "Charm", "effect": {"speed": 0.4}},
    {"name": "Clockwork Talon", "rarity": "Uncommon", "type": "Weapon", "effect": {"crit": 0.02}},
    {"name": "Hexed Ribbon", "rarity": "Uncommon", "type": "Charm", "effect": {"atk": 2}},
    {"name": "Hellbloom Tea", "rarity": "Uncommon", "type": "Consumable", "effect": {"heal": 20}},
    {"name": "Shacklebreak Wraps", "rarity": "Uncommon", "type": "Armor", "effect": {"max_hp": 8}},
    {"name": "Furnace Eye", "rarity": "Uncommon", "type": "Charm", "effect": {"crit": 0.03}},
    {"name": "Brandsteel Pike", "rarity": "Uncommon", "type": "Weapon", "effect": {"atk": 3}},
    {"name": "Pyreheart Gem", "rarity": "Rare", "type": "Charm", "effect": {"atk": 2, "crit": 0.03}},
    {"name": "Aegis of the Fallen", "rarity": "Rare", "type": "Armor", "effect": {"defense": 3}},
    {"name": "Bonefire Tonic", "rarity": "Rare", "type": "Consumable", "effect": {"heal": 30}},
    {"name": "Gallows Hook", "rarity": "Rare", "type": "Weapon", "effect": {"atk": 4}},
    {"name": "Mournstep Anklet", "rarity": "Rare", "type": "Charm", "effect": {"speed": 0.6}},
    {"name": "Soulglass Circlet", "rarity": "Rare", "type": "Armor", "effect": {"max_hp": 12}},
    {"name": "Inferno Ledger", "rarity": "Rare", "type": "Charm", "effect": {"atk": 1, "defense": 1}},
    {"name": "Penance Hookblade", "rarity": "Rare", "type": "Weapon", "effect": {"atk": 5}},
    {"name": "Blood Ember Phial", "rarity": "Rare", "type": "Consumable", "effect": {"heal": 34}},
    {"name": "Wispbone Carapace", "rarity": "Rare", "type": "Armor", "effect": {"defense": 2, "max_hp": 6}},
    {"name": "Crown of Sparks", "rarity": "Epic", "type": "Charm", "effect": {"crit": 0.05}},
    {"name": "Hellsplitter", "rarity": "Epic", "type": "Weapon", "effect": {"atk": 6}},
    {"name": "Monolith Mail", "rarity": "Epic", "type": "Armor", "effect": {"defense": 4}},
    {"name": "Rune of Urgency", "rarity": "Epic", "type": "Charm", "effect": {"speed": 0.8}},
    {"name": "Ash Oracle Draught", "rarity": "Epic", "type": "Consumable", "effect": {"heal": 42}},
    {"name": "Stormchain Loop", "rarity": "Epic", "type": "Charm", "effect": {"atk": 3, "speed": 0.3}},
    {"name": "Ruinforged Grips", "rarity": "Epic", "type": "Armor", "effect": {"defense": 3, "max_hp": 8}},
    {"name": "Tyrant's Divider", "rarity": "Epic", "type": "Weapon", "effect": {"atk": 7}},
    {"name": "Sable Halo", "rarity": "Epic", "type": "Charm", "effect": {"crit": 0.04, "defense": 1}},
    {"name": "Eclipsed Ember", "rarity": "Epic", "type": "Consumable", "effect": {"heal": 46}},
    {"name": "Wrathscar Greatsword", "rarity": "Legendary", "type": "Weapon", "effect": {"atk": 9}},
    {"name": "Prideglass Mantle", "rarity": "Legendary", "type": "Armor", "effect": {"defense": 5, "max_hp": 10}},
    {"name": "Envy's Mirror Shard", "rarity": "Legendary", "type": "Charm", "effect": {"crit": 0.08}},
    {"name": "Greedcoil Ring", "rarity": "Legendary", "type": "Charm", "effect": {"atk": 4, "crit": 0.03}},
    {"name": "Lustfire Perfume", "rarity": "Legendary", "type": "Consumable", "effect": {"heal": 50}},
    {"name": "Glutton Mawplate", "rarity": "Legendary", "type": "Armor", "effect": {"max_hp": 18}},
    {"name": "Slothbound Hourglass", "rarity": "Legendary", "type": "Charm", "effect": {"defense": 2, "speed": 0.7}},
    {"name": "Thronebreaker Brand", "rarity": "Legendary", "type": "Weapon", "effect": {"atk": 10}},
    {"name": "Pandemonium Core", "rarity": "Legendary", "type": "Charm", "effect": {"atk": 3, "defense": 2}},
    {"name": "Ash Saint's Reliquary", "rarity": "Legendary", "type": "Consumable", "effect": {"heal": 60}},
    {"name": "Charred Oathblade", "rarity": "Mythic", "type": "Weapon", "effect": {"atk": 12}},
    {"name": "Abyssweave Vestment", "rarity": "Mythic", "type": "Armor", "effect": {"defense": 6, "max_hp": 12}},
    {"name": "Soulthief Signet", "rarity": "Mythic", "type": "Charm", "effect": {"crit": 0.1}},
    {"name": "Hellrunner Emblem", "rarity": "Mythic", "type": "Charm", "effect": {"speed": 1.1}},
    {"name": "Phoenix Blood Ampoule", "rarity": "Mythic", "type": "Consumable", "effect": {"heal": 70}},
    {"name": "Cataclysm Prism", "rarity": "Mythic", "type": "Charm", "effect": {"atk": 5, "crit": 0.04}},
    {"name": "Underking Pauldrons", "rarity": "Mythic", "type": "Armor", "effect": {"defense": 4, "max_hp": 16}},
    {"name": "Veilpiercer", "rarity": "Mythic", "type": "Weapon", "effect": {"atk": 11, "speed": 0.4}},
    {"name": "Dawnbound Catalyst", "rarity": "Mythic", "type": "Consumable", "effect": {"heal": 80}},
    {"name": "Crown of the Redeemed", "rarity": "Mythic", "type": "Charm", "effect": {"atk": 4, "defense": 2, "crit": 0.03}},
]
