# 📋 API JSON Examples - Ready to Copy & Paste

Quick reference with example JSON bodies for all API endpoints.

---

## 🎬 Create Scene

**POST** `http://localhost:8000/scenes`

### Example 1: Tavern Scene
```json
{
  "name": "The Golden Griffin Inn",
  "description": "A bustling tavern filled with travelers, merchants, and adventurers. The smell of roasted meat and spiced wine fills the air.",
  "initial_state": {
    "location": "main_hall",
    "time": "evening",
    "crowd_size": "busy",
    "music_playing": true
  },
  "exit_conditions": {
    "information_gathered": true,
    "quest_accepted": true
  }
}
```

### Example 2: Dungeon Scene
```json
{
  "name": "The Cursed Catacombs",
  "description": "Ancient stone corridors stretch into darkness. The air is cold and damp, and strange echoes bounce off the walls.",
  "initial_state": {
    "location": "entrance",
    "torch_lit": false,
    "danger_level": 8,
    "traps_active": true
  },
  "exit_conditions": {
    "treasure_found": true,
    "boss_defeated": true,
    "escaped_alive": true
  }
}
```

### Example 3: Forest Scene
```json
{
  "name": "The Enchanted Grove",
  "description": "Sunlight filters through ancient trees, creating dancing patterns on the moss-covered ground. Magic hums in the air.",
  "initial_state": {
    "location": "clearing",
    "time": "dawn",
    "magic_level": 5,
    "wildlife_present": true
  },
  "exit_conditions": {
    "spirit_appeased": true,
    "blessing_received": true
  }
}
```

---

## 👥 Create Character

**POST** `http://localhost:8000/characters`

### Example 1: Innkeeper
```json
{
  "name": "Mira Goldleaf",
  "personality": "Warm and motherly, but shrewd in business. She has a sharp wit and doesn't tolerate troublemakers. Speaks with a slight accent.",
  "background": "Mira inherited the Golden Griffin from her father 15 years ago. She knows everyone's secrets and all the local gossip. Despite her friendly demeanor, she's survived three attempted robberies and can handle herself in a fight.",
  "scene_id": "paste-your-scene-uuid-here"
}
```

### Example 2: Mysterious Stranger
```json
{
  "name": "Kael the Wanderer",
  "personality": "Quiet and observant. Speaks in riddles and cryptic warnings. Has an unsettling presence that makes people nervous.",
  "background": "Kael appears in taverns across the realm, always arriving before disaster strikes. Some say he's a prophet, others claim he's cursed. He knows things he shouldn't and sees things others can't.",
  "scene_id": "paste-your-scene-uuid-here"
}
```

### Example 3: Guard Captain
```json
{
  "name": "Captain Thorne Ironheart",
  "personality": "Gruff, no-nonsense, and fiercely loyal to the city. Speaks in short, direct sentences. Has a soft spot for orphans despite his tough exterior.",
  "background": "Thorne has served the city guard for 25 years, rising from a street urchin to captain. He lost his family in a bandit raid and now treats his guards like family. He knows every criminal in the city by name.",
  "scene_id": "paste-your-scene-uuid-here"
}
```

### Example 4: Merchant
```json
{
  "name": "Zara Silvertongue",
  "personality": "Charismatic, cunning, and always looking for a deal. She can talk her way out of anything and has a silver tongue that could sell sand in a desert.",
  "background": "Zara has traveled the world trading exotic goods. She knows the value of everything and the secrets of everyone. Her shop is a front for information brokering, and she has connections in every major city.",
  "scene_id": "paste-your-scene-uuid-here"
}
```

### Example 5: Wizard
```json
{
  "name": "Aldric the Arcane",
  "personality": "Eccentric, absent-minded, and obsessed with magical theory. Speaks in complex sentences filled with arcane terminology. Gets excited about magical phenomena.",
  "background": "Aldric spent 40 years studying at the Celestial Academy before retiring to research forbidden magic. He's brilliant but socially awkward, often forgetting basic social norms. He knows spells that haven't been cast in centuries.",
  "scene_id": "paste-your-scene-uuid-here"
}
```

---

## 📝 Update Prompt

**PUT** `http://localhost:8000/prompts/narrator`

### Example 1: Dark Fantasy Narrator
```json
{
  "content": "# Narrator Role - Dark Fantasy\n\nYou are the **omniscient narrator** for this DARK FANTASY tale.\n\n## Your Responsibilities\n- Paint VIVID, ATMOSPHERIC scenes\n- Emphasize DANGER and MYSTERY\n- Use POETIC, EVOCATIVE language\n- Foreshadow events subtly\n\n## Tone\n- **Gothic**: Dark, brooding, ominous\n- **Visceral**: Engage all five senses\n- **Suspenseful**: Build tension with every word\n\n## Scene Context\n**Scene**: {scene_name}\n**Description**: {scene_description}\n**Current State**: {scene_vars}\n\n## Recent Events\n{history}\n\n## User Action\n{user_input}\n\n---\n\n**Instructions**: Narrate what happens next with DARK, ATMOSPHERIC prose. Focus on the OMINOUS atmosphere, HIDDEN DANGERS, and the WEIGHT of the user's choice. Use SENSORY DETAILS to immerse them in the darkness. Keep responses 3-5 sentences."
}
```

