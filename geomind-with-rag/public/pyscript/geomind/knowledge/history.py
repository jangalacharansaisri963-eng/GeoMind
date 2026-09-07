"""
Comprehensive History Knowledge Base: Events, Figures, Causes, Consequences, and Civilizations.
"""
from typing import Any, Dict, List, Optional
import os
import json
from geomind.core.types import Domain, Intent, QueryResult
from geomind.knowledge.base import KnowledgeSource


_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load_hist_json(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(_DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


ERAS_CACHE: Dict[str, Dict[str, Any]] = {}
for _era in _load_hist_json("historical_eras.json"):
    ERAS_CACHE[_era["name"].lower()] = _era
    for _a in _era.get("aliases", []):
        ERAS_CACHE[_a.lower()] = _era


HISTORICAL_EVENTS: Dict[str, Dict[str, Any]] = {
    "world war 1": {
        "title": "World War I",
        "aliases": ["ww1", "wwi", "world war i", "world war 1", "first world war", "the great war"],
        "period": "July 28, 1914 – November 11, 1918",
        "overview": "A catastrophic global conflict originating in Europe that pitted the Allied Powers (France, Great Britain, Russia, Italy, and later the United States) against the Central Powers (Germany, Austria-Hungary, Ottoman Empire, and Bulgaria).",
        "causes": [
            "M-A-I-N Causes: Militarism (arms races, naval competition), Alliances (entangling mutual defense treaties), Imperialism (colonial rivalry in Africa and Asia), and Nationalism (ethnic tensions in the Balkans).",
            "Immediate Catalyst: The assassination of Archduke Franz Ferdinand of Austria and his wife Sophie in Sarajevo on June 28, 1914, by Gavrilo Princip (a Bosnian Serb nationalist associated with the Black Hand)."
        ],
        "consequences": [
            "Collapse of four major continental empires: the Russian Empire (Bolshevik Revolution 1917), German Empire, Austro-Hungarian Empire, and Ottoman Empire.",
            "Treaty of Versailles (1919): Imposed severe reparations, territorial losses, and the 'War Guilt Clause' on Germany, which fostered deep resentment that later contributed to World War II.",
            "Creation of the League of Nations to promote international peace and collective security.",
            "Redrawing of the map of Europe and the Middle East (e.g., creation of Poland, Czechoslovakia, Yugoslavia; the Sykes-Picot Agreement and mandates in the Middle East).",
            "Devastating human toll: an estimated 20 million deaths (military and civilian) and 21 million wounded, followed immediately by the 1918 Spanish Flu pandemic."
        ],
        "key_figures": ["Archduke Franz Ferdinand", "Woodrow Wilson", "Kaiser Wilhelm II", "David Lloyd George", "Georges Clemenceau", "Tsar Nicholas II"]
    },
    "world war 2": {
        "title": "World War II",
        "aliases": ["ww2", "wwii", "world war ii", "world war 2", "second world war"],
        "period": "September 1, 1939 – September 2, 1945",
        "overview": "The deadliest conflict in human history, involving the vast majority of the world's nations formed into two opposing military alliances: the Allies and the Axis powers (Nazi Germany, Imperial Japan, and Fascist Italy).",
        "causes": [
            "The punitive terms and instability created by the 1919 Treaty of Versailles.",
            "The worldwide Great Depression (1929), which destabilized democracies and fueled the rise of totalitarian fascist regimes in Germany, Italy, and Japan.",
            "Aggressive expansionism and militarism: Japanese invasion of Manchuria (1931), Italian invasion of Ethiopia (1935), and Nazi rearmament and territorial annexations.",
            "Failure of the League of Nations and the policy of appeasement by Western democracies.",
            "Immediate Catalyst: Nazi Germany's invasion of Poland on September 1, 1939, prompting Britain and France to declare war."
        ],
        "consequences": [
            "Complete defeat of the Axis powers and unconditional surrender of Germany and Japan.",
            "The Holocaust: Systematic genocide by the Nazi regime murdering six million European Jews and millions of others (Romani, Soviet prisoners, disabled people, dissidents).",
            "Beginning of the Atomic Age following the U.S. atomic bombings of Hiroshima and Nagasaki in August 1945.",
            "Establishment of the United Nations (UN) in 1945 to replace the defunct League of Nations.",
            "Emergence of two global superpowers—the United States and the Soviet Union—ushering in the Cold War era.",
            "Accelerated decolonization across Asia and Africa (including independence for India in 1947).",
            "Human toll: An estimated 70 to 85 million fatalities, representing about 3% of the 1940 world population."
        ],
        "key_figures": ["Winston Churchill", "Franklin D. Roosevelt", "Adolf Hitler", "Joseph Stalin", "Harry S. Truman", "Dwight D. Eisenhower", "Hideki Tojo"]
    },
    "french revolution": {
        "title": "The French Revolution",
        "aliases": ["french rev", "revolution of 1789"],
        "period": "1789 – 1799",
        "overview": "A transformative period of social and political upheaval in France that completely dismantled the Ancien Régime, overthrew the Bourbon monarchy, and established a secular republic based on Enlightenment principles.",
        "causes": [
            "Severe financial crisis and national debt driven by French involvement in the American Revolutionary War and Seven Years' War.",
            "Deep social inequality in the Estate System: The First Estate (Clergy) and Second Estate (Nobility) enjoyed tax exemptions and feudal privileges, while the heavily taxed Third Estate (commoners, peasants, bourgeoisie) had negligible political power.",
            "Enlightenment ideas advocating popular sovereignty, individual liberties, and separation of powers (Rousseau, Voltaire, Montesquieu).",
            "Agricultural failure and widespread food shortages (famine, soaring bread prices in 1788–1789)."
        ],
        "consequences": [
            "Abolition of feudalism, hereditary nobility, and clerical privileges in France.",
            "Declaration of the Rights of Man and of the Citizen (1789), affirming universal natural human equality and popular sovereignty.",
            "Execution of King Louis XVI and Queen Marie Antoinette by guillotine (1793) and the radical Reign of Terror led by Maximilien Robespierre.",
            "Rise of Napoleon Bonaparte, who seized power in the Coup of 18 Brumaire (1799) and crowned himself Emperor in 1804.",
            "Spread of nationalism, legal equality (Napoleonic Code), and democratic ideals across Europe and Latin America."
        ],
        "key_figures": ["Louis XVI", "Maximilien Robespierre", "Napoleon Bonaparte", "Jean-Paul Marat", "Georges Danton", "Marie Antoinette"]
    },
    "american revolution": {
        "title": "The American Revolution",
        "aliases": ["american revolutionary war", "us war of independence"],
        "period": "1775 – 1783",
        "overview": "An epic political and military struggle through which Thirteen North American colonies rejected British monarchical rule to forge an independent sovereign republic: the United States of America.",
        "causes": [
            "'Taxation without representation': British imposition of taxes without colonial parliamentary representation (Stamp Act 1765, Townshend Acts 1767, Tea Act 1773).",
            "Enforcement of the Coercive / Intolerable Acts (1774) following the Boston Tea Party (1773).",
            "Growing intellectual influence of Enlightenment philosophers, especially John Locke's theories of natural rights (life, liberty, property) and social contract.",
            "Skirmishes at Lexington and Concord (April 1775) sparking active armed hostilities."
        ],
        "consequences": [
            "Declaration of Independence (July 4, 1776) authored by Thomas Jefferson.",
            "Recognition of American independence by Great Britain in the Treaty of Paris (1783).",
            "Drafting and ratification of the United States Constitution (1787) and Bill of Rights (1791), establishing a federal republic with separation of powers.",
            "Inspiration for subsequent democratic revolutions worldwide, notably the French Revolution and Latin American wars of independence."
        ],
        "key_figures": ["George Washington", "Thomas Jefferson", "Benjamin Franklin", "John Adams", "Alexander Hamilton", "King George III"]
    },
    "industrial revolution": {
        "title": "The Industrial Revolution",
        "aliases": ["first industrial revolution"],
        "period": "c. 1760 – 1840",
        "overview": "The great socio-economic transition from agrarian, handicraft economies to mechanized, factory-based manufacturing powered by steam and machine tools, originating in Great Britain.",
        "causes": [
            "Abundant domestic natural resources in Britain (coal, iron ore) and access to global raw materials through colonial commerce.",
            "Invention of transformative mechanical technologies: James Watt's improved steam engine, the spinning jenny, and the power loom.",
            "Agricultural Revolution in Britain freeing rural surplus labor for industrial factory work.",
            "A stable legal and financial system protecting patents, capital investments, and private property."
        ],
        "consequences": [
            "Mass urbanization: Rapid migration of populations from rural villages to industrial manufacturing centers (e.g., Manchester, Birmingham).",
            "Dramatic expansion of global productivity, international trade, and the rise of industrial capitalism.",
            "Harsh early labor conditions (child labor, 14-16 hour workdays, dangerous environments), leading to the birth of trade unions and socialist philosophy (Marx and Engels).",
            "Development of modern transportation networks (steam locomotives, railways, steamships) and telegraph communications."
        ],
        "key_figures": ["James Watt", "Eli Whitney", "Richard Arkwright", "George Stephenson", "Karl Marx", "Adam Smith"]
    },
    "cold war": {
        "title": "The Cold War",
        "aliases": ["the cold war era"],
        "period": "1947 – 1991",
        "overview": "An intense geopolitical, ideological, and economic confrontation between the capitalist Western Bloc (led by the United States and NATO) and the communist Eastern Bloc (led by the Soviet Union and Warsaw Pact).",
        "causes": [
            "Fundamental ideological incompatibility between liberal capitalism and Marxist-Leninist communism.",
            "Post-WWII division of Europe and Soviet establishment of satellite communist regimes in Eastern Europe (the 'Iron Curtain').",
            "Mutual distrust over atomic weapons and conflicting visions for post-war European reconstruction."
        ],
        "consequences": [
            "Nuclear arms race and the doctrine of Mutually Assured Destruction (MAD).",
            "Major regional proxy wars (Korean War, Vietnam War, Soviet-Afghan War).",
            "The Space Race: Pioneered human spaceflight, culminating in the Apollo 11 Moon landing (1969) and satellite technologies.",
            "Collapse of the Soviet Union (December 1991) and dissolution of the Warsaw Pact, ending bipolarity and leading to the enlargement of NATO and the European Union."
        ],
        "key_figures": ["Harry S. Truman", "Joseph Stalin", "John F. Kennedy", "Nikita Khrushchev", "Ronald Reagan", "Mikhail Gorbachev"]
    }
}


HISTORICAL_FIGURES: Dict[str, Dict[str, Any]] = {
    "napoleon bonaparte": {
        "name": "Napoleon Bonaparte",
        "aliases": ["napoleon", "bonaparte", "emperor napoleon"],
        "period": "1769 – 1821",
        "role": "French Military Commander and Emperor of the French",
        "overview": "A brilliant Corsican-born general who rose during the French Revolution, seized power in 1799, and dominated European continental affairs through the Napoleonic Wars before his final defeat at Waterloo (1815).",
        "key_achievements": [
            "Napoleonic Code (Civil Code of 1804): Standardized civil law across France and Europe, abolishing feudal privileges and establishing legal equality and secularism.",
            "Conquered much of continental Europe, establishing client kingdoms and reforming administrative and educational institutions.",
            "Reorganized the French financial system, creating the Bank of France."
        ],
        "significance": "Transformed modern military tactics, spread modern legal institutions and metric standardization throughout Europe, and unintentionally stimulated 19th-century European nationalism."
    },
    "mahatma gandhi": {
        "name": "Mahatma Gandhi",
        "aliases": ["gandhi", "mohandas gandhi", "bapu"],
        "period": "1869 – 1948",
        "role": "Leader of the Indian Independence Movement",
        "overview": "An Indian lawyer, anti-colonial nationalist, and political ethicist who pioneered Satyagraha—mass civil disobedience through nonviolent resistance—leading India to independence from British rule in 1947.",
        "key_achievements": [
            "Led historic mass nonviolent movements: Non-Cooperation Movement (1920), the Salt March (Dandi March, 1930), and the Quit India Movement (1942).",
            "Championed social reform in India, advocating for women's rights, religious harmony, and the eradication of untouchability.",
            "Showcased nonviolent resistance as a practical strategy for social and political change."
        ],
        "significance": "Globally inspired civil rights and freedom movements, directly influencing Martin Luther King Jr., Nelson Mandela, and the Dalai Lama."
    },
    "julius caesar": {
        "name": "Julius Caesar",
        "aliases": ["caesar", "gaius julius caesar"],
        "period": "100 BC – 44 BC",
        "role": "Roman General, Statesman, and Dictator",
        "overview": "A celebrated Roman general and statesman whose military conquest of Gaul and subsequent civil war transformed the Roman Republic into the Roman Empire.",
        "key_achievements": [
            "Conquest of Gaul (58–50 BC), vastly expanding Roman territory to the Atlantic Ocean and English Channel.",
            "Crossed the Rubicon River in 49 BC, starting a civil war and emerging as Dictator perpetuo (dictator in perpetuity).",
            "Reformed the Roman calendar (Julian calendar), introducing the 365-day year with leap years."
        ],
        "significance": "His assassination on the Ides of March (March 15, 44 BC) by Roman senators led to further civil wars and the eventual rise of his adopted heir, Augustus, the first Roman Emperor."
    },
    "abraham lincoln": {
        "name": "Abraham Lincoln",
        "aliases": ["lincoln", "honest abe"],
        "period": "1809 – 1865",
        "role": "16th President of the United States",
        "overview": "Presided over the United States during the American Civil War (1861–1865), successfully preserving the Union, abolishing slavery, and bolstering the federal government.",
        "key_achievements": [
            "Issued the Emancipation Proclamation (January 1, 1863), declaring all enslaved persons in Confederate states free.",
            "Delivered the historic Gettysburg Address (November 1863), redefining the Civil War as a dedication to human equality and democracy.",
            "Championed the passage of the Thirteenth Amendment to the U.S. Constitution, which permanently banned slavery."
        ],
        "significance": "Widely regarded as one of the greatest U.S. presidents for his moral leadership, preservation of democratic government, and ending institutional slavery."
    },
    "alexander the great": {
        "name": "Alexander the Great",
        "aliases": ["alexander iii of macedon", "alexander"],
        "period": "356 BC – 323 BC",
        "role": "King of Macedonia and Conqueror",
        "overview": "A Macedonian king who conquered the mighty Achaemenid Persian Empire and created one of history's largest contiguous empires, stretching from Greece to northwestern India by age 30.",
        "key_achievements": [
            "Remained undefeated in battle, utilizing superior phalanx infantry and companion cavalry tactics (Battles of Issus and Gaugamela).",
            "Founded over twenty cities bearing his name, most famously Alexandria in Egypt.",
            "Spread Greek language, philosophy, science, and art across the Mediterranean and Near East."
        ],
        "significance": "Initiated the Hellenistic Era, characterized by extensive cultural synthesis between Greek, Persian, Egyptian, and Indian civilizations."
    }
}


class HistoryKnowledgeSource(KnowledgeSource):
    """Knowledge engine for historical events, figures, causes, and consequences."""

    @property
    def domain(self) -> Domain:
        return Domain.HISTORY

    def can_handle(self, intent: Intent, text: str) -> bool:
        return intent in {
            Intent.HISTORICAL_EVENT,
            Intent.HISTORICAL_FIGURE,
            Intent.CAUSE_AND_CONSEQUENCE
        }

    def find_event(self, term: str) -> Optional[Dict[str, Any]]:
        clean = term.strip().lower()
        if clean in HISTORICAL_EVENTS:
            return HISTORICAL_EVENTS[clean]
        for key, event in HISTORICAL_EVENTS.items():
            if clean == event["title"].lower() or clean in event["aliases"] or clean in key or any(alias in clean for alias in event["aliases"]):
                return event
        return None

    def find_figure(self, term: str) -> Optional[Dict[str, Any]]:
        clean = term.strip().lower()
        if clean in HISTORICAL_FIGURES:
            return HISTORICAL_FIGURES[clean]
        for key, fig in HISTORICAL_FIGURES.items():
            if clean == fig["name"].lower() or clean in fig["aliases"] or clean in key or any(alias in clean for alias in fig["aliases"]):
                return fig
        return None

    def query(self, intent: Intent, entities: List[str], raw_text: str, context: Optional[str] = None) -> Optional[QueryResult]:
        if not entities:
            return None

        primary = entities[0].lower().strip()

        # Check if entity is a historical event
        event = self.find_event(primary)
        if event:
            causes_formatted = "\n".join(f"- {c}" for c in event["causes"])
            consequences_formatted = "\n".join(f"- {c}" for c in event["consequences"])
            figures_formatted = ", ".join(f"**{f}**" for f in event["key_figures"])

            # If user specifically asked for causes or consequences
            if intent == Intent.CAUSE_AND_CONSEQUENCE:
                text = (
                    f"📜 **Historical Analysis: Causes & Consequences of {event['title']}**\n\n"
                    f"**Period**: {event['period']}\n\n"
                    f"### 🔍 Root Causes & Catalysts\n{causes_formatted}\n\n"
                    f"### 🌍 Lasting Consequences & Global Impact\n{consequences_formatted}\n\n"
                    f"### 👤 Key Historical Figures\n{figures_formatted}"
                )
                return QueryResult(
                    text=text,
                    interpreted_query=f"causes and consequences of {event['title']}",
                    domain=Domain.HISTORY,
                    intent=Intent.CAUSE_AND_CONSEQUENCE,
                    entities=[(primary, event["title"])],
                    metadata=event,
                    sources=["GeoMind Historical Compendium", "Cambridge World History"]
                )

            # Full Event overview
            text = (
                f"🏛️ **Historical Event: {event['title']}**\n\n"
                f"**Date / Era**: {event['period']}\n\n"
                f"{event['overview']}\n\n"
                f"### 🔍 Key Causes\n{causes_formatted}\n\n"
                f"### 💥 Major Consequences\n{consequences_formatted}\n\n"
                f"### 👤 Key Figures Involved\n{figures_formatted}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"historical overview of {event['title']}",
                domain=Domain.HISTORY,
                intent=Intent.HISTORICAL_EVENT,
                entities=[(primary, event["title"])],
                metadata=event,
                sources=["GeoMind Historical Compendium"]
            )

        # Check if entity is a historical figure
        figure = self.find_figure(primary)
        if figure:
            achievements_str = "\n".join(f"- {a}" for a in figure["key_achievements"])
            text = (
                f"👤 **Historical Figure: {figure['name']}**\n\n"
                f"- **Era**: {figure['period']}\n"
                f"- **Role**: {figure['role']}\n\n"
                f"{figure['overview']}\n\n"
                f"### 🏆 Key Achievements & Actions\n{achievements_str}\n\n"
                f"### 🌟 Enduring Historical Significance\n{figure['significance']}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"biography of {figure['name']}",
                domain=Domain.HISTORY,
                intent=Intent.HISTORICAL_FIGURE,
                entities=[(primary, figure["name"])],
                metadata=figure,
                sources=["GeoMind Biographical Archives"]
            )

        # Check if entity is a historical era
        if primary in ERAS_CACHE:
            era = ERAS_CACHE[primary]
            features_str = "\n".join(f"- {f}" for f in era.get("major_developments", []))
            figures_str = ", ".join(era.get("key_figures", []))
            text = (
                f"⏳ **Historical Era: {era['name']}**\n\n"
                f"- **Time Period**: {era.get('period', 'Historical Period')}\n"
                f"- **Geographic Scope**: {era.get('region', 'Global / Regional')}\n\n"
                f"{era.get('description', '')}\n\n"
                f"### 💡 Major Developments & Transformations\n{features_str}\n\n"
                f"### 👥 Notable Historical Figures\n{figures_str}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"historical overview of {era['name']}",
                domain=Domain.HISTORY,
                intent=Intent.HISTORICAL_EVENT,
                entities=[(primary, era['name'])],
                metadata=era,
                sources=["GeoMind Historical Compendium", "Wikipedia World History"]
            )

        return None
