from enum import Enum, auto


class StatOriginal(Enum):
    Invalid = -1
    Strength = 0
    Energy = auto()
    Dexterity = auto()
    Vitality = auto()
    StatPoints = auto()
    SkillPoints = auto()
    Life = auto()
    MaxLife = auto()
    Mana = auto()
    MaxMana = auto()
    Stamina = auto()
    MaxStamina = auto()
    Level = auto()
    Experience = auto()
    Gold = auto()
    StashGold = auto()
    EnhancedDefense = auto()
    EnhancedDamageMax = auto()
    EnhancedDamage = auto()
    AttackRating = auto()
    ChanceToBlock = auto()
    MinDamage = auto()
    MaxDamage = auto()
    TwoHandedMinDamage = auto()
    TwoHandedMaxDamage = auto()
    DamagePercent = auto()
    ManaRecovery = auto()
    ManaRecoveryBonus = auto()
    StaminaRecoveryBonus = auto()
    LastExp = auto()
    NextExp = auto()
    Defense = auto()
    DefenseVsMissiles = auto()
    DefenseVsHth = auto()
    NormalDamageReduction = auto()
    MagicDamageReduction = auto()
    DamageReduced = auto()
    MagicResist = auto()
    MaxMagicResist = auto()
    FireResist = auto()
    MaxFireResist = auto()
    LightningResist = auto()
    MaxLightningResist = auto()
    ColdResist = auto()
    MaxColdResist = auto()
    PoisonResist = auto()
    MaxPoisonResist = auto()
    DamageAura = auto()
    FireMinDamage = auto()
    FireMaxDamage = auto()
    LightningMinDamage = auto()
    LightningMaxDamage = auto()
    MagicMinDamage = auto()
    MagicMaxDamage = auto()
    ColdMinDamage = auto()
    ColdMaxDamage = auto()
    ColdLength = auto()
    PoisonMinDamage = auto()
    PoisonMaxDamage = auto()
    PoisonLength = auto()
    LifeSteal = auto()
    LifeStealMax = auto()
    ManaSteal = auto()
    ManaStealMax = auto()
    StaminaDrainMinDamage = auto()
    StaminaDrainMaxDamage = auto()
    StunLength = auto()
    VelocityPercent = auto()
    AttackRate = auto()
    OtherAnimRate = auto()
    Quantity = auto()
    Value = auto()
    Durability = auto()
    MaxDurability = auto()
    ReplenishLife = auto()
    MaxDurabilityPercent = auto()
    MaxLifePercent = auto()
    MaxManaPercent = auto()
    AttackerTakesDamage = auto()
    GoldFind = auto()
    MagicFind = auto()
    Knockback = auto()
    TimeDuration = auto()
    AddClassSkills = auto()
    Unused84 = auto()
    AddExperience = auto()
    LifeAfterEachKill = auto()
    ReducePrices = auto()
    DoubleHerbDuration = auto()
    LightRadius = auto()
    LightColor = auto()
    Requirements = auto()
    LevelRequire = auto()
    IncreasedAttackSpeed = auto()
    LevelRequirePercent = auto()
    LastBlockFrame = auto()
    FasterRunWalk = auto()
    NonClassSkill = auto()
    State = auto()
    FasterHitRecovery = auto()
    PlayerCount = auto()
    PoisonOverrideLength = auto()
    FasterBlockRate = auto()
    BypassUndead = auto()
    BypassDemons = auto()
    FasterCastRate = auto()
    BypassBeasts = auto()
    SingleSkill = auto()
    SlainMonstersRestInPeace = auto()
    CurseResistance = auto()
    PoisonLengthReduced = auto()
    NormalDamage = auto()
    HitCausesMonsterToFlee = auto()
    HitBlindsTarget = auto()
    DamageTakenGoesToMana = auto()
    IgnoreTargetsDefense = auto()
    TargetDefense = auto()
    PreventMonsterHeal = auto()
    HalfFreezeDuration = auto()
    AttackRatingPercent = auto()
    MonsterDefensePerHit = auto()
    DemonDamagePercent = auto()
    UndeadDamagePercent = auto()
    DemonAttackRating = auto()
    UndeadAttackRating = auto()
    Throwable = auto()
    FireSkills = auto()
    AllSkills = auto()
    AttackerTakesLightDamage = auto()
    IronMaidenLevel = auto()
    LifeTapLevel = auto()
    ThornsPercent = auto()
    BoneArmor = auto()
    BoneArmorMax = auto()
    FreezesTarget = auto()
    OpenWounds = auto()
    CrushingBlow = auto()
    KickDamage = auto()
    ManaAfterKill = auto()
    HealAfterDemonKill = auto()
    ExtraBlood = auto()
    DeadlyStrike = auto()
    AbsorbFirePercent = auto()
    AbsorbFire = auto()
    AbsorbLightningPercent = auto()
    AbsorbLightning = auto()
    AbsorbMagicPercent = auto()
    AbsorbMagic = auto()
    AbsorbColdPercent = auto()
    AbsorbCold = auto()
    SlowsTarget = auto()
    Aura = auto()
    Indestructible = auto()
    CannotBeFrozen = auto()
    SlowerStaminaDrain = auto()
    Reanimate = auto()
    Pierce = auto()
    MagicArrow = auto()
    ExplosiveArrow = auto()
    ThrowMinDamage = auto()
    ThrowMaxDamage = auto()
    SkillHandofAthena = auto()
    SkillStaminaPercent = auto()
    SkillPassiveStaminaPercent = auto()
    SkillConcentration = auto()
    SkillEnchant = auto()
    SkillPierce = auto()
    SkillConviction = auto()
    SkillChillingArmor = auto()
    SkillFrenzy = auto()
    SkillDecrepify = auto()
    SkillArmorPercent = auto()
    Alignment = auto()
    Target0 = auto()
    Target1 = auto()
    GoldLost = auto()
    ConverisonLevel = auto()
    ConverisonMaxHP = auto()
    UnitDooverlay = auto()
    AttackVsMonType = auto()
    DamageVsMonType = auto()
    Fade = auto()
    ArmorOverridePercent = auto()
    Unused183 = auto()
    Unused184 = auto()
    Unused185 = auto()
    Unused186 = auto()
    Unused187 = auto()
    AddSkillTab = auto()
    Unused189 = auto()
    Unused190 = auto()
    Unused191 = auto()
    Unused192 = auto()
    Unused193 = auto()
    NumSockets = auto()
    SkillOnAttack = auto()
    SkillOnKill = auto()
    SkillOnDeath = auto()
    SkillOnHit = auto()
    SkillOnLevelUp = auto()
    Unused200 = auto()
    SkillOnGetHit = auto()
    Unused202 = auto()
    Unused203 = auto()
    ItemChargedSkill = auto()
    Unused205 = auto()
    Unused206 = auto()
    Unused207 = auto()
    Unused208 = auto()
    Unused209 = auto()
    Unused210 = auto()
    Unused211 = auto()
    Unused212 = auto()
    Unused213 = auto()
    DefensePerLevel = auto()
    ArmorPercentPerLevel = auto()
    LifePerLevel = auto()
    ManaPerLevel = auto()
    MaxDamagePerLevel = auto()
    MaxDamagePercentPerLevel = auto()
    StrengthPerLevel = auto()
    DexterityPerLevel = auto()
    EnergyPerLevel = auto()
    VitalityPerLevel = auto()
    AttackRatingPerLevel = auto()
    AttackRatingPercentPerLevel = auto()
    ColdDamageMaxPerLevel = auto()
    FireDamageMaxPerLevel = auto()
    LightningDamageMaxPerLevel = auto()
    PoisonDamageMaxPerLevel = auto()
    ResistColdPerLevel = auto()
    ResistFirePerLevel = auto()
    ResistLightningPerLevel = auto()
    ResistPoisonPerLevel = auto()
    AbsorbColdPerLevel = auto()
    AbsorbFirePerLevel = auto()
    AbsorbLightningPerLevel = auto()
    AbsorbPoisonPerLevel = auto()
    ThornsPerLevel = auto()
    ExtraGoldPerLevel = auto()
    MagicFindPerLevel = auto()
    RegenStaminaPerLevel = auto()
    StaminaPerLevel = auto()
    DamageDemonPerLevel = auto()
    DamageUndeadPerLevel = auto()
    AttackRatingDemonPerLevel = auto()
    AttackRatingUndeadPerLevel = auto()
    CrushingBlowPerLevel = auto()
    OpenWoundsPerLevel = auto()
    KickDamagePerLevel = auto()
    DeadlyStrikePerLevel = auto()
    FindGemsPerLevel = auto()
    ReplenishDurability = auto()
    ReplenishQuantity = auto()
    ExtraStack = auto()
    FindItem = auto()
    SlashDamage = auto()
    SlashDamagePercent = auto()
    CrushDamage = auto()
    CrushDamagePercent = auto()
    ThrustDamage = auto()
    ThrustDamagePercent = auto()
    AbsorbSlash = auto()
    AbsorbCrush = auto()
    AbsorbThrust = auto()
    AbsorbSlashPercent = auto()
    AbsorbCrushPercent = auto()
    AbsorbThrustPercent = auto()
    ArmorByTime = auto()
    ArmorPercentByTime = auto()
    LifeByTime = auto()
    ManaByTime = auto()
    MaxDamageByTime = auto()
    MaxDamagePercentByTime = auto()
    StrengthByTime = auto()
    DexterityByTime = auto()
    EnergyByTime = auto()
    VitalityByTime = auto()
    AttackRatingByTime = auto()
    AttackRatingPercentByTime = auto()
    ColdDamageMaxByTime = auto()
    FireDamageMaxByTime = auto()
    LightningDamageMaxByTime = auto()
    PoisonDamageMaxByTime = auto()
    ResistColdByTime = auto()
    ResistFireByTime = auto()
    ResistLightningByTime = auto()
    ResistPoisonByTime = auto()
    AbsorbColdByTime = auto()
    AbsorbFireByTime = auto()
    AbsorbLightningByTime = auto()
    AbsorbPoisonByTime = auto()
    FindGoldByTime = auto()
    MagicFindByTime = auto()
    RegenStaminaByTime = auto()
    StaminaByTime = auto()
    DamageDemonByTime = auto()
    DamageUndeadByTime = auto()
    AttackRatingDemonByTime = auto()
    AttackRatingUndeadByTime = auto()
    CrushingBlowByTime = auto()
    OpenWoundsByTime = auto()
    KickDamageByTime = auto()
    DeadlyStrikeByTime = auto()
    FindGemsByTime = auto()
    PierceCold = auto()
    PierceFire = auto()
    PierceLightning = auto()
    PiercePoison = auto()
    DamageVsMonster = auto()
    DamagePercentVsMonster = auto()
    AttackRatingVsMonster = auto()
    AttackRatingPercentVsMonster = auto()
    AcVsMonster = auto()
    AcPercentVsMonster = auto()
    FireLength = auto()
    BurningMin = auto()
    BurningMax = auto()
    ProgressiveDamage = auto()
    ProgressiveSteal = auto()
    ProgressiveOther = auto()
    ProgressiveFire = auto()
    ProgressiveCold = auto()
    ProgressiveLightning = auto()
    ExtraCharges = auto()
    ProgressiveAttackRating = auto()
    PoisonCount = auto()
    DamageFrameRate = auto()
    PierceIdx = auto()
    FireSkillDamage = auto()
    LightningSkillDamage = auto()
    ColdSkillDamage = auto()
    PoisonSkillDamage = auto()
    EnemyFireResist = auto()
    EnemyLightningResist = auto()
    EnemyColdResist = auto()
    EnemyPoisonResist = auto()
    PassiveCriticalStrike = auto()
    PassiveDodge = auto()
    PassiveAvoid = auto()
    PassiveEvade = auto()
    PassiveWarmth = auto()
    PassiveMasteryMeleeAttackRating = auto()
    PassiveMasteryMeleeDamage = auto()
    PassiveMasteryMeleeCritical = auto()
    PassiveMasteryThrowAttackRating = auto()
    PassiveMasteryThrowDamage = auto()
    PassiveMasteryThrowCritical = auto()
    PassiveWeaponBlock = auto()
    SummonResist = auto()
    ModifierListSkill = auto()
    ModifierListLevel = auto()
    LastSentHPPercent = auto()
    SourceUnitType = auto()
    SourceUnitID = auto()
    ShortParam1 = auto()
    QuestItemDifficulty = auto()
    PassiveMagicMastery = auto()
    PassiveMagicPierce = auto()


