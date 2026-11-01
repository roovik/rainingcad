SEASONS_STRIP=[("Winter","Weeks 1&ndash;11","Jan 3 &ndash; Mar 20","11 breeds"),
               ("Spring","Weeks 12&ndash;24","Mar 21 &ndash; Jun 19","13 breeds"),
               ("Summer","Weeks 25&ndash;37","Jun 20 &ndash; Sep 18","13 breeds"),
               ("Fall","Weeks 38&ndash;50","Sep 19 &ndash; Dec 18","13 breeds")]
CFG={
 "winter":{"name":"Winter","first":1,"last":11,"count":"eleven","Count":"Eleven"},
 "spring":{"name":"Spring","first":12,"last":24,"count":"thirteen","Count":"Thirteen"},
 "summer":{"name":"Summer","first":25,"last":37,"count":"thirteen","Count":"Thirteen"},
 "fall":{"name":"Fall","first":38,"last":50,"count":"thirteen","Count":"Thirteen"}}
for k,v in CFG.items(): v["kicker"]=f'{v["name"]} &middot; '+{"winter":"Weeks 1&ndash;11","spring":"Weeks 12&ndash;24","summer":"Weeks 25&ndash;37","fall":"Weeks 38&ndash;50"}[k]
ESSAYS={
"winter":["For a cat, winter arrives as a map of warm places. The radiator. The laptop. The patch of floor where the sun lands at ten past two. Overnight, the whole house reorganizes itself around heat, and a cat who ignored the sofa all summer is suddenly its most loyal resident.",
 "Some cats were built for this. The Norwegian Forest Cat and the Siberian wear thick double coats that laugh at the cold. The Birman and the Turkish Angora carry their winter silk as if it were nothing. For them, snow is a view.",
 "Others have different plans. The Sphynx would like a heated blanket, a lap, and a word with whoever lowered the thermostat. The Devon Rex would like to be inside your sweater. The Abyssinian would like to be somewhere else entirely, and will find a way.",
 "For those who love them, winter is the season of closeness. The days shorten. The evenings lengthen. The lap fills up. In the dark months a cat asks for little and gives a great deal. Warmth against your feet. A slow purr in the next room. A reason to stay in, and a reason to be glad of it.",
 "Every cold morning with a cat holds a small lesson. Find the warm spot. Stay in it. Stretch when you are ready, and not before.",
 "These are the Cats of Winter. Eleven weeks, eleven friends, and one long, quiet season to enjoy them."],
"spring":["For a cat, spring arrives at the window. The glass fills with birds. The air through the screen carries a hundred new smells at once. A cat who spent the winter asleep is suddenly on watch, and the sill becomes a post that must be held from dawn.",
 "Some cats were born for the thaw. The Maine Coon patrols the yard like a small lion. The Bengal and the Savannah treat the garden as a jungle that has been waiting for them. The Egyptian Mau, one of the fastest of the domestic breeds, would like a head start.",
 "Others bring their opinions. The Siamese and the Oriental Shorthair narrate the season in full sentences. The Persian and the Exotic Shorthair watch the sun move across the rug and approve. The Russian Blue observes the new arrivals in silence and files a report.",
 "Then there are the cats who came for the company. The Ragdoll goes limp in the first warm lap of the year. The Scottish Fold sits upright in the doorway like a small, round neighbor.",
 "For those who love them, spring is the season of the open door. Windows go up. Sunbeams come back. A cat pauses on the threshold, weighs the whole outdoors, and decides to think about it.",
 "These are the Cats of Spring. Thirteen weeks, thirteen friends, and one long, green season to enjoy them."],
"summer":["For a cat, summer is the season of the long afternoon. The days run slow. The floor is cool. Every shady corner has been tested, ranked, and assigned to a nap, and nobody is in a hurry to get up.",
 "Some cats were built for the heat of it. The Somali and the Singapura come from warm places and are happiest where the sun is strong. The Turkish Van is known as the swimming cat, and has been seen to wade into a lake on purpose. The Balinese and the Tonkinese would like a patch of sun and an audience.",
 "Others take a quieter view. The Himalayan and the Ragamuffin sprawl across the coolest tile in the house. The Nebelung and the Havana Brown watch the garden from the shade. The Bombay, a small black panther in the living room, prefers the dim of a closed curtain.",
 "And then there are the cats with places to be. The Manx runs the hallway at dusk like a short, determined comet. The Korat and the Selkirk Rex patrol the porch. Every summer evening someone finds a moth, and the whole household takes an interest.",
 "For those who love them, summer is the season of the long evening. The porch light comes on late. A cat settles on the warm step, half asleep, fully on duty. Every summer day with a cat is a small vacation, taken at its own pace.",
 "These are the Cats of Summer. Thirteen weeks, thirteen friends, and one long, golden season to enjoy them."],
"fall":["For a cat, fall arrives as a change in the light. The air turns crisp. The leaves come down, and every one of them is a toy. The window gets a new view, and a cat who napped all summer remembers that it has a great deal to do.",
 "Some cats treat the season as a hunt. The American Bobtail, the Pixiebob and the Chausie like the look of a leaf pile. The Toyger and the Ocicat wear the colors of the woods. The Lykoi, the so-called werewolf cat, looks right at home in the October dusk.",
 "Others treat it as a reason to come inside. The LaPerm and the American Curl would like a blanket and a place near the fire. The Peterbald and the Donskoy, nearly bare, would like a sunny sill, a warm lap, and not one more word about the draft.",
 "For those who love them, fall is the season of coming home. The days grow short. The lamp comes on early. The kitchen smells of something good, and a cat waits at the door as if you had been gone for years. Rake the leaves. Then sit with the cat, and let the evening arrive.",
 "These are the Cats of Fall. Thirteen weeks, thirteen friends, and one long, amber season to enjoy them."]}
