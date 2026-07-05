# Darshan House of Nature - Design

Gesture 9 of the Darshan interface: the House of Nature (Prakriti) - the
corpus's knowledge of the elements, the earth, the body, health, illness and
longevity, offered as cited heritage with a responsibility architecture
stronger than any other surface of the application.

Companions: `darshan_library_design.md` (depths and facets),
`darshan_sky_map_design.md` (seasons and rhythms),
`content/consciousness_core/silence_and_non_answering.md` (restraint law).

## 1. The Responsibility Architecture First

Health is a restraint case in the consciousness core. The House of Nature is
therefore built inside a fence, stated before any content:

```text
This is heritage, not prescription.
The traditions kept profound knowledge of the body, health and long life.
Darshan cites that knowledge faithfully, at its source, in its context -
and never diagnoses, never prescribes, never doses,
never counsels against qualified medical care.
```

The fence, concretely:

1. **The heritage notice**: every surface in the House carries a permanent,
   quiet notice: *heritage knowledge from the sources, cited; not medical
   advice; it accompanies qualified care, never replaces it.* Not a dismissable
   modal - part of the page, always.
2. **Three tiers of content, three behaviors**:
   - **Safe tier** (offerable as micro-movements): rest, gentle breath
     awareness, walking, sunlight, regularity of meals and sleep, moderation
     (mitahara), quiet - the regimen wisdom no tradition disputes and no
     physician objects to.
   - **Documentary tier** (readable, never offered as practice): fasting
     disciplines, advanced pranayama, herbal knowledge, kaya kalpa
     procedures - rendered at D2-D6 as what the texts say, fully cited, with
     a standing mark: *practiced traditionally under qualified guidance;
     Darshan does not instruct this.*
   - **Closed tier** (never rendered as guidance in any form): dosages,
     disease-specific treatment claims, anything contradicting urgent care.
     Questions in this tier route to the crisis protocol: acknowledgment,
     grounding, "a physician's eyes are needed here", human support named.
3. **Illness routes to restraint**: arrival through illness-related doors or
   questions triggers the same restraint posture as the consciousness core
   demands - fewer words, no interpretation of symptoms, warmth without
   claims.
4. **Double editorial gate**: health-touching corpus content passes two
   reviews before rendering above D2 - the normal editorial review plus a
   safety review against this fence (see section 5).

## 2. The Rooms of the House

### The Elements (Pancha Mahabhuta)

The five elements as the traditions actually teach them - earth (prithvi),
water (apas), fire (agni), air (vayu), ether (akasha):

- each element a room: its teachings across the corpus (Upanishadic
  cosmology, Tantric element meditation, the Siddha alchemy of the
  Tirumandiram, Sri Aurobindo on matter and its ascent), its correspondences
  (senses, koshas, seasons), its practices at the safe tier (walking on
  earth, sitting by water, watching fire, conscious breath, listening to
  silence);
- elements become a **facet** in the Library (added to `content/ontology/`),
  so the whole corpus is browsable by element - and the facet grows richer
  as the corpus grows.

### The Land (Bhumi)

The earth as teacher and as sacred: the corpus on nature, place, sacredness
of land, the Mother on flowers and their significances (a beloved corpus of
its own once imported), gardens, seasons of cultivation - joined to the Sky
Map's ritus. Practices at the safe tier: presence outdoors, tending
something that grows.

### The Body as Temple (Kaya)

The traditions' reverence for the body as instrument of sadhana: dinacharya
(the shape of a day), ritucharya (living with the seasons), mitahara
(measured food), rest and waking, the body in the Integral Yoga (the
Mother's yoga of the cells at documentary tier, cited to her works). The
becoming path's day-as-ashram links here: the rhythm is itself the health
teaching.

### Long Life (Kaya Kalpa and the Siddha Room)

The Siddha tradition's longevity knowledge - Thirumandiram's verses on the
preservation of the body, kaya kalpa as the texts describe it - rendered
honestly and almost entirely at documentary tier: what Tirumular teaches,
where, in his words, with scholarly framing and the standing under-guidance
mark. This room states plainly that it exists to preserve and give access to
the heritage, not to coach immortality.

### Healing Memory (the Medicine of the Ancestors)

Where the imported corpus documents traditional medicine (Siddha, Ayurvedic
texts as they arrive from the ongoing imports), the House renders it as a
**library of healing memory**: systems explained, worldviews honored,
passages cited - documentary tier throughout, with the fence visible, and
with a consistent bridge line: *for living application of these systems,
qualified Siddha/Ayurvedic physicians and licensed medical care exist; this
room is their memory, not their replacement.*

## 3. Consultation Flows

- **From curiosity** (Browse door): wander the rooms as a library - the
  default and safest posture.
- **From the Sky Map**: season and inner weather link into regimen wisdom
  ("sharad has begun - what the traditions keep in autumn"), safe tier only.
- **From a situation door** ("illness" door): restraint posture immediately -
  acknowledgment, the fence, one gentle safe-tier movement, human support
  named; documentary depth reachable but never pushed.
- **From the Inquiry**: health-classified questions get contract-enforced
  restraint (this already exists in the response contract; the House adds
  the heritage notice to any passage it serves such answers).

## 4. What This Unlocks Without Betraying Care

The affection of this gesture: most seekers have never been shown that the
traditions held a *whole physiology of the sacred* - that the Upanishads
count the sheaths of the body, that Tirumular sings the body as the temple
where the Lord dances, that the Mother took the body's transformation as the
final frontier of yoga. Making that visible, cited and safe is a gift no
wellness app gives; refusing to turn it into prescriptions is what keeps it
a gift.

## 5. Editorial Pipeline Additions

Extends `darshan_library_design.md` section 6:

1. **Tier tagging**: health-touching passages carry a `health_tier` mark
   (safe / documentary / closed) assigned in the double gate; untagged
   health content defaults to documentary rendering with the fence.
2. **Safety review**: a second reviewer (safety hat) checks tier assignment,
   the absence of dosage/prescription leakage into safe tier, and the
   presence of under-guidance marks; the review is logged in frontmatter.
3. **Corpus growth protocol**: as the parallel import agent lands new
   collections (Ayurveda, Siddha medicine, nature texts), their manifests
   declare `health_sensitive: true` where applicable, which forces the
   double gate before any passage of that collection renders above D2 -
   the House grows only as fast as the review does.
4. **Element facet**: `content/ontology/` gains the pancha mahabhuta
   taxonomy so element rooms and Library facets share one source of truth.

## 6. The Living Corpus

The House of Nature and the Sky Map are designed for a corpus that is still
arriving. Rooms render in three states: **open** (collection imported and
reviewed), **arriving** (manifest registered, import under way - the room
shows its introduction and the fence, with "the texts are on their way",
honestly), and **future** (named in the shelf's horizon without pretense).
The app's evolution to "a new level of consciousness" is thus visible to the
seeker as the library breathing - and never as vaporware pages pretending to
content that does not exist.