descpriority = {
    "item_armor_bytime": 180,
    "item_armorpercent_bytime": 180,
    "item_hp_bytime": 180,
    "item_mana_bytime": 180,
    "item_maxdamage_bytime": 180,
    "item_maxdamage_percent_bytime": 180,
    "item_strength_bytime": 180,
    "item_dexterity_bytime": 180,
    "item_energy_bytime": 180,
    "item_vitality_bytime": 180,
    "item_tohit_bytime": 180,
    "item_tohitpercent_bytime": 180,
    "item_cold_damagemax_bytime": 180,
    "item_fire_damagemax_bytime": 180,
    "item_ltng_damagemax_bytime": 180,
    "item_pois_damagemax_bytime": 180,
    "item_resist_cold_bytime": 180,
    "item_resist_fire_bytime": 180,
    "item_resist_ltng_bytime": 180,
    "item_resist_pois_bytime": 180,
    "item_absorb_cold_bytime": 180,
    "item_absorb_fire_bytime": 180,
    "item_absorb_ltng_bytime": 180,
    "item_find_gold_bytime": 180,
    "item_find_magic_bytime": 180,
    "item_regenstamina_bytime": 180,
    "item_stamina_bytime": 180,
    "item_damage_demon_bytime": 180,
    "item_damage_undead_bytime": 180,
    "item_tohit_demon_bytime": 180,
    "item_tohit_undead_bytime": 180,
    "item_crushingblow_bytime": 180,
    "item_openwounds_bytime": 180,
    "item_kick_damage_bytime": 180,
    "item_deadlystrike_bytime": 180,
    "item_indesctructible": 160,
    "item_skillonattack	": 60,
    "item_skillonkill": 160,
    "item_skillondeath": 160,
    "item_skillonhit": 160,
    "item_skillonlevelup": 160,
    "item_skillongethit": 160,
    "item_aura": 159,
    "item_charge_noconsume": 159,
    "item_allskills": 158,
    "item_elemskill": 157,
    "item_addskill_tab": 151,
    "item_addclassskills": 150,
    "item_fastermovevelocity": 148,
    "item_fasterattackrate": 145,
    "item_fastercastrate": 142,
    "item_fastergethitrate": 139,
    "item_fasterblockrate": 136,
    "toblock": 134,
    "item_explosivearrow": 133,
    "item_pierc": 132,
    "item_magicarrow": 131,
    "item_mindamage_percent": 130,
    "item_maxdamage_percent": 129,
    "item_maxdamage_percent_perlevel": 128,
    "mindamage": 127,
    "maxdamage": 126,
    "item_maxdamage_perlevel": 125,
    "secondary_mindamage": 124,
    "secondary_maxdamage": 123,
    "item_normaldamage": 122,
    "item_kickdamage": 121,
    "item_kick_damage_perlevel": 120,
    "item_ignoretargetac": 119,
    "item_fractionaltargetac": 118,
    "item_tohit_percent": 117,
    "item_tohitpercent_perlevel": 116,
    "tohit": 115,
    "item_tohit_perlevel": 114,
    "item_demondamage_percent": 112,
    "item_damage_demon_perlevel": 111,
    "item_demon_tohit": 110,
    "item_tohit_demon_perlevel": 109,
    "item_undeaddamage_percent": 108,
    "attack_vs_montype": 108,
    "item_damage_undead_perlevel": 107,
    "item_undead_tohit": 106,
    "damage_vs_montype": 106,
    "item_tohit_undead_perlevel": 105,
    "magicmindam": 104,
    "magicmaxdam": 103,
    "firemindam": 102,
    "firemaxdam": 101,
    "item_pierce_cold_immunity": 100,
    "item_pierce_fire_immunity": 100,
    "item_pierce_light_immunity": 100,
    "item_pierce_poison_immunity": 100,
    "item_pierce_damage_immunity": 100,
    "item_pierce_magic_immunity": 100,
    "item_fire_damagemax_perlevel": 100,
    "lightmindam": 99,
    "lightmaxdam": 98,
    "item_ltng_damagemax_perlevel": 97,
    "coldmindam": 96,
    "coldmaxdam": 95,
    "item_cold_damagemax_perlevel": 94,
    "poisonmindam": 92,
    "poisonmaxdam": 91,
    "item_pois_damagemax_perlevel": 90,
    "manadrainmindam": 89,
    "lifedrainmindam": 88,
    "item_pierce_cold": 88,
    "item_pierce_fire": 88,
    "item_pierce_ltng": 88,
    "item_pierce_pois": 88,
    "passive_fire_mastery": 88,
    "passive_ltng_mastery": 88,
    "passive_cold_mastery": 88,
    "passive_pois_mastery": 88,
    "passive_fire_pierce": 88,
    "passive_ltng_pierce": 88,
    "passive_cold_pierce": 88,
    "passive_pois_pierce": 88,
    "item_crushingblow": 87,
    "item_crushingblow_perlevel": 86,
    "item_deadlystrike": 85,
    "item_deadlystrike_perlevel": 84,
    "item_openwounds": 83,
    "item_openwounds_perlevel": 82,
    "item_nonclassskill": 81,
    "item_singleskill": 81,
    "item_restinpeace": 81,
    "item_preventheal": 81,
    "item_stupidity": 80,
    "item_howl": 79,
    "item_freeze": 78,
    "item_slow": 77,
    "item_knockback": 76,
    "item_damagetargetac": 75,
    "item_armor_percent": 74,
    "item_armorpercent_perlevel": 73,
    "item_armor_perlevel": 72,
    "armorclass": 71,
    "armorclass_vs_hth": 70,
    "armorclass_vs_missile": 69,
    "strength": 67,
    "item_strength_perlevel": 66,
    "dexterity": 65,
    "item_dexterity_perlevel": 64,
    "vitality": 63,
    "item_vitality_perlevel": 62,
    "energy": 61,
    "item_energy_perlevel": 60,
    "maxhp": 59,
    "item_maxhp_percent": 58,
    "item_hp_perlevel": 57,
    "hpregen": 56,
    "maxmana": 55,
    "item_maxmana_percent": 54,
    "item_mana_perlevel": 53,
    "manarecoverybonus": 52,
    "maxstamina": 51,
    "item_stamina_perlevel": 50,
    "item_staminadrainpct": 49,
    "staminarecoverybonus": 48,
    "item_regenstamina_perlevel": 47,
    "maxmagicresist": 46,
    "maxpoisonresist": 45,
    "maxcoldresist": 44,
    "maxlightresist": 43,
    "maxfireresist": 42,
    "magicresist": 41,
    "coldresist": 40,
    "item_resist_cold_perlevel": 39,
    "lightresist": 38,
    "item_resist_ltng_perlevel": 37,
    "fireresist": 36,
    "item_resist_fire_perlevel": 35,
    "poisonresist": 34,
    "item_absorbmagic": 33,
    "item_resist_pois_perlevel": 33,
    "item_absorb_cold_perlevel": 32,
    "item_absorbcold": 31,
    "item_absorb_ltng_perlevel": 30,
    "item_absorblight": 29,
    "item_absorb_fire_perlevel": 28,
    "item_absorbfire": 27,
    "item_absorbmagic_percent": 26,
    "item_absorbcold_percent": 25,
    "item_absorblight_percent": 24,
    "item_absorbfire_percent": 23,
    "normal_damage_reduction": 22,
    "damageresist": 22,
    "magic_damage_reduction": 21,
    "item_cannotbefrozen": 20,
    "item_halffreezeduration": 19,
    "item_poisonlengthresist": 18,
    "item_reanimate": 17,
    "item_healafterkill": 16,
    "item_manaafterkill": 16,
    "item_healafterdemonkill": 15,
    "item_attackertakeslightdamage": 14,
    "item_attackertakesdamage": 13,
    "item_thorns_perlevel": 12,
    "item_addexperience": 11,
    "item_damagetomana": 11,
    "item_goldbonus": 10,
    "item_find_gold_perlevel": 9,
    "item_magicbonus": 8,
    "item_reducedprices": 8,
    "item_find_magic_perlevel": 7,
    "item_lightradius": 6,
    "item_throwable": 5,
    "item_noconsume": 4,
    "item_extra_stack": 4,
    "item_maxdurability_percent": 3,
    "item_replenish_quantity": 2,
    "item_charged_skill": 1,
    "item_replenish_durability": 1,
    "item_req_percent": 0,
}


