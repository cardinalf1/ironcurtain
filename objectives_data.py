"""
Cold War Eras, Objectives, and Dynamic Boundaries Database (1945–1991).
Contains 10 Playable Historical Chunks (Eras), Era-Relative Dynamic Boundaries,
Start-of-Era World Flashpoints, and Tailored National Objectives for all 8 Powers.
"""

from typing import Dict, List, Any

# ==============================================================================
# THE 10 COLD WAR PLAYABLE CHUNKS / ERAS (1945–1991)
# ==============================================================================
COLD_WAR_ERAS: Dict[int, Dict[str, Any]] = {
    1: {
        "era_id": 1,
        "name": "Era 1: 1945–1947",
        "title": "Dawn of the Atomic Age & Decolonization",
        "years_label": "1945–1947",
        "year_start": 1945,
        "year_end": 1947,
        "theme": "Hiroshima, Potsdam, British Raj decolonization, 4-zone Germany, Truman Doctrine.",
        "historical_defcon": 4,
        "summary": "World War II ends with the atomic bomb and Potsdam Conference. Germany is occupied by four Allied powers. In South Asia, the British Empire rules the British Raj while Indian leaders negotiate independence and face partition. Truman announces the Truman Doctrine to contain Soviet communism.",
        "flashpoint": {
            "headline": "Potsdam Division, Hiroshima & The End of the British Raj",
            "affected_theaters": "Central Europe, South Asia & East Asia",
            "briefing": "The atomic bomb ended WWII, but peace is fragile. Germany is carved into four Allied occupation zones, Korea is partitioned at the 38th parallel, and in India, the British Raj prepares for an agonizing partition into India and Pakistan amid widespread communal tensions.",
            "historical_baseline": "Potsdam Agreement (1945), Truman Doctrine (1947), Indian Independence Act (August 1947)."
        }
    },
    2: {
        "era_id": 2,
        "name": "Era 2: 1948–1952",
        "title": "The Hardening Blocs & Red China",
        "years_label": "1948–1952",
        "year_start": 1948,
        "year_end": 1952,
        "theme": "Berlin Airlift, German partition (FRG/GDR), Soviet A-bomb, PRC founded, Sovereign India, Korean War.",
        "historical_defcon": 3,
        "summary": "Stalin blockades West Berlin, prompting the Allied Airlift. Germany partitions into the FRG and GDR. The Soviets test their first atomic bomb (RDS-1), Mao proclaims the People's Republic of China, and the Korean War erupts across the 38th parallel. India drafts its democratic constitution.",
        "flashpoint": {
            "headline": "The Berlin Blockade, Soviet Atomic Breakthrough & War in Korea",
            "affected_theaters": "Berlin, Manchuria & Korean Peninsula",
            "briefing": "The Cold War has erupted into open proxy warfare. Soviet nuclear monopoly breakthrough shocks Washington. Mao's victory in China shifts the Asian balance of power, and North Korean tanks roll across the 38th parallel, drawing US and UN armed intervention.",
            "historical_baseline": "Berlin Airlift (1948–49), Soviet atomic test (1949), PRC founded (1949), Korean War outbreak (1950)."
        }
    },
    3: {
        "era_id": 3,
        "name": "Era 3: 1953–1958",
        "title": "Post-Stalin Thaw & Non-Aligned Awakening",
        "years_label": "1953–1958",
        "year_start": 1953,
        "year_end": 1958,
        "theme": "Korean Armistice, 17th parallel Vietnam partition, Warsaw Pact, Bandung NAM, Suez Crisis.",
        "historical_defcon": 4,
        "summary": "Stalin dies, initiating a Soviet leadership thaw under Khrushchev. An armistice freezes Korea at the DMZ. Indochina is partitioned at the 17th parallel. Developing nations convene at the Bandung Conference to establish the Non-Aligned Movement. The Suez Crisis shatters British imperial prestige.",
        "flashpoint": {
            "headline": "Khrushchev's Thaw, The Bandung Conference & The Suez Debacle",
            "affected_theaters": "Middle East, Indochina & Eastern Europe",
            "briefing": "Khrushchev denounces Stalin, raising hopes for peaceful coexistence. Developing nations led by India, Yugoslavia, and Egypt unite at Bandung to reject superpower hegemony. The UK and France attempt an invasion of the Suez Canal, only to be humiliated by US and Soviet pressure.",
            "historical_baseline": "Korean Armistice (1953), Bandung Conference (1955), Warsaw Pact created (1955), Suez Crisis (1956), Hungarian Revolution (1956)."
        }
    },
    4: {
        "era_id": 4,
        "name": "Era 4: 1959–1963",
        "title": "To the Brink of Armageddon",
        "years_label": "1959–1963",
        "year_start": 1959,
        "year_end": 1963,
        "theme": "Cuban Revolution, Berlin Wall, Sino-Soviet Split, Cuban Missile Crisis, African Decolonization.",
        "historical_defcon": 2,
        "summary": "Fidel Castro's revolutionaries take power in Havana, aligning with Moscow. East Germany erects the Berlin Wall to stem the brain drain. Beijing and Moscow split ideologically. The deployment of Soviet nuclear missiles in Cuba brings the superpowers to the verge of thermonuclear war.",
        "flashpoint": {
            "headline": "The Berlin Wall Fortified & The Cuban Missile Crisis",
            "affected_theaters": "Caribbean, Berlin & Sino-Soviet Border",
            "briefing": "The world stands hours from global nuclear war. Soviet medium-range ballistic missiles in Cuba are discovered by US U-2 spy planes. Kennedy imposes a naval quarantine. Meanwhile, concrete and barbed wire sever Berlin in two.",
            "historical_baseline": "Cuban Revolution (1959), Berlin Wall built (1961), Cuban Missile Crisis (October 1962), Partial Test Ban Treaty (1963)."
        }
    },
    5: {
        "era_id": 5,
        "name": "Era 5: 1964–1969",
        "title": "Proxy Quagmires & Cultural Revolution",
        "years_label": "1964–1969",
        "year_start": 1964,
        "year_end": 1969,
        "theme": "Vietnam escalation, China atomic bomb, Prague Spring, Six-Day War, Nuclear Non-Proliferation.",
        "historical_defcon": 3,
        "summary": "The US commits hundreds of thousands of combat troops to South Vietnam. China conducts its first nuclear test and descends into the Cultural Revolution. Warsaw Pact tanks crush Czechoslovakia's Prague Spring under the Brezhnev Doctrine. The Six-Day War reshapes the Middle East.",
        "flashpoint": {
            "headline": "The Gulf of Tonkin Escalation & The Prague Spring Crackdown",
            "affected_theaters": "Southeast Asia, Central Europe & Middle East",
            "briefing": "Over 500,000 American soldiers fight in the jungles of Vietnam against Viet Cong guerrillas and the NVA. In Prague, Alexander Dubček's 'socialism with a human face' is ruthlessly suppressed by Soviet armor, establishing the Brezhnev Doctrine.",
            "historical_baseline": "Gulf of Tonkin Resolution (1964), China's nuclear test (1964), Six-Day War (1967), Prague Spring invasion (1968), NPT signed (1968)."
        }
    },
    6: {
        "era_id": 6,
        "name": "Era 6: 1970–1975",
        "title": "Détente & Triangular Diplomacy",
        "years_label": "1970–1975",
        "year_start": 1970,
        "year_end": 1975,
        "theme": "1971 Indo-Pak War & Bangladesh, Nixon in China, SALT I, Fall of Saigon, Smiling Buddha.",
        "historical_defcon": 4,
        "summary": "Nixon visits Mao in Beijing, executing triangular diplomacy. India defeats Pakistan in the 1971 war, liberating Bangladesh, and conducts its first nuclear test ('Smiling Buddha'). The US and USSR sign SALT I. The Vietnam War concludes with the Fall of Saigon.",
        "flashpoint": {
            "headline": "Nixon's Opening to China, Bangladesh Independence & Fall of Saigon",
            "affected_theaters": "South Asia, Indochina & Moscow",
            "briefing": "Diplomatic earthquake: Washington recognizes Beijing to isolate Moscow. In South Asia, the Pakistan army's atrocities in East Bengal lead to Indian military intervention, birthing sovereign Bangladesh. North Vietnamese tanks crash through Saigon's presidential palace gates.",
            "historical_baseline": "Indo-Pakistani War & Bangladesh (1971), Nixon in China (1972), SALT I treaty (1972), India's Smiling Buddha nuclear test (1974), Fall of Saigon (1975)."
        }
    },
    7: {
        "era_id": 7,
        "name": "Era 7: 1976–1980",
        "title": "The Second Cold War & The Afghan Trap",
        "years_label": "1976–1980",
        "year_start": 1976,
        "year_end": 1980,
        "theme": "Iranian Revolution, Soviet invasion of Afghanistan, Sandinista victory, Polish Solidarity.",
        "historical_defcon": 3,
        "summary": "Détente collapses. The Iranian Revolution overthrows the Shah, precipitating the US hostage crisis. The Soviet 40th Army invades Afghanistan to prop up a client communist regime, triggering US-backed Mujahideen resistance. Polish workers found the anti-communist trade union Solidarity.",
        "flashpoint": {
            "headline": "The Fall of the Shah & Soviet Armor in Kabul",
            "affected_theaters": "Persian Gulf, Afghanistan & Eastern Europe",
            "briefing": "Détente is officially dead. The Islamic Republic of Iran takes 52 American diplomats hostage. In December 1979, Soviet Spetsnaz and motorized divisions seize Kabul, sparking a bloody ten-year guerrilla war that drains Moscow's treasury and morale.",
            "historical_baseline": "Iranian Islamic Revolution (1979), Sandinistas take Nicaragua (1979), Soviet invasion of Afghanistan (1979), Solidarity formed in Poland (1980)."
        }
    },
    8: {
        "era_id": 8,
        "name": "Era 8: 1981–1984",
        "title": "Star Wars & Nuclear Brinkmanship",
        "years_label": "1981–1984",
        "year_start": 1981,
        "year_end": 1984,
        "theme": "Reagan Doctrine, SDI 'Star Wars', Able Archer 83, KAL 007, Soviet gerontocracy.",
        "historical_defcon": 2,
        "summary": "Ronald Reagan labels the USSR the 'Evil Empire' and announces the Strategic Defense Initiative (SDI). Tensions soar as the Soviets shoot down Korean Air Lines 007. NATO's Able Archer 83 exercise causes KGB leaders to fear a preemptive Western nuclear decapitation strike.",
        "flashpoint": {
            "headline": "The 'Evil Empire' Speech, KAL 007 Shootdown & Able Archer 83",
            "affected_theaters": "North Atlantic, Central Europe & Sea of Japan",
            "briefing": "A dangerous peak in superpower paranoia. Reagan funds anti-communist insurgents globally while launching 'Star Wars' space-based defenses. The Soviet Union, suffering through three dying general secretaries in three years, places nuclear bombers on hair-trigger alert during NATO's Able Archer drill.",
            "historical_baseline": "Reagan's SDI speech (1983), KAL 007 disaster (September 1983), Able Archer 83 war scare (November 1983), Chernenko-Andropov transitions."
        }
    },
    9: {
        "era_id": 9,
        "name": "Era 9: 1985–1989",
        "title": "Glasnost, Perestroika & Fall of the Wall",
        "years_label": "1985–1989",
        "year_start": 1985,
        "year_end": 1989,
        "theme": "Gorbachev reforms, Chernobyl, INF Treaty, Soviet Afghan withdrawal, Fall of the Berlin Wall.",
        "historical_defcon": 4,
        "summary": "Mikhail Gorbachev ascends in Moscow, implementing Glasnost (openness) and Perestroika (restructuring). The catastrophic Chernobyl meltdown reveals Soviet systemic rot. Reagan and Gorbachev sign the historic INF Treaty. In 1989, peaceful revolutions sweep Eastern Europe, and the Berlin Wall is torn down.",
        "flashpoint": {
            "headline": "Chernobyl Disaster, The INF Treaty & The Fall of the Berlin Wall",
            "affected_theaters": "Berlin, Eastern Europe & Moscow",
            "briefing": "History accelerates beyond imagination. Gorbachev refuses to use the Red Army to crush Eastern European protests. On November 9, 1989, joyful crowds breach Checkpoint Charlie and begin demolishing the Berlin Wall with sledgehammers, signaling the collapse of communist Europe.",
            "historical_baseline": "Gorbachev comes to power (1985), Chernobyl (1986), INF Treaty signed (1987), Soviet withdrawal from Afghanistan (1989), Fall of Berlin Wall (Nov 1989)."
        }
    },
    10: {
        "era_id": 10,
        "name": "Era 10: 1990–1991",
        "title": "The Final Curtain & Soviet Dissolution",
        "years_label": "1990–1991",
        "year_start": 1990,
        "year_end": 1991,
        "theme": "German Reunification, Gulf War, August Coup, Soviet dissolution, End of the Cold War.",
        "historical_defcon": 5,
        "summary": "Germany reunifies peacefully under NATO. A multinational coalition liberates Kuwait with joint US-Soviet diplomatic consensus. In August 1991, hardline communist coup plotters fail. On December 25, 1991, Gorbachev resigns, the hammer and sickle is lowered from the Kremlin, and the Cold War ends.",
        "flashpoint": {
            "headline": "Reunification of Germany, The August Coup & Dissolution of the USSR",
            "affected_theaters": "Moscow, Reunified Berlin & Persian Gulf",
            "briefing": "The 46-year twilight struggle reaches its dramatic resolution. Following the failed hardline communist coup in Moscow, the Baltic states break away, Ukraine votes overwhelmingly for sovereignty, and the USSR formally dissolves into 15 independent nations on Christmas Day, 1991.",
            "historical_baseline": "German Reunification (October 1990), Gulf War (Jan 1991), Moscow August Coup (1991), Belavezha Accords & Dissolution of USSR (Dec 25-26, 1991)."
        }
    }
}

