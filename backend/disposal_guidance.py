"""Catalog of waste items. The AI (CLIP) picks the closest item below by comparing
the photo with each item's text description ("prompt").

For every item we store: waste type (dry / wet / hazardous ...), whether it is
recyclable, HOW to prepare/dispose of it and WHERE to take it.
This is general advice - rules differ by city, so always check locally.
"""

LOCAL_NOTE = "Rules differ by city - check with your local municipal body or ward office."

RECYCLE_TEXT = {
    True: "Yes, this is recyclable.",
    "limited": "Only partly recyclable - many places do not accept it.",
    False: "No, this is not recyclable.",
}

DRY_BIN = "Dry-waste bin (usually the blue bin), or hand it to your municipal dry-waste collector"
SCRAP = "a local scrap dealer (kabadiwala) or recycling centre"
EWASTE_POINT = "an authorised e-waste collection centre or a store take-back programme"

ITEMS = {}


def item(key, name, prompt, wtype, recyclable, icon, how, where, warning=None, extra=""):
    ITEMS[key] = dict(name=name, prompt=prompt, waste_type=wtype, recyclable=recyclable,
                      icon=icon, how=how, where=where, warning=warning, extra=extra)


# ---- Dry, recyclable ----
item("plastic_bottle", "Plastic bottle", "a plastic bottle", "Dry waste", True, "🧴",
     "Empty it, rinse it, crush it and put the cap back on.", f"{DRY_BIN}, or {SCRAP}.",
     extra="PET bottles (water, soft drinks) are widely recycled into fibre and new containers.")
item("plastic_container", "Plastic container or tub", "a plastic food container or tub", "Dry waste", True, "🥡",
     "Wash off food, let it dry, and keep the lid separate if it is a different plastic.", f"{DRY_BIN}, or {SCRAP}.",
     extra="Check the recycling number: 1, 2 and 5 are the most widely accepted.")
item("paper", "Paper / newspaper", "paper, newspaper or a magazine", "Dry waste", True, "📄",
     "Keep it dry and clean. Remove plastic covers and spiral bindings.", f"{DRY_BIN}, or {SCRAP} (they usually pay for paper).",
     extra="Greasy, wet or heavily soiled paper cannot be recycled.")
item("cardboard", "Cardboard", "a cardboard box", "Dry waste", True, "📦",
     "Remove tape and labels, flatten the box and keep it dry.", f"{DRY_BIN}, or {SCRAP}.",
     extra="Food-soaked cardboard (like pizza boxes) usually cannot be recycled.")
item("glass_bottle", "Glass bottle or jar", "a glass bottle or glass jar", "Dry waste", True, "🍾",
     "Empty and rinse it. Do not mix it with broken glass or ceramics.", f"Glass collection point, {SCRAP}, or the dry-waste collector.",
     warning="If the glass is chipped or cracked, wrap it in thick paper before disposal.",
     extra="Glass can be recycled again and again.")
item("metal_can", "Metal can or tin", "a metal drink can or food tin can", "Dry waste", True, "🥫",
     "Empty and rinse it. Crush it to save space.", f"{DRY_BIN}, or {SCRAP}.",
     warning="Sharp lids can cut: press the lid inside the can.",
     extra="Aluminium and steel can be recycled many times.")
item("aluminium_foil", "Aluminium foil", "crumpled aluminium foil", "Dry waste", True, "🪙",
     "Wipe off food. Scrunch clean foil into a ball so it does not blow away.", f"{DRY_BIN}, or {SCRAP}.",
     extra="Only clean foil is accepted.")
item("scrap_metal", "Scrap metal", "scrap metal, a metal rod, or an old iron tool", "Dry waste", True, "🔩",
     "Keep it separate from other waste.", f"{SCRAP} - metal has good resale value.")

# ---- Dry, limited or not recyclable ----
item("plastic_bag", "Plastic bag / wrapper", "a plastic bag, plastic wrapper or chips packet", "Dry waste", "limited", "🛍️",
     "Reuse bags as much as possible. Keep thin plastic dry and clean and collect it separately.",
     "Dry-waste collector (some cities have special plastic-film collection).",
     extra="Multi-layer snack wrappers are usually not recycled.")
item("carton", "Juice / milk carton", "a tetra pak juice or milk carton", "Dry waste", "limited", "🧃",
     "Rinse, flatten and let it dry.", f"{DRY_BIN}. Only some recyclers accept cartons.",
     extra="Cartons are layers of paper, plastic and foil, which need special recycling.")
item("disposable_cup", "Disposable cup", "a paper cup or disposable coffee cup", "Dry waste", "limited", "🥤",
     "Empty it and keep the lid separate.", f"{DRY_BIN}. Most paper cups have a plastic lining and are hard to recycle.")
item("thermocol", "Thermocol / Styrofoam", "styrofoam or thermocol packaging", "Dry waste", False, "📦",
     "Do not burn it. Reuse as packing material if possible.", "General dry-waste collection.",
     extra="It breaks into small pieces and is rarely accepted.")
item("tissue", "Used tissue", "used tissue paper or paper napkins", "Dry waste", False, "🧻",
     "Wrap and place in the general bin.", "General (reject) waste bin.")
item("ceramic", "Broken ceramic / crockery", "broken ceramic, crockery or a broken mug", "Dry waste", False, "🏺",
     "Wrap sharp pieces in thick paper before throwing.", "General (reject) waste bin - not with glass recycling.",
     warning="Sharp pieces can injure waste workers. Wrap them well.")
item("broken_glass", "Broken glass", "broken glass pieces", "Dry waste", False, "⚠️",
     "Wrap in thick paper or cardboard, tape it, and write 'Broken glass' on it.", "General dry-waste bin, clearly labelled.",
     warning="Wear gloves. Never put loose broken glass in a bag that workers will handle.")