class StatOriginal(Enum):
    invalid = -1
    strength = 0
    energy = auto()
    dexterity = auto()
    vitality = auto()
    statpts = auto()
    newskills = auto()
    hitpoints = auto()
    maxhp = auto()
    mana = auto()
    maxmana = auto()
    stamina = auto()
    maxstamina = auto()
    level = auto()
    experience = auto()
    gold = auto()
    goldbank = auto()
    item_armor_percent = auto()
    item_maxdamage_percent = auto()
    item_mindamage_percent = auto()
    tohit = auto()
    toblock = auto()
    mindamage = auto()
    maxdamage = auto()
    secondary_mindamage = auto()
    secondary_maxdamage = auto()
    damagepercent = auto()
    manarecovery = auto()
    manarecoverybonus = auto()
    staminarecoverybonus = auto()
    lastexp = auto()
    nextexp = auto()
    armorclass = auto()
    armorclass_vs_missile = auto()
    armorclass_vs_hth = auto()
    normal_damage_reduction = auto()
    magic_damage_reduction = auto()
    damageresist = auto()
    magicresist = auto()
    maxmagicresist = auto()
    fireresist = auto()
    maxfireresist = auto()
    lightresist = auto()
    maxlightresist = auto()
    coldresist = auto()
    maxcoldresist = auto()
    poisonresist = auto()
    maxpoisonresist = auto()
    damageaura = auto()
    firemindam = auto()
    firemaxdam = auto()
    lightmindam = auto()
    lightmaxdam = auto()
    magicmindam = auto()
    magicmaxdam = auto()
    coldmindam = auto()
    coldmaxdam = auto()
    coldlength = auto()
    poisonmindam = auto()
    poisonmaxdam = auto()
    poisonlength = auto()
    lifedrainmindam = auto()
    lifedrainmaxdam = auto()
    manadrainmindam = auto()
    manadrainmaxdam = auto()
    stamdrainmindam = auto()
    stamdrainmaxdam = auto()
    stunlength = auto()
    velocitypercent = auto()
    attackrate = auto()
    other_animrate = auto()
    quantity = auto()
    value = auto()
    durability = auto()
    maxdurability = auto()
    hpregen = auto()
    item_maxdurability_percent = auto()
    item_maxhp_percent = auto()
    item_maxmana_percent = auto()
    item_attackertakesdamage = auto()
    item_goldbonus = auto()
    item_magicbonus = auto()
    item_knockback = auto()
    item_timeduration = auto()
    item_addclassskills = auto()
    unsentparam1 = auto()
    item_addexperience = auto()
    item_healafterkill = auto()
    item_reducedprices = auto()
    item_doubleherbduration = auto()
    item_lightradius = auto()
    item_lightcolor = auto()
    item_req_percent = auto()
    item_levelreq = auto()
    item_fasterattackrate = auto()
    item_levelreqpct = auto()
    lastblockframe = auto()
    item_fastermovevelocity = auto()
    item_nonclassskill = auto()
    state = auto()
    item_fastergethitrate = auto()
    monster_playercount = auto()
    skill_poison_override_length = auto()
    item_fasterblockrate = auto()
    skill_bypass_undead = auto()
    skill_bypass_demons = auto()
    item_fastercastrate = auto()
    skill_bypass_beasts = auto()
    item_singleskill = auto()
    item_restinpeace = auto()
    curse_resistance = auto()
    item_poisonlengthresist = auto()
    item_normaldamage = auto()
    item_howl = auto()
    item_stupidity = auto()
    item_damagetomana = auto()
    item_ignoretargetac = auto()
    item_fractionaltargetac = auto()
    item_preventheal = auto()
    item_halffreezeduration = auto()
    item_tohit_percent = auto()
    item_damagetargetac = auto()
    item_demondamage_percent = auto()
    item_undeaddamage_percent = auto()
    item_demon_tohit = auto()
    item_undead_tohit = auto()
    item_throwable = auto()
    item_elemskill = auto()
    item_allskills = auto()
    item_attackertakeslightdamage = auto()
    ironmaiden_level = auto()
    lifetap_level = auto()
    thorns_percent = auto()
    bonearmor = auto()
    bonearmormax = auto()
    item_freeze = auto()
    item_openwounds = auto()
    item_crushingblow = auto()
    item_kickdamage = auto()
    item_manaafterkill = auto()
    item_healafterdemonkill = auto()
    item_extrablood = auto()
    item_deadlystrike = auto()
    item_absorbfire_percent = auto()
    item_absorbfire = auto()
    item_absorblight_percent = auto()
    item_absorblight = auto()
    item_absorbmagic_percent = auto()
    item_absorbmagic = auto()
    item_absorbcold_percent = auto()
    item_absorbcold = auto()
    item_slow = auto()
    item_aura = auto()
    item_indesctructible = auto()
    item_cannotbefrozen = auto()
    item_staminadrainpct = auto()
    item_reanimate = auto()
    item_pierce = auto()
    item_magicarrow = auto()
    item_explosivearrow = auto()
    item_throw_mindamage = auto()
    item_throw_maxdamage = auto()
    skill_handofathena = auto()
    skill_staminapercent = auto()
    skill_passive_staminapercent = auto()
    skill_concentration = auto()
    skill_enchant = auto()
    skill_pierce = auto()
    skill_conviction = auto()
    skill_chillingarmor = auto()
    skill_frenzy = auto()
    skill_decrepify = auto()
    skill_armor_percent = auto()
    alignment = auto()
    target0 = auto()
    target1 = auto()
    goldlost = auto()
    conversion_level = auto()
    conversion_maxhp = auto()
    unit_dooverlay = auto()
    attack_vs_montype = auto()
    damage_vs_montype = auto()
    fade = auto()
    armor_override_percent = auto()
    lasthitreactframe = auto()
    create_season = auto()
    bonus_mindamage = auto()
    bonus_maxdamage = auto()
    item_pierce_cold_immunity = auto()
    item_addskill_tab = auto()
    item_pierce_fire_immunity = auto()
    item_pierce_light_immunity = auto()
    item_pierce_poison_immunity = auto()
    item_pierce_damage_immunity = auto()
    item_pierce_magic_immunity = auto()
    item_numsockets = auto()
    item_skillonattack = auto()
    item_skillonkill = auto()
    item_skillondeath = auto()
    item_skillonhit = auto()
    item_skillonlevelup = auto()
    item_charge_noconsume = auto()
    item_skillongethit = auto()
    modifierlist_castid = auto()
    unused203 = auto()
    item_charged_skill = auto()
    item_noconsume = auto()
    passive_mastery_noconsume = auto()
    passive_mastery_replenish_oncrit = auto()
    unused208 = auto()
    unused209 = auto()
    unused210 = auto()
    unused211 = auto()
    passive_mastery_gethit_rate = auto()
    passive_mastery_attack_speed = auto()
    item_armor_perlevel = auto()
    item_armorpercent_perlevel = auto()
    item_hp_perlevel = auto()
    item_mana_perlevel = auto()
    item_maxdamage_perlevel = auto()
    item_maxdamage_percent_perlevel = auto()
    item_strength_perlevel = auto()
    item_dexterity_perlevel = auto()
    item_energy_perlevel = auto()
    item_vitality_perlevel = auto()
    item_tohit_perlevel = auto()
    item_tohitpercent_perlevel = auto()
    item_cold_damagemax_perlevel = auto()
    item_fire_damagemax_perlevel = auto()
    item_ltng_damagemax_perlevel = auto()
    item_pois_damagemax_perlevel = auto()
    item_resist_cold_perlevel = auto()
    item_resist_fire_perlevel = auto()
    item_resist_ltng_perlevel = auto()
    item_resist_pois_perlevel = auto()
    item_absorb_cold_perlevel = auto()
    item_absorb_fire_perlevel = auto()
    item_absorb_ltng_perlevel = auto()
    item_absorb_pois_perlevel = auto()
    item_thorns_perlevel = auto()
    item_find_gold_perlevel = auto()
    item_find_magic_perlevel = auto()
    item_regenstamina_perlevel = auto()
    item_stamina_perlevel = auto()
    item_damage_demon_perlevel = auto()
    item_damage_undead_perlevel = auto()
    item_tohit_demon_perlevel = auto()
    item_tohit_undead_perlevel = auto()
    item_crushingblow_perlevel = auto()
    item_openwounds_perlevel = auto()
    item_kick_damage_perlevel = auto()
    item_deadlystrike_perlevel = auto()
    item_find_gems_perlevel = auto()
    item_replenish_durability = auto()
    item_replenish_quantity = auto()
    item_extra_stack = auto()
    item_find_item = auto()
    item_slash_damage = auto()
    item_slash_damage_percent = auto()
    item_crush_damage = auto()
    item_crush_damage_percent = auto()
    item_thrust_damage = auto()
    item_thrust_damage_percent = auto()
    item_absorb_slash = auto()
    item_absorb_crush = auto()
    item_absorb_thrust = auto()
    item_absorb_slash_percent = auto()
    item_absorb_crush_percent = auto()
    item_absorb_thrust_percent = auto()
    item_armor_bytime = auto()
    item_armorpercent_bytime = auto()
    item_hp_bytime = auto()
    item_mana_bytime = auto()
    item_maxdamage_bytime = auto()
    item_maxdamage_percent_bytime = auto()
    item_strength_bytime = auto()
    item_dexterity_bytime = auto()
    item_energy_bytime = auto()
    item_vitality_bytime = auto()
    item_tohit_bytime = auto()
    item_tohitpercent_bytime = auto()
    item_cold_damagemax_bytime = auto()
    item_fire_damagemax_bytime = auto()
    item_ltng_damagemax_bytime = auto()
    item_pois_damagemax_bytime = auto()
    item_resist_cold_bytime = auto()
    item_resist_fire_bytime = auto()
    item_resist_ltng_bytime = auto()
    item_resist_pois_bytime = auto()
    item_absorb_cold_bytime = auto()
    item_absorb_fire_bytime = auto()
    item_absorb_ltng_bytime = auto()
    item_absorb_pois_bytime = auto()
    item_find_gold_bytime = auto()
    item_find_magic_bytime = auto()
    item_regenstamina_bytime = auto()
    item_stamina_bytime = auto()
    item_damage_demon_bytime = auto()
    item_damage_undead_bytime = auto()
    item_tohit_demon_bytime = auto()
    item_tohit_undead_bytime = auto()
    item_crushingblow_bytime = auto()
    item_openwounds_bytime = auto()
    item_kick_damage_bytime = auto()
    item_deadlystrike_bytime = auto()
    item_find_gems_bytime = auto()
    item_pierce_cold = auto()
    item_pierce_fire = auto()
    item_pierce_ltng = auto()
    item_pierce_pois = auto()
    item_damage_vs_monster = auto()
    item_damage_percent_vs_monster = auto()
    item_tohit_vs_monster = auto()
    item_tohit_percent_vs_monster = auto()
    item_ac_vs_monster = auto()
    item_ac_percent_vs_monster = auto()
    firelength = auto()
    burningmin = auto()
    burningmax = auto()
    progressive_damage = auto()
    progressive_steal = auto()
    progressive_other = auto()
    progressive_fire = auto()
    progressive_cold = auto()
    progressive_lightning = auto()
    item_extra_charges = auto()
    progressive_tohit = auto()
    poison_count = auto()
    damage_framerate = auto()
    pierce_idx = auto()
    passive_fire_mastery = auto()
    passive_ltng_mastery = auto()
    passive_cold_mastery = auto()
    passive_pois_mastery = auto()
    passive_fire_pierce = auto()
    passive_ltng_pierce = auto()
    passive_cold_pierce = auto()
    passive_pois_pierce = auto()
    passive_critical_strike = auto()
    passive_dodge = auto()
    passive_avoid = auto()
    passive_evade = auto()
    passive_warmth = auto()
    passive_mastery_melee_th = auto()
    passive_mastery_melee_dmg = auto()
    passive_mastery_melee_crit = auto()
    passive_mastery_throw_th = auto()
    passive_mastery_throw_dmg = auto()
    passive_mastery_throw_crit = auto()
    passive_weaponblock = auto()
    passive_summon_resist = auto()
    modifierlist_skill = auto()
    modifierlist_level = auto()
    last_sent_hp_pct = auto()
    source_unit_type = auto()
    source_unit_id = auto()
    shortparam1 = auto()
    questitemdifficulty = auto()
    passive_mag_mastery = auto()
    passive_mag_pierce = auto()
    skill_cooldown = auto()
    skill_missile_damage_scale = auto()

    def priority(self):
        if self.name not in descpriority:
            return -1
        return descpriority[self.name]