# ==============================================================================
# ERA-RELATIVE DYNAMIC TERRITORY & BOUNDARY DEFAULTS
# ==============================================================================
ERA_TERRITORY_DEFAULTS: Dict[int, Dict[str, Dict[str, Any]]] = {
    1: {  # 1945-1947: Post-WWII Occupations & British Raj
        "India": {
            "name": "British Raj (Crown Colony)",
            "current_controller": "United Kingdom",
            "status": "COLONY_TRANSITION",
            "original_owner": "India",
            "alignment": 0.4,
            "military_garrison": 4,
            "notes": "Administered under the British Crown; Indian Interim Ministry negotiating independence."
        },
        "GER_WEST": {
            "name": "Western Allied Zones (Germany)",
            "current_controller": "USA",
            "status": "OCCUPIED",
            "original_owner": "Germany",
            "alignment": 0.8,
            "military_garrison": 5,
            "notes": "Joint US, British, and French occupation zones administered by Allied Control Council."
        },
        "GER_EAST": {
            "name": "Soviet Occupation Zone (Germany)",
            "current_controller": "USSR",
            "status": "OCCUPIED",
            "original_owner": "Germany",
            "alignment": -0.8,
            "military_garrison": 5,
            "notes": "Administered by the Soviet Military Administration in Germany (SMAD)."
        },
        "KOR_SOUTH": {
            "name": "US Army Military Zone (Korea)",
            "current_controller": "USA",
            "status": "OCCUPIED",
            "original_owner": "Korea",
            "alignment": 0.6,
            "military_garrison": 3,
            "notes": "US Army Military Government in Korea (USAMGIK) south of the 38th parallel."
        },
        "KOR_NORTH": {
            "name": "Soviet Civil Administration (Korea)",
            "current_controller": "USSR",
            "status": "OCCUPIED",
            "original_owner": "Korea",
            "alignment": -0.6,
            "military_garrison": 3,
            "notes": "Soviet military administration governing north of the 38th parallel."
        },
        "Vietnam": {
            "name": "French Indochina",
            "current_controller": "France",
            "status": "OCCUPIED",
            "original_owner": "Vietnam",
            "alignment": 0.5,
            "military_garrison": 3,
            "notes": "French colonial expeditionary corps battling Viet Minh insurgents."
        },
        "China": {
            "name": "Republic of China (Civil War)",
            "current_controller": "China",
            "status": "CONTESTED",
            "original_owner": "China",
            "alignment": 0.1,
            "military_garrison": 4,
            "notes": "Nationalist KMT vs Communist CCP fighting nationwide civil war."
        },
        "Cuba": {
            "name": "Republic of Cuba",
            "current_controller": "Cuba",
            "status": "SOVEREIGN",
            "original_owner": "Cuba",
            "alignment": 0.7,
            "military_garrison": 1,
            "notes": "Pro-American civilian/military leadership aligned with Washington."
        }
    },
    2: {  # 1948-1952: Decolonized India, Divided Germany & PRC
        "India": {
            "name": "Sovereign Republic of India",
            "current_controller": "India",
            "status": "SOVEREIGN",
            "original_owner": "India",
            "alignment": 0.0,
            "military_garrison": 3,
            "notes": "Fully independent sovereign democracy (post-August 1947 Partition; 1950 Constitution)."
        },
        "GER_WEST": {
            "name": "Federal Republic of Germany (FRG / West)",
            "current_controller": "West Germany",
            "status": "PARTITIONED",
            "original_owner": "Germany",
            "alignment": 0.8,
            "military_garrison": 4,
            "notes": "Democratic West German state aligned with NATO; capital in Bonn."
        },
        "GER_EAST": {
            "name": "German Democratic Republic (GDR / East)",
            "current_controller": "East Germany",
            "status": "PARTITIONED",
            "original_owner": "Germany",
            "alignment": -0.8,
            "military_garrison": 4,
            "notes": "Socialist East German state aligned with Soviet bloc; capital in East Berlin."
        },
        "KOR_SOUTH": {
            "name": "Republic of Korea (South)",
            "current_controller": "South Korea",
            "status": "PARTITIONED",
            "original_owner": "Korea",
            "alignment": 0.7,
            "military_garrison": 4,
            "notes": "ROK state defending southern peninsula against northern assault."
        },
        "KOR_NORTH": {
            "name": "DPRK (North Korea)",
            "current_controller": "North Korea",
            "status": "PARTITIONED",
            "original_owner": "Korea",
            "alignment": -0.7,
            "military_garrison": 4,
            "notes": "Communist DPRK forces pushing south across 38th parallel."
        },
        "China": {
            "name": "People's Republic of China",
            "current_controller": "China",
            "status": "SOVEREIGN",
            "original_owner": "China",
            "alignment": -0.7,
            "military_garrison": 5,
            "notes": "Mao's PRC proclaimed in Beijing; KMT forces evacuated to Taiwan."
        }
    },
    3: {  # 1953-1958: Korean Armistice & Vietnam Partition
        "KOR_SOUTH": {
            "name": "Republic of Korea (DMZ Frontier)",
            "current_controller": "South Korea",
            "status": "PARTITIONED",
            "original_owner": "Korea",
            "alignment": 0.7,
            "military_garrison": 4,
            "notes": "Post-1953 Armistice border along the Demilitarized Zone (DMZ)."
        },
        "KOR_NORTH": {
            "name": "DPRK (North Korea DMZ)",
            "current_controller": "North Korea",
            "status": "PARTITIONED",
            "original_owner": "Korea",
            "alignment": -0.7,
            "military_garrison": 4,
            "notes": "Fortified armistice frontier at the 38th parallel."
        },
        "Vietnam": {
            "name": "Partitioned Vietnam (17th Parallel)",
            "current_controller": "Vietnam",
            "status": "PARTITIONED",
            "original_owner": "Vietnam",
            "alignment": -0.2,
            "military_garrison": 3,
            "notes": "Divided at 17th parallel following French defeat at Dien Bien Phu."
        }
    },
    4: {  # 1959-1963: Revolutionary Cuba & The Berlin Wall
        "Cuba": {
            "name": "Socialist Republic of Cuba",
            "current_controller": "Cuba",
            "status": "SOVEREIGN",
            "original_owner": "Cuba",
            "alignment": -0.8,
            "military_garrison": 3,
            "notes": "Fidel Castro's revolutionary government aligned with Moscow."
        },
        "GER_WEST": {
            "name": "West Germany (Berlin Wall Border)",
            "current_controller": "West Germany",
            "status": "PARTITIONED",
            "original_owner": "Germany",
            "alignment": 0.8,
            "military_garrison": 4,
            "notes": "Border fortified by the concrete Berlin Wall erected August 1961."
        },
        "GER_EAST": {
            "name": "East Germany (Berlin Wall Border)",
            "current_controller": "East Germany",
            "status": "PARTITIONED",
            "original_owner": "Germany",
            "alignment": -0.8,
            "military_garrison": 4,
            "notes": "GDR border troops enforcing shoot-to-kill orders along the Wall."
        }
    },
    6: {  # 1970-1975: Unified Vietnam & Bangladesh Independence
        "Vietnam": {
            "name": "Unified Socialist Republic of Vietnam",
            "current_controller": "Vietnam",
            "status": "SOVEREIGN",
            "original_owner": "Vietnam",
            "alignment": -0.7,
            "military_garrison": 4,
            "notes": "Reunified under Hanoi following the 1975 Fall of Saigon."
        }
    },
    10: {  # 1990-1991: German Reunification & Soviet Collapse
        "GER_WEST": {
            "name": "Federal Republic of Germany (Reunified)",
            "current_controller": "Germany",
            "status": "SOVEREIGN",
            "original_owner": "Germany",
            "alignment": 0.8,
            "military_garrison": 3,
            "notes": "Peacefully reunified Germany incorporating East and West (October 1990)."
        },
        "GER_EAST": {
            "name": "Eastern Länder (Reunified Germany)",
            "current_controller": "Germany",
            "status": "SOVEREIGN",
            "original_owner": "Germany",
            "alignment": 0.8,
            "military_garrison": 2,
            "notes": "Former GDR territory integrated into democratic federal Germany."
        }
    }
}