# ---- Wet / organic ----
item("food_waste", "Food waste", "leftover cooked food or food scraps", "Wet waste", False, "🍛",
     "Drain extra liquid. Do not wrap it in plastic bags.", "Wet-waste bin (usually the green bin) or home compost / community compost pit.",
     extra="It can be composted into manure instead.")
item("peels", "Fruit / vegetable peels", "fruit peels, vegetable scraps and peels", "Wet waste", False, "🍌",
     "Keep it free of plastic and stickers.", "Wet-waste bin or home compost.",
     extra="It composts well instead.")
item("garden", "Leaves / garden waste", "dry leaves, flowers and garden waste", "Wet waste", False, "🍃",
     "Collect it separately from other waste.", "Compost pit or the garden-waste collection in your area.",
     extra="It makes good compost or mulch instead.")

# ---- Hazardous / e-waste / sanitary ----
item("battery", "Battery", "a used battery", "Hazardous waste", True, "🔋",
     "Do not throw it in any bin. Tape the ends of lithium batteries.", f"A battery collection box at shops or {EWASTE_POINT}.",
     warning="Batteries can leak toxic chemicals and cause fires.",
     extra="Metals in batteries can be recovered by authorised recyclers only.")
item("ewaste", "Electronic item / e-waste", "an old mobile phone, charger, cables or electronic device", "E-waste", True, "📱",
     "Remove the battery if possible. Wipe your personal data from phones and laptops.", f"{EWASTE_POINT}.",
     warning="Never burn or break electronics. Never give e-waste to the regular dry-waste collector.",
     extra="Only authorised recyclers can safely recover its metals.")
item("bulb", "Bulb / tube light", "a light bulb or tube light", "Hazardous waste", "limited", "💡",
     "Wrap it carefully so it does not break.", f"{EWASTE_POINT} (CFL and tube lights contain mercury).",
     warning="CFL and tube lights contain mercury: do not break them.")
item("medicine", "Medicines / strips", "medicine tablets, strips or syrup bottles", "Hazardous waste", False, "💊",
     "Keep them in a sealed pouch and do not flush them.", "Pharmacy take-back or the biomedical-waste collection if available.",
     warning="Keep away from children and animals.")
item("sanitary", "Sanitary pad / diaper", "a sanitary napkin or baby diaper", "Sanitary waste", False, "🩹",
     "Wrap in newspaper or a pouch and mark it (a red dot or 'sanitary').", "Separate sanitary-waste collection or the general reject bin.",
     warning="Never mix it with recyclable dry waste.")
item("chemical", "Paint / chemical container", "a paint can or chemical bottle", "Hazardous waste", False, "🧪",
     "Keep it sealed and in the original container.", "Hazardous-waste collection drive or authorised facility.",
     warning="Do not pour chemicals down the drain or into the soil.")

# ---- Reuse / other ----
item("clothes", "Clothes / textiles", "old clothes or fabric", "Dry waste", "limited", "👕",
     "Wash them. Donate wearable clothes and cut worn-out ones into cleaning rags.", "NGO or clothes donation drive, or a textile recycler.",
     extra="Reuse is better than recycling.")
item("shoes", "Shoes / footwear", "old shoes or slippers", "Dry waste", "limited", "👟",
     "Clean them. Donate pairs that are still usable.", "NGO or donation drive; otherwise the dry-waste collector.",
     extra="Reuse is better than recycling.")

# ---- Special cases ----
item("mixed_pile", "Mixed waste pile", "a pile of mixed garbage and rubbish", "Mixed waste", None, "🗑️",
     "This looks like several kinds of waste together. Separate it into dry, wet and hazardous items first.",
     "Re-upload each item separately for specific guidance.",
     warning="Mixed waste cannot be recycled. Separating at home is the most useful step.")
item("not_waste", "Not a waste item", "a person, an animal, a room or a landscape", "None", None, "🙂",
     "This photo does not look like a waste item.", "Upload a clear photo of one item.")


def labels():
    """Keys and prompts in a fixed order for the AI model."""
    keys = list(ITEMS)
    return keys, [f"a photo of {ITEMS[k]['prompt']}" for k in keys]


def name_of(key):
    return ITEMS[key]["name"] if key in ITEMS else key


UNCERTAIN = {
    "title": "Not sure", "icon": "❓", "recyclable": None, "waste_type": "Unknown",
    "explanation": "The model is not confident enough to give a reliable answer.",
    "disposal": "Try a clearer photo: one item, good light, plain background.",
    "recycling": "When in doubt, do not put it in the recycling bin - wrong items can contaminate a whole batch.",
    "where": "Check your local recycling guide or ask your municipal waste collector.",
    "warning": "If the item could be hazardous (battery, chemicals, sharp or broken glass), treat it as hazardous waste.",
}


def get_guidance(key, uncertain=False):
    """Return advice for an item key. Unknown keys are treated as uncertain."""
    it = None if uncertain else ITEMS.get(key)
    if it is None or key == "not_waste":
        data = dict(UNCERTAIN)
        if key == "not_waste" and not uncertain:
            data["explanation"] = "This photo does not look like a waste item."
    else:
        rec = RECYCLE_TEXT.get(it["recyclable"], "Recyclability depends on the items.")
        data = {
            "title": it["name"], "icon": it["icon"], "recyclable": it["recyclable"],
            "waste_type": it["waste_type"],
            "explanation": f"The photo looks most like: {it['name'].lower()}.",
            "disposal": it["how"], "recycling": (rec + " " + it["extra"]).strip(),
            "where": it["where"], "warning": it["warning"],
        }
    return {**data, "local_note": LOCAL_NOTE}
