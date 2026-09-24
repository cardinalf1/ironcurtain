"""
The Iron Curtain - Canonical Historical Timeline & Curriculum Database (1945-1953)
Provides factual ground-truth context for the 'History Mirror' debrief engine.
"""

HISTORICAL_YEARS = {
    1945: {
        "title": "Post-Potsdam Dawn: The Division of the World",
        "key_actors": ["Harry S. Truman", "Joseph Stalin", "Clement Attlee", "Chiang Kai-shek", "Mao Zedong"],
        "summary": "World War II concludes in Europe and Asia. The Potsdam Conference cements the quadripartite occupation of Germany and Berlin. The United States conducts the Trinity test and drops atomic bombs on Hiroshima and Nagasaki, inaugurating the nuclear age. The Soviet Union moves swiftly to install friendly communist regimes across Eastern Europe while Korean partition along the 38th parallel begins.",
        "real_world_events": [
            "August 1945: Atomic bombings of Hiroshima and Nagasaki force unconditional Japanese surrender.",
            "July-August 1945: Potsdam Conference establishes Allied Control Council and German occupation zones.",
            "September 1945: USSR solidifies military control over Poland, Romania, Bulgaria, and Hungary.",
            "November 1945: Soviets delay withdrawal from northern Iran (Azerbaijan Crisis) in violation of wartime agreements.",
            "December 1945: Division of Korea into Soviet (North) and American (South) zones of occupation."
        ],
        "flashpoints": [
            {"lat": 52.52, "lon": 13.40, "name": "Occupied Berlin & Germany", "tension": 40},
            {"lat": 35.68, "lon": 51.38, "name": "Northern Iran Crisis", "tension": 55},
            {"lat": 38.00, "lon": 127.00, "name": "Korean 38th Parallel", "tension": 30}
        ],
        "discussion_questions": [
            "Did the atomic bomb end WWII or begin the Cold War?",
            "Could a shared international control system (like the Baruch Plan) have realistically prevented an arms race in 1945?",
            "How did the devastation of Europe leave a power vacuum that forced local nations to pick superpower allegiances?"
        ],
        "historical_defcon": 4,
        "historical_us_nukes": 2,
        "historical_ussr_nukes": 0
    },
    1946: {
        "title": "The Iron Curtain Descends: The Long Telegram & Fulton",
        "key_actors": ["Winston Churchill", "George F. Kennan", "Vyacheslav Molotov", "Nikolai Novikov"],
        "summary": "Diplomatic pleasantries evaporate. George Kennan's 8,000-word 'Long Telegram' from Moscow outlines the Soviet worldview and lays the conceptual foundation for Containment. Winston Churchill delivers his 'Sinews of Peace' address in Fulton, Missouri, warning that 'from Stettin in the Baltic to Trieste in the Adriatic, an iron curtain has descended across the Continent.' The Baruch Plan for international atomic disarmament is vetoed, sealing an inevitable nuclear race.",
        "real_world_events": [
            "February 1946: George F. Kennan sends the 'Long Telegram' from the US Embassy in Moscow.",
            "March 1946: Winston Churchill delivers the 'Iron Curtain' speech at Westminster College, Fulton, MO.",
            "June 1946: Bernard Baruch presents the US atomic disarmament plan to the UN; USSR rejects inspections and demands immediate US bomb destruction.",
            "September 1946: Soviet Ambassador Nikolai Novikov sends a counter-telegram accusing the US of striving for world supremacy.",
            "Autumn 1946: The Greek Civil War escalates between monarchists backed by the UK and communist partisans backed by Yugoslavia."
        ],
        "flashpoints": [
            {"lat": 37.98, "lon": 23.72, "name": "Greek Civil War (Athens / Epirus)", "tension": 60},
            {"lat": 39.90, "lon": 32.85, "name": "Turkish Straits Crisis", "tension": 65},
            {"lat": 53.55, "lon": 14.55, "name": "Stettin-Trieste Demarcation", "tension": 45}
        ],
        "discussion_questions": [
            "Was the Cold War driven more by ideological fundamentalism or classic great-power balance-of-power geopolitics?",
            "Why did both Washington and Moscow view the other's defensive moves as aggressive encirclement?",
            "How did non-nuclear powers (like the UK, France, and China) navigate being junior partners or battlegrounds?"
        ],
        "historical_defcon": 4,
        "historical_us_nukes": 9,
        "historical_ussr_nukes": 0
    },
    1947: {
        "title": "Containment & The Marshall Plan: Lines Drawn in the Sand",
        "key_actors": ["Harry S. Truman", "George C. Marshall", "Andrei Zhdanov", "Jawaharlal Nehru"],
        "summary": "With Britain on the brink of financial insolvency and unable to sustain military aid to Greece and Turkey, Truman announces the 'Truman Doctrine'—declaring that the US must assist free peoples resisting subjugation by armed minorities or outside pressures. Secretary of State George Marshall unveils the European Recovery Program (Marshall Plan). Stalin forbids Eastern European satellites from accepting aid and founds the Cominform to enforce rigid ideological discipline. Meanwhile, India achieves independence.",
        "real_world_events": [
            "March 1947: Truman delivers his address to Congress requesting $400M in emergency aid for Greece and Turkey.",
            "June 1947: Harvard Commencement Address: General Marshall outlines the $13 billion economic recovery package for Europe.",
            "August 1947: Indian Independence and Partition; Jawaharlal Nehru champions a path of non-alignment.",
            "September 1947: Andrei Zhdanov outlines the 'Two Camps' doctrine at the founding of the Communist Information Bureau (Cominform).",
            "December 1947: France and Italy face massive communist-led general strikes, heightening US fears of subversion."
        ],
        "flashpoints": [
            {"lat": 39.93, "lon": 116.40, "name": "Chinese Civil War Turning Point", "tension": 70},
            {"lat": 48.85, "lon": 2.35, "name": "Western European Labor Strikes", "tension": 50},
            {"lat": 28.61, "lon": 77.20, "name": "Indian Partition & Non-Alignment", "tension": 35}
        ],
        "discussion_questions": [
            "Was the Marshall Plan an act of humanitarian generosity or economic imperialism designed to open captive markets?",
            "Why was economic reconstruction viewed as a more potent weapon against communism than military divisions?",
            "Could India remain truly neutral between two armed ideological giants?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 13,
        "historical_ussr_nukes": 0
    },
    1948: {
        "title": "The First Crisis: The Berlin Blockade & Tito-Stalin Split",
        "key_actors": ["Ernst Reuter", "Lucius D. Clay", "Josip Broz Tito", "Jan Masaryk", "Joseph Stalin"],
        "summary": "In February, Czechoslovakian communists execute a police coup; Foreign Minister Jan Masaryk is found dead in Prague. In Western Germany, the Allies introduce the Deutsche Mark, sparking outrage in Moscow. On June 24, Soviet forces sever all road, rail, and canal links to West Berlin. General Lucius Clay and Ernst Reuter coordinate 'Operation Vittles'—the Berlin Airlift—flying in 2.3 million tons of food and coal over 324 days. Simultaneously, Yugoslavia breaks with Moscow in a stunning display of communist heterodoxy.",
        "real_world_events": [
            "February 1948: Czechoslovak Coup d'état establishes an authoritarian communist regime in Prague.",
            "June 1948: Western Allies unify economic zones and launch the Deutsche Mark; USSR initiates the Berlin Blockade.",
            "June 1948: Operation Vittles begins; US and RAF cargo aircraft fly around-the-clock sorties into Tempelhof and Gatow.",
            "June 1948: Tito-Stalin split: Cominform expels Yugoslavia; Tito turns to Western loans and grain to survive Soviet embargo.",
            "December 1948: UN adopts the Universal Declaration of Human Rights and Genocide Convention."
        ],
        "flashpoints": [
            {"lat": 52.52, "lon": 13.40, "name": "Berlin Air Corridors (Airlift)", "tension": 85},
            {"lat": 50.07, "lon": 14.43, "name": "Prague Coup D'état", "tension": 65},
            {"lat": 44.78, "lon": 20.44, "name": "Yugoslav-Soviet Border Tensions", "tension": 75}
        ],
        "discussion_questions": [
            "Why did neither Truman nor Stalin want to shoot down transport planes or ram blockades during Berlin 1948?",
            "How did Yugoslavia's independent defiance complicate the simplistic American view of monolithic communism?",
            "What risks did the Berlin Airlift carry for accidental escalation into World War III?"
        ],
        "historical_defcon": 2,
        "historical_us_nukes": 50,
        "historical_ussr_nukes": 0
    },
    1949: {
        "title": "Twin Shocks: The Soviet Bomb & The Fall of China",
        "key_actors": ["Mao Zedong", "Igor Kurchatov", "Dean Acheson", "Konrad Adenauer", "Klaus Fuchs"],
        "summary": "The year that altered the global equilibrium. In April, twelve Western nations sign the North Atlantic Treaty (NATO). In May, Stalin lifts the failed Berlin Blockade. On August 29, the Soviet Union detonates its first atomic bomb ('RDS-1' or 'Joe-1') at Semipalatinsk, ending the American nuclear monopoly years ahead of CIA estimates thanks to Klaus Fuchs' espionage. In October, Mao Zedong proclaims the People's Republic of China on Tiananmen Square, plunging Washington into bitter domestic recrimination.",
        "real_world_events": [
            "April 1949: North Atlantic Treaty Organization (NATO) created in Washington (Article 5 collective defense).",
            "May 1949: USSR formally ends the Berlin Blockade after 11 months of Allied airlift.",
            "May & October 1949: Federal Republic of Germany (West) and German Democratic Republic (East) are founded.",
            "August 1949: USSR detonates RDS-1 atomic weapon at Semipalatinsk; US spy planes detect radioactive isotopes over the Pacific.",
            "October 1949: Mao Zedong proclaims the founding of the People's Republic of China; Chiang Kai-shek flees to Taiwan."
        ],
        "flashpoints": [
            {"lat": 50.43, "lon": 78.22, "name": "Semipalatinsk Nuclear Test Site", "tension": 80},
            {"lat": 39.90, "lon": 116.40, "name": "Proclamation of PRC in Beijing", "tension": 75},
            {"lat": 25.03, "lon": 121.56, "name": "Taiwan Strait Evacuation", "tension": 70}
        ],
        "discussion_questions": [
            "How did the loss of the atomic monopoly fundamentally change American military doctrine?",
            "Why did the 'Fall of China' trigger intense political witch-hunts and paranoia in Washington?",
            "Did NATO deter Soviet aggression in Western Europe or provoke Soviet consolidation in the East?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 170,
        "historical_ussr_nukes": 1
    },
    1950: {
        "title": "Hot War in Asia: Korea & The Peril of Total Escalation",
        "key_actors": ["Kim Il Sung", "Syngman Rhee", "Douglas MacArthur", "Peng Dehuai", "Harry S. Truman"],
        "summary": "On June 25, North Korean troops cross the 38th parallel with Soviet armor and munitions. The UN Security Council (boycotted by the USSR over Taiwan's seat) votes to intervene under US leadership. General Douglas MacArthur orchestrates the daring amphibious landing at Incheon, recaptures Seoul, and advances north toward the Yalu River. Warning of imperialist invasion, Mao commits 300,000 Chinese 'People's Volunteers,' ambushing UN forces in freezing blizzards and nearly triggering World War III.",
        "real_world_events": [
            "April 1950: US National Security Council Paper 68 (NSC-68) advocates quadrupling defense spending to wage Cold War.",
            "June 1950: North Korea invades the South; Truman commits US forces under the UN flag without congressional declaration of war.",
            "September 1950: MacArthur's Incheon Amphibious Landing turns the tide; UN forces sweep into North Korea.",
            "November 1950: Chinese forces secretly cross the Yalu and launch massive counter-offensive; UN forces retreat in disorder.",
            "December 1950: Truman publicly states he will take whatever steps necessary, including atomic weapons, leading Attlee to fly to DC."
        ],
        "flashpoints": [
            {"lat": 37.45, "lon": 126.70, "name": "Incheon Landing & Korean War Front", "tension": 90},
            {"lat": 40.12, "lon": 124.38, "name": "Yalu River Border (Chinese Entry)", "tension": 95},
            {"lat": 38.90, "lon": -77.03, "name": "Washington NSC-68 Mobilization", "tension": 70}
        ],
        "discussion_questions": [
            "Why did the superpowers choose to fight via proxy in Korea rather than direct confrontation in Europe?",
            "How close did the United States come to dropping atomic bombs on China in late 1950?",
            "What does Truman's decision not to use nuclear weapons in Korea reveal about early atomic taboo?"
        ],
        "historical_defcon": 2,
        "historical_us_nukes": 299,
        "historical_ussr_nukes": 5
    },
    1951: {
        "title": "Stalemate & The MacArthur Crisis: Civilian Supremacy",
        "key_actors": ["Douglas MacArthur", "Matthew Ridgway", "Harry S. Truman", "Robert Schuman"],
        "summary": "General MacArthur openly agitates for expanding the war into mainland China, demanding naval blockades, bombing Manchuria, and unleashing Nationalist forces from Taiwan. When he publicly rebukes Truman's policy of limited war, Truman relieves the legendary general of command—a profound test of civilian control over the military. Under General Matthew Ridgway, the front settles into a grinding trench war along the 38th parallel while preliminary armistice negotiations drag on at Kaesong.",
        "real_world_events": [
            "January 1951: Chinese and North Korean troops recapture Seoul before being driven back by UN 'meatgrinder' tactics.",
            "April 1951: Truman fires MacArthur for insubordination; Matthew Ridgway assumes Far East Command.",
            "April 1951: Treaty of Paris signed, establishing the European Coal and Steel Community (foundation of the EU).",
            "July 1951: Armistice talks begin at Kaesong, deadlocked over repatriation of Chinese and North Korean POWs.",
            "September 1951: Treaty of San Francisco restores Japanese sovereignty; US-Japan Security Treaty concluded."
        ],
        "flashpoints": [
            {"lat": 38.30, "lon": 127.10, "name": "Iron Triangle (Korean Trench Front)", "tension": 75},
            {"lat": 35.67, "lon": 139.65, "name": "Tokyo Far East Command HQ", "tension": 60},
            {"lat": 48.85, "lon": 2.35, "name": "Paris (Schuman Plan / ECSC)", "tension": 40}
        ],
        "discussion_questions": [
            "Why is civilian control over nuclear-armed military forces critical to preventing accidental war?",
            "How can a limited war stalemate be strategically preferable to total military victory in a nuclear world?",
            "How did Western European economic integration serve as a defense against both Germany and the USSR?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 438,
        "historical_ussr_nukes": 25
    },
    1952: {
        "title": "The Thermonuclear Leap: Ivy Mike & Expanding Alliances",
        "key_actors": ["Edward Teller", "Dwight D. Eisenhower", "Winston Churchill", "Fulvio Suvich"],
        "summary": "The technological lethality of war reaches unimaginable scales. On November 1, the United States detonates 'Ivy Mike' at Enewetak Atoll—the world's first thermonuclear fusion hydrogen bomb. With a yield of 10.4 megatons (700 times larger than Hiroshima), it vaporizes the entire island of Elugelab, leaving a mile-wide crater on the ocean floor. Britain detonates its first atomic bomb in Australia, becoming the third nuclear power. General Dwight D. Eisenhower wins the US Presidency, pledging to go to Korea.",
        "real_world_events": [
            "February 1952: Greece and Turkey formally join NATO, securing the alliance's southern flank on the Black Sea.",
            "March 1952: Stalin sends his famous 'Stalin Note' proposing a unified, neutral Germany; Western powers reject it as a ploy to delay rearmament.",
            "October 1952: United Kingdom conducts Operation Hurricane off Western Australia, becoming the 3rd nuclear power.",
            "November 1952: Operation Ivy Mike: US detonates 10.4-megaton thermonuclear device; nuclear destruction becomes truly existential.",
            "November 1952: Eisenhower elected US President in a landslide; promises to end the Korean stalemate."
        ],
        "flashpoints": [
            {"lat": 11.66, "lon": 162.18, "name": "Enewetak Atoll (Ivy Mike H-Bomb)", "tension": 85},
            {"lat": -20.43, "lon": 115.55, "name": "Montebello Islands (British A-Bomb)", "tension": 60},
            {"lat": 39.93, "lon": 32.85, "name": "Ankara (NATO Southern Expansion)", "tension": 65}
        ],
        "discussion_questions": [
            "Did the development of thermonuclear hydrogen bombs make war impossible or merely apocalyptic?",
            "Was Stalin's 1952 proposal for a neutral, unified Germany a missed opportunity for peace or a trap?",
            "Why did medium powers like the UK feel compelled to build their own independent atomic deterrent?"
        ],
        "historical_defcon": 2,
        "historical_us_nukes": 841,
        "historical_ussr_nukes": 50
    },
    1953: {
        "title": "The Thaw & The Threshold: The Death of Stalin & Armistice",
        "key_actors": ["Joseph Stalin", "Nikita Khrushchev", "Georgy Malenkov", "Dwight D. Eisenhower", "Mohammad Mossadegh"],
        "summary": "On March 5, 1953, Joseph Stalin suffers a fatal stroke at his Kuntsevo dacha, throwing the Soviet leadership into frantic collective power struggles between Malenkov, Beria, and Khrushchev. In July, after three years of brutal warfare and 3 million dead, the Korean Armistice Agreement is signed at Panmunjom. In East Germany, Soviet tanks crush the June 17 workers' uprising. In Iran, the CIA and MI6 orchestrate 'Operation Ajax' to topple nationalist Prime Minister Mohammad Mossadegh, establishing the template for covert Cold War intervention.",
        "real_world_events": [
            "March 1953: Death of Joseph Stalin; Malenkov and Khrushchev signal an early desire for 'peaceful coexistence.'",
            "June 1953: Soviet tanks crush the East German Workers' Uprising in East Berlin, demonstrating Moscow's red line.",
            "July 1953: Korean Armistice Agreement signed at Panmunjom; Korean DMZ created along the 38th parallel.",
            "August 1953: USSR tests 'Joe-4' (RDS-6s), their first boosted fission / thermonuclear device, shocking Western intelligence.",
            "August 1953: CIA and MI6 execute Operation Ajax, overthrowing elected Prime Minister Mossadegh in Iran to reinstate the Shah."
        ],
        "flashpoints": [
            {"lat": 55.75, "lon": 37.61, "name": "Moscow Kremlin (Stalin's Funeral & Succession)", "tension": 75},
            {"lat": 37.95, "lon": 126.67, "name": "Panmunjom Armistice Signature", "tension": 55},
            {"lat": 35.68, "lon": 51.38, "name": "Tehran (Operation Ajax Coup)", "tension": 70},
            {"lat": 52.52, "lon": 13.40, "name": "East Berlin Uprising", "tension": 80}
        ],
        "discussion_questions": [
            "Did Stalin's death offer a real chance to end the Cold War, or were the geopolitical alliances already set in stone?",
            "Why did the Korean War end in an armistice rather than a peace treaty?",
            "How did covert operations (like Operation Ajax in Iran) allow superpowers to wage conflict without triggering nuclear red lines?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 1169,
        "historical_ussr_nukes": 120
    },
    1956: {
        "title": "Khrushchev's Thaw, The Bandung Conference & The Suez Debacle",
        "key_actors": ["Nikita Khrushchev", "Dwight D. Eisenhower", "Gamal Abdel Nasser", "Jawaharlal Nehru", "Josip Broz Tito"],
        "summary": "Khrushchev denounces Stalin at the 20th Party Congress. Developing nations unite at the 1955 Bandung Conference to pioneer the Non-Aligned Movement. The Warsaw Pact is founded to counter West Germany's entry into NATO. The Suez Crisis shatters British and French imperial delusions under joint US-Soviet pressure, while Soviet tanks crush the Hungarian Revolution in Budapest.",
        "real_world_events": [
            "April 1955: Bandung Conference convenes 29 Afro-Asian nations, inaugurating the Non-Aligned Movement.",
            "May 1955: Warsaw Pact established as collective defense treaty for Soviet satellites.",
            "February 1956: Khrushchev's 'Secret Speech' repudiates Stalin's excesses.",
            "October-November 1956: Hungarian Revolution crushed by Soviet armor.",
            "November 1956: Suez Crisis: US financial pressure halts Anglo-French-Israeli military takeover of the canal."
        ],
        "flashpoints": [
            {"lat": 30.04, "lon": 31.23, "name": "Suez Canal (Port Said)", "tension": 85},
            {"lat": 47.49, "lon": 19.04, "name": "Budapest (Hungarian Uprising)", "tension": 90},
            {"lat": -6.91, "lon": 107.61, "name": "Bandung (Non-Aligned Conference)", "tension": 30}
        ],
        "discussion_questions": [
            "How did the Suez Crisis signal the definitive end of the British Empire as a global superpower?",
            "Why did the United States oppose its closest allies (UK and France) during the Suez Crisis?",
            "How did the Non-Aligned Movement alter the bipolar dynamic of the Cold War?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 4618,
        "historical_ussr_nukes": 426
    },
    1962: {
        "title": "To the Brink of Armageddon: The Berlin Wall & Cuban Missile Crisis",
        "key_actors": ["John F. Kennedy", "Nikita Khrushchev", "Fidel Castro", "Che Guevara", "Robert McNamara"],
        "summary": "In August 1961, East Germany erects the Berlin Wall to stem the refugee exodus. In October 1962, Soviet nuclear ballistic missiles deployed in Cuba trigger a 13-day naval quarantine and bring the world within hours of thermonuclear extinction. Kennedy and Khrushchev negotiate a secret resolution: Soviet missiles leave Cuba in exchange for US pledges not to invade and the withdrawal of Jupiter missiles from Turkey.",
        "real_world_events": [
            "August 1961: Construction of the Berlin Wall begins, sealing West Berlin.",
            "October 1962: US spy planes photograph Soviet SS-4 nuclear launch sites under construction in Cuba.",
            "October 22, 1962: President Kennedy announces naval quarantine of Cuba.",
            "October 27, 1962: 'Black Saturday': U-2 spy plane shot down over Cuba; nuclear submarine B-59 nearly launches nuclear torpedo.",
            "October 28, 1962: Khrushchev announces withdrawal of Soviet missiles; hotline established between Washington and Moscow."
        ],
        "flashpoints": [
            {"lat": 23.11, "lon": -82.36, "name": "San Cristobal (Cuban Missile Sites)", "tension": 95},
            {"lat": 52.52, "lon": 13.40, "name": "Berlin Wall (Checkpoint Charlie)", "tension": 85},
            {"lat": 39.93, "lon": 32.85, "name": "Izmir (Jupiter Missiles Turkey)", "tension": 70}
        ],
        "discussion_questions": [
            "Was the Cuban Missile Crisis primarily an offensive gambit by Khrushchev or a defensive move to protect Castro's revolution?",
            "How close did the world actually come to full-scale nuclear war in October 1962?",
            "Why was back-channel diplomacy crucial to resolving the crisis?"
        ],
        "historical_defcon": 2,
        "historical_us_nukes": 25540,
        "historical_ussr_nukes": 3322
    },
    1968: {
        "title": "Proxy Quagmires & Cultural Storms: Vietnam, Lop Nur & Prague",
        "key_actors": ["Lyndon B. Johnson", "Leonid Brezhnev", "Mao Zedong", "Alexander Dubček", "Ho Chi Minh"],
        "summary": "The United States escalates military involvement in Vietnam to over 500,000 troops following the Gulf of Tonkin Resolution, suffering the Tet Offensive shock in 1968. China detonates its first atomic bomb at Lop Nur and enters the Cultural Revolution. In Czechoslovakia, Soviet and Warsaw Pact tanks crush the Prague Spring under the Brezhnev Doctrine. The Nuclear Non-Proliferation Treaty (NPT) is signed.",
        "real_world_events": [
            "October 1964: China conducts its first nuclear test (Project 596) at Lop Nur.",
            "1965–1968: Operation Rolling Thunder and massive US troop deployments to South Vietnam.",
            "January 1968: Tet Offensive shatters US domestic consensus on the Vietnam War.",
            "August 1968: 500,000 Warsaw Pact troops invade Czechoslovakia, crushing the Prague Spring.",
            "July 1968: Treaty on the Non-Proliferation of Nuclear Weapons (NPT) opened for signature."
        ],
        "flashpoints": [
            {"lat": 10.82, "lon": 106.63, "name": "Saigon / Mekong Delta (Vietnam War)", "tension": 85},
            {"lat": 50.07, "lon": 14.43, "name": "Prague (Warsaw Pact Invasion)", "tension": 80},
            {"lat": 40.16, "lon": 90.00, "name": "Lop Nur (Chinese Nuclear Site)", "tension": 75}
        ],
        "discussion_questions": [
            "Why did the US military intervention in Vietnam fail to achieve political stability?",
            "What was the significance of China's independent nuclear test for the bipolar Cold War?",
            "How did the Brezhnev Doctrine limit sovereignty within the socialist camp?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 29561,
        "historical_ussr_nukes": 9079
    },
    1973: {
        "title": "Détente & The Changing Chessboard: Beijing, SALT I & Yom Kippur",
        "key_actors": ["Richard Nixon", "Henry Kissinger", "Mao Zedong", "Leonid Brezhnev", "Indira Gandhi"],
        "summary": "Richard Nixon visits Beijing, executing triangular diplomacy to isolate the USSR. India defeats Pakistan in the 1971 war, liberating sovereign Bangladesh, and detonates its first nuclear device ('Smiling Buddha') in 1974. Washington and Moscow sign the SALT I agreement. The Yom Kippur War triggers the OPEC oil embargo and world economic stagflation. The Vietnam War concludes as Saigon falls in 1975.",
        "real_world_events": [
            "December 1971: Indo-Pakistani War leads to the unconditional surrender of Pakistani forces in Dacca and the independence of Bangladesh.",
            "February 1972: Nixon's historic visit to the People's Republic of China ends 25 years of diplomatic isolation.",
            "May 1972: Nixon and Brezhnev sign SALT I and the Anti-Ballistic Missile (ABM) Treaty in Moscow.",
            "October 1973: Yom Kippur War brings US and Soviet nuclear forces to DEFCON 3 alert; OPEC imposes oil embargo.",
            "May 1974: India conducts 'Smiling Buddha' underground nuclear test at Pokhran.",
            "April 1975: Fall of Saigon unifies Vietnam under communist government."
        ],
        "flashpoints": [
            {"lat": 23.81, "lon": 90.41, "name": "Dhaka (Bangladesh Liberation)", "tension": 80},
            {"lat": 31.04, "lon": 34.85, "name": "Sinai Peninsula (Yom Kippur War)", "tension": 85},
            {"lat": 27.09, "lon": 71.75, "name": "Pokhran (Smiling Buddha Nuclear Test)", "tension": 70}
        ],
        "discussion_questions": [
            "How did Nixon and Kissinger's opening to China fundamentally alter Soviet strategic calculations?",
            "Why did the 1971 Indo-Pak war cement India's regional hegemony in South Asia?",
            "Was Détente a genuine transition toward peace or merely a temporary tactical pause in the arms race?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 27863,
        "historical_ussr_nukes": 16408
    },
    1979: {
        "title": "The Second Cold War: The Fall of the Shah & The Afghan Quagmire",
        "key_actors": ["Jimmy Carter", "Leonid Brezhnev", "Ayatollah Khomeini", "Margaret Thatcher", "Babrak Karmal"],
        "summary": "Détente collapses completely. The Iranian Islamic Revolution overthrows the pro-Western Shah, followed by the 444-day US Embassy hostage crisis. In December 1979, the Soviet Union invades Afghanistan to prop up a failing client regime, triggering a brutal guerrilla war backed by the CIA and Pakistan. Margaret Thatcher is elected in Britain, launching a new conservative anti-communist front.",
        "real_world_events": [
            "January-February 1979: Iranian Revolution overthrows the Shah; Ayatollah Khomeini establishes the Islamic Republic.",
            "November 1979: Iranian students storm the US Embassy in Tehran, taking 52 Americans hostage.",
            "December 1979: Soviet airborne troops and 40th Army invade Afghanistan; US halts grain exports and boycotts the Moscow Olympics.",
            "July 1979: Sandinista National Liberation Front overthrows the Somoza dictatorship in Nicaragua.",
            "August 1980: Lech Wałęsa leads the founding of the independent Solidarity trade union at the Gdańsk shipyards."
        ],
        "flashpoints": [
            {"lat": 34.55, "lon": 69.20, "name": "Kabul (Soviet Afghan Invasion)", "tension": 90},
            {"lat": 35.68, "lon": 51.38, "name": "Tehran (US Embassy Hostage Crisis)", "tension": 85},
            {"lat": 54.35, "lon": 18.64, "name": "Gdańsk (Solidarity Strikes Poland)", "tension": 75}
        ],
        "discussion_questions": [
            "Why did the Soviet leadership decide to intervene militarily in Afghanistan, and how did it become their 'Vietnam'?",
            "How did the rise of political Islam in Iran introduce a powerful third force outside the traditional Cold War framework?",
            "What role did economic stagnation in the Soviet bloc play in the emergence of Solidarity in Poland?"
        ],
        "historical_defcon": 3,
        "historical_us_nukes": 24104,
        "historical_ussr_nukes": 26978
    },
    1983: {
        "title": "Star Wars & The Nuclear Threshold: Able Archer & KAL 007",
        "key_actors": ["Ronald Reagan", "Yuri Andropov", "Margaret Thatcher", "François Mitterrand", "Helmut Kohl"],
        "summary": "Ronald Reagan announces the Strategic Defense Initiative ('Star Wars') and describes the USSR as an 'Evil Empire.' Tensions peak in September 1983 when Soviet interceptor jets shoot down Korean Air Lines Flight 007. In November, NATO's 'Able Archer 83' command exercise triggers genuine fear in Moscow of a decapitating preemptive Western nuclear attack, bringing Soviet nuclear forces to hair-trigger alert.",
        "real_world_events": [
            "March 1983: Reagan delivers 'Evil Empire' speech and unveils the space-based Strategic Defense Initiative (SDI).",
            "September 1983: Soviet Su-15 fighter shoots down Korean Air Lines 007 over Sakhalin Island, killing all 269 civilians.",
            "October 1983: US forces invade Grenada to depose a hardline Marxist military junta.",
            "November 1983: NATO conducts Able Archer 83; Soviet nuclear forces in the GDR and Baltic placed on highest alert.",
            "1982–1985: Soviet succession crisis: Brezhnev, Andropov, and Chernenko die in rapid succession."
        ],
        "flashpoints": [
            {"lat": 46.50, "lon": 142.50, "name": "Sea of Okhotsk (KAL 007 Shootdown)", "tension": 90},
            {"lat": 50.85, "lon": 4.35, "name": "Brussels / SHAPE (Able Archer 83 Alert)", "tension": 95},
            {"lat": 12.11, "lon": -61.67, "name": "Grenada (Operation Urgent Fury)", "tension": 70}
        ],
        "discussion_questions": [
            "How close did the Able Archer 83 exercise bring the superpowers to an accidental nuclear war?",
            "Did Reagan's 'Star Wars' initiative bankrupt the Soviet military-industrial complex or destabilize mutual deterrence?",
            "How did the rapid deaths of three Soviet leaders in three years weaken Moscow's strategic coherence?"
        ],
        "historical_defcon": 2,
        "historical_us_nukes": 23308,
        "historical_ussr_nukes": 35804
    },
    1989: {
        "title": "Glasnost, Perestroika & The Fall of the Wall",
        "key_actors": ["Mikhail Gorbachev", "Ronald Reagan", "George H.W. Bush", "Lech Wałęsa", "Erich Honecker"],
        "summary": "Mikhail Gorbachev launches Glasnost and Perestroika. The 1986 Chernobyl disaster exposes systemic Soviet dysfunction. In 1987, Reagan and Gorbachev sign the historic INF Treaty, eliminating intermediate-range missiles. In 1989, Gorbachev renounces the Brezhnev Doctrine. Peaceful revolutions sweep Eastern Europe, culminating in the joyous opening and demolition of the Berlin Wall on November 9, 1989.",
        "real_world_events": [
            "April 1986: Catastrophic explosion at Chernobyl Nuclear Power Plant in Ukraine.",
            "December 1987: Reagan and Gorbachev sign the Intermediate-Range Nuclear Forces (INF) Treaty in Washington.",
            "February 1989: Last Soviet troops withdraw from Afghanistan.",
            "June 1989: Solidarity wins historic parliamentary elections in Poland; Tiananmen Square protests cleared in Beijing.",
            "November 9, 1989: East German spokesman accidentally announces immediate travel permits; Berlin Wall falls."
        ],
        "flashpoints": [
            {"lat": 52.52, "lon": 13.40, "name": "Berlin Wall (Demolition & Reunification)", "tension": 30},
            {"lat": 51.38, "lon": 30.09, "name": "Chernobyl Nuclear Reactor 4", "tension": 85},
            {"lat": 39.90, "lon": 116.39, "name": "Beijing (Tiananmen Square)", "tension": 80}
        ],
        "discussion_questions": [
            "Was the collapse of communism in Eastern Europe driven primarily by internal economic failure or Gorbachev's personal choices?",
            "Why did the Berlin Wall fall without a single shot being fired by Soviet or East German troops?",
            "How did the INF Treaty prove that disarmament, not merely limitation, was possible?"
        ],
        "historical_defcon": 4,
        "historical_us_nukes": 22217,
        "historical_ussr_nukes": 37927
    },
    1991: {
        "title": "The Final Curtain: German Unity, Desert Storm & Soviet Dissolution",
        "key_actors": ["George H.W. Bush", "Mikhail Gorbachev", "Boris Yeltsin", "Helmut Kohl", "Saddam Hussein"],
        "summary": "Germany peacefully reunifies under NATO in October 1990. A 35-nation coalition liberates Kuwait during Operation Desert Storm with US-Soviet diplomatic consensus. In August 1991, hardline communist plotters attempt a coup in Moscow, but are defeated by popular resistance led by Boris Yeltsin. On December 25, 1991, the Soviet flag is lowered from the Kremlin; the USSR dissolves into 15 sovereign nations, ending the Cold War.",
        "real_world_events": [
            "October 1990: Federal Republic of Germany reunifies, absorbing the former German Democratic Republic.",
            "January-February 1991: Operation Desert Storm liberates Kuwait with overwhelming coalition air and ground campaign.",
            "July 1991: Bush and Gorbachev sign START I, mandating massive reductions in strategic nuclear warheads.",
            "August 1991: Hardline communist GKChP coup against Gorbachev collapses after three days; Baltic states break away.",
            "December 25, 1991: Gorbachev resigns; Soviet Union formally ceases to exist on December 26, 1991."
        ],
        "flashpoints": [
            {"lat": 55.75, "lon": 37.61, "name": "Moscow Kremlin (Soviet Flag Lowered)", "tension": 20},
            {"lat": 29.37, "lon": 47.97, "name": "Kuwait City (Operation Desert Storm)", "tension": 60},
            {"lat": 52.52, "lon": 13.40, "name": "Reunified Berlin Capital", "tension": 15}
        ],
        "discussion_questions": [
            "Did the United States 'win' the Cold War, or did the Soviet Union collapse under its own internal contradictions?",
            "How did the peaceful management of thousands of Soviet nuclear warheads avert a post-Soviet nuclear catastrophe?",
            "What new global geopolitical order emerged following the dissolution of the Soviet Union in 1991?"
        ],
        "historical_defcon": 5,
        "historical_us_nukes": 19008,
        "historical_ussr_nukes": 30300
    }
}

# Aliases for Era ID Lookups (1 through 10)
HISTORICAL_YEARS[1] = HISTORICAL_YEARS[1945]
HISTORICAL_YEARS[2] = HISTORICAL_YEARS[1952]
HISTORICAL_YEARS[3] = HISTORICAL_YEARS[1956]
HISTORICAL_YEARS[4] = HISTORICAL_YEARS[1962]
HISTORICAL_YEARS[5] = HISTORICAL_YEARS[1968]
HISTORICAL_YEARS[6] = HISTORICAL_YEARS[1973]
HISTORICAL_YEARS[7] = HISTORICAL_YEARS[1979]
HISTORICAL_YEARS[8] = HISTORICAL_YEARS[1983]
HISTORICAL_YEARS[9] = HISTORICAL_YEARS[1989]
HISTORICAL_YEARS[10] = HISTORICAL_YEARS[1991]