# ==============================================================================
# LONG-TERM GRAND STRATEGY OBJECTIVES (1945–1991)
# ==============================================================================
LONG_TERM_OBJECTIVES: Dict[str, Dict[str, Any]] = {
    "USA": {
        "title": "Pax Americana & The Long Twilight Struggle",
        "description": "Maintain global democratic containment against Soviet expansionism, preserve NATO unity across four decades, achieve technological superiority (Apollo, SDI), and shepherd a peaceful dissolution of the Soviet bloc without a thermonuclear exchange.",
        "success_criteria": "Keep DEFCON >= 2, maintain Western European stability, surpass rival economies ($3500M+ treasury), and witness the peaceful end of the Cold War.",
        "target_score": 100
    },
    "USSR": {
        "title": "Socialist Bastion, Strategic Parity & Soviet Preservation",
        "description": "Break the Western atomic monopoly, construct a defensive perimeter in Eastern Europe (Warsaw Pact), support anti-colonial revolution in the Third World, achieve strategic nuclear parity, and reform the Soviet economy to avoid systemic collapse.",
        "success_criteria": "Build an atomic arsenal, protect Warsaw Pact boundaries, project influence in Asia/Africa, and preserve Soviet political cohesion without state bankruptcy.",
        "target_score": 100
    },
    "United Kingdom": {
        "title": "Imperial Devolution, Special Relationship & Deterrence",
        "description": "Manage the retreat from the British Empire (India, Suez, Africa) with diplomatic dignity, preserve the Anglo-American Special Relationship, build an independent nuclear deterrent, and maintain sovereign solvency.",
        "success_criteria": "Maintain treasury solvency, avoid total diplomatic humiliation, secure British nuclear capability, and protect homeland frontiers.",
        "target_score": 100
    },
    "France": {
        "title": "Grandeur, Force de Frappe & European Leadership",
        "description": "Recover from colonial wars in Indochina and Algeria, pioneer the European Economic Community (EEC), construct an independent nuclear deterrent (Force de Frappe), and steer an autonomous third path between Washington and Moscow.",
        "success_criteria": "Build independent nuclear capability, anchor Franco-German partnership, preserve domestic stability >= 60%, and avoid foreign satellite status.",
        "target_score": 100
    },
    "China": {
        "title": "Middle Kingdom Revival & Anti-Hegemonic Sovereignty",
        "description": "Win the Chinese Civil War, resist imperialist encirclement in Korea, declare independence from Soviet hegemony (Sino-Soviet Split), achieve thermonuclear status (1964), enter the United Nations, and initiate historic economic modernization.",
        "success_criteria": "Consolidate mainland authority, secure nuclear capability, achieve UN P5 diplomatic recognition, and achieve domestic economic growth.",
        "target_score": 100
    },
    "India": {
        "title": "Non-Aligned Leadership & Sovereign Self-Reliance",
        "description": "Secure independence from the British Raj in Era 1, manage the trauma of Partition, architect the Non-Aligned Movement (Bandung 1955), safeguard territorial integrity in regional wars, achieve nuclear deterrence (Smiling Buddha), and resist superpower vassalage.",
        "success_criteria": "Achieve full independence in Era 1, preserve strictly non-aligned neutrality (-0.3 <= alignment <= 0.3), safeguard borders, and foster self-reliant industrialization.",
        "target_score": 100
    },
    "Yugoslavia": {
        "title": "Titoist Third Way & Non-Aligned Federal Unity",
        "description": "Survive Stalin's wrath following the 1948 Tito-Stalin split, pioneer socialist self-management, balance between Western loans and Eastern trade, co-found the Non-Aligned Movement, and maintain brotherhood and unity across the multi-ethnic Yugoslav federation.",
        "success_criteria": "Survive Soviet blockade and assassinations, sustain trade with both blocs, maintain independent defense, and keep the Yugoslav federation united.",
        "target_score": 100
    },
    "Cuba": {
        "title": "Socialist Vanguard & Internationalist Resilience",
        "description": "Overthrow corrupt dictatorship in Era 4, survive US invasions (Bay of Pigs) and economic blockades, navigate the Cuban Missile Crisis, and project anti-imperialist influence through medical and military internationalism in Africa and Latin America.",
        "success_criteria": "Consolidate revolution in Era 4, survive economic sanctions, maintain Soviet alliance without sovereign vassalage, and preserve national revolution through 1991.",
        "target_score": 100
    }
}