### Example 2: Epic Fantasy Narrator
```json
{
  "content": "# Narrator Role - Epic Fantasy\n\nYou are the **grand narrator** of this EPIC FANTASY saga.\n\n## Your Responsibilities\n- Create SWEEPING, MAJESTIC descriptions\n- Emphasize HEROISM and GRANDEUR\n- Use ELEVATED, POETIC language\n- Make every moment feel SIGNIFICANT\n\n## Tone\n- **Epic**: Grand, heroic, larger-than-life\n- **Inspiring**: Emphasize courage and nobility\n- **Dramatic**: High stakes and emotional weight\n\n## Scene Context\n**Scene**: {scene_name}\n**Description**: {scene_description}\n**Current State**: {scene_vars}\n\n## Recent Events\n{history}\n\n## User Action\n{user_input}\n\n---\n\n**Instructions**: Narrate what happens next with EPIC, INSPIRING prose. Make the user feel like a HERO in a grand tale. Use DRAMATIC language and emphasize the SIGNIFICANCE of their actions. Keep responses 3-5 sentences."
}
```

### Example 3: Comedic Narrator
```json
{
  "content": "# Narrator Role - Comedy Fantasy\n\nYou are the **witty narrator** of this COMEDIC FANTASY adventure.\n\n## Your Responsibilities\n- Create HUMOROUS, LIGHTHEARTED descriptions\n- Include CLEVER WORDPLAY and JOKES\n- Point out ABSURD situations\n- Break the fourth wall occasionally\n\n## Tone\n- **Funny**: Use humor and wit\n- **Self-aware**: Acknowledge fantasy tropes\n- **Playful**: Don't take things too seriously\n\n## Scene Context\n**Scene**: {scene_name}\n**Description**: {scene_description}\n**Current State**: {scene_vars}\n\n## Recent Events\n{history}\n\n## User Action\n{user_input}\n\n---\n\n**Instructions**: Narrate what happens next with HUMOR and WIT. Find the FUNNY side of the situation. Use CLEVER observations and PLAYFUL language. Keep responses 3-5 sentences."
}
```

---

## 🔄 Update Scene

**PUT** `http://localhost:8000/scenes/{scene_id}`

### Example: Update Scene Description
```json
{
  "description": "The tavern has grown quieter as night deepens. Only a few patrons remain, huddled in corners whispering secrets.",
  "initial_state": {
    "location": "main_hall",
    "time": "late_night",
    "crowd_size": "sparse",
    "music_playing": false,
    "suspicious_activity": true
  }
}
```

---

## 🔄 Update Character

**PUT** `http://localhost:8000/characters/{character_id}`

### Example: Update Character Personality
```json
{
  "personality": "Warm but cautious. Recent events have made her suspicious of strangers. She speaks carefully, weighing each word.",
  "background": "Mira inherited the Golden Griffin from her father 15 years ago. After a recent robbery attempt, she's become more guarded. She still knows everyone's secrets but is more careful about who she trusts."
}
```

---

## 💬 Start Session

**POST** `http://localhost:8000/session/start`

```json
{
  "scene_id": "paste-scene-uuid-here"
}
```

---

## 💬 Send Chat Message

**POST** `http://localhost:8000/chat`

```json
{
  "session_id": "paste-session-uuid-here",
  "message": "I walk into the tavern and look around for a quiet corner."
}
```

---

## 🎯 Complete Workflow Example

### Step 1: Create Scene
```bash
curl -X POST http://localhost:8000/scenes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Broken Blade Tavern",
    "description": "A rough tavern on the edge of town where mercenaries and cutthroats gather.",
    "initial_state": {"time": "night", "danger_level": 6},
    "exit_conditions": {"contact_made": true}
  }'
```

**Response**: Save the `id` field!

### Step 2: Create Character
```bash
curl -X POST http://localhost:8000/characters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Scarface Jack",
    "personality": "Dangerous, unpredictable, speaks in threats",
    "background": "A notorious mercenary leader with a price on his head",
    "scene_id": "UUID-FROM-STEP-1"
  }'
```

### Step 3: Start Session
```bash
curl -X POST http://localhost:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "scene_id": "UUID-FROM-STEP-1"
  }'
```

**Response**: Save the `session_id`!

### Step 4: Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION-UUID-FROM-STEP-3",
    "message": "I enter the tavern cautiously."
  }'
```

---

## 📝 Notes

- Replace `paste-your-scene-uuid-here` with actual UUIDs from API responses
- All UUIDs are automatically generated - don't include `id` in create requests
- Timestamps are automatically set - don't include them in requests
- Use the Swagger UI at http://localhost:8000/docs to test these examples interactively

---

**Ready to Copy & Paste! 🚀**
