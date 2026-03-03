"""
Apply Claude's interpretive analysis to analysis_database.json.

This script contains hand-crafted rhetorical analysis for all 85 spreads
of The Medium is the Massage, generated through direct visual inspection
of each spread image following phase_b_methodology_v2.md.

Pass 1: argument, contemporary_domain_candidates, movement_mapping, mapping_rationale, notes
Pass 2: relationship_to_previous, relationship_to_next, multi_spread_patterns
"""

import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'analysis_database.json')
BACKUP_PATH = DB_PATH.replace('.json', '_backup_pre_analysis.json')

# =============================================================================
# PASS 1 ANALYSIS: Per-spread interpretive analysis
# Fields: argument, contemporary_domain_candidates, movement_mapping,
#         mapping_rationale, notes
# =============================================================================

PASS1 = {
    "spread_001": {
        "argument": "The cover announces the book's central thesis by embedding it within a visual collage: a blurred close-up face beneath bold typography transforms the book-as-object into a demonstration of its own argument—the medium (design, typography, image) IS the message, before a single word of theory is read.",
        "contemporary_domain_candidates": ["algorithmic_identity", "attention_and_cognition"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The cover's fusion of commercial packaging with radical theory anticipates how algorithmic platforms collapse intellectual content into visual branding; the blurred face beneath typography enacts the contemporary condition where identity is mediated through designed interfaces.",
        "notes": "Design enacts argument: the blurred face makes the human subject secondary to the typographic medium. The warm color palette and full-bleed image create an immersive sensory environment before any argument is articulated. This is the book's first demonstration that form precedes content.",
        "design_enacts_argument": True,
        "design_argument_description": "The blurred face subordinated to bold typography literally demonstrates that the medium (design) overwhelms the message (the human subject), performing the book's thesis before stating it."
    },
    "spread_002": {
        "argument": "The blurb page performs an ironic self-demonstration: the publishing industry's conventional promotional apparatus (blurbs, marketing copy) frames McLuhan's radical critique of exactly such media packaging, creating a tension between the book's commercial form and its theoretical content.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "attention_and_cognition"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The tension between radical media theory and its commercial packaging directly parallels how platform economics (Amazon reviews, algorithmic recommendation, influencer marketing) frame and distribute critical thought about those very platforms.",
        "notes": "The blurb describes the book as a 'collide-o-scopic journey'—a neologism combining collide, kaleidoscope, and oscilloscope that itself enacts McLuhan's method of compressing multiple meanings into a single verbal image. The promotional language ironically demonstrates how media environments shape the reception of ideas about media environments."
    },
    "spread_003": {
        "argument": "The credits page reveals the collaborative, multi-authored nature of the work (McLuhan/Fiore/Agel), challenging the myth of sole authorship even as copyright conventions demand attribution to named individuals—making visible the tension between collaborative production and individualist intellectual property regimes.",
        "contemporary_domain_candidates": ["authorship_and_creativity"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The three-person credit (theorist/designer/producer) directly anticipates contemporary debates about collaborative authorship in the age of AI co-creation, remix culture, and the dissolving boundary between creator, curator, and tool.",
        "notes": "The Bantam Books copyright notice and production credits constitute a media environment of their own: legal language, institutional affiliation, ISBN conventions—all invisible infrastructure that shapes how intellectual work circulates. McLuhan would note that we read through these conventions without seeing them."
    },
    "spread_004": {
        "argument": "The Browning epigraph ('a man's reach should exceed his grasp, or what's a heaven for?') positions the reader at a threshold, establishing that the book will demand cognitive stretching—an invitation to engage with material that deliberately exceeds conventional comprehension strategies.",
        "contemporary_domain_candidates": ["attention_and_cognition"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The demand for cognitive reaching beyond habitual grasp parallels the contemporary challenge of sustained, effortful attention in an environment of algorithmic recommendation and infinite scrolling that rewards shallow engagement.",
        "notes": "The epigraph functions as a contract with the reader: expect disorientation. This is a rhetorical strategy of setting expectations that prepares the reader to accept the book's unconventional form. The choice of Browning (a Victorian poet) to introduce a media theory text also demonstrates McLuhan's method of using old cultural forms to illuminate new conditions."
    },
    "spread_005": {
        "argument": "The title page deploys massive typography to demonstrate its own thesis: the physical scale and visual weight of 'The Medium is the Massage' transforms the act of reading from decoding words into encountering a visual environment, showing that presentation fundamentally shapes reception.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "attention_and_cognition"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The oversized typography that fills the page enacts the shift from reading-as-decoding to reading-as-experiencing—a transition now ubiquitous in social media's emphasis on visual impact over textual content, where headlines, memes, and display text function as images rather than prose.",
        "notes": "The title itself contains the famous 'typo' (massage for message) that McLuhan deliberately retained, adding layers: massage (physical manipulation), mass age (the era of mass media), mess age (the confusion of the era). The typography makes this wordplay visceral rather than intellectual.",
        "design_enacts_argument": True,
        "design_argument_description": "Typography at environmental scale transforms reading into a spatial encounter, demonstrating that the medium of presentation (size, weight, placement) determines the message's reception more than its semantic content."
    },
    "spread_006": {
        "argument": "The split continuation of the title across a page turn forces the reader to experience the book as a temporal, physical medium—meaning emerges through the bodily act of turning pages, not from instantaneous comprehension, making the book's materiality impossible to ignore.",
        "contemporary_domain_candidates": ["attention_and_cognition", "embodiment_and_disembodiment"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "Splitting content across a physical threshold anticipates how digital interfaces sequence content delivery (loading screens, scroll-reveals, pagination) to shape the temporality of comprehension; the page-turn becomes a proto-UX design choice that controls attention through material constraint.",
        "notes": "The page break within the title is the book's first structural demonstration of McLuhan's thesis: the physical medium (bound pages that must be turned sequentially) shapes the message (the title can only be completed through physical action). This is the book teaching the reader how to read it."
    },
    "spread_007": {
        "argument": "The sardonic interjection 'and how!' paired with an expressive figure introduces humor and vernacular speech as legitimate modes of intellectual inquiry, arguing that popular culture's responses to media saturation are as analytically valid as scholarly ones.",
        "contemporary_domain_candidates": ["attention_and_cognition", "synthetic_media_and_post_truth"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The use of colloquial humor to frame serious theory prefigures how meme culture, satirical commentary, and internet humor now serve as primary vehicles for vernacular media criticism, collapsing the distinction between entertainment and analysis.",
        "notes": "The comedic tone performs a critical function: it lowers the reader's intellectual defenses, creating receptivity to ideas that might otherwise provoke resistance. McLuhan understood that humor operates as an 'anti-environment'—a probe that makes invisible structures visible through incongruity."
    },
    "spread_008": {
        "argument": "McLuhan's declaration that media 'work us over completely' reframes media not as neutral tools selected by autonomous users but as active environmental forces that reshape perception, cognition, and social relations at every level—a thesis that demands the reader abandon the instrumental view of technology.",
        "contemporary_domain_candidates": ["ambient_intelligence", "agency_and_autonomy"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The claim that media operate on us 'completely' without our awareness directly anticipates ambient computing environments (smart homes, wearables, algorithmic feeds) that shape behavior through environmental design rather than conscious choice, raising fundamental questions about human agency in designed environments.",
        "notes": "This is the book's core theoretical claim, stated plainly before the visual demonstrations begin. The word 'completely' is crucial—it insists on totality, refusing the comfortable notion that media affect only certain domains of life. The subsequent 75 spreads will demonstrate this completeness."
    },
    "spread_009": {
        "argument": "The exhaustive enumeration of media's domains of effect—personal, political, economic, aesthetic, psychological, moral, ethical, social—functions as a rhetorical accumulation that overwhelms any attempt to limit media's reach, insisting through sheer listing that no human domain escapes media transformation.",
        "contemporary_domain_candidates": ["ambient_intelligence", "agency_and_autonomy"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The comprehensive list of affected domains mirrors how contemporary platform ecosystems (Google, Meta, Amazon) have infiltrated every aspect of life simultaneously, from personal relationships to political discourse to economic exchange, making the 'completeness' McLuhan described structurally literal.",
        "notes": "The rhetorical strategy of accumulation is significant: rather than arguing for media's pervasiveness through logic, McLuhan demonstrates it through enumeration. Each additional domain in the list makes the claim harder to resist. This is itself a media-aware rhetorical choice—overwhelming through quantity rather than persuading through syllogism."
    },
    "spread_010": {
        "argument": "The completion of the opening thesis—that media shape and control 'the scale and form of human association and action'—establishes the environmental theory of media that the entire book will demonstrate: media are not content-delivery systems but architectures of social possibility.",
        "contemporary_domain_candidates": ["ambient_intelligence", "agency_and_autonomy", "surveillance_and_control"],
        "movement_mapping": ["prologue"],
        "mapping_rationale": "The insistence that media control the 'scale and form' of human association anticipates how platform architectures (algorithmic sorting, network effects, engagement metrics, content moderation) determine who can associate with whom and on what terms, functioning as governance systems.",
        "notes": "The phrase 'scale and form' is precise: 'scale' refers to the reach and scope of human connection (from village to globe), while 'form' refers to the qualitative nature of that connection (linear vs. simultaneous, fragmented vs. holistic). Together they describe what we now call 'platform governance'—the structural determination of social possibility by technological architecture."
    },
    "spread_011": {
        "argument": "The inventory beginning with 'you' and 'your family,' paired with a surveillance-style photograph, demonstrates that electric media have dissolved the boundary between public observation and private existence—your most intimate life is now within media's operational reach.",
        "contemporary_domain_candidates": ["surveillance_and_control", "public_private_collapse"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The surveillance photograph addressing 'you' directly anticipates ubiquitous data collection (smart devices, social media tracking, facial recognition) that makes private life permanently observable; the direct second-person address mirrors how platforms create the experience of being perpetually watched and personally addressed.",
        "notes": "The shift to second person ('you') is a critical rhetorical move: it interpellates the reader, making them the subject of media's effects rather than a detached observer. The photographic style—grainy, candid, surveillance-like—makes visible the invisible watching that electric media enable. This spread begins the 'inventory' section promised in the subtitle."
    },
    "spread_012": {
        "argument": "Extending the inventory to 'your neighborhood' and 'your education' reveals how media don't just enter private spaces but restructure the public institutions—schools, communities—through which people organize collective life and transmit cultural knowledge.",
        "contemporary_domain_candidates": ["ambient_intelligence", "global_village_revisited"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Media's restructuring of neighborhoods and education maps onto how digital platforms have replaced physical community (NextDoor, social media groups) and transformed learning (MOOCs, YouTube tutorials, AI tutors), creating new forms of locality and pedagogy that no longer require physical co-presence.",
        "notes": "The progression from 'you' to 'your family' to 'your neighborhood' to 'your education' traces an expanding circle of media influence: from individual perception to domestic life to community structure to institutional knowledge. Each step outward makes the environmental claim more encompassing."
    },
    "spread_013": {
        "argument": "The physically rotated text forces readers to reorient their bodies to continue reading, enacting the disruption that new media cause to established perceptual habits—the body itself must adapt when the medium changes, proving that media effects are physical, not merely intellectual.",
        "contemporary_domain_candidates": ["attention_and_cognition", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The forced physical rotation parallels how mobile device usage has restructured bodily orientation (portrait vs. landscape, head-down posture, thumb-scrolling), and how VR/AR demands new embodied relationships with information—media literally reshape how bodies inhabit space.",
        "notes": "This is the book's most direct physical demonstration of its thesis: by rotating the text, Fiore forces the reader to rotate the book (or their head), making the reading body suddenly visible. The medium of the book is literally working the reader over. This spread about education is itself educating the reader through physical experience rather than abstract instruction.",
        "design_enacts_argument": True,
        "design_argument_description": "Rotated text forces bodily reorientation, making the reader physically experience how media environments restructure habitual perception—the body must change to accommodate the medium's demands."
    },
    "spread_014": {
        "argument": "The extension of the media inventory to 'your job' reveals how communications technologies restructure not just leisure and culture but the fundamental conditions of labor—work itself is a media-saturated environment whose form is determined by dominant communication technologies.",
        "contemporary_domain_candidates": ["labor_and_value", "ambient_intelligence"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Media's transformation of work anticipates the gig economy, remote work, platform labor, and algorithmic management where employment is inseparable from digital infrastructure—the 'job' is now constituted by the communication platforms through which it is performed.",
        "notes": "Including 'your job' in the media inventory is quietly radical: it insists that economic life is a media effect, not just a market outcome. The means of communication determine the means of production—a McLuhanesque revision of Marx that becomes obvious in the age of platform capitalism."
    },
    "spread_015": {
        "argument": "Including 'your government' in the inventory argues that political institutions are not merely users of media but are fundamentally constituted by the dominant communications technologies of their era—democratic forms that emerged under print conditions face transformation under electronic conditions.",
        "contemporary_domain_candidates": ["surveillance_and_control", "global_village_revisited"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The claim that media reshape government anticipates how social media have transformed political campaigns, governance, and civic discourse—from algorithmic influence operations to the erosion of shared factual reality to the real-time publicization of state action.",
        "notes": "The inventory's inclusion of government completes the move from private to public: you → family → neighborhood → education → job → government. Each domain is revealed as a media environment rather than an autonomous institution. The implication is that changing the communication medium changes the form of governance, a thesis now demonstrated by the effects of social media on democratic institutions."
    },
    "spread_016": {
        "argument": "The final inventory item—'the others'—combined with a crowd photograph suggests that media's deepest effect is on the constitution of collective otherness itself: how 'we' and 'they' are defined, perceived, and related to is fundamentally a media effect.",
        "contemporary_domain_candidates": ["global_village_revisited", "algorithmic_identity"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The vague category 'the others' anticipates how algorithmic sorting creates filter bubbles that define who the others are, while simultaneously connecting people across traditional boundaries—McLuhan's global village realized as a global platform where proximity and otherness are algorithmically constructed.",
        "notes": "The deliberate vagueness of 'the others' is powerful: it refuses to specify who the others are because the point is that media determine that question. In a print culture, the others are those outside your literate community; in an electronic culture, the others are simultaneously everyone (global village) and no one (because electronic connection dissolves the boundaries that create otherness)."
    },
    "spread_017": {
        "argument": "The core McLuhan thesis—'All media are extensions of some human faculty'—reframes every technology as a prosthetic amplification of the body or mind, establishing the conceptual foundation for understanding media not as external tools but as organic outgrowths of human biological capacities.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment", "ambient_intelligence"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The extensions thesis directly anticipates smartphones as memory prosthetics, social media as social-faculty extensions, AI as cognitive extension, and brain-computer interfaces—each extending human faculties to a degree that blurs the boundary between biological organism and technological apparatus.",
        "notes": "This spread serves as a theoretical hinge: it completes the inventory (what media affect) and introduces the mechanism (how they work—through extension). The 'extensions' concept is McLuhan's most generative theoretical tool because it allows any technology to be analyzed as a sensory/cognitive prosthesis, revealing its hidden effects on the extended faculty and the organism as a whole."
    },
    "spread_018": {
        "argument": "The extreme close-up of a bare human foot, stripped of any technological extension, presents the unadorned body as the ground zero of media theory—before prosthetic extension, there is the biological organism with its inherent capacities and limitations, establishing a phenomenological baseline.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Beginning the extensions demonstration with the naked body establishes a phenomenological baseline increasingly relevant as digital technologies render the body optional (remote work, virtual avatars, disembodied AI interaction)—what is the 'unextended' human when all faculties are digitally amplified?",
        "notes": "The foot is an inspired choice for the first extension example: it is the most humble, least glamorous body part, grounding the theoretical discussion in physical reality. The extreme close-up forces intimacy with the biological body, creating a visceral contrast with the technological extensions that follow.",
        "design_enacts_argument": True,
        "design_argument_description": "The extreme close-up of bare flesh creates unavoidable bodily intimacy, grounding the abstract 'extensions' thesis in physical reality before the technological examples begin."
    },
    "spread_019": {
        "argument": "The declaration that 'the wheel is an extension of the foot' exemplifies McLuhan's analytical method: by revealing the hidden bodily logic within a familiar technology, he defamiliarizes both the technology and the body, showing each as incomplete without the other.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment", "labor_and_value"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The wheel/foot pairing makes visible the embodied origins of transportation technology, anticipating how autonomous vehicles and delivery drones complete the abstraction of locomotion from human bodies—each step in transportation technology further extends and eventually replaces the foot's original function.",
        "notes": "The pedagogical structure is deliberate: thesis (all media are extensions) → example (the foot) → connection (the wheel extends the foot). This three-step demonstration will be repeated for eye/book, skin/clothing, and nervous system/electric circuitry, creating a cumulative argument through parallel structure."
    },
    "spread_020": {
        "argument": "The visual composite of wheel and foot transforms the abstract 'extensions' metaphor into a concrete image, demonstrating that the relationship between body and technology is not merely analogical but functionally continuous—the technology literally grows from the body's needs.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The visual merging of organic and mechanical forms anticipates contemporary prosthetics, exoskeletons, and the broader transhumanist imagination where human-machine boundaries dissolve—the composite image prefigures the cyborg as a literal figure rather than a metaphor.",
        "notes": "Fiore's design choice to visually merge body and machine is a powerful enactment of McLuhan's thesis. The image doesn't illustrate the argument—it IS the argument, showing rather than telling that extension is a continuous relationship, not a discrete tool-use transaction."
    },
    "spread_021": {
        "argument": "Identifying the book as 'an extension of the eye' reveals that literacy is not a neutral cognitive skill but a sensory reorganization that privileges visual-sequential processing over acoustic, tactile, and communal modes of knowing—reading literally reshapes the sensorium.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "attention_and_cognition"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The book/eye connection illuminates how screens have further extended and transformed visual processing, while the resurgence of non-visual media (podcasts, voice assistants, spatial audio) represents a partial reversal of the visual dominance that print created.",
        "notes": "Moving from foot/wheel to eye/book escalates the argument: transportation extends physical capacity, but literacy extends perception itself. The stakes increase with each example. McLuhan's point is that the book didn't just store information—it restructured consciousness toward linearity, privacy, and individual perspective."
    },
    "spread_022": {
        "argument": "The extreme close-up of a human eye mirrors the earlier foot image, establishing a consistent visual grammar: each extension begins with the naked organ, forcing the reader to see the biological apparatus that technology will amplify and, in amplifying, transform.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment", "surveillance_and_control"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The isolated eye anticipates eye-tracking technology, iris scanning, and the broader surveillance apparatus that transforms the organ of seeing into an object of being seen—the eye that reads is simultaneously the eye that is read by the technology it gazes into.",
        "notes": "The parallel structure (foot close-up → wheel; eye close-up → book) creates a formal rhythm that is itself a medium-aware design choice. The reader begins to expect the pattern: organ → extension. This predictability is a form of training—the reader is learning McLuhan's analytical method through repeated formal experience."
    },
    "spread_023": {
        "argument": "Extending the body metaphor to clothing-as-skin reveals fashion and bodily covering as communication media—technologies that encode social identity, regulate environmental interaction, and reshape how the body interfaces with the world, far beyond mere physical protection.",
        "contemporary_domain_candidates": ["algorithmic_identity", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Clothing-as-skin-extension anticipates wearable technology (smartwatches, fitness trackers, AR glasses) and virtual fashion (digital clothing, avatar customization) where the boundary between body, garment, interface, and identity dissolves into a continuous designed surface.",
        "notes": "The clothing/skin pairing introduces a social dimension absent from foot/wheel and eye/book: clothing communicates identity to others, making it a medium in the social-communicative sense as well as the prosthetic-extension sense. This expands McLuhan's 'extensions' concept from individual capacity to social signaling."
    },
    "spread_024": {
        "argument": "The culminating extension—'electric circuitry is an extension of the central nervous system'—argues that electronic media don't merely extend individual senses but externalize the entire integrative network of consciousness, creating a collective technological nervous system at planetary scale.",
        "contemporary_domain_candidates": ["ambient_intelligence", "global_village_revisited"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The externalized nervous system directly describes the internet, IoT, cloud computing, and AI as literal realizations of McLuhan's metaphor—a global information-processing network that extends not just individual senses but the integrative function of consciousness itself.",
        "notes": "This is the climax of the extensions sequence, and it fundamentally changes the argument's scale. Foot→wheel and eye→book extend individual capacities; nervous system→electric circuitry extends the organizing principle of consciousness itself. The implication is that electronic media don't just amplify human faculties—they externalize the self, creating a shared technological subjectivity.",
        "design_enacts_argument": True,
        "design_argument_description": "The placement as the culminating extension in a carefully escalating series (foot→eye→skin→nervous system) creates a formal crescendo that mirrors the theoretical escalation from individual prosthesis to collective consciousness."
    },
    "spread_025": {
        "argument": "The Alice in Wonderland quotation introduces the theme of epistemological vertigo: in a world where everything communicates and every medium has moral consequences, the challenge shifts from finding meaning to navigating an excess of it—Wonderland as media environment.",
        "contemporary_domain_candidates": ["synthetic_media_and_post_truth", "attention_and_cognition"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Alice's Wonderland—where rules shift without warning and meaning proliferates uncontrollably—directly describes the contemporary experience of information overload, where algorithmic feeds create an Alice-like condition of perpetual disorientation amid excessive, contradictory meaning.",
        "notes": "The first of several Alice in Wonderland references throughout the book. Carroll's work functions as McLuhan's literary mirror: both depict environments where the rules of perception shift unexpectedly, forcing the protagonist to constantly readjust. Alice is the reader's avatar in the media landscape—perpetually confused but perpetually adapting."
    },
    "spread_026": {
        "argument": "The transition to ear imagery and alphabetic history marks a pivotal shift: the alphabet was a technology that translated the fluid, immersive acoustic world into fixed visual signs, fundamentally restructuring human consciousness toward linearity, sequence, and detached observation.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "attention_and_cognition"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The alphabet's sensory translation (ear to eye) anticipates contemporary cross-modal translations—voice-to-text, text-to-image AI, multimodal interfaces—each of which restructures cognition in ways McLuhan would recognize as extensions that amputate as much as they amplify.",
        "notes": "This spread begins the book's deep historical argument: the alphabet is not merely a notation system but a perceptual technology that created the preconditions for Western civilization's defining characteristics—individualism, linear logic, legal systems, scientific method. The ear/eye contrast will structure the rest of the book's analysis."
    },
    "spread_027": {
        "argument": "The pre-alphabetic world is characterized as a total sensory environment of 'simultaneous interplay' where ear, touch, smell, and sight participated together, establishing a contrast with the fragmented, vision-dominated world that literacy created—a lost wholeness that electronic media may restore.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The recovery of pre-literate multisensory immersion maps onto immersive digital experiences (VR, spatial computing, haptic feedback, spatial audio) that attempt to reintegrate the senses after centuries of visual dominance created by print culture.",
        "notes": "McLuhan's idealization of pre-literate culture is strategic rather than nostalgic: he uses it as a diagnostic contrast to make print culture's effects visible. The 'tribal' world serves as an anti-environment that reveals the hidden biases of literate consciousness."
    },
    "spread_028": {
        "argument": "The concept of address and naming reveals how identity is constituted through media infrastructure: to have an address is to be locatable, categorizable, and governable within a communications network—identity is a media effect, not a pre-existing essence.",
        "contemporary_domain_candidates": ["algorithmic_identity", "surveillance_and_control"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The address-as-identity concept directly anticipates IP addresses, digital identifiers, social media handles, and the broader apparatus of computational identity that makes individuals trackable and addressable within networks—identity as a function of one's position in a communication grid.",
        "notes": "The seemingly mundane observation about addresses contains a radical insight: naming and addressing are technologies of governance. To name is to classify; to address is to locate. The postal system, the census, the telephone directory—each creates a different kind of addressable subject. Digital platforms create yet another: the uniquely identified, perpetually trackable data-subject."
    },
    "spread_029": {
        "argument": "Characterizing printing as 'a ditto device' strips it of cultural prestige and reveals its core operation: mechanical reproduction that standardizes content, creates identical copies, and transforms knowledge from a communal oral process into a reproducible commodity—the ancestor of all copy-paste cultures.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "labor_and_value"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The 'ditto device' framing anticipates how digital reproduction (copy-paste, screenshots, reposts, generative AI) has made the concept of an 'original' increasingly meaningless, raising the ditto principle to a scale where the copy/original distinction collapses entirely.",
        "notes": "The phrase 'ditto device' is deliberately deflationary—it reduces the printing press, Western civilization's most prestigious technology, to a copying machine. This defamiliarization is McLuhan's signature move: strip away the cultural aura to reveal the underlying operation. The resonance with Benjamin's 'mechanical reproduction' thesis is clear but McLuhan goes further, seeing reproduction as the medium's primary message."
    },
    "spread_030": {
        "argument": "Renaissance perspective is revealed as a media effect of print culture: the fixed viewpoint, the vanishing point, the uniform visual field are all extensions of the linear, sequential logic that print imposed on consciousness—even art's most celebrated achievement is a typographic side-effect.",
        "contemporary_domain_candidates": ["synthetic_media_and_post_truth", "attention_and_cognition"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Print culture's creation of a single 'correct' perspective anticipates how algorithmic feeds create personalized perspectives that feel objective but are constructed—each user's information environment appears as the natural order of things, just as Renaissance perspective appeared as 'realistic' rather than conventional.",
        "notes": "Connecting Renaissance perspective to print technology is one of McLuhan's most audacious claims: it argues that visual art's formal innovations were driven not by aesthetic genius but by the perceptual restructuring that a new medium (print) imposed on consciousness. The vanishing point is a typographic artifact, not a window on reality."
    },
    "spread_031": {
        "argument": "The physically inverted and disrupted text shatters print-era reading conventions, forcing the reader to experience the cognitive disorientation that occurs when a dominant medium's ground rules are violated—this is what electronic media do to print consciousness, made viscerally immediate.",
        "contemporary_domain_candidates": ["attention_and_cognition", "post_literacy_and_language"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Disrupted text orientation enacts the experience of encountering information in constantly shifting formats, paralleling how digital platforms reshape presentation conventions (vertical video, Stories format, TikTok's scroll mechanic) in ways that demand perpetual cognitive readjustment.",
        "notes": "The inverted text is the book's most aggressive formal disruption so far. Where the rotated text of spread 013 required physical adaptation, the inverted text requires cognitive adaptation—the reader must decode the visual pattern against their habitual reading direction. This escalation mirrors the book's argument that electronic media create progressively more disorienting environments.",
        "design_enacts_argument": True,
        "design_argument_description": "Inverted and disrupted typography forces the reader to experience print conventions being violated from within, demonstrating that the 'invisible' rules of the reading environment become visible only when broken."
    },
    "spread_032": {
        "argument": "The continued typographic disruption across multiple spreads creates a cumulative assault on print-era reading habits, arguing through sustained formal experience that the dissolution of stable media conventions is not a momentary glitch but a permanent condition of electronic culture.",
        "contemporary_domain_candidates": ["attention_and_cognition", "post_literacy_and_language"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The sustained disruption parallels the contemporary experience of perpetual format-shifting—moving between incompatible media conventions (email, messaging, social feeds, video) that each demand different cognitive orientations, making adaptability rather than mastery the core literacy skill.",
        "notes": "The repetition of disruption across multiple spreads is itself significant: it's not a one-time trick but a sustained condition. The reader cannot simply adjust once and settle into a new pattern—the disruption keeps shifting, modeling the perpetual instability of electronic media environments."
    },
    "spread_033": {
        "argument": "The photograph of prison bars visualizes McLuhan's argument that print culture's linear, sequential logic creates invisible perceptual prisons—constraining thought to one-thing-at-a-time processing while appearing to offer intellectual freedom through universal literacy.",
        "contemporary_domain_candidates": ["agency_and_autonomy", "surveillance_and_control"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The prison-as-environment metaphor anticipates how digital platforms create similarly invisible enclosures (filter bubbles, algorithmic curation, platform lock-in, Terms of Service) that constrain perception and choice while appearing to expand both—comfortable prisons disguised as playgrounds.",
        "notes": "The prison imagery is the book's starkest visual metaphor: print culture doesn't just shape perception, it imprisons it. The bars represent the invisible grid of linearity, sequence, and fixed perspective that literate consciousness mistakes for the natural order of thought. Electronic media don't free us from this prison—they replace it with a different kind of enclosure."
    },
    "spread_034": {
        "argument": "The Joycean wordplay 'A cell for citters to cit in' condenses the prison metaphor into linguistic form—the 'cell' is simultaneously a prison room, a biological unit, and a monastic retreat, demonstrating that language itself is a medium whose structures constrain and enable thought.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "agency_and_autonomy"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "Joyce's multi-layered puns anticipate how digital language (hashtags, memes, emoji, copypasta) creates compressed, multi-referential communication where meaning is unstable and context-dependent—every digital utterance, like Joyce's puns, carries multiple simultaneous readings determined by the reader's platform context.",
        "notes": "The Joyce reference is strategic: Joyce is McLuhan's primary literary ally, the writer who most fully explored how the medium of language shapes consciousness. Finnegans Wake—written to be heard rather than silently read—represents Joyce's attempt to create a post-literate literature that recovers acoustic consciousness within the visual medium of print."
    },
    "spread_035": {
        "argument": "The introduction of the 'global village' concept marks the transition from diagnosing print culture's effects to envisioning electronic culture's emergent reality: instantaneous global connection that recreates tribal acoustic interdependence at planetary scale, with all the intimacy and hostility that implies.",
        "contemporary_domain_candidates": ["global_village_revisited", "ambient_intelligence"],
        "movement_mapping": ["movement_1_environment"],
        "mapping_rationale": "The global village is McLuhan's most directly prophetic concept, now realized and complicated by social media's simultaneous creation of planetary connection and tribal conflict—the village is real, but so are its gossip, surveillance, conformity pressures, and tribal warfare.",
        "notes": "McLuhan's global village was never utopian—he consistently warned that villages are characterized by gossip, surveillance, conformity pressure, and inter-tribal conflict as much as by intimacy and participation. The contemporary misreading of the concept as techno-optimism obscures McLuhan's deeply ambivalent understanding of electronic retribalisation."
    },
    "spread_036": {
        "argument": "The visual presentation of electronic circuitry transforms abstract technological infrastructure into a visible pattern, arguing that the form of electronic networks—non-linear, simultaneous, interconnected—is itself the message that restructures society, independent of any content transmitted through them.",
        "contemporary_domain_candidates": ["ambient_intelligence", "global_village_revisited"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The circuit-as-pattern anticipates how network topology (internet architecture, social graphs, neural network architectures) functions as an invisible environment that structures human interaction and cognition—the shape of the network determines the shape of thought.",
        "notes": "This spread marks the book's transition into Movement 2: from the relatively measured analysis of print culture's effects to the accelerating, more fragmented examination of electronic culture's consequences. The pacing itself begins to accelerate, with shorter text passages and more dramatic visual interventions."
    },
    "spread_037": {
        "argument": "Electronic interdependence 'recreates the world in the image of a global village'—not merely connecting distant people but fundamentally transforming spatial and temporal experience so that events anywhere are experienced everywhere simultaneously, abolishing the distances that print perspective created.",
        "contemporary_domain_candidates": ["global_village_revisited", "public_private_collapse"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The recreation of the world through electronic interdependence directly describes social media feeds where war, celebrity gossip, and personal updates arrive simultaneously on the same screen—the hierarchies of relevance that distance and print culture maintained are algorithmically flattened.",
        "notes": "The word 'recreates' is key—not 'connects' or 'links' but 'recreates.' McLuhan insists that electronic media don't simply add a communication layer to existing reality; they produce a fundamentally different reality with different spatial, temporal, and social coordinates. This is not enhancement but ontological transformation."
    },
    "spread_038": {
        "argument": "When the environment itself becomes the art form—when the entire sensory surround is aesthetically constructed—the distinction between art and life dissolves, making everyone simultaneously artist and audience in a total media environment that demands creative participation rather than passive consumption.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "ambient_intelligence"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The environment-as-art concept anticipates the aestheticization of everyday life through social media (Instagram filters, TikTok performances, curated feeds) and immersive technologies (AR overlays, smart environments) that transform the ordinary into the designed.",
        "notes": "The Rauschenberg-style visual collage enacts the art/life dissolution it describes. Fiore's design doesn't illustrate the concept but demonstrates it: the page itself is an environment-as-art-form, asking the reader to experience it rather than merely decode it. The reader becomes the audience of the book's own environmental art."
    },
    "spread_039": {
        "argument": "The New Yorker cartoon deployed as critical evidence demonstrates that popular culture has already absorbed the awareness of media complexity that McLuhan theorizes—humor and cartoons process cultural anxiety about technological change more effectively than academic analysis.",
        "contemporary_domain_candidates": ["attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The cartoon's use as evidence anticipates how memes, viral tweets, and internet humor now serve as primary vehicles for cultural criticism and media analysis, often processing collective technological anxiety faster and more accurately than institutional knowledge production.",
        "notes": "The book's repeated use of New Yorker cartoons serves multiple functions: it validates popular culture as a source of insight, it provides comic relief within a dense theoretical argument, and it demonstrates that media awareness permeates society unevenly—cartoonists, like artists, perceive environmental shifts before theorists formalize them."
    },
    "spread_040": {
        "argument": "The railway exemplifies how each medium creates an entire new environment rather than simply adding capacity: railways didn't just transport goods but created suburbs, restructured labor, transformed concepts of distance and time, and produced entirely new forms of social organization—all independent of cargo.",
        "contemporary_domain_candidates": ["ambient_intelligence", "labor_and_value"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The railway's total environmental restructuring parallels how the internet has restructured not just communication but real estate (remote work), commerce (e-commerce), social organization (online communities), labor (gig economy), and even temporal experience (24/7 connectivity)—all independent of any specific content transmitted.",
        "notes": "The railway example is pedagogically powerful because it makes the 'medium is the message' thesis concrete and indisputable: no one can seriously argue that the railway's significance lay in its cargo rather than in the spatial, temporal, economic, and social reorganization it produced. This clarity makes it a stepping stone to the less obvious claim that electronic media similarly restructure all of life."
    },
    "spread_041": {
        "argument": "The rear-view mirror metaphor diagnoses humanity's most persistent cognitive failure regarding technology: we habitually perceive new media through the conceptual categories of old ones, perpetually looking backward while accelerating forward, which prevents us from perceiving the actual novel effects of current technologies.",
        "contemporary_domain_candidates": ["attention_and_cognition", "synthetic_media_and_post_truth"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The rear-view mirror is McLuhan's most potent diagnostic tool for the present: it explains why AI is debated in industrial-era terms (automation/jobs) rather than in terms of its genuinely novel effects on cognition, creativity, and reality—we keep seeing the future through past frameworks.",
        "notes": "This is arguably McLuhan's most practically useful concept. The rear-view mirror explains: why early television was 'radio with pictures,' why early internet was 'electronic newspaper,' why early social media was 'digital town square,' and why current AI discourse frames it as 'sophisticated tool' rather than perceiving its environmental effects. Each generation uses old media metaphors to domesticate new media threats."
    },
    "spread_042": {
        "argument": "The dense collage of overlapping images and text demonstrates the condition of information saturation as an aesthetic and cognitive experience: when information accumulates beyond linear processing capacity, pattern recognition replaces sequential analysis and juxtaposition becomes the dominant mode of meaning-making.",
        "contemporary_domain_candidates": ["attention_and_cognition", "synthetic_media_and_post_truth"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The information-collision aesthetic directly prefigures the algorithmic feed where unrelated content collides without hierarchy or context, and the speed of information flow makes sustained analysis impossible—meaning emerges from adjacency rather than argument.",
        "notes": "The visual collage enacts the cognitive condition it describes: the reader cannot process all elements sequentially and must instead perceive the page as a simultaneous pattern. This shift from sequential to pattern perception is exactly what McLuhan argues electronic media force on consciousness."
    },
    "spread_043": {
        "argument": "The word LOVE displayed at environmental scale transforms a concept from denotation to spatial experience: you don't read LOVE, you inhabit it, demonstrating that when language reaches a certain scale and visual intensity it ceases to function as text and becomes an environment.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The word-as-environment treatment anticipates how social media reduces complex ideas to visual slogans and reaction buttons (like/heart/angry), where language functions not as argument but as emotional atmosphere—a meme is an environment, not a text.",
        "notes": "Robert Indiana's LOVE sculpture (1964) made exactly this transition from word to environment in physical space. Fiore's page design achieves the same effect in print. The word LOVE at this scale cannot be 'read'—it can only be experienced. This is the post-literate condition: language persists but ceases to function as linear discourse.",
        "design_enacts_argument": True,
        "design_argument_description": "Typography at environmental scale transforms the word from a readable sign into an inhabitable space, demonstrating the post-literate condition where language becomes image and reading becomes spatial experience."
    },
    "spread_044": {
        "argument": "The critique of forcing new media to do old media's work identifies a perpetual failure of technological imagination: every generation shoehorns new media into old patterns (TV as radio-with-pictures, internet as digital newspaper), wasting the new medium's transformative potential to preserve comfortable habits.",
        "contemporary_domain_candidates": ["attention_and_cognition", "agency_and_autonomy"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "This critique applies directly to every major digital transition: early websites as brochures, early social media as blogs, early streaming as broadcast, current AI as search engines—the rear-view mirror in action, perpetually domesticating the new by forcing it into old conceptual containers.",
        "notes": "This spread provides the prescriptive complement to the rear-view mirror diagnosis: if the problem is looking backward, the solution is perceiving the new medium's own inherent logic rather than imposing old frameworks. McLuhan never fully achieved this prescription himself—the challenge of perceiving a medium's effects from within remains the central difficulty of media ecology."
    },
    "spread_045": {
        "argument": "The word ENVIRONMENT split across two spreads (ENVIRO- / -NMENT) uses the book's physical structure to make its own medium visible: the gutter, the page break, the act of turning—normally invisible infrastructure—suddenly becomes the message, revealing the book as an environment.",
        "contemporary_domain_candidates": ["ambient_intelligence", "attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "Making the reading environment visible by disrupting it parallels how digital detox movements, screen-time apps, and platform design criticism attempt to make invisible digital environments perceptible—following McLuhan's principle that environments become visible only when something breaks them.",
        "notes": "This is one of the book's most brilliant formal gestures. The split word ENVIRONMENT literally cannot be perceived as a single unit because the book's physical structure (the page break) intervenes. The medium (the bound book) becomes visible precisely by interrupting the message (the word 'ENVIRONMENT'). The reader must actively reconstruct the word across the break, performing the very perceptual work the book describes.",
        "design_enacts_argument": True,
        "design_argument_description": "Splitting ENVIRONMENT across the physical page break forces the reader to perceive the book's material structure (gutter, binding, page sequence) that normally functions as invisible background—the medium becomes visible by disrupting its own message."
    },
    "spread_046": {
        "argument": "The continuation of the split ENVIRONMENT (-NMENT) completes the demonstration: the reader who has turned the page has already performed the proof—the physical environment of the book shaped their experience of a word about environments, making the theoretical claim experientially undeniable.",
        "contemporary_domain_candidates": ["ambient_intelligence", "attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The completed word arriving only after physical action (page turn) mirrors how digital environments deliver meaning incrementally (loading screens, progressive disclosure, infinite scroll) rather than instantaneously, making the temporal structure of the medium part of the message.",
        "notes": "The two-spread ENVIRONMENT sequence is the book's most concentrated formal demonstration of its thesis. No amount of theoretical argumentation could be as persuasive as the reader's own experience of having the word 'environment' interrupted by the book's environment. Theory becomes experience; argument becomes proof."
    },
    "spread_047": {
        "argument": "The thesis that 'environments are invisible' explains why media effects are so powerful and so difficult to perceive: like water to a fish, the dominant medium constitutes the unquestioned background of all experience—it is the ground, never the figure, of consciousness.",
        "contemporary_domain_candidates": ["ambient_intelligence", "agency_and_autonomy"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "Environmental invisibility is the master concept for understanding why algorithmic bias, surveillance capitalism, and platform manipulation are so resistant to critique—they operate as infrastructure rather than content, shaping experience from the unperceived background rather than presenting themselves as objects of conscious evaluation.",
        "notes": "This is the book's deepest philosophical claim: the most powerful media effects are precisely those we cannot perceive because they constitute the perceptual apparatus itself. The fish/water analogy (though McLuhan attributes it to various sources) captures the radical difficulty of media ecology: the object of study is the very condition of the subject's perception."
    },
    "spread_048": {
        "argument": "The artist is positioned as the essential early-warning system of media change: trained in pattern recognition and sensitivity to formal qualities, the artist perceives environmental shifts that others experience only as vague unease—art is not decoration but survival equipment in an age of media transformation.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "agency_and_autonomy"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The artist-as-sentinel anticipates how speculative designers, critical technologists, science fiction writers, and digital artists now serve as the primary interpreters of technological transformation, perceiving algorithmic environments that most users inhabit unconsciously.",
        "notes": "McLuhan's elevation of the artist is not aesthetic snobbery but a functional claim: the artist's perceptual training makes environmental shifts visible before they are theoretically articulable. This explains why science fiction consistently anticipates technological developments more accurately than futurology—artists perceive patterns that analysts, trapped in old categories, cannot."
    },
    "spread_049": {
        "argument": "The W.C. Fields image reinforces humor as a critical tool and the entertainer as a media-aware figure—the comedians, clowns, and satirists who play with media conventions demonstrate a practical understanding of media effects that precedes and exceeds formal theory.",
        "contemporary_domain_candidates": ["attention_and_cognition", "authorship_and_creativity"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The entertainer as media critic anticipates how comedians, satirists, and internet humorists now function as public intellectuals of media ecology—Jon Stewart, meme creators, and YouTube essayists process media transformation through humor more effectively than academic media studies.",
        "notes": "The repeated deployment of entertainers (W.C. Fields, later the Beatles, Bob Dylan) as intellectual figures is itself a McLuhanesque move: it demonstrates that the boundary between entertainment and insight is a print-culture artifact that electronic media dissolve."
    },
    "spread_050": {
        "argument": "The celebration of the amateur—exemplified by Faraday's self-education—argues that formal training in existing categories can be a perceptual handicap: the amateur's fresh, untrained perception is better equipped to perceive genuinely new patterns because it carries no obligation to existing frameworks.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The amateur's advantage anticipates the democratization of media production (YouTube creators, citizen journalists, open-source developers) and the persistent pattern where outsiders and autodidacts perceive platform dynamics more clearly than credentialed professionals trained in pre-digital frameworks.",
        "notes": "The Faraday example is paired with an Oppenheimer quotation about children's superior sensory perception. Both point to the same insight: expertise in old environments becomes a liability in new ones. The amateur and the child share a freedom from trained incapacity—they see what professionals have learned not to notice."
    },
    "spread_051": {
        "argument": "Humor is theorized as 'a system of communications and as a probe of our environment'—not mere entertainment but an anti-environmental tool that makes invisible structures visible through incongruity, operating through compressed pattern recognition rather than linear argument.",
        "contemporary_domain_candidates": ["attention_and_cognition", "synthetic_media_and_post_truth"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "Humor as environmental probe anticipates how internet humor (memes, shitposting, satirical deepfakes) functions as vernacular media criticism, processing collective anxiety about technological change faster than institutional analysis and revealing hidden platform dynamics through comedic exaggeration.",
        "notes": "The characterization of humor as 'a compressed overlay of stories' with 'no story line—no sequence' directly describes the meme: a compressed, non-linear, pattern-based form of communication that conveys complex cultural observations through juxtaposition rather than narrative. McLuhan's 1967 description of humor's structure is a precise definition of internet humor's form."
    },
    "spread_052": {
        "argument": "The Dance of Death silhouettes spanning both pages argue that technological transition generates existential terror expressed through art: medieval woodcuts depicting death's universality correspond to contemporary Theater of the Absurd—both are cultural responses to the vertigo of media shift.",
        "contemporary_domain_candidates": ["attention_and_cognition", "agency_and_autonomy"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The clash between old and new technologies producing cultural anxiety directly describes the current AI transition, where anxieties about automation, deep fakes, and algorithmic control generate cultural products (dystopian fiction, AI art discourse, techno-pessimism) that function as contemporary Dance of Death imagery.",
        "notes": "The full-bleed silhouettes create a powerful visual effect: the figures appear to march across the page in a procession that bridges both pages, suggesting that technological transitions sweep up all of society in their movement. The text below identifies this as a recurring pattern—each major technological shift produces its own cultural expression of displacement anxiety.",
        "design_enacts_argument": True,
        "design_argument_description": "Full-bleed silhouettes marching across both pages create an unstoppable visual procession that embodies the irresistible force of technological transition sweeping through society."
    },
    "spread_053": {
        "argument": "The juxtaposition of a young woman with a cello and an elderly person's weathered face, paired with Montaigne's 'we must live with the living,' argues that technological change demands generational bridge-building—the old acoustic culture (cello) and the lived wisdom of age must coexist with youth's embrace of the new.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment", "global_village_revisited"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The generational juxtaposition anticipates the digital divide and intergenerational conflict over technology—the challenge of integrating embodied, pre-digital wisdom with digital-native fluency, neither dismissing the old nor uncritically embracing the new.",
        "notes": "The Montaigne quotation is precisely chosen: it insists on engagement with the living present rather than retreat into nostalgic past or anxious future. This is McLuhan's own position—neither technophile nor technophobe but engaged diagnostician of the present moment's perceptual transformations."
    },
    "spread_054": {
        "argument": "The full-bleed close-up of a kiss—two faces meeting across the page gutter—uses the book's physical structure to argue that genuine human intimacy persists within and through technological mediation, and that the body's capacity for direct sensory contact remains the foundation of all communication.",
        "contemporary_domain_candidates": ["embodiment_and_disembodiment", "public_private_collapse"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The intimate kiss spanning the book's structural division (the gutter) anticipates how digital media both enable and complicate intimacy—dating apps, video calls, haptic technologies that mediate touch—where the platform's structure (like the book's gutter) is always present between connecting bodies.",
        "notes": "The absence of text is significant: this is pure image, pure body, pure sensation. After pages of theoretical argument, the book returns to pre-verbal, pre-literate bodily experience. The kiss crosses the gutter—the book's structural division—suggesting that human connection persists despite the medium's attempts to divide.",
        "design_enacts_argument": True,
        "design_argument_description": "The kiss spanning the gutter demonstrates that bodily intimacy crosses the medium's structural divisions, while the full-bleed scale transforms the viewer into an intimate witness of embodied connection."
    },
    "spread_055": {
        "argument": "The analysis of youth culture—dropouts and teach-ins—argues that the younger generation's rejection of institutional education is not rebellion but rational response to a media environment that has made compartmentalized, classified knowledge obsolete: youth demand roles, not goals; involvement, not instruction.",
        "contemporary_domain_candidates": ["attention_and_cognition", "labor_and_value"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "Youth's rejection of compartmentalized education for participatory involvement anticipates the contemporary shift from credential-based to portfolio-based career paths, from passive lecture to active project-based learning, and from institutional gatekeeping to platform-mediated self-education.",
        "notes": "The dropout/teach-in analysis is remarkably prescient: McLuhan sees both phenomena as expressions of the same media shift—the young reject the old medium (classified, compartmentalized instruction) and demand the new one (participatory, multi-sensory involvement). The phrase 'they want R-O-L-E-S, not goals' captures the shift from print-culture individualism to electronic-culture participation."
    },
    "spread_056": {
        "argument": "The photograph of Amherst seniors walking out on Secretary McNamara's address—captioned EDUCATION—demonstrates that the clash between institutional authority and youth consciousness is not political disagreement but media incompatibility: the lecture format cannot contain electronic-age awareness.",
        "contemporary_domain_candidates": ["attention_and_cognition", "agency_and_autonomy"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The walkout as media protest anticipates how digital-native generations reject institutional communication formats (lectures, press conferences, official statements) in favor of participatory, horizontal, peer-to-peer modes—the format, not the content, is what's being rejected.",
        "notes": "The single word EDUCATION in massive type beneath the walkout photograph creates a powerful ironic commentary: what is being 'educated' here? The students are educating the institution about its own obsolescence. The photograph documents a moment where the invisible environment of the lecture hall becomes visible through its rejection."
    },
    "spread_057": {
        "argument": "Bob Dylan's silhouette with the rotated quotation 'something is happening but you don't know what it is, do you, Mister Jones?' positions the musician as the definitive cultural diagnostician of media transition—the artist who perceives the environmental shift that institutional consciousness cannot.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "Dylan as environmental prophet anticipates how musicians, filmmakers, and cultural producers continue to perceive and articulate media shifts before theorists and policymakers—from Radiohead's prescience about digital alienation to Black Mirror's diagnostic fiction.",
        "notes": "The rotated text forces the reader to physically reorient to read Dylan's words, enacting the reorientation that the quote demands. 'Mister Jones'—the conventional, print-literate consciousness—cannot perceive the environmental shift that Dylan (the artist-as-antenna) registers through direct sensory experience. The visual treatment makes reading the quote an experience of the disorientation it describes.",
        "design_enacts_argument": True,
        "design_argument_description": "Rotated text forces physical reorientation, making the reader embody the perceptual shift that Dylan's lyrics diagnose—you must change your position to receive the message."
    },
    "spread_058": {
        "argument": "The juxtaposition of an abstract ink blot with a New Yorker cartoon about youth spending power argues that the old culture perceives the new generation's behavior as unintelligible chaos (the blot) while simultaneously being forced to acknowledge its economic power (the cartoon)—incomprehension meets dependency.",
        "contemporary_domain_candidates": ["labor_and_value", "attention_and_cognition"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The tension between cultural incomprehension and economic recognition anticipates how legacy institutions relate to digital-native generations and platforms: unable to understand TikTok culture but compelled to advertise on it, mystified by creator economics but dependent on its attention flows.",
        "notes": "The ink blot is a Rorschach test: it means whatever the viewer projects onto it. This is itself a media-theoretical statement—abstract, open forms are products of acoustic/electronic consciousness, while the cartoon represents print culture's attempt to rationalize what it cannot comprehend. The two images represent two modes of perception coexisting on the same page."
    },
    "spread_059": {
        "argument": "The multi-exposure photograph paired with the Joycean wordplay 'History as she is harped. Rite words in rote order' argues that electronic media transform history from a linear narrative into a simultaneous field of recurring patterns—history becomes music rather than chronicle.",
        "contemporary_domain_candidates": ["synthetic_media_and_post_truth", "post_literacy_and_language"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The transformation of history from linear narrative to simultaneous pattern describes how digital media compress temporal experience—everything is simultaneously accessible, historical context collapses, and the present becomes a palimpsest of all periods, making 'fake news' possible because chronological authority dissolves.",
        "notes": "The multi-exposure photographic technique creates a visual palimpsest: multiple moments layered into a single image, making temporal sequence visible as spatial overlay. This is the visual equivalent of Joyce's verbal technique in Finnegans Wake, where all of history is compressed into a single night's dream. The punning 'Rite words in rote order' (right words in rote order) simultaneously suggests ritual (rite) and mechanical repetition (rote)."
    },
    "spread_060": {
        "argument": "The comic-book BANG! explosion paired with text about the ear's omnidirectional, immersive, non-hierarchical perception argues that acoustic space—where sounds come from everywhere simultaneously—is the perceptual model for electronic media, replacing print's fixed visual perspective with total surround.",
        "contemporary_domain_candidates": ["attention_and_cognition", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_2_acceleration"],
        "mapping_rationale": "The ear's 360-degree, always-on, unfiltered reception directly models the contemporary notification environment where alerts, messages, and updates arrive from all directions simultaneously without the user's active selection—we live in acoustic space even when staring at screens.",
        "notes": "The BANG! is brilliantly chosen: it is the comic-book representation of sound in a visual medium—a visual translation of acoustic experience. This translation IS the book's subject: how do different sensory modes get translated across media? The ear 'favors no particular point of view'—unlike the eye, it has no equivalent of perspective. This makes acoustic space the more democratic but also more overwhelming sensory model.",
        "design_enacts_argument": True,
        "design_argument_description": "The explosive BANG! visual fills the page like sound fills a room—omnidirectionally, irresistibly, without offering the reader a detached 'point of view' from which to observe it."
    },
    "spread_061": {
        "argument": "The Socratic critique from Phaedrus—that writing will 'create forgetfulness in the learners' souls'—reveals that anxiety about new media's cognitive effects is not modern but ancient: every major media transition provokes the same warning that the new technology will destroy the capacities the old one cultivated.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "attention_and_cognition"],
        "movement_mapping": ["hinge_m2_m3"],
        "mapping_rationale": "Socrates' warning about writing mirrors contemporary warnings about Google making us stupid, GPS destroying spatial memory, and AI eroding critical thinking—each generation's media anxiety follows the same pattern of mourning the cognitive capacities the old medium cultivated.",
        "notes": "This spread begins the Hinge section bridging Movements 2 and 3. The return to ancient Greece signals a shift from contemporary analysis to deep historical pattern-recognition. McLuhan uses Socrates to demonstrate that media anxiety is not a modern phenomenon but a structural feature of every media transition. The Greek busts on the left page visually anchor the argument in classical authority."
    },
    "spread_062": {
        "argument": "The juxtaposition of text about myth, memory, and the Beatles with a vintage 'Develop A Powerful Memory?' advertisement argues that oral culture's mnemonic power is simultaneously mourned and commodified—the lost capacity becomes a product to be purchased, revealing how market logic colonizes every media transition.",
        "contemporary_domain_candidates": ["attention_and_cognition", "labor_and_value"],
        "movement_mapping": ["hinge_m2_m3"],
        "mapping_rationale": "The commodification of memory anticipates brain-training apps, productivity tools, and the 'second brain' industry that monetizes the cognitive capacities that digital media have atrophied—selling back to users the mental faculties that the platforms have displaced.",
        "notes": "The mention of the Beatles as people who 'put on the audience, putting on a whole vestiture, a whole time, a Zeit' is significant: McLuhan sees the Beatles not as musicians but as environmental artists who create total sensory events. 'Young people are looking for a formula for putting on the universe'—this anticipates immersive experience design, VR, and the contemporary desire for total media environments."
    },
    "spread_063": {
        "argument": "The handwritten letters and enlarged punctuation marks argue that print culture contains vestigial traces of oral/acoustic culture—punctuation is a visual technology designed to encode vocal rhythms (pause, emphasis, inflection) into silent text, revealing print's hidden dependency on the oral world it displaced.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "embodiment_and_disembodiment"],
        "movement_mapping": ["hinge_m2_m3"],
        "mapping_rationale": "Punctuation as acoustic encoding anticipates how digital communication reinvents paralinguistic cues through emoji, capitalization, ellipses, and formatting conventions—each a visual attempt to encode the vocal/gestural information that text inherently strips away.",
        "notes": "The oversized punctuation marks (periods, commas, question marks, quotation marks) are presented as visual objects rather than transparent signifiers, defamiliarizing the typographic conventions that readers normally look through. This is another instance of making the medium visible by enlarging it past the threshold of transparency."
    },
    "spread_064": {
        "argument": "The voiceprint images paired with John Cage quotations and the declaration of 'JOY and revolution' argue that the electronic recovery of voice—through recording, transmission, and now visual representation—constitutes both an aesthetic revolution (Cage) and an identity revolution (voiceprints as unique as fingerprints).",
        "contemporary_domain_candidates": ["algorithmic_identity", "authorship_and_creativity"],
        "movement_mapping": ["hinge_m2_m3"],
        "mapping_rationale": "Voiceprints as identity verification anticipates voice recognition technology, vocal biometrics, and the broader use of biological signatures as digital identity—the voice becomes simultaneously a creative medium (Cage's expanded music) and a surveillance instrument (voiceprint identification).",
        "notes": "The Cage quotations are carefully selected: 'The highest purpose is to have no purpose at all' and 'Everything we do is music' express the aesthetic corollary of McLuhan's media theory—when the environment becomes the art form, purposelessness becomes the highest purpose and everything becomes music. The voiceprint images make the voice visible, reversing the alphabet's translation of sight into sound."
    },
    "spread_065": {
        "argument": "James Joyce, presented with a massive close-up of an ear, is positioned as the literary prophet who discovered how to live simultaneously in all cultural modes: Finnegans Wake is the verbal equivalent of electronic media's simultaneous, multi-layered, acoustic consciousness—the book that made print behave like television.",
        "contemporary_domain_candidates": ["post_literacy_and_language", "authorship_and_creativity"],
        "movement_mapping": ["hinge_m2_m3"],
        "mapping_rationale": "Joyce's Finnegans Wake as a text that operates across all cultural modes simultaneously anticipates hypertext, transmedia storytelling, and the internet's layered, cross-referential, non-linear information environment—a literary prototype for the condition of living in all media simultaneously.",
        "notes": "The ear close-up is as significant as the earlier eye and foot close-ups: it establishes the ear as the organ of electronic consciousness, just as the eye was the organ of print consciousness. Joyce's placement at the Hinge point of the book is strategic: he is the artist who bridges print and electronic cultures, demonstrating in prose what McLuhan theorizes in analysis. The Vico cycle ('the wake of human progress can disappear again into the night of sacral or auditory man') connects this to cyclical theories of media history."
    },
    "spread_066": {
        "argument": "The large copyright symbol © paired with text about authorship's history argues that intellectual property is a media artifact: the concept of individual authorship was created by print technology, and electronic media's return to collaborative, fluid, copyable content threatens to dissolve the legal and economic structures built on print-era individuality.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "labor_and_value"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The historicization of copyright directly anticipates the contemporary crisis of intellectual property in the digital age—from music piracy to AI training data to open-source software to meme culture, every digital copyright controversy demonstrates that print-era IP concepts cannot contain electronic media's inherent reproducibility.",
        "notes": "The giant © symbol is both a visual icon and a conceptual provocation: copyright, presented at monumental scale, becomes visible as a media artifact rather than a natural right. The text traces authorship from medieval scribal anonymity through Gutenberg's creation of the author-as-brand to the electronic dissolution of individual authorship. The repeated phrase 'A ditto, ditto device' echoes spread 029, creating a structural rhyme."
    },
    "spread_067": {
        "argument": "The analysis of television as a medium that 'completes the cycle of the human sensorium' argues that TV is not degraded cinema but an entirely different sensory technology—one that demands participation, involvement, and multi-sensory engagement rather than the detached observation that print and cinema cultivated.",
        "contemporary_domain_candidates": ["attention_and_cognition", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The characterization of television as participatory and immersive anticipates how streaming, social media, and interactive platforms have intensified the demand for active engagement—from binge-watching's temporal immersion to social media's demand for constant participation to gaming's complete sensory involvement.",
        "notes": "McLuhan's television analysis is often misread as praise; it is actually a diagnosis. Television demands participation not because it is engaging but because its low-resolution image requires the viewer to fill in missing information. This 'cool' medium creates involvement not through richness but through incompleteness. The Jules Verne illustration ironically comments on failed predictions—even visionaries use rear-view mirrors."
    },
    "spread_068": {
        "argument": "The Kennedy funeral photograph—the most-watched television event of its era—demonstrates that TV transforms public ritual into participatory experience: the entire nation simultaneously witnessed and participated in grief, collapsing the distance between event and audience that print-era media maintained.",
        "contemporary_domain_candidates": ["public_private_collapse", "global_village_revisited"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "Television's transformation of the Kennedy funeral into shared participatory ritual anticipates how social media creates shared real-time experiences of public events (from disasters to celebrity deaths to political crises) where the audience is simultaneously witness, mourner, and commentator.",
        "notes": "The text's observation that 'the television generation is a grim bunch' is a diagnostic rather than a judgment: television involvement creates emotional seriousness because the viewer is a participant, not a spectator. The Kennedy funeral is the paradigmatic example—television didn't report the event, it made 200 million people experience it simultaneously. This is the global village's emotional register."
    },
    "spread_069": {
        "argument": "The critique that television's critics 'insist on regarding television as merely a degraded form of print technology' is McLuhan's most direct statement of the rear-view mirror problem applied to a specific medium: judging TV by print standards guarantees misunderstanding both media.",
        "contemporary_domain_candidates": ["attention_and_cognition", "synthetic_media_and_post_truth"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The misunderstanding of television through print-era categories directly parallels the misunderstanding of social media through broadcast-era categories, AI through software-era categories, and every new medium through the conceptual framework of its predecessor.",
        "notes": "The Carver theater marquee and New Yorker cartoon create a visual environment of mid-century media culture: the movie theater, the sophisticated magazine cartoon, television in the living room. These are all media environments that coexist and interfere with each other, creating the complex media ecology that McLuhan navigates."
    },
    "spread_070": {
        "argument": "The claim that 'Hollywood is often a fomenter of anti-colonialist revolutions' reveals an unexpected dimension of media effects: movies don't just entertain but create desire by displaying consumer goods and lifestyles to colonized populations, making deprivation visible and therefore intolerable—media as revolutionary agent.",
        "contemporary_domain_candidates": ["global_village_revisited", "labor_and_value"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "Hollywood's unintended revolutionary effect through displaying Western consumer plenty to colonized populations directly anticipates how social media exposes global wealth inequality, how influencer culture creates aspiration and resentment simultaneously, and how platform capitalism makes economic disparity viscerally visible.",
        "notes": "The Sukarno quotation about refrigerators as revolutionary symbols is devastatingly precise: the medium (cinema) delivers the message (consumer plenty) to an audience (colonized peoples) for whom that message becomes revolutionary motivation. The 'content' of movies (plots, characters) is irrelevant—the real message is the environmental display of material possibility. The Variety headline 'Ice Boxes Sabotage Colonialism' condenses this thesis into tabloid form."
    },
    "spread_071": {
        "argument": "The giant letter 'A' filling the entire spread, with tiny figures visible at its base, redefines art as environmental rather than object-based: when art reaches architectural scale, it ceases to be something you look at and becomes something you inhabit—the gallery becomes a media environment.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "ambient_intelligence"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "Art at environmental scale anticipates immersive art installations (teamLab, Meow Wolf), AR art, and the broader shift from art-as-object to art-as-experience that characterizes contemporary aesthetic practice—art becomes atmosphere rather than artifact.",
        "notes": "The letterform 'A' (beginning 'Art') at monumental scale transforms typography into architecture. The tiny human figures at the base establish scale: the letter dwarfs the viewer, making the medium (typography) impossible to read and forcing it to be experienced as environment. This three-spread sequence (Art / is anything / you can get away with) splits a sentence across pages just as ENVIRONMENT was split earlier.",
        "design_enacts_argument": True,
        "design_argument_description": "The monumental letterform dwarfs the human figures at its base, physically demonstrating art's transformation from object-scale to environment-scale—you cannot read the letter, only inhabit it."
    },
    "spread_072": {
        "argument": "The continuation 'is anything' with a photograph of people dwarfed by a massive sculpture (Niki de Saint Phalle's work) demonstrates that art's function in the electronic age is environmental immersion: the audience doesn't contemplate art from a distance but is physically enveloped by it.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The walk-through sculpture anticipates immersive digital environments, VR art spaces, and the transformation of the audience from observer to inhabitant—the same shift from detached contemplation to embodied participation that defines the transition from print to electronic culture.",
        "notes": "The Niki de Saint Phalle sculpture ('The biggest and best woman in the world—an 82-foot-long, 20-foot-high sculpture') is literally a walk-in artwork—visitors enter through the figure's legs. This is art as architecture, as environment, as bodily experience. The photograph shows people inside and around the sculpture, documenting the moment when the gallery-goer becomes the artwork's inhabitant."
    },
    "spread_073": {
        "argument": "The completion 'you can get away with' paired with images of the Beatles meeting Prime Minister Wilson and Balinese art philosophy ('We have no art. We do everything as well as we can') argues that the boundary between art and life, between high and popular culture, has dissolved—art is whatever the environment permits.",
        "contemporary_domain_candidates": ["authorship_and_creativity", "public_private_collapse"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The dissolution of art/life boundaries anticipates how social media collapses the distinction between creative expression and daily documentation, how influencer culture makes living itself a performance, and how the Balinese principle of integrated aesthetic practice describes the contemporary demand to 'curate' every aspect of existence.",
        "notes": "The three-spread sentence 'Art is anything you can get away with' (attributed to McLuhan himself) is simultaneously a provocation and a precise definition for the electronic age. The Balinese quotation provides the anthropological counterpoint: cultures without a separate concept of 'art' integrate aesthetic quality into all activities. Electronic culture is returning to this condition, where everything is potentially art and art is potentially everything."
    },
    "spread_074": {
        "argument": "The 'some like it hot, some like it cold' spread uses Marilyn Monroe and Cold War imagery to argue that information war has replaced physical war as the primary mode of conflict: when weapons become too powerful to use, war becomes a contest of media environments rather than military forces.",
        "contemporary_domain_candidates": ["surveillance_and_control", "global_village_revisited"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "Information as the primary theater of conflict directly describes contemporary cyber warfare, disinformation campaigns, social media manipulation, and the broader transformation of geopolitical conflict from kinetic to informational—wars fought through platforms rather than on battlefields.",
        "notes": "The Monroe/Khrushchev juxtaposition (hot/cold) operates on multiple levels: Monroe represents 'hot' media (high-definition cinema), Khrushchev represents 'cold' war (low-intensity information conflict). The text's claim that 'the hydrogen bomb is history's exclamation point—it ends an age-long sentence of manifest violence' argues that nuclear weapons made hot war obsolete, forcing conflict into the information domain."
    },
    "spread_075": {
        "argument": "The Alice in Wonderland battle illustration—chaotic, crowded, absurd—visualizes the condition of information warfare where traditional military categories dissolve into incomprehensible complexity: you cannot tell soldiers from civilians, combatants from bystanders, in the information battlefield.",
        "contemporary_domain_candidates": ["synthetic_media_and_post_truth", "surveillance_and_control"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The indistinguishable chaos of Carroll's battle scene anticipates the contemporary information warfare landscape where state actors, trolls, bots, activists, and ordinary users are indistinguishable participants in conflicts whose boundaries and stakes are unclear to all participants.",
        "notes": "The return to Alice in Wonderland at this late point creates a structural bookend with spread 025. Alice's Wonderland has become a battlefield—the epistemological vertigo of the earlier spread has escalated into full-scale information conflict. The caption 'Did you happen to meet any soldiers, my dear, as you came through the woods?' suggests that in information war, you cannot identify the combatants even when surrounded by them."
    },
    "spread_076": {
        "argument": "The declaration that 'the environment as a processor of information is propaganda' combined with protest imagery and fire argues that media environments are never neutral—they are inherently ideological, and the only counter to environmental propaganda is dialogue that addresses the medium itself rather than its programmers.",
        "contemporary_domain_candidates": ["surveillance_and_control", "agency_and_autonomy"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The environment-as-propaganda thesis directly describes how platform algorithms constitute ideological environments that shape perception without explicit messaging—feed curation, content moderation, and interface design function as environmental propaganda independent of any individual's intentions.",
        "notes": "The cartoon caption 'See Dick. See Dick protest. Protest, Dick! Protest!' brilliantly satirizes how even resistance becomes formatted by the media environment it opposes—protest itself becomes a media genre with its own conventions. The fire imagery on the right page introduces apocalyptic urgency: if environments are propaganda, then unconscious media consumption is ideological submission."
    },
    "spread_077": {
        "argument": "Laotze's poem about the usefulness of emptiness paired with fire imagery and the East-West convergence thesis argues that electronic media are 'Orientalizing the West'—replacing Western values of containment, separation, and classification with Eastern values of flow, integration, and emptiness-as-function.",
        "contemporary_domain_candidates": ["global_village_revisited", "embodiment_and_disembodiment"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The East-West media convergence anticipates how mindfulness apps, meditation practices, and holistic design thinking have entered Western tech culture, and how the internet's networked, non-hierarchical, flowing structure shares structural affinities with Eastern philosophical traditions.",
        "notes": "The fire imagery spanning both pages creates an environmental surround that enacts the dissolution of boundaries the text describes. The hands visible within the flames suggest human presence within elemental transformation. Laotze's insight that usefulness comes from emptiness ('we are helped by what is not') anticipates negative space in design thinking and the recognition that what media exclude is as significant as what they include."
    },
    "spread_078": {
        "argument": "The protest banner 'Keep in Circulation the Rumor that GOD is Alive' paired with Meister Eckhardt's mysticism argues that the 'death of God' is the death of the Newtonian clockwork universe—a media effect of the old mechanical worldview—while the electronic age creates conditions for new forms of the sacred that operate through circulation and rumor rather than institution and doctrine.",
        "contemporary_domain_candidates": ["synthetic_media_and_post_truth", "global_village_revisited"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The characterization of belief as 'rumor in circulation' anticipates how viral media, conspiracy theories, and memetic belief systems circulate through platforms—truth and meaning are now functions of circulatory velocity rather than institutional authority, making 'post-truth' a media condition rather than a moral failure.",
        "notes": "The dark brushstrokes on the right page evoke both erasure and creation—Eckhardt's 'Only the hand that erases can write the true thing' connects artistic negation to spiritual insight. The protest banner's ironic plea to 'keep in circulation' treats belief itself as a media phenomenon—God survives not through proof but through transmission. This is the global village's theology: belief as meme."
    },
    "spread_079": {
        "argument": "The New York Times headline about the 1965 Northeast blackout functions as a full-spread demonstration of McLuhan's thesis: when electric technology fails, its environmental presence becomes instantly visible—the blackout reveals the medium by removing it, making the invisible infrastructure of electronic civilization suddenly and terrifyingly apparent.",
        "contemporary_domain_candidates": ["ambient_intelligence", "agency_and_autonomy"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The blackout as revelation of invisible infrastructure anticipates internet outages, cloud service failures, and platform shutdowns that momentarily reveal how completely digital infrastructure has become the environment of daily life—each failure makes the invisible medium visible.",
        "notes": "This is the book's most powerful real-world example of the 'environments are invisible' thesis: nobody noticed the electrical grid until it failed. The newspaper headline itself is ironic—a print medium reporting the failure of the electronic medium, like a messenger from one era reporting the death of another. The text's suggestion that a six-month blackout would make media effects undeniable is a thought experiment in forced environmental awareness.",
        "design_enacts_argument": True,
        "design_argument_description": "The newspaper front page displayed as a full spread transforms a document of electric failure into a demonstration that media environments become visible only through breakdown."
    },
    "spread_080": {
        "argument": "The businessman surfing a wave, with text referencing Poe's 'Descent into the Maelstrom,' offers McLuhan's ultimate methodological prescription: the way to survive in a media maelstrom is not to fight the current but to study its patterns from within—detached observation from inside the vortex, using the medium's own dynamics to navigate it.",
        "contemporary_domain_candidates": ["agency_and_autonomy", "attention_and_cognition"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The surfer-in-the-maelstrom anticipates the contemporary need for 'digital literacy' understood not as technical skill but as the ability to perceive and navigate algorithmic environments from within—pattern recognition inside the platform vortex rather than futile attempts to stand outside it.",
        "notes": "The surfer metaphor is the book's prescriptive culmination: if media environments are inescapable (you cannot get off the wave), then the only viable strategy is to understand their dynamics well enough to ride them. Poe's mariner survived the maelstrom by studying its patterns while inside it—this is McLuhan's model for media ecology as a discipline. The businessman's briefcase makes the image contemporary and slightly absurd: this is survival equipment for the information age.",
        "design_enacts_argument": True,
        "design_argument_description": "The full-bleed wave image places the reader inside the dynamic environment, with the suited surfer modeling the stance of engaged, pattern-recognizing participation within overwhelming media forces."
    },
    "spread_081": {
        "argument": "The faceless numbered figures juxtaposed with the Caterpillar's question 'and who are you?' from Alice in Wonderland confronts the reader with the identity crisis of electronic culture: mass media simultaneously individuate (you are a number, uniquely tracked) and de-individuate (you are one of many identical figures, faceless in the crowd).",
        "contemporary_domain_candidates": ["algorithmic_identity", "surveillance_and_control"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The numbered faceless figures directly anticipate how digital platforms assign unique identifiers to users while simultaneously reducing them to data points in aggregate—you are both uniquely tracked (surveillance) and categorically interchangeable (algorithmic classification).",
        "notes": "The Alice Caterpillar's question 'Who are you?' becomes the fundamental question of the electronic age. The numbered figures are both individuated (each has a unique number) and depersonalized (all are faceless, identically dressed). This paradox—unique identification combined with categorical fungibility—is the precise condition of platform identity."
    },
    "spread_082": {
        "argument": "Alice's response—'I hardly know, sir, just at present—at least I know who I was when I got up this morning, but I think I must have been changed several times since then'—is presented as the definitive statement of electronic-age identity: selfhood is no longer stable but continuously transformed by the media environments it passes through.",
        "contemporary_domain_candidates": ["algorithmic_identity", "agency_and_autonomy"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "Alice's fluid, environmentally-determined identity directly describes the contemporary experience of digital selfhood: different platforms elicit different personas, algorithmic recommendations reshape preferences, and identity becomes a function of which media environment one currently inhabits.",
        "notes": "The continued crowd of numbered faceless figures reinforces the mass-individuation paradox. Alice's admission that she has 'been changed several times' is not a confession of weakness but a description of the electronic condition: in a world of rapid media transitions, stable identity is an anachronism. The question is not 'who are you?' but 'which version of you is currently active?'"
    },
    "spread_083": {
        "argument": "The New Yorker cartoon of a son explaining McLuhan to his father—in a study filled with books—is the book's self-aware conclusion: McLuhan's ideas are transmitted through the very generational media gap they describe, with the younger generation perceiving what the older, book-formed generation cannot.",
        "contemporary_domain_candidates": ["attention_and_cognition", "global_village_revisited"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The son explaining new media theory to a book-surrounded father anticipates every subsequent generational technology gap—parents and children inhabiting different media environments, with mutual incomprehension as the structural condition of accelerating media change.",
        "notes": "The cartoon is a masterpiece of self-referential humor: a New Yorker cartoon (print medium) depicting a young person explaining McLuhan (media theorist) to an older person surrounded by books (print culture). The son has a guitar (acoustic/oral culture) leaning against his chair. Every element of the image enacts McLuhan's thesis about media generation gaps. The book-lined study is an environmental portrait of print consciousness."
    },
    "spread_084": {
        "argument": "The photo credits page, listing dozens of image sources (press agencies, museums, magazines, individual photographers), reveals the book as a work of media archaeology—assembled from the fragments of existing media culture, it is itself a demonstration that new media are made from the recombined elements of old ones.",
        "contemporary_domain_candidates": ["authorship_and_creativity"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The credits page as media inventory anticipates the contemporary condition of remix culture, mashup aesthetics, and aggregation platforms where creative work is assembled from pre-existing media fragments—the book's own production method (collage from mass media) prefigures the fundamental creative mode of digital culture.",
        "notes": "The credits page is often overlooked but is itself a significant text: it documents the media ecology from which the book was assembled—United Press International, Newsweek, CBS News, The New Yorker, museums, individual photographers. This is a map of mid-1960s American media culture. The sheer number of sources demonstrates the book's collage method: McLuhan/Fiore/Agel assembled a theory of media FROM media."
    },
    "spread_085": {
        "argument": "The back cover's Whitehead quotation—'It is the business of the future to be dangerous'—closes the book with a philosophical mandate: the appropriate response to media transformation is not comfort-seeking but courageous engagement with danger, because the future's danger is precisely what makes it productive of genuine novelty.",
        "contemporary_domain_candidates": ["agency_and_autonomy", "attention_and_cognition"],
        "movement_mapping": ["movement_3_dreamscape"],
        "mapping_rationale": "The insistence that the future must be dangerous anticipates the contemporary tension between precautionary and accelerationist responses to technological transformation—between those who seek to manage technology's dangers and those who argue that danger is the necessary condition of innovation.",
        "notes": "The Whitehead quotation provides the book's philosophical frame: Browning's 'reach should exceed grasp' (spread 004) at the beginning and Whitehead's 'business of the future to be dangerous' at the end. Together they argue that productive engagement with media change requires both cognitive stretching and existential courage. The dark, partially obscured image suggests that the future remains only partially visible—we proceed into it with incomplete knowledge, as McLuhan's own analysis acknowledges."
    },
}

# =============================================================================
# APPLICATION LOGIC
# =============================================================================

def apply_analysis():
    """Apply Pass 1 and Pass 2 analysis to the database."""
    from pass2_analysis import PASS2

    # Load database
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)

    # Create backup
    import shutil
    if not os.path.exists(BACKUP_PATH):
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print(f"Backup created: {BACKUP_PATH}")

    spreads = db['spreads']
    updated = 0
    skipped = 0

    for spread in spreads:
        sid = spread['id']

        # Apply Pass 1
        if sid in PASS1:
            p1 = PASS1[sid]

            # Update rhetoric.argument
            if 'argument' in p1:
                spread['rhetoric']['argument'] = p1['argument']

            # Update themes
            if 'contemporary_domain_candidates' in p1:
                spread['themes']['contemporary_domain_candidates'] = p1['contemporary_domain_candidates']
            if 'movement_mapping' in p1:
                spread['themes']['movement_mapping'] = p1['movement_mapping']
            if 'mapping_rationale' in p1:
                spread['themes']['mapping_rationale'] = p1['mapping_rationale']

            # Update notes
            if 'notes' in p1:
                spread['notes'] = p1['notes']

            # Update design_enacts_argument if provided
            if 'design_enacts_argument' in p1:
                spread['rhetoric']['design_enacts_argument'] = p1['design_enacts_argument']
            if 'design_argument_description' in p1:
                spread['rhetoric']['design_argument_description'] = p1['design_argument_description']

            updated += 1
        else:
            skipped += 1

        # Apply Pass 2
        if sid in PASS2:
            p2 = PASS2[sid]

            if 'relationship_to_previous' in p2:
                spread['progression']['relationship_to_previous'] = p2['relationship_to_previous']
            if 'relationship_to_next' in p2:
                spread['progression']['relationship_to_next'] = p2['relationship_to_next']
            if 'multi_spread_patterns' in p2:
                spread['rhetoric']['multi_spread_patterns'] = p2['multi_spread_patterns']

    # Update metadata
    db['metadata']['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
    db['metadata']['analysis_model'] = 'claude-opus-4-6+qwen3-vl (phase_b_v2 enrichment)'

    # Write updated database
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"Analysis applied successfully!")
    print(f"  Pass 1 updated: {updated} spreads")
    print(f"  Pass 1 skipped (no data): {skipped} spreads")
    print(f"  Pass 2 relationships: {len(PASS2)} spreads")
    print(f"  Database saved to: {DB_PATH}")

    # Verification
    verify_analysis(db)


def verify_analysis(db):
    """Run quality checks on the updated database."""
    spreads = db['spreads']

    empty_arguments = 0
    empty_domains = 0
    empty_movements = 0
    empty_rationale = 0
    empty_prev = 0
    empty_next = 0
    brief_arguments = 0

    for s in spreads:
        sid = s['id']
        arg = s['rhetoric'].get('argument', '')
        domains = s['themes'].get('contemporary_domain_candidates', [])
        movements = s['themes'].get('movement_mapping', [])
        rationale = s['themes'].get('mapping_rationale', '')
        prev_rel = s['progression'].get('relationship_to_previous', '')
        next_rel = s['progression'].get('relationship_to_next', '')

        if not arg:
            empty_arguments += 1
        elif len(arg) < 50 or 'Brief textual element' in arg:
            brief_arguments += 1
        if not domains:
            empty_domains += 1
        if not movements:
            empty_movements += 1
        if not rationale:
            empty_rationale += 1
        if not prev_rel and sid != 'spread_001':
            empty_prev += 1
        if not next_rel and sid != 'spread_085':
            empty_next += 1

    print(f"\n=== Verification Report ===")
    print(f"  Empty arguments: {empty_arguments}/85")
    print(f"  Brief/auto-gen arguments: {brief_arguments}/85")
    print(f"  Empty domain candidates: {empty_domains}/85")
    print(f"  Empty movement mappings: {empty_movements}/85")
    print(f"  Empty mapping rationale: {empty_rationale}/85")
    print(f"  Empty relationship_to_previous: {empty_prev}/84 (excl. first)")
    print(f"  Empty relationship_to_next: {empty_next}/84 (excl. last)")

    if (empty_arguments + brief_arguments + empty_domains + empty_movements +
            empty_rationale + empty_prev + empty_next) == 0:
        print("  [OK] All fields populated successfully!")
    else:
        total_gaps = (empty_arguments + brief_arguments + empty_domains +
                     empty_movements + empty_rationale + empty_prev + empty_next)
        print(f"  [!] {total_gaps} gaps remaining")


if __name__ == '__main__':
    apply_analysis()