# ==============================================================================
# ERA-SPECIFIC ANNUAL HISTORICAL OBJECTIVES (10 ERAS × 8 POWERS)
# ==============================================================================
ANNUAL_OBJECTIVES: Dict[int, Dict[str, List[Dict[str, Any]]]] = {
    # --------------------------------------------------------------------------
    # ERA 1: 1945–1947 // DAWN OF THE ATOMIC AGE & DECOLONIZATION
    # --------------------------------------------------------------------------
    1: {
        "USA": [
            {"title": "Marshall Plan & European Reconstruction", "description": "Inject economic credits to revitalize Western Europe and prevent communist electoral victories.", "metric_type": "TREASURY_SOLVENCY", "threshold": 2200, "weight": 10},
            {"title": "Truman Doctrine Containment", "description": "Provide aid to Greece and Turkey to resist Soviet pressure on the Turkish Straits.", "metric_type": "BUFFER_ALIGNMENT", "target": "Greece", "weight": 10},
            {"title": "Preserve Atomic Monopoly & Deterrence", "description": "Keep atomic stockpile ready while avoiding general thermonuclear escalation.", "metric_type": "AVOID_DEFCON_1", "weight": 10}
        ],
        "USSR": [
            {"title": "Consolidate Eastern European Buffer", "description": "Install friendly socialist administrations across Poland, Hungary, and Romania.", "metric_type": "BUFFER_ALIGNMENT", "target": "Poland", "weight": 10},
            {"title": "Crash Atomic Project (RDS-1)", "description": "Direct intelligence and uranium to Semipalatinsk testing grounds to break US monopoly.", "metric_type": "NUCLEAR_R_D", "threshold": 50, "weight": 10},
            {"title": "Extract German War Reparations", "description": "Dismantle industrial machinery in the Soviet zone to rebuild devastated Soviet homeland.", "metric_type": "TREASURY_SOLVENCY", "threshold": 700, "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Orderly Devolution of the British Raj", "description": "Manage the transfer of power and partition in India while limiting catastrophic communal violence.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 60, "weight": 10},
            {"title": "Avert Sterling Balance Bankruptcy", "description": "Secure the Anglo-American loan and stabilize imperial currency reserves.", "metric_type": "TREASURY_SOLVENCY", "threshold": 350, "weight": 10},
            {"title": "Allied Security in West Germany", "description": "Coordinate British occupation zone governance in the Ruhr with Washington.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_WEST", "weight": 10}
        ],
        "France": [
            {"title": "Restauration of the French Republic", "description": "Rebuild democratic institutions and rebuild coal and steel production in Lorraine.", "metric_type": "TREASURY_SOLVENCY", "threshold": 250, "weight": 10},
            {"title": "Re-establish Control in Indochina", "description": "Deploy expeditionary forces to Saigon and Hanoi to counter Viet Minh resistance.", "metric_type": "TERRITORIAL_CONTROL", "target": "Vietnam", "weight": 10}
        ],
        "China": [
            {"title": "Win the Revolutionary Civil War", "description": "Defeat Nationalist forces in Manchuria and liberate northern rural provinces.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10},
            {"title": "Secure Soviet Lend-Lease & Arms", "description": "Secure captured Japanese equipment and Soviet industrial logistics in the northeast.", "metric_type": "TREASURY_SOLVENCY", "threshold": 150, "weight": 10}
        ],
        "India": [
            {"title": "Secure National Independence from the British Raj", "description": "Negotiate constitutional sovereignty and end British colonial rule over the subcontinent.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 15},
            {"title": "Manage the Anguish of Partition", "description": "Mitigate cross-border refugee chaos and preserve national unity following the August 1947 split.", "metric_type": "TERRITORIAL_CONTROL", "target": "India", "weight": 10},
            {"title": "Lay Foundations for Non-Alignment", "description": "Reject imperial military pacts and establish independent foreign policy.", "metric_type": "DETERRENCE_STABILITY", "weight": 5}
        ],
        "Yugoslavia": [
            {"title": "Consolidate Partisan Republic", "description": "Nationalize war industries and rebuild the Adriatic transport network.", "metric_type": "TREASURY_SOLVENCY", "threshold": 120, "weight": 10},
            {"title": "Balkan Federation Solidarity", "description": "Provide aid to Greek communist partisans fighting in the mountains.", "metric_type": "BUFFER_ALIGNMENT", "target": "Greece", "weight": 10}
        ],
        "Cuba": [
            {"title": "Sugar Quota Stability", "description": "Negotiate preferential sugar export terms with the United States.", "metric_type": "TREASURY_SOLVENCY", "threshold": 80, "weight": 10},
            {"title": "Suppress Island Agitation", "description": "Contain strikes and student radicalism in Havana to maintain civil order.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 60, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 2: 1948–1952 // THE HARDENING BLOCS & RED CHINA
    # --------------------------------------------------------------------------
    2: {
        "USA": [
            {"title": "Defeat the Berlin Blockade via Airlift", "description": "Sustain West Berlin's population with round-the-clock air transport without direct war.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_WEST", "weight": 10},
            {"title": "Establish the NATO Defense Shield", "description": "Sign the North Atlantic Treaty cementing transatlantic collective defense.", "metric_type": "BUFFER_ALIGNMENT", "target": "West Germany", "weight": 10},
            {"title": "Defend South Korea across the 38th Parallel", "description": "Commit UN forces to halt the North Korean advance and preserve the ROK.", "metric_type": "TERRITORIAL_CONTROL", "target": "KOR_SOUTH", "weight": 10}
        ],
        "USSR": [
            {"title": "Detonate First Atomic Bomb (RDS-1)", "description": "Break the imperialist atomic monopoly and achieve nuclear power status.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Found the German Democratic Republic (GDR)", "description": "Establish a socialist German state in response to the Western Bizone.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_EAST", "weight": 10},
            {"title": "Forge Sino-Soviet Friendship Treaty", "description": "Sign the 30-year mutual defense alliance with Mao's new government in Beijing.", "metric_type": "BUFFER_ALIGNMENT", "target": "China", "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Join NATO & Launch Operation Hurricane", "description": "Begin domestic plutonium extraction to test Britain's first atomic bomb.", "metric_type": "NUCLEAR_R_D", "threshold": 60, "weight": 10},
            {"title": "Deploy Troops to the Korean Conflict", "description": "Send British Commonwealth brigade to defend the Pusan perimeter alongside US allies.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "France": [
            {"title": "Launch the Schuman Declaration (ECSC)", "description": "Pool Franco-German coal and steel to make European war materially impossible.", "metric_type": "TREASURY_SOLVENCY", "threshold": 300, "weight": 10},
            {"title": "Withstand Viet Minh Pressure in Tonkin", "description": "Defend northern Vietnamese garrison outposts with American military assistance.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 50, "weight": 10}
        ],
        "China": [
            {"title": "Proclaim the People's Republic of China", "description": "Mao Zedong declares the establishment of the PRC on Tiananmen gate.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10},
            {"title": "People's Volunteer Army Crosses the Yalu", "description": "Intervene in the Korean War to push UN forces back from the Chinese frontier.", "metric_type": "TERRITORIAL_CONTROL", "target": "KOR_NORTH", "weight": 10}
        ],
        "India": [
            {"title": "Adopt Democratic Republic Constitution", "description": "Enact the Constitution of India in 1950, securing universal suffrage and federal democracy.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10},
            {"title": "Mediate the Korean War Crisis", "description": "Chair the Neutral Nations Repatriation Commission to broker prisoner-of-war peace.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Initiate the First Five-Year Plan", "description": "Prioritize irrigation, dams, and agriculture to achieve food sovereignty.", "metric_type": "TREASURY_SOLVENCY", "threshold": 220, "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Survive the Tito-Stalin Split", "description": "Resist Soviet economic blockade, military troop build-ups on the border, and KGB infiltration.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10},
            {"title": "Open Commercial Lifeline to the West", "description": "Accept US grain and economic credits without abandoning self-managed socialism.", "metric_type": "TREASURY_SOLVENCY", "threshold": 160, "weight": 10}
        ],
        "Cuba": [
            {"title": "Weather Political Unrest in Havana", "description": "Batista stages a military coup in 1952, suspending the constitution amid rising public fury.", "metric_type": "TREASURY_SOLVENCY", "threshold": 100, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 3: 1953–1958 // POST-STALIN THAW & NON-ALIGNED AWAKENING
    # --------------------------------------------------------------------------
    3: {
        "USA": [
            {"title": "Conclude Korean Armistice Agreement", "description": "Sign cease-fire at Panmunjom freezing borders along the 38th parallel DMZ.", "metric_type": "TERRITORIAL_CONTROL", "target": "KOR_SOUTH", "weight": 10},
            {"title": "Eisenhower 'New Look' Deterrence", "description": "Rely on massive retaliatory nuclear capability and SAC bombers to deter aggression.", "metric_type": "AVOID_DEFCON_1", "weight": 10},
            {"title": "Halt Suez Invasion Escalation", "description": "Pressure Britain, France, and Israel into immediate ceasefire at Suez.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "USSR": [
            {"title": "Khrushchev Secret Speech & De-Stalinization", "description": "Denounce Stalin's cult of personality and reform the Gulag camp system.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10},
            {"title": "Form the Warsaw Pact Alliance", "description": "Establish unified military pact countering West Germany's integration into NATO.", "metric_type": "BUFFER_ALIGNMENT", "target": "Poland", "weight": 10},
            {"title": "Suppress the Hungarian Uprising", "description": "Deploy armor to Budapest to maintain the integrity of the socialist bloc.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_EAST", "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Operation Hurricane Atomic Weapon Success", "description": "Complete independent British nuclear deterrent test in the Montebello Islands.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Survive the Suez Crisis Fallout", "description": "Withdraw troops from Port Said and rebuild fractured relations with Washington.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 50, "weight": 10}
        ],
        "France": [
            {"title": "Exit Indochina after Dien Bien Phu", "description": "Conclude the First Indochina War at Geneva; partition Vietnam at 17th parallel.", "metric_type": "TREASURY_SOLVENCY", "threshold": 320, "weight": 10},
            {"title": "Sign the Treaty of Rome (EEC)", "description": "Co-found the European Common Market to anchor French agriculture and industry.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 60, "weight": 10}
        ],
        "China": [
            {"title": "First Five-Year Plan & Industrialization", "description": "Build heavy steel, coal, and machine tool production with Soviet advisors.", "metric_type": "TREASURY_SOLVENCY", "threshold": 250, "weight": 10},
            {"title": "First Taiwan Strait Crisis", "description": "Artillery bombardment of Nationalist offshore islands (Quemoy and Matsu).", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "India": [
            {"title": "Co-Architect the Bandung Conference (1955)", "description": "Unite 29 Asian and African states to declare neutrality and launch the Non-Aligned Movement.", "metric_type": "BUFFER_ALIGNMENT", "target": "Yugoslavia", "weight": 10},
            {"title": "Panchsheel Principles of Peaceful Coexistence", "description": "Sign the Five Principles of peaceful coexistence with Premier Zhou Enlai.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Steel Plants & Heavy Public Sector Boom", "description": "Construct state-of-the-art steel plants at Bhilai and Rourkela with foreign tech.", "metric_type": "TREASURY_SOLVENCY", "threshold": 260, "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Pioneer the Non-Aligned Movement at Brioni", "description": "Tito hosts Nehru and Nasser on the island of Brioni to formalize the Non-Aligned axis.", "metric_type": "BUFFER_ALIGNMENT", "target": "India", "weight": 10},
            {"title": "Khrushchev Reconciliation with Belgrade", "description": "Accept Soviet apology in Belgrade while defending Yugoslav ideological independence.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10}
        ],
        "Cuba": [
            {"title": "Granma Landing & Sierra Maestra Guerrillas", "description": "Fidel Castro and Che Guevara launch the revolutionary guerrilla campaign from the mountains.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 4: 1959–1963 // TO THE BRINK OF ARMAGEDDON
    # --------------------------------------------------------------------------
    4: {
        "USA": [
            {"title": "Naval Quarantine during Cuban Missile Crisis", "description": "Establish naval blockade and negotiate withdrawal of Soviet missiles in exchange for Turkey Jupiter missiles.", "metric_type": "AVOID_DEFCON_1", "weight": 15},
            {"title": "Stand Ground at Checkpoint Charlie", "description": "Maintain Allied military access rights into West Berlin following construction of the Wall.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_WEST", "weight": 10},
            {"title": "Sign the Partial Nuclear Test Ban Treaty", "description": "Outlaw atmospheric and underwater nuclear testing to protect global ecology.", "metric_type": "DETERRENCE_STABILITY", "weight": 5}
        ],
        "USSR": [
            {"title": "Deploy Nuclear Ballistic Missiles to Cuba (Operation Anadyr)", "description": "Deter US invasion of Cuba and offset Western missile superiority in Europe.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Construct the Berlin Wall (1961)", "description": "Erect fortified barrier around West Berlin to halt skilled refugee flight from the GDR.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_EAST", "weight": 10},
            {"title": "Sino-Soviet Split Ideological Severance", "description": "Recall Soviet engineers and technical blueprints from China over doctrinal rifts.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Nassau Agreement & Polaris Submarines", "description": "Secure submarine-launched Polaris ballistic missiles from the US for British deterrence.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Wind of Change Decolonization across Africa", "description": "Grant independence to Ghana, Nigeria, and Kenya in an orderly constitutional transition.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 60, "weight": 10}
        ],
        "France": [
            {"title": "De Gaulle Establishes the Fifth Republic", "description": "Return of General Charles de Gaulle to presidency with robust executive powers.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10},
            {"title": "Conclude the Algerian War via Evian Accords", "description": "Grant independence to Algeria, ending bitter eight-year conflict.", "metric_type": "TREASURY_SOLVENCY", "threshold": 380, "weight": 10},
            {"title": "First French Nuclear Test (Gerboise Bleue)", "description": "Detonate France's first atomic bomb in the Sahara, joining the nuclear club.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10}
        ],
        "China": [
            {"title": "Survive Great Leap Forward Aftermath", "description": "Restore agricultural output and rural grain reserves following economic mismanagement.", "metric_type": "TREASURY_SOLVENCY", "threshold": 200, "weight": 10},
            {"title": "1962 Sino-Indian Border War", "description": "Assert military control over Aksai Chin and declare unilateral ceasefire.", "metric_type": "TERRITORIAL_CONTROL", "target": "China", "weight": 10}
        ],
        "India": [
            {"title": "First NAM Summit in Belgrade (1961)", "description": "Co-found the formal Non-Aligned Movement alongside Tito and Nasser.", "metric_type": "BUFFER_ALIGNMENT", "target": "Yugoslavia", "weight": 10},
            {"title": "Liberation of Goa (1961)", "description": "Integrate the Portuguese colonial enclave of Goa into the Indian Union.", "metric_type": "TERRITORIAL_CONTROL", "target": "India", "weight": 10},
            {"title": "Rebuild Defense Readiness after 1962 Border War", "description": "Modernize border mountain divisions and secure Western and Soviet air defense aid.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Host the First Non-Aligned Summit in Belgrade", "description": "Welcoming 25 sovereign states to establish the Non-Aligned Charter.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Implement Market Socialist Decentralization", "description": "Grant enterprise autonomy to workers' councils to improve consumer production.", "metric_type": "TREASURY_SOLVENCY", "threshold": 200, "weight": 10}
        ],
        "Cuba": [
            {"title": "Triumph of the Cuban Revolution (1959)", "description": "Batista flees; Castro's revolutionary forces enter Havana triumphant.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 90, "weight": 10},
            {"title": "Crush the CIA Bay of Pigs Invasion (1961)", "description": "Defeat exile assault brigade at Playa Girón within 72 hours.", "metric_type": "TERRITORIAL_CONTROL", "target": "Cuba", "weight": 10},
            {"title": "Survive the Missile Crisis Quarantine", "description": "Maintain sovereign socialist state despite US naval blockade and trade embargo.", "metric_type": "AVOID_DEFCON_1", "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 5: 1964–1969 // PROXY QUAGMIRES & CULTURAL REVOLUTION
    # --------------------------------------------------------------------------
    5: {
        "USA": [
            {"title": "Vietnam War Military Escalation", "description": "Deploy combat forces to South Vietnam following the Gulf of Tonkin Resolution.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Apollo 11 Moon Landing (July 1969)", "description": "Achieve lunar landing triumph, demonstrating global technological preeminence.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10},
            {"title": "Sign Nuclear Non-Proliferation Treaty (NPT)", "description": "Co-sponsor NPT to prevent the spread of nuclear arms to non-nuclear nations.", "metric_type": "AVOID_DEFCON_1", "weight": 10}
        ],
        "USSR": [
            {"title": "Brezhnev Doctrine & Prague Spring Intervention", "description": "Crush Czechoslovak liberalization to enforce socialist bloc discipline.", "metric_type": "BUFFER_ALIGNMENT", "target": "Poland", "weight": 10},
            {"title": "Massive ICBM Parity Buildup", "description": "Expand silo-based intercontinental missile arsenal to match US warhead counts.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Military Aid to North Vietnam", "description": "Supply modern SAM anti-aircraft missiles and radar to Hanoi.", "metric_type": "TREASURY_SOLVENCY", "threshold": 800, "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Withdrawal East of Suez", "description": "End permanent military garrisons in Singapore, Malaysia, and the Persian Gulf.", "metric_type": "TREASURY_SOLVENCY", "threshold": 450, "weight": 10},
            {"title": "Refuse Troop Deployment to Vietnam", "description": "Wilson resists US pressure to send British combat units to the jungle war.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10}
        ],
        "France": [
            {"title": "Withdraw from NATO Integrated Military Command (1966)", "description": "De Gaulle evicts US headquarters from French soil while remaining in Atlantic alliance.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10},
            {"title": "Survive May 1968 Student Strikes", "description": "Restore civic order following general student riots and wildcat union strikes in Paris.", "metric_type": "TREASURY_SOLVENCY", "threshold": 420, "weight": 10}
        ],
        "China": [
            {"title": "Detonate First Atomic Bomb (Project 596, 1964)", "description": "Mushroom cloud over Lop Nur marks China's arrival as nuclear power.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Navigate the Storm of the Cultural Revolution", "description": "Mobilize Red Guards while keeping military command structures functional.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10},
            {"title": "Zhenbao Island Clash with Soviet Union (1969)", "description": "Repel Soviet border armor along the frozen Ussuri River frontier.", "metric_type": "TERRITORIAL_CONTROL", "target": "China", "weight": 10}
        ],
        "India": [
            {"title": "Defend Sovereignty in 1965 War", "description": "Repel military offensive across the Punjab and Kashmir frontiers.", "metric_type": "TERRITORIAL_CONTROL", "target": "India", "weight": 10},
            {"title": "Launch the Green Revolution", "description": "Introduce high-yielding wheat varieties and achieve national food self-sufficiency.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10},
            {"title": "Refuse to Sign Discriminatory NPT", "description": "Reject the Non-Proliferation Treaty as nuclear apartheid, reserving sovereign defense options.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Denounce Soviet Invasion of Czechoslovakia", "description": "Condemn the Brezhnev Doctrine and mobilize the Yugoslav Territorial Defense force.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10},
            {"title": "Economic Integration with Western Europe", "description": "Facilitate guest worker remittances from West Germany to boost hard currency.", "metric_type": "TREASURY_SOLVENCY", "threshold": 240, "weight": 10}
        ],
        "Cuba": [
            {"title": "Export Revolution to Latin America & Africa", "description": "Che Guevara leads guerrilla campaigns in the Congo and Bolivia.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10},
            {"title": "Weather Full US Trade Embargo", "description": "Rely on Soviet oil shipments and subsidized sugar purchases to sustain economy.", "metric_type": "TREASURY_SOLVENCY", "threshold": 120, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 6: 1970–1975 // DÉTENTE & TRIANGULAR DIPLOMACY
    # --------------------------------------------------------------------------
    6: {
        "USA": [
            {"title": "Nixon Visits Beijing (Triangular Diplomacy)", "description": "Historic breakthrough opening relations with Mao to exploit the Sino-Soviet rift.", "metric_type": "BUFFER_ALIGNMENT", "target": "China", "weight": 10},
            {"title": "Sign Strategic Arms Limitation Treaty (SALT I)", "description": "Cap anti-ballistic missile systems and ICBM launchers alongside Brezhnev in Moscow.", "metric_type": "AVOID_DEFCON_1", "weight": 10},
            {"title": "Withdrawal from Vietnam & Paris Peace Accords", "description": "Complete US combat troop pullout from Southeast Asia.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 60, "weight": 10}
        ],
        "USSR": [
            {"title": "Sign the Helsinki Final Act (1975)", "description": "Secure Western recognition of post-WWII European borders and Soviet sphere in Eastern Europe.", "metric_type": "BUFFER_ALIGNMENT", "target": "Poland", "weight": 10},
            {"title": "Summit Détente with the West", "description": "Expand grain imports from the US and sign the Apollo-Soyuz joint space handshake.", "metric_type": "TREASURY_SOLVENCY", "threshold": 950, "weight": 10},
            {"title": "Support Communist Victory in Vietnam", "description": "Supply artillery and armor leading to the 1975 Fall of Saigon and Vietnamese reunification.", "metric_type": "TERRITORIAL_CONTROL", "target": "Vietnam", "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Accession to the European Economic Community (1973)", "description": "Enter the Common Market to revitalize industrial exports and financial services.", "metric_type": "TREASURY_SOLVENCY", "threshold": 500, "weight": 10},
            {"title": "Weather 1973 OPEC Oil Shock", "description": "Manage emergency fuel rationing and economic stagflation following Yom Kippur War.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 50, "weight": 10}
        ],
        "France": [
            {"title": "Deploy First Nuclear Submarines (SNLE)", "description": "Launch the Redoutable class ballistic missile submarine for invulnerable sea deterrence.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Pioneer European Space Independence (Ariane)", "description": "Lead the foundation of the European Space Agency and launch rocket programs.", "metric_type": "TREASURY_SOLVENCY", "threshold": 500, "weight": 10}
        ],
        "China": [
            {"title": "Restore UN Seat & Expel Taiwan (1971)", "description": "UN General Assembly recognizes PRC as the sole legitimate government of China.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Establish Bilateral Ties with Washington", "description": "Joint Sino-US Communiqué in Shanghai opposing hegemony in the Asia-Pacific.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "India": [
            {"title": "Liberation of Bangladesh in 1971 War", "description": "Defeat Pakistan armed forces in East Bengal, securing the birth of sovereign Bangladesh.", "metric_type": "TERRITORIAL_CONTROL", "target": "India", "weight": 15},
            {"title": "Operation Smiling Buddha Nuclear Test (1974)", "description": "Conduct peaceful underground nuclear explosion at Pokhran, achieving nuclear capability.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Sign 1971 Indo-Soviet Treaty of Friendship", "description": "Secure Soviet diplomatic umbrella to deter US Seventh Fleet and Chinese intervention.", "metric_type": "BUFFER_ALIGNMENT", "target": "USSR", "weight": 5}
        ],
        "Yugoslavia": [
            {"title": "Promulgate the 1974 Yugoslav Constitution", "description": "Grant maximum autonomy to six republics and two provinces (Kosovo and Vojvodina).", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10},
            {"title": "Host Conference on Security and Co-operation in Europe", "description": "Promote non-aligned diplomacy at the Helsinki Accords process.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "Cuba": [
            {"title": "Operation Carlota: Military Mission to Angola", "description": "Deploy tens of thousands of Cuban troops to defend the MPLA in the Angolan Civil War.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Join Comecon (CMEA)", "description": "Full integration into the socialist economic trade bloc with guaranteed oil subsidies.", "metric_type": "TREASURY_SOLVENCY", "threshold": 160, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 7: 1976–1980 // THE SECOND COLD WAR & THE AFGHAN TRAP
    # --------------------------------------------------------------------------
    7: {
        "USA": [
            {"title": "Camp David Accords Peace Treaty (1978)", "description": "Broker historic peace treaty between Egypt and Israel.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Respond to the Iran Hostage Crisis", "description": "Impose sanctions and embargoes following seizure of the US Embassy in Tehran.", "metric_type": "TREASURY_SOLVENCY", "threshold": 2600, "weight": 10},
            {"title": "Carter Doctrine & Boycott Moscow Olympics", "description": "Declare Persian Gulf a vital US security interest following Soviet Afghan invasion.", "metric_type": "AVOID_DEFCON_1", "weight": 10}
        ],
        "USSR": [
            {"title": "Invasion of Afghanistan (December 1979)", "description": "Deploy 40th Army to Kabul to preserve client communist regime against insurgents.", "metric_type": "TERRITORIAL_CONTROL", "target": "Iran", "weight": 10},
            {"title": "Deploy SS-20 Saber Intermediate Missiles", "description": "Place modern mobile nuclear missiles targeting European capitals.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Suppress Polish Solidarity Movement", "description": "Pressure Warsaw authorities to declare martial law and ban the trade union.", "metric_type": "BUFFER_ALIGNMENT", "target": "Poland", "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Election of Margaret Thatcher (1979)", "description": "Launch economic deregulation, privatize state industries, and reinforce Atlantic alliance.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10},
            {"title": "Agree to Station US Cruise Missiles at Greenham Common", "description": "Support NATO dual-track decision countering Soviet SS-20s.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10}
        ],
        "France": [
            {"title": "Mirage 2000 Fighter Jet Deployment", "description": "Strengthen high-altitude air defense interception capabilities.", "metric_type": "TREASURY_SOLVENCY", "threshold": 600, "weight": 10},
            {"title": "Operation Caban in Central Africa", "description": "Execute military operations to preserve French geopolitical interests in Francophone Africa.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10}
        ],
        "China": [
            {"title": "Deng Xiaoping Launches Reform and Opening-Up (1978)", "description": "Historic plenum introduces Special Economic Zones and market agricultural incentives.", "metric_type": "TREASURY_SOLVENCY", "threshold": 380, "weight": 10},
            {"title": "1979 Sino-Vietnamese War", "description": "Launch punitive border incursion into Vietnam to counter Soviet-backed expansion.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "India": [
            {"title": "Launch First Indian Satellite (Aryabhata)", "description": "Orbit first domestic satellite, demonstrating civilian space capability.", "metric_type": "TREASURY_SOLVENCY", "threshold": 320, "weight": 10},
            {"title": "Balance Regional Geopolitics after Afghan War", "description": "Maintain cordial ties with Moscow while preventing superpower arms race in Pakistan.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Sustain Democratic Resilience", "description": "Restore constitutional democratic norms following the 1977 general election.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Mourn the Passing of Marshal Tito (May 1980)", "description": "Tito passes away in Ljubljana; conduct peaceful transition to rotating collective presidency.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10},
            {"title": "Manage Ballooning Foreign Debt Crisis", "description": "Negotiate IMF debt rescheduling while battling rising inflation across republics.", "metric_type": "TREASURY_SOLVENCY", "threshold": 200, "weight": 10}
        ],
        "Cuba": [
            {"title": "Host the 6th Non-Aligned Summit in Havana (1979)", "description": "Fidel Castro chairs the NAM summit, advocating revolutionary solidarity.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Mariel Boatlift Crisis (1980)", "description": "Manage mass emigration of 125,000 citizens to Florida while maintaining security.", "metric_type": "TREASURY_SOLVENCY", "threshold": 140, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 8: 1981–1984 // STAR WARS & NUCLEAR BRINKMANSHIP
    # --------------------------------------------------------------------------
    8: {
        "USA": [
            {"title": "Strategic Defense Initiative (SDI 'Star Wars')", "description": "Fund research into space-based laser anti-missile shields to make ICBMs obsolete.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10},
            {"title": "Reagan Doctrine Global Freedom Fighters", "description": "Provide Stinger missiles to Afghan Mujahideen and aid Contras in Nicaragua.", "metric_type": "BUFFER_ALIGNMENT", "target": "Iran", "weight": 10},
            {"title": "Survive the Able Archer 83 War Scare", "description": "De-escalate nuclear readiness drills without provoking Soviet preemptive launch.", "metric_type": "AVOID_DEFCON_1", "weight": 10}
        ],
        "USSR": [
            {"title": "Operate Operation RYAN Intelligence Alert", "description": "KGB and GRU place global assets on alert for suspected Western surprise attack.", "metric_type": "AVOID_DEFCON_1", "weight": 10},
            {"title": "Counter KAL 007 International Fallout", "description": "Contain diplomatic crisis after interceptor jets down South Korean airliner.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10},
            {"title": "Sustain Military War Effort in Afghanistan", "description": "Maintain airborne assaults against stubborn Mujahideen valley strongholds.", "metric_type": "TREASURY_SOLVENCY", "threshold": 750, "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Victory in the Falklands War (1982)", "description": "Deploy royal naval task force 8,000 miles to recapture Falkland Islands from Argentina.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 15},
            {"title": "Trident Nuclear Submarine Upgrade", "description": "Secure agreement with Reagan for American Trident II ballistic missiles.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10}
        ],
        "France": [
            {"title": "Election of François Mitterrand (1981)", "description": "First socialist president of Fifth Republic enacts welfare expansion and nationalizations.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10},
            {"title": "Firm Stance against Soviet Euromissiles", "description": "Mitterrand addresses German Bundestag supporting NATO missile deployment.", "metric_type": "DETERRENCE_STABILITY", "weight": 10}
        ],
        "China": [
            {"title": "Sino-British Joint Declaration on Hong Kong (1984)", "description": "Deng and Thatcher agree to return Hong Kong in 1997 under 'One Country, Two Systems'.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Establish Shenzhen Special Economic Zone", "description": "Attract foreign direct investment and launch high-tech manufacturing boom.", "metric_type": "TREASURY_SOLVENCY", "threshold": 500, "weight": 10}
        ],
        "India": [
            {"title": "Operation Meghdoot on Siachen Glacier (1984)", "description": "Secure highest battlefield in the world in the Karakoram range.", "metric_type": "TERRITORIAL_CONTROL", "target": "India", "weight": 10},
            {"title": "Host NAM & CHOGM Summits in New Delhi", "description": "Indira Gandhi leads global Non-Aligned diplomacy and South-South economic co-operation.", "metric_type": "BUFFER_ALIGNMENT", "target": "Yugoslavia", "weight": 10},
            {"title": "Preserve National Unity amid Internal Crisis", "description": "Weather domestic political friction and preserve constitutional continuity.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Host the 1984 Winter Olympics in Sarajevo", "description": "Global showcase of Yugoslav hospitality, modern sports infrastructure, and unity.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Contain Rising Ethnic Tensions in Kosovo", "description": "Prevent student and nationalist protests from fracturing the federal union.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 65, "weight": 10}
        ],
        "Cuba": [
            {"title": "Decisive Turn in the Angolan Civil War", "description": "Reinforce frontline battalions and MiG-23 squadrons against South African armor.", "metric_type": "TERRITORIAL_CONTROL", "target": "Cuba", "weight": 10},
            {"title": "Food Security & Defense Mobilization", "description": "Construct nationwide bomb shelters against anticipated US invasion under Reagan.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 80, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 9: 1985–1989 // GLASNOST, PERESTROIKA & FALL OF THE WALL
    # --------------------------------------------------------------------------
    9: {
        "USA": [
            {"title": "Sign the Intermediate-Range Nuclear Forces (INF) Treaty (1987)", "description": "Reagan and Gorbachev agree to dismantle an entire class of land-based nuclear missiles.", "metric_type": "AVOID_DEFCON_1", "weight": 15},
            {"title": "Tear Down This Wall! Berlin Challenge", "description": "Reagan demands at Brandenburg Gate that Gorbachev open the border barrier.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Support Peaceful Democratic Transitions in Eastern Europe", "description": "Encourage peaceful transitions as the Berlin Wall falls on November 9, 1989.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_WEST", "weight": 10}
        ],
        "USSR": [
            {"title": "Launch Glasnost (Openness) & Perestroika (Restructuring)", "description": "Permit political debate, relax press censorship, and reform command economy.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10},
            {"title": "Manage the Chernobyl Disaster Catastrophe (1986)", "description": "Entomb Reactor 4 in concrete sarcophagus and evacuate contaminated exclusion zones.", "metric_type": "TREASURY_SOLVENCY", "threshold": 650, "weight": 10},
            {"title": "Withdraw the 40th Army from Afghanistan (1989)", "description": "Cross the Friendship Bridge over the Amu Darya, concluding 10-year conflict.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Thatcher-Gorbachev Diplomatic Channel", "description": "Thatcher declares 'We can do business together,' facilitating US-Soviet summits.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Financial Big Bang (1986)", "description": "Deregulation cements London's position as the financial capital of Europe.", "metric_type": "TREASURY_SOLVENCY", "threshold": 650, "weight": 10}
        ],
        "France": [
            {"title": "Channel Tunnel Construction (Eurotunnel)", "description": "Break ground on mega-engineering undersea tunnel linking France and Britain.", "metric_type": "TREASURY_SOLVENCY", "threshold": 700, "weight": 10},
            {"title": "Prepare Single European Act & Monetary Union", "description": "Lay foundations for the European Union alongside German Chancellor Kohl.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10}
        ],
        "China": [
            {"title": "Maintain Political Stability in 1989", "description": "Clear Tiananmen Square and maintain communist party authority over modernization.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10},
            {"title": "Accelerate Coastal Export Economy", "description": "Expand manufacturing zones in Guangdong to drive double-digit GDP expansion.", "metric_type": "TREASURY_SOLVENCY", "threshold": 750, "weight": 10}
        ],
        "India": [
            {"title": "Pioneer Computer & Telecom Revolution", "description": "Establish nationwide software technology parks and digital telecommunications.", "metric_type": "TREASURY_SOLVENCY", "threshold": 400, "weight": 10},
            {"title": "Peacekeeping Mission in Sri Lanka (IPKF)", "description": "Deploy peacekeepers to implement the Indo-Sri Lanka peace accord.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Integrated Guided Missile Program (Prithvi & Agni)", "description": "Test surface-to-surface ballistic missiles to safeguard national frontiers.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Confront Hyperinflation Crisis", "description": "Introduce currency reform to halt run on the Yugoslav dinar.", "metric_type": "TREASURY_SOLVENCY", "threshold": 150, "weight": 10},
            {"title": "Resist Nationalist Polarization", "description": "Prevent nationalist rhetoric in Belgrade and Zagreb from tearing the league apart.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 50, "weight": 10}
        ],
        "Cuba": [
            {"title": "Decisive Triumph at Cuito Cuanavale (1988)", "description": "Halt South African armor in Angola, forcing Namibia's independence and retreat of apartheid forces.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 90, "weight": 10},
            {"title": "Prepare for the 'Special Period'", "description": "Ration strategic reserves as Soviet oil deliveries drop amid Moscow's crisis.", "metric_type": "TREASURY_SOLVENCY", "threshold": 110, "weight": 10}
        ]
    },

    # --------------------------------------------------------------------------
    # ERA 10: 1990–1991 // THE FINAL CURTAIN & SOVIET DISSOLUTION
    # --------------------------------------------------------------------------
    10: {
        "USA": [
            {"title": "Operation Desert Storm (Gulf War 1991)", "description": "Lead 35-nation coalition to liberate Kuwait with joint UN consensus.", "metric_type": "TERRITORIAL_CONTROL", "target": "Iran", "weight": 10},
            {"title": "Two-Plus-Four Treaty & German Reunification", "description": "Shepherd peaceful reunification of Germany inside NATO.", "metric_type": "TERRITORIAL_CONTROL", "target": "GER_WEST", "weight": 10},
            {"title": "Peaceful Soviet Dissolution & START I", "description": "Sign START I arms reduction; ensure Soviet nuclear arsenal remains under secure unified control.", "metric_type": "AVOID_DEFCON_1", "weight": 15}
        ],
        "USSR": [
            {"title": "Survive the August Coup Attempt (1991)", "description": "Hardline communist coup collapses after popular resistance in Moscow led by Yeltsin.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 50, "weight": 10},
            {"title": "Manage Orderly Transition to Sovereign Republics", "description": "Facilitate peaceful devolution of power to 15 independent nations (CIS).", "metric_type": "AVOID_DEFCON_1", "weight": 10},
            {"title": "Safeguard the Nuclear Command Chain", "description": "Consolidate strategic warheads from Ukraine, Kazakhstan, and Belarus to Moscow.", "metric_type": "NUCLEAR_DETERRENCE", "weight": 10}
        ],
        "United Kingdom": [
            {"title": "Deploy Desert Rats to Liberation of Kuwait", "description": "British armored division plays key role in Gulf War coalition victory.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10},
            {"title": "Negotiate Maastricht Treaty Opt-Outs", "description": "Secure national opt-outs on the Euro currency while shaping the new European Union.", "metric_type": "TREASURY_SOLVENCY", "threshold": 700, "weight": 10}
        ],
        "France": [
            {"title": "Sign the Maastricht Treaty (Birth of the EU)", "description": "Establish the European Union and commit to the future Euro single currency.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10},
            {"title": "Deploy Division Daguet to the Gulf War", "description": "Protect the coalition's western flank during the liberation of Kuwait.", "metric_type": "TREASURY_SOLVENCY", "threshold": 750, "weight": 10}
        ],
        "China": [
            {"title": "Deng Xiaoping's Southern Tour (1992 Preview)", "description": "Cement permanent commitment to market socialist reforms and private enterprise.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 85, "weight": 10},
            {"title": "Maintain Sovereign Cohesion post-Soviet Collapse", "description": "Avoid ideological collapse that destroyed the USSR; build strong trade surpluses.", "metric_type": "TREASURY_SOLVENCY", "threshold": 900, "weight": 10}
        ],
        "India": [
            {"title": "1991 Economic Liberalization & Balance of Payments Crisis", "description": "Finance Minister Manmohan Singh dismantles the 'License Raj', opening the economy to global trade.", "metric_type": "TREASURY_SOLVENCY", "threshold": 480, "weight": 15},
            {"title": "Anchor 'Look East' Foreign Policy", "description": "Expand strategic and commercial partnerships with ASEAN and East Asian tigers.", "metric_type": "DETERRENCE_STABILITY", "weight": 10},
            {"title": "Maintain Sovereign Independence in the Unipolar World", "description": "Preserve autonomous nuclear and military doctrine following Soviet collapse.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 75, "weight": 10}
        ],
        "Yugoslavia": [
            {"title": "Prevent Descent into Total Civil War", "description": "Slovenia and Croatia declare independence; federal army struggles to contain conflict.", "metric_type": "AVOID_DEFCON_1", "weight": 10},
            {"title": "Preserve Common Market Assets", "description": "Protect industrial lifelines amidst ethnic polarization and international embargoes.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 40, "weight": 10}
        ],
        "Cuba": [
            {"title": "Survive the 'Special Period in Peacetime'", "description": "Survive the total collapse of Soviet oil subsidies and 80% loss of foreign trade.", "metric_type": "TREASURY_SOLVENCY", "threshold": 100, "weight": 15},
            {"title": "Preserve Socialist Sovereign Continuity", "description": "Adopt bicycle transport, urban organic agriculture, and biotech to endure without Moscow.", "metric_type": "DOMESTIC_APPROVAL", "threshold": 70, "weight": 10}
        ]
    }
}
