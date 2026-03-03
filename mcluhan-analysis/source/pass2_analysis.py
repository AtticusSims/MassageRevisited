"""
Pass 2 analysis: Sequential progression relationships and multi-spread patterns.
Imported by apply_analysis.py.
"""

# =============================================================================
# PASS 2: Sequential Relationships
# Fields: relationship_to_previous, relationship_to_next, multi_spread_patterns
# =============================================================================

PASS2 = {
    "spread_001": {
        "relationship_to_previous": "",
        "relationship_to_next": "The cover's visual thesis (media as immersive environment) gives way to the blurb's verbal marketing—the transition from design-as-argument to text-as-commerce immediately demonstrates the gap between the book's formal innovation and its commercial packaging.",
        "multi_spread_patterns": None
    },
    "spread_002": {
        "relationship_to_previous": "The blurb page translates the cover's visual thesis into promotional language, creating an ironic tension: the book's radical content is packaged in the conventional form it critiques.",
        "relationship_to_next": "Moves from commercial framing to institutional framing—publisher credits and copyright represent the legal/economic infrastructure that makes the book possible as a commodity.",
        "multi_spread_patterns": "spreads_001_003:front_matter_sequence: Cover → blurb → credits form a three-spread institutional frame that the book's content will progressively undermine."
    },
    "spread_003": {
        "relationship_to_previous": "Credits extend the institutional apparatus begun in the blurb, revealing the collaborative production (McLuhan/Fiore/Agel) that the single-author convention obscures.",
        "relationship_to_next": "The transition from institutional credits to the Browning epigraph marks the shift from commercial framing to intellectual framing—from 'who made this' to 'how to approach it.'",
        "multi_spread_patterns": None
    },
    "spread_004": {
        "relationship_to_previous": "The Browning epigraph pivots from institutional framing (credits) to cognitive preparation, establishing the reader's stance toward the challenging material ahead.",
        "relationship_to_next": "The epigraph's invitation to 'reach beyond your grasp' prepares the reader for the title page's visual overwhelm—the cognitive stretch begins immediately.",
        "multi_spread_patterns": "spreads_004_085:epigraph_bookend: The Browning epigraph ('reach should exceed grasp') at the beginning pairs with the Whitehead quotation ('business of the future to be dangerous') at the end, framing the entire book as an exercise in productive cognitive risk."
    },
    "spread_005": {
        "relationship_to_previous": "The title page delivers on the epigraph's promise of cognitive stretching: the oversized typography forces the reader to experience reading as environmental encounter rather than information transfer.",
        "relationship_to_next": "The title splits across the page turn, forcing the reader to experience the book's physical structure as part of its message—the materiality of the medium becomes unavoidable.",
        "multi_spread_patterns": "spreads_005_007:title_sequence: The title unfolds across three spreads (The Medium is the / Massage / and how!) creating a temporal experience that enacts the book's thesis about sequential media."
    },
    "spread_006": {
        "relationship_to_previous": "Completes the title begun on the previous spread, proving through physical experience that meaning in this book is temporally distributed across the act of reading.",
        "relationship_to_next": "The completion of the title gives way to the sardonic 'and how!' which shifts register from declarative to comedic, establishing the book's tonal range.",
        "multi_spread_patterns": None
    },
    "spread_007": {
        "relationship_to_previous": "The comedic 'and how!' deflates the title's theoretical gravity, establishing humor as a legitimate analytical mode that will recur throughout the book.",
        "relationship_to_next": "The joke transitions to the book's first serious theoretical declaration ('All media work us over completely'), establishing the pattern of oscillation between humor and gravity.",
        "multi_spread_patterns": None
    },
    "spread_008": {
        "relationship_to_previous": "After the title sequence's demonstration, this spread states the thesis explicitly—the reader has already experienced it physically and now receives it verbally.",
        "relationship_to_next": "The general claim ('work us over completely') leads to specific enumeration of the domains of effect, moving from assertion to evidence.",
        "multi_spread_patterns": "spreads_008_010:thesis_statement: Three spreads unfold the core thesis progressively: media work us over completely → in every domain → by shaping scale and form of association."
    },
    "spread_009": {
        "relationship_to_previous": "Elaborates the preceding claim of 'completeness' by listing specific domains, transforming abstract assertion into concrete enumeration.",
        "relationship_to_next": "The enumeration of domains leads to the mechanism: media don't just affect these domains, they shape and control the 'scale and form' of human association within them.",
        "multi_spread_patterns": None
    },
    "spread_010": {
        "relationship_to_previous": "Completes the thesis by revealing the mechanism: not just 'working us over' but specifically 'shaping and controlling the scale and form of human association and action.'",
        "relationship_to_next": "The completed thesis immediately yields to the 'inventory' section—having stated what media do, the book now demonstrates it through specific examples beginning with 'you.'",
        "multi_spread_patterns": None
    },
    "spread_011": {
        "relationship_to_previous": "The inventory section begins by applying the preceding thesis to the reader's own life—'you' as the first item makes the theoretical claim personal and immediate.",
        "relationship_to_next": "Expands outward from individual ('you') to domestic ('your family') to communal ('your neighborhood'), tracing concentric circles of media influence.",
        "multi_spread_patterns": "spreads_011_016:inventory_sequence: Six spreads trace expanding circles of media influence: you → family → neighborhood → education → job → government → others, demonstrating the thesis of completeness through systematic enumeration."
    },
    "spread_012": {
        "relationship_to_previous": "Expands the inventory from individual and family to institutional domains (neighborhood, education), escalating the scope of media's environmental reach.",
        "relationship_to_next": "The mention of education prepares for the rotated-text spread that forces the reader to physically experience educational reorientation.",
        "multi_spread_patterns": None
    },
    "spread_013": {
        "relationship_to_previous": "The rotated text about education physically enacts the reorientation that the preceding spread's inventory intellectually described—theory becomes bodily experience.",
        "relationship_to_next": "Returns to the inventory's expanding circles (your job) after the physical disruption, with the reader now carrying the bodily memory of forced reorientation.",
        "multi_spread_patterns": None
    },
    "spread_014": {
        "relationship_to_previous": "Continues the inventory's expansion from education to labor, each domain demonstrating another area of life constituted by media environments.",
        "relationship_to_next": "From labor to government—the inventory reaches its most public domain before the final expansion to 'the others.'",
        "multi_spread_patterns": None
    },
    "spread_015": {
        "relationship_to_previous": "Escalates from labor to governance, the most explicitly political item in the inventory, arguing that political structures are media artifacts.",
        "relationship_to_next": "The final inventory item ('the others') represents the maximum expansion—from self to the entire social field of otherness.",
        "multi_spread_patterns": None
    },
    "spread_016": {
        "relationship_to_previous": "Completes the inventory's expansion from intimate ('you') to universal ('the others'), demonstrating that media transformation is total in scope.",
        "relationship_to_next": "The completed inventory yields to theoretical explanation: having shown WHAT media affect, the book now explains HOW through the 'extensions' thesis.",
        "multi_spread_patterns": None
    },
    "spread_017": {
        "relationship_to_previous": "The 'extensions' thesis provides the mechanism for the inventory's claims: media affect everything because they are extensions of human faculties themselves.",
        "relationship_to_next": "The abstract thesis immediately yields to concrete demonstration: the foot as the first bodily faculty to be examined.",
        "multi_spread_patterns": "spreads_017_024:extensions_sequence: Eight spreads demonstrate the extensions thesis through escalating examples: foot/wheel → eye/book → skin/clothing → nervous system/circuitry, each pair increasing the stakes from locomotion to consciousness itself."
    },
    "spread_018": {
        "relationship_to_previous": "The bare foot grounds the abstract 'extensions' thesis in physical reality—the body is the starting point for all technological extension.",
        "relationship_to_next": "The unextended foot prepares for its technological partner: the wheel as foot-extension.",
        "multi_spread_patterns": None
    },
    "spread_019": {
        "relationship_to_previous": "Names the relationship between the previously shown foot and its technological extension: 'The wheel is an extension of the foot.'",
        "relationship_to_next": "The verbal statement yields to visual demonstration: the composite foot-wheel image that makes the extension relationship visually concrete.",
        "multi_spread_patterns": None
    },
    "spread_020": {
        "relationship_to_previous": "Visualizes the foot-wheel extension that the preceding spread stated verbally, transforming conceptual metaphor into visual evidence.",
        "relationship_to_next": "The completed foot/wheel pair prepares for the next extension pair: eye/book, escalating from locomotion to perception.",
        "multi_spread_patterns": None
    },
    "spread_021": {
        "relationship_to_previous": "Escalates from physical extension (foot/wheel) to perceptual extension (eye/book), raising the stakes from bodily capacity to cognitive organization.",
        "relationship_to_next": "The statement about the book extending the eye prepares for the eye close-up that mirrors the earlier foot close-up, establishing the visual grammar of the extensions sequence.",
        "multi_spread_patterns": None
    },
    "spread_022": {
        "relationship_to_previous": "The eye close-up parallels the earlier foot close-up, creating a formal rhythm: organ → statement → organ → statement across the extensions sequence.",
        "relationship_to_next": "Transitions from visual perception (eye) to social communication (skin/clothing), expanding the extensions thesis from individual senses to social interfaces.",
        "multi_spread_patterns": None
    },
    "spread_023": {
        "relationship_to_previous": "Expands the extensions thesis from individual sensation (eye) to social communication (clothing/skin), introducing the interpersonal dimension of media extension.",
        "relationship_to_next": "Prepares for the culminating extension: from individual faculties (foot, eye, skin) to the integrative nervous system—the organizing principle of consciousness itself.",
        "multi_spread_patterns": None
    },
    "spread_024": {
        "relationship_to_previous": "The nervous system/electric circuitry pair climaxes the extensions sequence: from individual organs to the total integrative system, from specific faculties to consciousness itself.",
        "relationship_to_next": "The completed extensions sequence yields to cultural commentary (Alice in Wonderland), shifting from systematic demonstration to associative exploration.",
        "multi_spread_patterns": None
    },
    "spread_025": {
        "argument_note": "Uses existing argument field",
        "relationship_to_previous": "After the systematic extensions sequence, Alice introduces a looser, more associative mode—the book shifts from demonstration to exploration.",
        "relationship_to_next": "Alice's epistemological vertigo prepares for the historical analysis of the alphabet and its effects on perception—why the world seems like Wonderland.",
        "multi_spread_patterns": "spreads_025_075:alice_references: Alice in Wonderland appears at three structural points (025, 034, 075/081-082), marking transitions from theory to culture (025), from analysis to wordplay (034), and from arguments to identity crisis (081-082), with Alice serving as the reader's avatar in the media landscape."
    },
    "spread_026": {
        "relationship_to_previous": "The ear/alphabet discussion explains why Alice's world is disorienting: the alphabet restructured consciousness from acoustic immersion to visual linearity, and that restructuring is now being reversed.",
        "relationship_to_next": "The alphabetic analysis leads to deeper historical context about pre-literate consciousness, building the case for what was lost in the translation from ear to eye.",
        "multi_spread_patterns": "spreads_026_034:print_culture_analysis: Nine spreads trace the effects of alphabetic/print technology: from the alphabet's invention through perspective, linear logic, and the prison of sequential consciousness, culminating in Joyce's linguistic breakout."
    },
    "spread_027": {
        "relationship_to_previous": "Elaborates the pre-alphabetic world introduced in the previous spread, establishing the multisensory baseline that alphabetic culture disrupted.",
        "relationship_to_next": "From the lost acoustic paradise to its practical consequences: how address, naming, and location systems created the governable literate subject.",
        "multi_spread_patterns": None
    },
    "spread_028": {
        "relationship_to_previous": "From abstract description of pre-literate wholeness to concrete analysis of how literacy creates addressable, governable identities through naming systems.",
        "relationship_to_next": "From naming systems to the printing press—the technology that industrialized alphabetic culture's tendencies toward uniformity and reproducibility.",
        "multi_spread_patterns": None
    },
    "spread_029": {
        "relationship_to_previous": "The 'ditto device' extends the previous spread's analysis of naming/addressing by showing how print mechanized and scaled these categorization impulses.",
        "relationship_to_next": "From the ditto device's uniformity to its perceptual effects: Renaissance perspective as the visual ideology of print culture.",
        "multi_spread_patterns": None
    },
    "spread_030": {
        "relationship_to_previous": "Renaissance perspective is revealed as a direct effect of the print uniformity described in the previous spread—the vanishing point is a typographic artifact.",
        "relationship_to_next": "The orderly perspective yields to its deliberate disruption: inverted text that shatters the visual conventions perspective established.",
        "multi_spread_patterns": None
    },
    "spread_031": {
        "relationship_to_previous": "The inverted text violently disrupts the orderly visual field that the previous spread's Renaissance perspective exemplified, making print conventions visible through violation.",
        "relationship_to_next": "The typographic disruption continues and intensifies, creating a sustained experience of perceptual instability.",
        "multi_spread_patterns": "spreads_031_032:disruption_pair: Two spreads of sustained typographic disruption create a cumulative experience of print-convention breakdown that mirrors the dissolution of stable media environments."
    },
    "spread_032": {
        "relationship_to_previous": "Continues and intensifies the previous spread's typographic disruption, refusing to let the reader regain perceptual equilibrium.",
        "relationship_to_next": "The textual disruption yields to visual metaphor: prison bars as the image of print culture's perceptual constraints.",
        "multi_spread_patterns": None
    },
    "spread_033": {
        "relationship_to_previous": "The prison bars make visual what the preceding text disruptions demonstrated experientially: print culture constrains perception within invisible bars of linearity and sequence.",
        "relationship_to_next": "The prison image yields to Joyce's verbal escape—if print is a prison, Joyce's wordplay is the jailbreak.",
        "multi_spread_patterns": None
    },
    "spread_034": {
        "relationship_to_previous": "Joyce's wordplay offers a linguistic escape from the print-culture prison depicted in the previous spread, using print's own medium (language) against its constraints.",
        "relationship_to_next": "From the prison of print culture to the liberation of electronic culture: the 'global village' concept emerges as print's constraints dissolve.",
        "multi_spread_patterns": None
    },
    "spread_035": {
        "relationship_to_previous": "The global village represents the post-print condition that the previous nine spreads' analysis of print culture makes intelligible—electronic media create what print destroyed.",
        "relationship_to_next": "The concept of the global village leads to the technological substrate that enables it: electric circuitry as visual pattern.",
        "multi_spread_patterns": "spreads_035_060:movement_2_acceleration: Twenty-five spreads of increasingly rapid-fire analysis, mixing theoretical claims, visual demonstrations, and cultural evidence at an accelerating pace that itself enacts the electric acceleration being described."
    },
    "spread_036": {
        "relationship_to_previous": "The electronic circuitry image provides the material basis for the preceding spread's global village concept—this is the physical infrastructure of electronic interdependence.",
        "relationship_to_next": "From the circuitry's form to its social effects: electronic interdependence as world-recreation.",
        "multi_spread_patterns": None
    },
    "spread_037": {
        "relationship_to_previous": "Articulates the social consequences of the electronic infrastructure shown in the previous spread: interdependence that 'recreates the world.'",
        "relationship_to_next": "From world-recreation to art-as-environment—when the whole world becomes a made thing, the aesthetic dimension becomes total.",
        "multi_spread_patterns": None
    },
    "spread_038": {
        "relationship_to_previous": "The environment-as-art concept extends the previous spread's world-recreation thesis: if electronic media recreate the world, then the world becomes an artwork.",
        "relationship_to_next": "A New Yorker cartoon provides comic relief and cultural evidence after the theoretical escalation.",
        "multi_spread_patterns": None
    },
    "spread_039": {
        "relationship_to_previous": "The cartoon provides a lighter register after the theoretical density, demonstrating that popular culture has already absorbed the insights being theorized.",
        "relationship_to_next": "From humor to the railway example—the book's most concrete demonstration of the medium-is-the-message thesis.",
        "multi_spread_patterns": None
    },
    "spread_040": {
        "relationship_to_previous": "The railway provides concrete historical evidence for the theoretical claims, grounding abstract media theory in indisputable industrial history.",
        "relationship_to_next": "The railway as a bygone medium prepares for the rear-view mirror concept—we see old media clearly but cannot perceive current ones.",
        "multi_spread_patterns": None
    },
    "spread_041": {
        "relationship_to_previous": "The rear-view mirror explains why the railway example is easy to see: we perceive old media's effects clearly while remaining blind to current media, always looking backward.",
        "relationship_to_next": "From the diagnosis of backward-looking perception to its experiential demonstration: information overload as collage.",
        "multi_spread_patterns": None
    },
    "spread_042": {
        "relationship_to_previous": "The information collage provides the experiential counterpart to the rear-view mirror diagnosis: this is what it feels like to be inside a media environment you cannot step outside of.",
        "relationship_to_next": "The visual overload yields to a single word at massive scale—from information cacophony to typographic simplicity.",
        "multi_spread_patterns": None
    },
    "spread_043": {
        "relationship_to_previous": "After the collage's overwhelming complexity, the simple word LOVE at massive scale creates a dramatic contrast—from noise to signal, from many to one.",
        "relationship_to_next": "From the word-as-environment to the diagnosis of forcing new media into old patterns—why we resist the kind of environmental experience LOVE represents.",
        "multi_spread_patterns": None
    },
    "spread_044": {
        "relationship_to_previous": "Explains the resistance to environmental media experiences like LOVE: we keep forcing new media into old patterns rather than perceiving their inherent logic.",
        "relationship_to_next": "The diagnosis of forced old-media-patterns prepares for the ENVIRONMENT split—the book's most dramatic demonstration of making the invisible visible.",
        "multi_spread_patterns": None
    },
    "spread_045": {
        "relationship_to_previous": "The split ENVIRONMENT demonstrates what happens when you stop forcing old patterns and let the medium reveal itself—the book's structure becomes the message.",
        "relationship_to_next": "The second half of ENVIRONMENT completes the page-turn demonstration, making the act of reading itself visible as a media experience.",
        "multi_spread_patterns": "spreads_045_046:environment_split: The word ENVIRONMENT split across two spreads is the book's most concentrated formal demonstration of its thesis—the medium (page break) literally interrupts the message (the word 'environment')."
    },
    "spread_046": {
        "relationship_to_previous": "Completes the ENVIRONMENT split, rewarding the reader's page-turn with the recognition that they have just proven the thesis through their own physical action.",
        "relationship_to_next": "The demonstrated invisibility of environments prepares for the explicit thesis: 'Environments are invisible.'",
        "multi_spread_patterns": None
    },
    "spread_047": {
        "relationship_to_previous": "States explicitly what the ENVIRONMENT split demonstrated experientially: environments are invisible because they constitute the background of all perception.",
        "relationship_to_next": "If environments are invisible, who can perceive them? The artist—introduced in the next spread as the essential counter-environmental figure.",
        "multi_spread_patterns": None
    },
    "spread_048": {
        "relationship_to_previous": "The artist answers the question implicit in environmental invisibility: if environments are invisible to normal perception, the artist's trained sensitivity is the survival equipment that makes them visible.",
        "relationship_to_next": "The artist's serious role is lightened by the entertainer figure—humor as a complementary mode of environmental perception.",
        "multi_spread_patterns": None
    },
    "spread_049": {
        "relationship_to_previous": "The entertainer complements the artist: both perceive environments through unconventional means—the artist through formal sensitivity, the entertainer through humor's incongruity.",
        "relationship_to_next": "From the entertainer to the amateur—another figure whose unconventional perception reveals what expertise obscures.",
        "multi_spread_patterns": "spreads_048_051:perception_figures: Four spreads present figures with enhanced environmental perception: artist, entertainer, amateur, humorist—each perceiving what conventional consciousness misses."
    },
    "spread_050": {
        "relationship_to_previous": "The amateur extends the theme of unconventional perception: like the artist and entertainer, the untrained eye sees what expertise has learned to overlook.",
        "relationship_to_next": "The amateur's unconventional perception connects to humor's probe function—both bypass trained incapacity to perceive environmental patterns.",
        "multi_spread_patterns": None
    },
    "spread_051": {
        "relationship_to_previous": "Humor is theorized as the fourth mode of environmental perception (after art, entertainment, and amateurism), completing the catalogue of anti-environmental probes.",
        "relationship_to_next": "The Dance of Death silhouettes dramatize the stakes: if you cannot perceive media environments, the consequences are existential—technology transitions produce cultural death anxiety.",
        "multi_spread_patterns": None
    },
    "spread_052": {
        "relationship_to_previous": "After the catalogue of perceptual tools (art, humor, amateurism), the Dance of Death shows what happens when environmental perception fails: existential crisis during technological transition.",
        "relationship_to_next": "The death anxiety yields to generational juxtaposition—young and old coexisting across the technological divide.",
        "multi_spread_patterns": None
    },
    "spread_053": {
        "relationship_to_previous": "The generational juxtaposition (young musician, elderly face) humanizes the Dance of Death's abstract anxiety, showing actual people living across the media divide.",
        "relationship_to_next": "From generational difference to pure bodily intimacy—the kiss that transcends all media mediation.",
        "multi_spread_patterns": None
    },
    "spread_054": {
        "relationship_to_previous": "The kiss provides a wordless counterpoint to the preceding intellectual content, asserting that embodied human connection persists beneath all media transformation.",
        "relationship_to_next": "From bodily intimacy to institutional crisis—the youth/education discussion returns to the social consequences of media change.",
        "multi_spread_patterns": None
    },
    "spread_055": {
        "relationship_to_previous": "After the embodied interlude, returns to social analysis: youth culture's rejection of institutional education as a response to media-environment change.",
        "relationship_to_next": "The theoretical analysis of education yields to photographic evidence: the Amherst walkout as documented proof of the clash.",
        "multi_spread_patterns": "spreads_055_058:education_crisis: Four spreads document the generational media clash in education: analysis → walkout photo → Dylan's diagnosis → cartoon/economic evidence."
    },
    "spread_056": {
        "relationship_to_previous": "The walkout photograph provides visual evidence for the preceding spread's analysis of educational crisis—theory confirmed by documented event.",
        "relationship_to_next": "From institutional rejection to cultural diagnosis: Dylan as the voice of the generation that perceives what institutions cannot.",
        "multi_spread_patterns": None
    },
    "spread_057": {
        "relationship_to_previous": "Dylan's 'something is happening' crystallizes the walkout's inarticulate protest into a cultural diagnosis—the musician perceives what the institution misses.",
        "relationship_to_next": "From Dylan's perception to the establishment's bafflement: the ink blot and cartoon show the older generation's inability to comprehend what the younger one perceives.",
        "multi_spread_patterns": None
    },
    "spread_058": {
        "relationship_to_previous": "The establishment's bafflement (ink blot) and grudging acknowledgment (economic cartoon) provide the counterpoint to Dylan's perception—the older generation sees chaos where the younger sees pattern.",
        "relationship_to_next": "From contemporary generational conflict to historical pattern: the Joyce/multi-exposure spread reveals that this conflict recurs with every media transition.",
        "multi_spread_patterns": None
    },
    "spread_059": {
        "relationship_to_previous": "The Joycean wordplay and multi-exposure photograph reframe the contemporary generational conflict within a recurring historical pattern of media transition.",
        "relationship_to_next": "From historical pattern to perceptual theory: the BANG!/ear-space discussion provides the theoretical framework for understanding acoustic vs. visual consciousness.",
        "multi_spread_patterns": None
    },
    "spread_060": {
        "relationship_to_previous": "The ear/acoustic-space theory provides the perceptual framework that explains the historical and generational conflicts traced in preceding spreads—it is ultimately about sensory reorganization.",
        "relationship_to_next": "From acoustic-space theory to its historical precedent: Socrates' warning about the alphabet destroying oral memory, marking the transition to the Hinge section.",
        "multi_spread_patterns": None
    },
    "spread_061": {
        "relationship_to_previous": "The Socratic warning about writing parallels the contemporary media anxieties just traced, revealing that the pattern of media-transition anxiety is as old as literacy itself.",
        "relationship_to_next": "From Socrates' anxiety about lost memory to the commercial exploitation of that loss: memory courses as commodified nostalgia for oral faculties.",
        "multi_spread_patterns": "spreads_061_065:hinge_section: Five spreads bridge Movements 2 and 3, moving from the deepest historical perspective (Socrates) through media archaeology (punctuation, voiceprints) to the literary synthesis (Joyce) that makes the transition to the dreamscape possible."
    },
    "spread_062": {
        "relationship_to_previous": "The memory advertisement ironically commodifies the oral faculty that Socrates warned literacy would destroy—the market exploits the very loss the philosopher mourned.",
        "relationship_to_next": "From memory's commodification to the visual traces of orality: punctuation marks as acoustic encoding within print.",
        "multi_spread_patterns": None
    },
    "spread_063": {
        "relationship_to_previous": "Punctuation marks reveal print's hidden acoustic dimension, connecting to the memory/orality theme by showing how visual text retains vestiges of vocal performance.",
        "relationship_to_next": "From punctuation's acoustic traces to voiceprints' visual traces—sound made visible through electronic technology, reversing the alphabet's original translation.",
        "multi_spread_patterns": None
    },
    "spread_064": {
        "relationship_to_previous": "Voiceprints reverse the alphabet's trajectory: where the alphabet made sound visible as letters, electronic technology makes sound visible as waveforms—a new kind of sensory translation.",
        "relationship_to_next": "From voiceprints to Joyce's ear—the literary artist who synthesized all modes of consciousness, positioned at the Hinge as the figure who bridges all transitions.",
        "multi_spread_patterns": None
    },
    "spread_065": {
        "relationship_to_previous": "Joyce synthesizes the Hinge section's themes: oral memory, acoustic consciousness, visual encoding, and electronic simultaneity converge in Finnegans Wake's multi-modal prose.",
        "relationship_to_next": "From Joyce's literary synthesis to the specific institutional crisis of authorship and copyright in the electronic age—from art to economics.",
        "multi_spread_patterns": None
    },
    "spread_066": {
        "relationship_to_previous": "The copyright/authorship discussion translates the Hinge section's theoretical insights into institutional terms: if electronic media dissolve print consciousness, they also dissolve print-era legal structures.",
        "relationship_to_next": "From the crisis of authorship to the rise of television—the specific electronic medium that most dramatically challenges print-era institutions.",
        "multi_spread_patterns": "spreads_066_070:media_institutions: Five spreads trace how electronic media (especially television and film) transform print-era institutions: authorship/copyright → television's sensory demands → TV's ritual function → critical misperception → cinema's revolutionary effects."
    },
    "spread_067": {
        "relationship_to_previous": "Television is introduced as the medium that most directly threatens the authorship/copyright structures described in the previous spread—it demands participation rather than consumption.",
        "relationship_to_next": "From television's theoretical description to its most powerful demonstration: the Kennedy funeral as shared national ritual.",
        "multi_spread_patterns": None
    },
    "spread_068": {
        "relationship_to_previous": "The Kennedy funeral demonstrates the participatory power theorized in the previous spread—200 million simultaneous mourners participating in a television ritual.",
        "relationship_to_next": "From television's power to its critical misunderstanding: critics who judge TV by print standards miss its essential nature.",
        "multi_spread_patterns": None
    },
    "spread_069": {
        "relationship_to_previous": "The critique of television critics applies the rear-view mirror concept (spread 041) to a specific case: judging TV through print-culture categories guarantees misperception.",
        "relationship_to_next": "From television's misperception to cinema's unexpected revolutionary effects—another case of media effects exceeding intended content.",
        "multi_spread_patterns": None
    },
    "spread_070": {
        "relationship_to_previous": "Cinema's revolutionary effects extend the previous spread's theme: media produce unintended consequences that exceed their creators' purposes or their critics' categories.",
        "relationship_to_next": "From cinema's political effects to art's environmental transformation—the giant 'A' begins the three-spread 'Art is anything you can get away with' sequence.",
        "multi_spread_patterns": None
    },
    "spread_071": {
        "relationship_to_previous": "The giant 'A' begins a three-spread sentence about art that extends the institutional analysis from media (cinema, TV) to aesthetics—art as the ultimate anti-environment.",
        "relationship_to_next": "The 'A' continues into 'is anything'—the sentence unfolds across page turns like the earlier ENVIRONMENT split.",
        "multi_spread_patterns": "spreads_071_073:art_definition: Three spreads spell out 'Art is anything you can get away with,' splitting the sentence across page turns to make the definition itself an environmental art experience."
    },
    "spread_072": {
        "relationship_to_previous": "Continues the art definition with 'is anything,' accompanied by the walk-through sculpture that demonstrates art's environmental scale.",
        "relationship_to_next": "Completes the sentence with 'you can get away with,' pairing the definition with cultural evidence (Beatles, Balinese art philosophy).",
        "multi_spread_patterns": None
    },
    "spread_073": {
        "relationship_to_previous": "Completes 'Art is anything you can get away with' and provides cultural evidence: Beatles meeting the PM, Balinese art philosophy, museum as cultural bloodbank.",
        "relationship_to_next": "From art's dissolution of boundaries to war's transformation by media—the hot/cold war analysis uses Monroe and Khrushchev.",
        "multi_spread_patterns": None
    },
    "spread_074": {
        "relationship_to_previous": "From art's boundary-dissolution to war's transformation: both represent institutions fundamentally restructured by electronic media environments.",
        "relationship_to_next": "The information-war thesis is illustrated by Alice's chaotic battle scene—war as Wonderland.",
        "multi_spread_patterns": "spreads_074_076:war_and_propaganda: Three spreads trace the transformation of conflict from physical to informational: hot/cold war → Alice's chaotic battle → environment as propaganda."
    },
    "spread_075": {
        "relationship_to_previous": "Alice's battle scene visualizes the chaotic, boundary-less information warfare described in the preceding spread—combatants indistinguishable from civilians.",
        "relationship_to_next": "From war's chaos to the diagnosis: the environment itself is propaganda, and dialogue (not protest) is the response.",
        "multi_spread_patterns": None
    },
    "spread_076": {
        "relationship_to_previous": "The environment-as-propaganda thesis explains the chaotic warfare of the preceding spreads: when the environment itself is ideological, traditional forms of opposition become formatted by the system they oppose.",
        "relationship_to_next": "From propaganda to philosophy: Laotze's emptiness-as-function offers an Eastern alternative to Western media-saturation.",
        "multi_spread_patterns": None
    },
    "spread_077": {
        "relationship_to_previous": "Laotze's philosophy provides an alternative framework to the Western propaganda problem: Eastern concepts of emptiness, flow, and integration offer perceptual resources for navigating electronic environments.",
        "relationship_to_next": "From Eastern philosophy to Western theology: the 'God is dead' discussion as another institutional crisis caused by media transformation.",
        "multi_spread_patterns": "spreads_076_079:dreamscape_philosophy: Four spreads move through escalating philosophical territory: propaganda → Eastern philosophy → theology → technological apocalypse, preparing for the book's final prescriptive sequence."
    },
    "spread_078": {
        "relationship_to_previous": "The God-is-alive banner extends the East-West convergence: electronic media make old Newtonian certainties dissolve while creating new conditions for mystical/networked forms of belief.",
        "relationship_to_next": "From the dissolution of the Newtonian God to the revelation of the electrical god: the blackout makes invisible technological infrastructure suddenly apparent.",
        "multi_spread_patterns": None
    },
    "spread_079": {
        "relationship_to_previous": "The blackout dramatically demonstrates the preceding spread's theme: the old God (Newtonian mechanism) is dead, but the new god (electrical infrastructure) reveals itself only through failure.",
        "relationship_to_next": "From technological revelation to practical prescription: the surfer-in-the-maelstrom as the model for navigating media environments.",
        "multi_spread_patterns": None
    },
    "spread_080": {
        "relationship_to_previous": "The surfer provides the practical response to the blackout's revelation: if you cannot escape the media environment, learn to surf its patterns from within.",
        "relationship_to_next": "From the surfer's practical wisdom to the identity crisis that media environments produce: the numbered, faceless figures confront the question 'who are you?'",
        "multi_spread_patterns": None
    },
    "spread_081": {
        "relationship_to_previous": "The identity crisis follows logically from the surfer's media navigation: even if you can ride the maelstrom, the question of who 'you' are within it remains unresolved.",
        "relationship_to_next": "Alice's answer—'I must have been changed several times since then'—provides the definitive statement of electronic-age identity as fluid and environmentally determined.",
        "multi_spread_patterns": "spreads_081_082:identity_crisis: Two spreads confront the book's final question—'who are you?'—with numbered faceless figures and Alice's admission of continuous transformation, defining electronic-age identity as fluid rather than fixed."
    },
    "spread_082": {
        "relationship_to_previous": "Alice's response completes the identity crisis introduced by the previous spread's faceless numbered figures, accepting fluid identity as the electronic-age condition.",
        "relationship_to_next": "From Alice's philosophical acceptance to the generational translation: a son explaining McLuhan to his book-formed father, comedy as conclusion.",
        "multi_spread_patterns": None
    },
    "spread_083": {
        "relationship_to_previous": "The cartoon translates the book's theoretical argument into domestic comedy, showing McLuhan's ideas circulating through the very generational gap they describe.",
        "relationship_to_next": "From the cartoon's self-aware humor to the credits page that reveals the book's own media archaeology—assembled from the fragments of mass media culture.",
        "multi_spread_patterns": None
    },
    "spread_084": {
        "relationship_to_previous": "The credits page follows the cartoon's self-referential humor with self-referential documentation, revealing the book's own construction from media fragments.",
        "relationship_to_next": "The institutional documentation of credits yields to the final philosophical statement: Whitehead's mandate for courageous engagement with the dangerous future.",
        "multi_spread_patterns": None
    },
    "spread_085": {
        "relationship_to_previous": "The Whitehead quotation closes the philosophical arc begun by the Browning epigraph (spread 004): from 'reach should exceed grasp' to 'the future must be dangerous'—cognitive risk as both opening and closing mandate.",
        "relationship_to_next": "",
        "multi_spread_patterns": None
    },
}
