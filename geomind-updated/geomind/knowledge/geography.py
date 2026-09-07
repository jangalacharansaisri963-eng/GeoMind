"""
Comprehensive Geography Knowledge Base: Countries, Capitals, Cities, Coordinates, and Natural Features.
"""
from typing import Any, Dict, List, Optional, Tuple
import os
import json
from geomind.core.types import GeoCoord, Domain, Intent, QueryResult
from geomind.knowledge.base import KnowledgeSource


_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load_geo_json(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(_DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _parse_coords(data: Any) -> Optional[GeoCoord]:
    if isinstance(data, GeoCoord):
        return data
    if isinstance(data, dict):
        lat = data.get("latitude") if data.get("latitude") is not None else data.get("lat", 0.0)
        lng = data.get("longitude") if data.get("longitude") is not None else (data.get("lon") or data.get("lng") or 0.0)
        return GeoCoord(float(lat), float(lng))
    if isinstance(data, (list, tuple)) and len(data) >= 2:
        return GeoCoord(float(data[0]), float(data[1]))
    return None


MOUNTAINS_CACHE: Dict[str, Dict[str, Any]] = {}
RIVERS_CACHE: Dict[str, Dict[str, Any]] = {}
OCEANS_CACHE: Dict[str, Dict[str, Any]] = {}
DESERTS_CACHE: Dict[str, Dict[str, Any]] = {}
ISLANDS_CACHE: Dict[str, Dict[str, Any]] = {}
LAKES_CACHE: Dict[str, Dict[str, Any]] = {}
WONDERS_CACHE: Dict[str, Dict[str, Any]] = {}
STRAITS_CACHE: Dict[str, Dict[str, Any]] = {}
EXTREMES_CACHE: Dict[str, Dict[str, Any]] = {}

for _m in _load_geo_json("mountains.json"):
    MOUNTAINS_CACHE[_m["name"].lower()] = _m
    for _a in _m.get("aliases", []):
        MOUNTAINS_CACHE[_a.lower()] = _m

for _r in _load_geo_json("rivers.json"):
    RIVERS_CACHE[_r["name"].lower()] = _r
    for _a in _r.get("aliases", []):
        RIVERS_CACHE[_a.lower()] = _r

for _o in _load_geo_json("oceans_seas.json"):
    OCEANS_CACHE[_o["name"].lower()] = _o
    for _a in _o.get("aliases", []):
        OCEANS_CACHE[_a.lower()] = _o

for _d in _load_geo_json("deserts.json"):
    DESERTS_CACHE[_d["name"].lower()] = _d
    for _a in _d.get("aliases", []):
        DESERTS_CACHE[_a.lower()] = _d

for _isl in _load_geo_json("islands.json"):
    ISLANDS_CACHE[_isl["name"].lower()] = _isl

for _lk in _load_geo_json("lakes.json"):
    LAKES_CACHE[_lk["name"].lower()] = _lk
    for _a in _lk.get("aliases", []):
        LAKES_CACHE[_a.lower()] = _lk

for _w in _load_geo_json("world_wonders_landmarks.json"):
    WONDERS_CACHE[_w["name"].lower()] = _w
    for _a in _w.get("aliases", []):
        WONDERS_CACHE[_a.lower()] = _w

for _st in _load_geo_json("straits_and_canals.json"):
    STRAITS_CACHE[_st["name"].lower()] = _st
    for _a in _st.get("aliases", []):
        STRAITS_CACHE[_a.lower()] = _st

for _ex in _load_geo_json("geographical_extremes.json"):
    EXTREMES_CACHE[_ex["record"].lower()] = _ex
    EXTREMES_CACHE[_ex["feature"].lower()] = _ex


# Comprehensive World Cities with coordinates and metadata
WORLD_CITIES: Dict[str, Dict[str, Any]] = {
    "delhi": {
        "name": "Delhi",
        "official_name": "National Capital Territory of Delhi",
        "country": "India",
        "coords": GeoCoord(28.6139, 77.2090),
        "population": 33000000,
        "is_capital": True,
        "description": "The capital territory of India, a massive metropolitan area in northern India featuring historic landmarks like the Red Fort and India Gate."
    },
    "new delhi": {
        "name": "New Delhi",
        "official_name": "New Delhi",
        "country": "India",
        "coords": GeoCoord(28.6139, 77.2090),
        "population": 250000,
        "is_capital": True,
        "description": "The seat of all three branches of the Government of India, located within the metropolis of Delhi."
    },
    "mumbai": {
        "name": "Mumbai",
        "official_name": "Mumbai (formerly Bombay)",
        "country": "India",
        "coords": GeoCoord(19.0760, 72.8777),
        "population": 21000000,
        "is_capital": False,
        "description": "India's largest city and financial capital, located on the western coast on the Arabian Sea, home to Bollywood and the Gateway of India."
    },
    "bangalore": {
        "name": "Bengaluru",
        "official_name": "Bengaluru (Bangalore)",
        "country": "India",
        "coords": GeoCoord(12.9716, 77.5946),
        "population": 13000000,
        "is_capital": False,
        "description": "The capital of India's southern Karnataka state, widely regarded as the 'Silicon Valley of India'."
    },
    "kolkata": {
        "name": "Kolkata",
        "official_name": "Kolkata (Calcutta)",
        "country": "India",
        "coords": GeoCoord(22.5726, 88.3639),
        "population": 15000000,
        "is_capital": False,
        "description": "The cultural capital of India and capital of West Bengal, situated on the eastern bank of the Hooghly River."
    },
    "tokyo": {
        "name": "Tokyo",
        "official_name": "Tokyo Metropolis",
        "country": "Japan",
        "coords": GeoCoord(35.6762, 139.6503),
        "population": 37400000,
        "is_capital": True,
        "description": "The bustling capital of Japan, the world's most populous metropolitan area, mixing ultramodern neon skyscrapers with historic temples."
    },
    "beijing": {
        "name": "Beijing",
        "official_name": "Beijing Municipality",
        "country": "China",
        "coords": GeoCoord(39.9042, 116.4074),
        "population": 21890000,
        "is_capital": True,
        "description": "China's sprawling national capital, with history dating back 3 millennia, known for modern architecture and ancient sites like the Forbidden City."
    },
    "shanghai": {
        "name": "Shanghai",
        "official_name": "Shanghai",
        "country": "China",
        "coords": GeoCoord(31.2304, 121.4737),
        "population": 27000000,
        "is_capital": False,
        "description": "China's biggest city and global financial hub, renowned for the waterfront promenade The Bund and soaring Oriental Pearl Tower."
    },
    "london": {
        "name": "London",
        "official_name": "Greater London",
        "country": "United Kingdom",
        "coords": GeoCoord(51.5074, -0.1278),
        "population": 9600000,
        "is_capital": True,
        "description": "The capital of England and the United Kingdom, a 21st-century city with history stretching to Roman times, home to Big Ben and the Tower of London."
    },
    "paris": {
        "name": "Paris",
        "official_name": "City of Paris",
        "country": "France",
        "coords": GeoCoord(48.8566, 2.3522),
        "population": 11100000,
        "is_capital": True,
        "description": "France's capital and a major European city, global center for art, fashion, gastronomy, and culture, defined by landmarks like the Eiffel Tower and Louvre."
    },
    "washington dc": {
        "name": "Washington, D.C.",
        "official_name": "District of Columbia",
        "country": "United States",
        "coords": GeoCoord(38.9072, -77.0369),
        "population": 710000,
        "is_capital": True,
        "description": "The U.S. capital, a compact city on the Potomac River, home to iconic neoclassical monuments and buildings including the Capitol and White House."
    },
    "new york": {
        "name": "New York City",
        "official_name": "City of New York",
        "country": "United States",
        "coords": GeoCoord(40.7128, -74.0060),
        "population": 8800000,
        "is_capital": False,
        "description": "The most populous city in the United States, composed of 5 boroughs, home to Times Square, Wall Street, and the Statue of Liberty."
    },
    "los angeles": {
        "name": "Los Angeles",
        "official_name": "City of Los Angeles",
        "country": "United States",
        "coords": GeoCoord(34.0522, -118.2437),
        "population": 3900000,
        "is_capital": False,
        "description": "The sprawling Southern California metropolis and center of the nation's film and television industry."
    },
    "cairo": {
        "name": "Cairo",
        "official_name": "Cairo Governorate",
        "country": "Egypt",
        "coords": GeoCoord(30.0444, 31.2357),
        "population": 22100000,
        "is_capital": True,
        "description": "Egypt’s sprawling capital set on the Nile River, near the legendary Giza pyramid complex and Great Sphinx."
    },
    "sydney": {
        "name": "Sydney",
        "official_name": "City of Sydney",
        "country": "Australia",
        "coords": GeoCoord(-33.8688, 151.2093),
        "population": 5300000,
        "is_capital": False,
        "description": "Capital of New South Wales and one of Australia's largest cities, famous for its sail-shaped Opera House and Harbour Bridge."
    },
    "canberra": {
        "name": "Canberra",
        "official_name": "Canberra",
        "country": "Australia",
        "coords": GeoCoord(-35.2809, 149.1300),
        "population": 460000,
        "is_capital": True,
        "description": "The purpose-built national capital of Australia, designed by Walter Burley Griffin."
    },
    "berlin": {
        "name": "Berlin",
        "official_name": "Berlin",
        "country": "Germany",
        "coords": GeoCoord(52.5200, 13.4050),
        "population": 3800000,
        "is_capital": True,
        "description": "Germany's capital, dating to the 13th century, famous for its turbulent 20th-century history, Brandenburg Gate, and vibrant arts scene."
    },
    "rome": {
        "name": "Rome",
        "official_name": "Roma Capitale",
        "country": "Italy",
        "coords": GeoCoord(41.9028, 12.4964),
        "population": 2870000,
        "is_capital": True,
        "description": "Italy's capital, a sprawling, cosmopolitan city with nearly 3,000 years of globally influential art, architecture, and the Colosseum."
    },
    "moscow": {
        "name": "Moscow",
        "official_name": "Moscow",
        "country": "Russia",
        "coords": GeoCoord(55.7558, 37.6173),
        "population": 13000000,
        "is_capital": True,
        "description": "The capital of Russia, its political and economic heart, home to the historic Kremlin and Saint Basil's Cathedral."
    },
    "ottawa": {
        "name": "Ottawa",
        "official_name": "City of Ottawa",
        "country": "Canada",
        "coords": GeoCoord(45.4215, -75.6972),
        "population": 1000000,
        "is_capital": True,
        "description": "Canada's capital city, situated on the Ottawa River in Ontario, known for Parliament Hill and the Rideau Canal."
    },
    "toronto": {
        "name": "Toronto",
        "official_name": "City of Toronto",
        "country": "Canada",
        "coords": GeoCoord(43.6532, -79.3832),
        "population": 2930000,
        "is_capital": False,
        "description": "The capital of Ontario, Canada's largest city and financial hub, characterized by the soaring CN Tower."
    },
    "brasilia": {
        "name": "Brasília",
        "official_name": "Federal District",
        "country": "Brazil",
        "coords": GeoCoord(-15.8267, -47.9218),
        "population": 3050000,
        "is_capital": True,
        "description": "The planned federal capital of Brazil founded in 1960, celebrated for Oscar Niemeyer's futuristic white architecture."
    },
    "sao paulo": {
        "name": "São Paulo",
        "official_name": "São Paulo",
        "country": "Brazil",
        "coords": GeoCoord(-23.5505, -46.6333),
        "population": 12300000,
        "is_capital": False,
        "description": "Brazil’s vibrant financial hub and the most populous city in the Western and Southern Hemispheres."
    },
    "buenos aires": {
        "name": "Buenos Aires",
        "official_name": "Autonomous City of Buenos Aires",
        "country": "Argentina",
        "coords": GeoCoord(-34.6037, -58.3816),
        "population": 3120000,
        "is_capital": True,
        "description": "Argentina’s big, cosmopolitan capital city on the Río de la Plata, famous for tango, European architecture, and Plaza de Mayo."
    },
    "nairobi": {
        "name": "Nairobi",
        "official_name": "Nairobi City County",
        "country": "Kenya",
        "coords": GeoCoord(-1.2921, 36.8219),
        "population": 4400000,
        "is_capital": True,
        "description": "Kenya's capital and commercial hub, famous for Nairobi National Park where wildlife roams against a backdrop of city skyscrapers."
    },
    "cape town": {
        "name": "Cape Town",
        "official_name": "City of Cape Town",
        "country": "South Africa",
        "coords": GeoCoord(-33.9249, 18.4241),
        "population": 4700000,
        "is_capital": True,  # Legislative capital
        "description": "A coastal city in South Africa, dominated by flat-topped Table Mountain, serving as South Africa's legislative capital."
    },
    "pretoria": {
        "name": "Pretoria",
        "official_name": "City of Tshwane",
        "country": "South Africa",
        "coords": GeoCoord(-25.7479, 28.2293),
        "population": 740000,
        "is_capital": True,  # Executive capital
        "description": "The administrative and executive capital of South Africa, known for jacaranda-lined streets."
    },
    "bloemfontein": {
        "name": "Bloemfontein",
        "official_name": "Mangaung Metropolitan Municipality",
        "country": "South Africa",
        "coords": GeoCoord(-29.0852, 26.1596),
        "population": 256000,
        "is_capital": True,  # Judicial capital
        "description": "The judicial capital of South Africa, situated in the Free State province."
    },
    "dubai": {
        "name": "Dubai",
        "official_name": "Emirate of Dubai",
        "country": "United Arab Emirates",
        "coords": GeoCoord(25.2048, 55.2708),
        "population": 3600000,
        "is_capital": False,
        "description": "A global business hub and luxury destination in the UAE, famous for ultramodern architecture like the Burj Khalifa."
    },
    "abu dhabi": {
        "name": "Abu Dhabi",
        "official_name": "Abu Dhabi",
        "country": "United Arab Emirates",
        "coords": GeoCoord(24.4539, 54.3773),
        "population": 1500000,
        "is_capital": True,
        "description": "The capital of the United Arab Emirates, situated on an island in the Persian Gulf."
    },
    "singapore": {
        "name": "Singapore",
        "official_name": "Republic of Singapore",
        "country": "Singapore",
        "coords": GeoCoord(1.3521, 103.8198),
        "population": 5900000,
        "is_capital": True,
        "description": "An island city-state off southern Malaysia, a global financial, shipping, and technological powerhouse."
    },
    "jakarta": {
        "name": "Jakarta",
        "official_name": "Special Capital Region of Jakarta",
        "country": "Indonesia",
        "coords": GeoCoord(-6.2088, 106.8456),
        "population": 10560000,
        "is_capital": True,
        "description": "Indonesia's massive capital on the northwest coast of Java, a dynamic cultural and economic metropolis."
    },
    "bangkok": {
        "name": "Bangkok",
        "official_name": "Krung Thep Maha Nakhon",
        "country": "Thailand",
        "coords": GeoCoord(13.7563, 100.5018),
        "population": 10800000,
        "is_capital": True,
        "description": "Thailand’s capital, ornate shrines and vibrant street life along the Chao Phraya River."
    },
    "seoul": {
        "name": "Seoul",
        "official_name": "Seoul Special City",
        "country": "South Korea",
        "coords": GeoCoord(37.5665, 126.9780),
        "population": 9900000,
        "is_capital": True,
        "description": "The capital of South Korea, a huge metropolis where modern skyscrapers and high-tech subways meet Buddhist temples and palaces."
    },
    "mexico city": {
        "name": "Mexico City",
        "official_name": "Ciudad de México",
        "country": "Mexico",
        "coords": GeoCoord(19.4326, -99.1332),
        "population": 9200000,
        "is_capital": True,
        "description": "The densely populated high-altitude capital of Mexico, built on the ruins of the Aztec capital Tenochtitlan."
    },
    "madrid": {
        "name": "Madrid",
        "official_name": "Community of Madrid",
        "country": "Spain",
        "coords": GeoCoord(40.4168, -3.7038),
        "population": 3300000,
        "is_capital": True,
        "description": "Spain's central capital, a city of elegant boulevards, manicured parks like El Retiro, and the Prado Museum."
    },
    "istanbul": {
        "name": "Istanbul",
        "official_name": "Istanbul",
        "country": "Turkey",
        "coords": GeoCoord(41.0082, 28.9784),
        "population": 15600000,
        "is_capital": False,
        "description": "A historic transcontinental city straddling the Bosporus Strait between Europe and Asia, home to the Hagia Sophia and Blue Mosque."
    },
    "ankara": {
        "name": "Ankara",
        "official_name": "Ankara",
        "country": "Turkey",
        "coords": GeoCoord(39.9334, 32.8597),
        "population": 5700000,
        "is_capital": True,
        "description": "Turkey's cosmopolitan capital, in the central Anatolian plateau, home to the performing arts and Anıtkabir."
    },
    "athens": {
        "name": "Athens",
        "official_name": "Municipality of Athens",
        "country": "Greece",
        "coords": GeoCoord(37.9838, 23.7275),
        "population": 3150000,
        "is_capital": True,
        "description": "The historic capital of Greece and cradle of Western civilization, dominated by 5th-century BC landmarks like the Acropolis and Parthenon."
    }
}


# Comprehensive Countries Knowledge Base
COUNTRIES_DATA: Dict[str, Dict[str, Any]] = {
    "india": {
        "name": "India",
        "official_name": "Republic of India (Bharat)",
        "capital": "New Delhi",
        "continent": "Asia",
        "region": "South Asia",
        "population": 1428627663,
        "area_sq_km": 3287263,
        "currency": "Indian Rupee (INR, ₹)",
        "languages": ["Hindi", "English", "22 scheduled languages"],
        "borders": ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh", "Myanmar"],
        "coords": GeoCoord(20.5937, 78.9629),
        "major_features": ["Himalayas", "Ganges River", "Deccan Plateau", "Thar Desert"],
        "overview": "India is the world's most populous nation and the largest democracy, bordered by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast."
    },
    "united states": {
        "name": "United States",
        "official_name": "United States of America",
        "capital": "Washington, D.C.",
        "continent": "North America",
        "region": "Northern America",
        "population": 339996563,
        "area_sq_km": 9833517,
        "currency": "United States Dollar (USD, $)",
        "languages": ["English"],
        "borders": ["Canada", "Mexico"],
        "coords": GeoCoord(37.0902, -95.7129),
        "major_features": ["Rocky Mountains", "Mississippi River", "Grand Canyon", "Great Lakes"],
        "overview": "A federal constitutional republic comprising 50 states, a federal district, and 5 major unincorporated territories. The world's largest economy by nominal GDP."
    },
    "china": {
        "name": "China",
        "official_name": "People's Republic of China",
        "capital": "Beijing",
        "continent": "Asia",
        "region": "East Asia",
        "population": 1411750000,
        "area_sq_km": 9596961,
        "currency": "Renminbi (Yuan, CNY, ¥)",
        "languages": ["Standard Chinese (Mandarin)"],
        "borders": ["Mongolia", "Russia", "North Korea", "Vietnam", "Laos", "Myanmar", "India", "Bhutan", "Nepal", "Pakistan", "Afghanistan", "Tajikistan", "Kyrgyzstan", "Kazakhstan"],
        "coords": GeoCoord(35.8617, 104.1954),
        "major_features": ["Yangtze River", "Yellow River", "Tibetan Plateau", "Gobi Desert"],
        "overview": "The world's second most populous country, an ancient civilization spanning millennia, and a dominant economic and technological power."
    },
    "japan": {
        "name": "Japan",
        "official_name": "State of Japan (Nihon-koku)",
        "capital": "Tokyo",
        "continent": "Asia",
        "region": "East Asia",
        "population": 124500000,
        "area_sq_km": 377975,
        "currency": "Japanese Yen (JPY, ¥)",
        "languages": ["Japanese"],
        "borders": [],  # Island nation
        "coords": GeoCoord(36.2048, 138.2529),
        "major_features": ["Mount Fuji", "Japanese Alps", "Pacific Ring of Fire"],
        "overview": "An island nation in East Asia situated in the northwest Pacific Ocean, renowned for its ancient traditions, cutting-edge technology, and cultural influence."
    },
    "united kingdom": {
        "name": "United Kingdom",
        "official_name": "United Kingdom of Great Britain and Northern Ireland",
        "capital": "London",
        "continent": "Europe",
        "region": "Western Europe",
        "population": 67736802,
        "area_sq_km": 242495,
        "currency": "Pound Sterling (GBP, £)",
        "languages": ["English"],
        "borders": ["Ireland"],
        "coords": GeoCoord(55.3781, -3.4360),
        "major_features": ["River Thames", "Ben Nevis", "Pennines", "White Cliffs of Dover"],
        "overview": "An island nation comprising England, Scotland, Wales, and Northern Ireland. The birthplace of the Industrial Revolution and parliamentary democracy."
    },
    "france": {
        "name": "France",
        "official_name": "French Republic",
        "capital": "Paris",
        "continent": "Europe",
        "region": "Western Europe",
        "population": 68000000,
        "area_sq_km": 643801,
        "currency": "Euro (EUR, €)",
        "languages": ["French"],
        "borders": ["Belgium", "Luxembourg", "Germany", "Switzerland", "Italy", "Monaco", "Spain", "Andorra"],
        "coords": GeoCoord(46.2276, 2.2137),
        "major_features": ["Alps", "Pyrenees", "Seine River", "Mont Blanc"],
        "overview": "A major Western European republic with a global heritage in philosophy, art, science, culinary traditions, and human rights."
    },
    "germany": {
        "name": "Germany",
        "official_name": "Federal Republic of Germany",
        "capital": "Berlin",
        "continent": "Europe",
        "region": "Central Europe",
        "population": 84400000,
        "area_sq_km": 357022,
        "currency": "Euro (EUR, €)",
        "languages": ["German"],
        "borders": ["Denmark", "Poland", "Czech Republic", "Austria", "Switzerland", "France", "Luxembourg", "Belgium", "Netherlands"],
        "coords": GeoCoord(51.1657, 10.4515),
        "major_features": ["Bavarian Alps", "Rhine River", "Black Forest", "Danube River"],
        "overview": "The most populous member state of the European Union and Europe's largest economy, known for engineering, science, and classical culture."
    },
    "egypt": {
        "name": "Egypt",
        "official_name": "Arab Republic of Egypt",
        "capital": "Cairo",
        "continent": "Africa",
        "region": "Northern Africa",
        "population": 110000000,
        "area_sq_km": 1002450,
        "currency": "Egyptian Pound (EGP, E£)",
        "languages": ["Arabic"],
        "borders": ["Libya", "Sudan", "Israel", "Palestine"],
        "coords": GeoCoord(26.8206, 30.8025),
        "major_features": ["Nile River", "Suez Canal", "Eastern Desert", "Sinai Peninsula"],
        "overview": "A transcontinental nation spanning the northeast corner of Africa and southwest corner of Asia via the Sinai Peninsula. Cradle of one of history's greatest civilizations."
    },
    "australia": {
        "name": "Australia",
        "official_name": "Commonwealth of Australia",
        "capital": "Canberra",
        "continent": "Oceania",
        "region": "Australasia",
        "population": 26400000,
        "area_sq_km": 7692024,
        "currency": "Australian Dollar (AUD, $)",
        "languages": ["English"],
        "borders": [],  # Surrounded by ocean
        "coords": GeoCoord(-25.2744, 133.7751),
        "major_features": ["Great Barrier Reef", "Outback", "Uluru", "Great Dividing Range"],
        "overview": "The world's smallest continent and largest island nation, noted for unique megadiverse wildlife and expansive landscapes."
    },
    "brazil": {
        "name": "Brazil",
        "official_name": "Federative Republic of Brazil",
        "capital": "Brasília",
        "continent": "South America",
        "region": "South America",
        "population": 215300000,
        "area_sq_km": 8515767,
        "currency": "Brazilian Real (BRL, R$)",
        "languages": ["Portuguese"],
        "borders": ["Uruguay", "Argentina", "Paraguay", "Bolivia", "Peru", "Colombia", "Venezuela", "Guyana", "Suriname", "French Guiana"],
        "coords": GeoCoord(-14.2350, -51.9253),
        "major_features": ["Amazon Rainforest", "Amazon River", "Pantanal", "Brazilian Highlands"],
        "overview": "The largest country in South America and Latin America, home to approximately 60% of the Amazon rainforest."
    },
    "canada": {
        "name": "Canada",
        "official_name": "Canada",
        "capital": "Ottawa",
        "continent": "North America",
        "region": "Northern America",
        "population": 40000000,
        "area_sq_km": 9984670,
        "currency": "Canadian Dollar (CAD, $)",
        "languages": ["English", "French"],
        "borders": ["United States"],
        "coords": GeoCoord(56.1304, -106.3468),
        "major_features": ["Rocky Mountains", "Canadian Shield", "Great Lakes", "St. Lawrence River"],
        "overview": "The second-largest country in the world by total area, stretching from the Atlantic to the Pacific and northward into the Arctic Ocean."
    },
    "russia": {
        "name": "Russia",
        "official_name": "Russian Federation",
        "capital": "Moscow",
        "continent": "Europe / Asia",
        "region": "Eastern Europe / Northern Asia",
        "population": 144400000,
        "area_sq_km": 17098242,
        "currency": "Russian Ruble (RUB, ₽)",
        "languages": ["Russian"],
        "borders": ["Norway", "Finland", "Estonia", "Latvia", "Lithuania", "Poland", "Belarus", "Ukraine", "Georgia", "Azerbaijan", "Kazakhstan", "China", "Mongolia", "North Korea"],
        "coords": GeoCoord(61.5240, 105.3188),
        "major_features": ["Siberia", "Ural Mountains", "Lake Baikal", "Volga River"],
        "overview": "The largest country in the world by area, covering more than one-eighth of Earth's inhabited land area and spanning eleven time zones."
    },
    "south africa": {
        "name": "South Africa",
        "official_name": "Republic of South Africa",
        "capital": "Pretoria (executive), Cape Town (legislative), Bloemfontein (judicial)",
        "continent": "Africa",
        "region": "Southern Africa",
        "population": 60600000,
        "area_sq_km": 1221037,
        "currency": "South African Rand (ZAR, R)",
        "languages": ["Zulu", "Xhosa", "Afrikaans", "English", "11 official languages"],
        "borders": ["Namibia", "Botswana", "Zimbabwe", "Mozambique", "Eswatini", "Lesotho"],
        "coords": GeoCoord(-30.5595, 22.9375),
        "major_features": ["Table Mountain", "Drakensberg", "Kruger National Park", "Kalahari"],
        "overview": "The southernmost country in Africa, famed for its diverse topography, multicultural population, and post-apartheid democratic transition."
    },
    "italy": {
        "name": "Italy",
        "official_name": "Italian Republic",
        "capital": "Rome",
        "continent": "Europe",
        "region": "Southern Europe",
        "population": 59000000,
        "area_sq_km": 301340,
        "currency": "Euro (EUR, €)",
        "languages": ["Italian"],
        "borders": ["France", "Switzerland", "Austria", "Slovenia", "San Marino", "Vatican City"],
        "coords": GeoCoord(41.8719, 12.5674),
        "major_features": ["Alps", "Apennines", "Po Valley", "Mount Vesuvius", "Mount Etna"],
        "overview": "A boot-shaped peninsula in Southern Europe, cradle of the Roman Empire and the Renaissance."
    },
    "greece": {
        "name": "Greece",
        "official_name": "Hellenic Republic",
        "capital": "Athens",
        "continent": "Europe",
        "region": "Southeast Europe",
        "population": 10400000,
        "area_sq_km": 131957,
        "currency": "Euro (EUR, €)",
        "languages": ["Greek"],
        "borders": ["Albania", "North Macedonia", "Bulgaria", "Turkey"],
        "coords": GeoCoord(39.0742, 21.8243),
        "major_features": ["Aegean Sea", "Mount Olympus", "Peloponnese", "Greek Islands"],
        "overview": "Considered the cradle of Western civilization, birthplace of democracy, Western philosophy, Olympic Games, and theater."
    },
    "kenya": {
        "name": "Kenya",
        "official_name": "Republic of Kenya",
        "capital": "Nairobi",
        "continent": "Africa",
        "region": "East Africa",
        "population": 55100000,
        "area_sq_km": 580367,
        "currency": "Kenyan Shilling (KES, KSh)",
        "languages": ["Swahili", "English"],
        "borders": ["Ethiopia", "Somalia", "Tanzania", "Uganda", "South Sudan"],
        "coords": GeoCoord(-1.2921, 36.8219),
        "major_features": ["Great Rift Valley", "Mount Kenya", "Maasai Mara", "Lake Victoria"],
        "overview": "An East African nation known for its savanna wildlife, the Great Rift Valley, and as a major regional economic and diplomatic hub."
    },
    "nigeria": {
        "name": "Nigeria",
        "official_name": "Federal Republic of Nigeria",
        "capital": "Abuja",
        "continent": "Africa",
        "region": "West Africa",
        "population": 223800000,
        "area_sq_km": 923768,
        "currency": "Nigerian Naira (NGN, ₦)",
        "languages": ["English", "Hausa", "Yoruba", "Igbo"],
        "borders": ["Benin", "Niger", "Chad", "Cameroon"],
        "coords": GeoCoord(9.0765, 7.3986),
        "major_features": ["Niger River", "Niger Delta", "Zuma Rock"],
        "overview": "Africa's most populous country and largest economy, a federal republic with a highly diverse cultural and linguistic landscape."
    },
    "mexico": {
        "name": "Mexico",
        "official_name": "United Mexican States",
        "capital": "Mexico City",
        "continent": "North America",
        "region": "Latin America",
        "population": 128900000,
        "area_sq_km": 1964375,
        "currency": "Mexican Peso (MXN, $)",
        "languages": ["Spanish"],
        "borders": ["United States", "Belize", "Guatemala"],
        "coords": GeoCoord(19.4326, -99.1332),
        "major_features": ["Sierra Madre", "Yucatan Peninsula", "Chichen Itza"],
        "overview": "A North American nation bridging the US and Central America, home to ancient Mesoamerican civilizations and one of the world's largest metropolitan areas."
    },
    "indonesia": {
        "name": "Indonesia",
        "official_name": "Republic of Indonesia",
        "capital": "Jakarta",
        "continent": "Asia",
        "region": "Southeast Asia",
        "population": 278700000,
        "area_sq_km": 1904569,
        "currency": "Indonesian Rupiah (IDR, Rp)",
        "languages": ["Indonesian"],
        "borders": ["Malaysia", "Papua New Guinea", "Timor-Leste"],
        "coords": GeoCoord(-6.2088, 106.8456),
        "major_features": ["Java", "Bali", "Borobudur", "Sumatra"],
        "overview": "The world's largest archipelago nation, spanning thousands of islands across Southeast Asia and Oceania, and the most populous Muslim-majority country."
    },
    "south korea": {
        "name": "South Korea",
        "official_name": "Republic of Korea",
        "capital": "Seoul",
        "continent": "Asia",
        "region": "East Asia",
        "population": 51700000,
        "area_sq_km": 100210,
        "currency": "South Korean Won (KRW, ₩)",
        "languages": ["Korean"],
        "borders": ["North Korea"],
        "coords": GeoCoord(37.5665, 126.9780),
        "major_features": ["Korean Peninsula", "Han River", "Jeju Island"],
        "overview": "A highly developed East Asian democracy known for rapid post-war industrialization and global leadership in technology and culture."
    },
    "saudi arabia": {
        "name": "Saudi Arabia",
        "official_name": "Kingdom of Saudi Arabia",
        "capital": "Riyadh",
        "continent": "Asia",
        "region": "Middle East",
        "population": 36400000,
        "area_sq_km": 2149690,
        "currency": "Saudi Riyal (SAR, ﷼)",
        "languages": ["Arabic"],
        "borders": ["Jordan", "Iraq", "Kuwait", "Qatar", "United Arab Emirates", "Oman", "Yemen"],
        "coords": GeoCoord(24.7136, 46.6753),
        "major_features": ["Arabian Desert", "Red Sea coast", "Mecca", "Medina"],
        "overview": "The largest country on the Arabian Peninsula, home to Islam's two holiest cities and a major global oil producer."
    },
    "argentina": {
        "name": "Argentina",
        "official_name": "Argentine Republic",
        "capital": "Buenos Aires",
        "continent": "South America",
        "region": "South America",
        "population": 46600000,
        "area_sq_km": 2780400,
        "currency": "Argentine Peso (ARS, $)",
        "languages": ["Spanish"],
        "borders": ["Chile", "Bolivia", "Paraguay", "Brazil", "Uruguay"],
        "coords": GeoCoord(-34.6037, -58.3816),
        "major_features": ["Andes Mountains", "Patagonia", "Iguazu Falls", "Pampas"],
        "overview": "The second-largest country in South America, spanning from subtropical north to sub-Antarctic Patagonia in the south."
    },
    "turkey": {
        "name": "Turkey",
        "official_name": "Republic of Turkiye",
        "capital": "Ankara",
        "continent": "Europe/Asia (Transcontinental)",
        "region": "Middle East / Southeast Europe",
        "population": 85300000,
        "area_sq_km": 783562,
        "currency": "Turkish Lira (TRY, ₺)",
        "languages": ["Turkish"],
        "borders": ["Greece", "Bulgaria", "Georgia", "Armenia", "Azerbaijan", "Iran", "Iraq", "Syria"],
        "coords": GeoCoord(39.9334, 32.8597),
        "major_features": ["Bosphorus Strait", "Anatolia", "Cappadocia"],
        "overview": "A transcontinental nation bridging Europe and Asia, with Istanbul straddling the Bosphorus as its cultural and economic center."
    },
    "thailand": {
        "name": "Thailand",
        "official_name": "Kingdom of Thailand",
        "capital": "Bangkok",
        "continent": "Asia",
        "region": "Southeast Asia",
        "population": 71800000,
        "area_sq_km": 513120,
        "currency": "Thai Baht (THB, ฿)",
        "languages": ["Thai"],
        "borders": ["Myanmar", "Laos", "Cambodia", "Malaysia"],
        "coords": GeoCoord(13.7563, 100.5018),
        "major_features": ["Chao Phraya River", "Gulf of Thailand", "Northern Highlands"],
        "overview": "A Southeast Asian kingdom known for its Buddhist temples, tropical beaches, and status as one of the region's largest economies."
    },
    "vietnam": {
        "name": "Vietnam",
        "official_name": "Socialist Republic of Vietnam",
        "capital": "Hanoi",
        "continent": "Asia",
        "region": "Southeast Asia",
        "population": 98900000,
        "area_sq_km": 331212,
        "currency": "Vietnamese Dong (VND, ₫)",
        "languages": ["Vietnamese"],
        "borders": ["China", "Laos", "Cambodia"],
        "coords": GeoCoord(21.0285, 105.8542),
        "major_features": ["Mekong Delta", "Ha Long Bay", "Red River Delta"],
        "overview": "A long, S-shaped Southeast Asian nation stretching along the South China Sea, with a fast-growing manufacturing economy."
    },
    "ethiopia": {
        "name": "Ethiopia",
        "official_name": "Federal Democratic Republic of Ethiopia",
        "capital": "Addis Ababa",
        "continent": "Africa",
        "region": "East Africa",
        "population": 126500000,
        "area_sq_km": 1104300,
        "currency": "Ethiopian Birr (ETB)",
        "languages": ["Amharic", "Oromo"],
        "borders": ["Eritrea", "Djibouti", "Somalia", "Kenya", "South Sudan", "Sudan"],
        "coords": GeoCoord(9.0300, 38.7400),
        "major_features": ["Simien Mountains", "Great Rift Valley", "Blue Nile"],
        "overview": "One of the oldest continuously independent nations in Africa, notable for the ancient rock-hewn churches of Lalibela and Simien Mountains."
    },
    "sweden": {
        "name": "Sweden",
        "official_name": "Kingdom of Sweden",
        "capital": "Stockholm",
        "continent": "Europe",
        "region": "Northern Europe",
        "population": 10500000,
        "area_sq_km": 450295,
        "currency": "Swedish Krona (SEK, kr)",
        "languages": ["Swedish"],
        "borders": ["Norway", "Finland"],
        "coords": GeoCoord(59.3293, 18.0686),
        "major_features": ["Scandinavian Mountains", "Baltic archipelago"],
        "overview": "A Scandinavian nation known for its extensive welfare state, innovation economy, and thousands of coastal and lake islands."
    },
    "norway": {
        "name": "Norway",
        "official_name": "Kingdom of Norway",
        "capital": "Oslo",
        "continent": "Europe",
        "region": "Northern Europe",
        "population": 5500000,
        "area_sq_km": 385207,
        "currency": "Norwegian Krone (NOK, kr)",
        "languages": ["Norwegian"],
        "borders": ["Sweden", "Finland", "Russia"],
        "coords": GeoCoord(59.9139, 10.7522),
        "major_features": ["Norwegian fjords", "Scandinavian Mountains", "Arctic coastline"],
        "overview": "A Scandinavian kingdom famed for its dramatic fjords, midnight sun, and sovereign wealth built on North Sea oil."
    },
    "spain": {
        "name": "Spain",
        "official_name": "Kingdom of Spain",
        "capital": "Madrid",
        "continent": "Europe",
        "region": "Southern Europe",
        "population": 47600000,
        "area_sq_km": 505990,
        "currency": "Euro (EUR, €)",
        "languages": ["Spanish"],
        "borders": ["France", "Portugal", "Andorra"],
        "coords": GeoCoord(40.4168, -3.7038),
        "major_features": ["Pyrenees", "Iberian Peninsula", "Canary Islands"],
        "overview": "An Iberian nation with a rich Roman, Moorish, and imperial history, known for its regional cultures from Catalonia to Andalusia."
    },
    "pakistan": {
        "name": "Pakistan",
        "official_name": "Islamic Republic of Pakistan",
        "capital": "Islamabad",
        "continent": "Asia",
        "region": "South Asia",
        "population": 240500000,
        "area_sq_km": 881913,
        "currency": "Pakistani Rupee (PKR, ₨)",
        "languages": ["Urdu", "English"],
        "borders": ["India", "China", "Afghanistan", "Iran"],
        "coords": GeoCoord(33.6844, 73.0479),
        "major_features": ["Karakoram Range", "Indus River", "Thar Desert"],
        "overview": "A South Asian nation home to the Indus Valley Civilization's heartland and some of the world's highest mountain peaks."
    },
    "philippines": {
        "name": "Philippines",
        "official_name": "Republic of the Philippines",
        "capital": "Manila",
        "continent": "Asia",
        "region": "Southeast Asia",
        "population": 117300000,
        "area_sq_km": 300000,
        "currency": "Philippine Peso (PHP, ₱)",
        "languages": ["Filipino", "English"],
        "borders": [],
        "coords": GeoCoord(14.5995, 120.9842),
        "major_features": ["Luzon", "Visayas", "Mindanao", "Pacific Ring of Fire"],
        "overview": "An archipelago of over 7,000 islands in Southeast Asia, shaped by Spanish and American colonial history and a vibrant island culture."
    },
    "bangladesh": {
        "name": "Bangladesh",
        "official_name": "People's Republic of Bangladesh",
        "capital": "Dhaka",
        "continent": "Asia",
        "region": "South Asia",
        "population": 172900000,
        "area_sq_km": 148460,
        "currency": "Bangladeshi Taka (BDT, ৳)",
        "languages": ["Bengali"],
        "borders": ["India", "Myanmar"],
        "coords": GeoCoord(23.8103, 90.4125),
        "major_features": ["Ganges Delta", "Sundarbans mangrove forest"],
        "overview": "One of the world's most densely populated nations, situated on the vast Ganges-Brahmaputra delta in South Asia."
    },
    "poland": {
        "name": "Poland",
        "official_name": "Republic of Poland",
        "capital": "Warsaw",
        "continent": "Europe",
        "region": "Central Europe",
        "population": 37700000,
        "area_sq_km": 312696,
        "currency": "Polish Zloty (PLN, zł)",
        "languages": ["Polish"],
        "borders": ["Germany", "Czech Republic", "Slovakia", "Ukraine", "Belarus", "Lithuania", "Russia"],
        "coords": GeoCoord(52.2297, 21.0122),
        "major_features": ["Vistula River", "Baltic coast", "Tatra Mountains"],
        "overview": "A Central European nation with a resilient history through partitions and war, now one of the EU's largest economies."
    },
    "netherlands": {
        "name": "Netherlands",
        "official_name": "Kingdom of the Netherlands",
        "capital": "Amsterdam",
        "continent": "Europe",
        "region": "Western Europe",
        "population": 17900000,
        "area_sq_km": 41850,
        "currency": "Euro (EUR, €)",
        "languages": ["Dutch"],
        "borders": ["Germany", "Belgium"],
        "coords": GeoCoord(52.3676, 4.9041),
        "major_features": ["Rhine Delta", "Polders", "North Sea coast"],
        "overview": "A low-lying Western European nation famed for its extensive water management, canals, and status as a global trade hub."
    },
    "new zealand": {
        "name": "New Zealand",
        "official_name": "New Zealand",
        "capital": "Wellington",
        "continent": "Oceania",
        "region": "Oceania",
        "population": 5200000,
        "area_sq_km": 268021,
        "currency": "New Zealand Dollar (NZD, $)",
        "languages": ["English", "Maori"],
        "borders": [],
        "coords": GeoCoord(-41.2865, 174.7762),
        "major_features": ["Southern Alps", "Fiordland", "North/South Islands"],
        "overview": "An island nation in the southwestern Pacific, known for dramatic landscapes ranging from fjords to volcanic plateaus and Maori culture."
    }
}


class GeographyKnowledgeSource(KnowledgeSource):
    """Knowledge engine for geographic inquiries."""

    @property
    def domain(self) -> Domain:
        return Domain.GEOGRAPHY

    def can_handle(self, intent: Intent, text: str) -> bool:
        return intent in {
            Intent.CAPITAL_LOOKUP,
            Intent.COUNTRY_INFO,
            Intent.CITY_INFO,
            Intent.LOCATION_COORDINATES,
            Intent.POPULATION_QUERY,
            Intent.BORDERING_COUNTRIES,
            Intent.CURRENCY_LOOKUP
        }

    def resolve_location(self, name: str) -> Optional[Tuple[str, GeoCoord, Dict[str, Any]]]:
        """Resolves a place name (city or country) to its standardized name, coordinates, and data."""
        clean = name.strip().lower()

        # Check cities first
        if clean in WORLD_CITIES:
            data = WORLD_CITIES[clean]
            return (data["name"], data["coords"], data)

        # Check countries
        if clean in COUNTRIES_DATA:
            data = COUNTRIES_DATA[clean]
            return (data["name"], data["coords"], data)

        # Check aliases
        aliases = {
            "usa": "united states",
            "us": "united states",
            "america": "united states",
            "uk": "united kingdom",
            "britain": "united kingdom",
            "great britain": "united kingdom",
            "uae": "abu dhabi",
            "drc": "democratic republic of the congo",
            "russia": "russia",
            "nyc": "new york",
            "la": "los angeles",
            "dc": "washington dc",
            "washington": "washington dc"
        }
        if clean in aliases:
            target = aliases[clean]
            if target in WORLD_CITIES:
                return (WORLD_CITIES[target]["name"], WORLD_CITIES[target]["coords"], WORLD_CITIES[target])
            if target in COUNTRIES_DATA:
                return (COUNTRIES_DATA[target]["name"], COUNTRIES_DATA[target]["coords"], COUNTRIES_DATA[target])

        # Check mountains
        if clean in MOUNTAINS_CACHE:
            m = MOUNTAINS_CACHE[clean]
            c = _parse_coords(m.get("coords"))
            if c:
                return (m["name"], c, m)

        # Check landmarks / wonders
        if clean in WONDERS_CACHE:
            w = WONDERS_CACHE[clean]
            c = _parse_coords(w.get("coords"))
            if c:
                return (w["name"], c, w)

        # Check lakes
        if clean in LAKES_CACHE:
            l = LAKES_CACHE[clean]
            c = _parse_coords(l.get("coords"))
            if c:
                return (l["name"], c, l)

        # Check straits & canals
        if clean in STRAITS_CACHE:
            st = STRAITS_CACHE[clean]
            c = _parse_coords(st.get("coords"))
            if c:
                return (st["name"], c, st)

        return None

    def query(self, intent: Intent, entities: List[str], raw_text: str, context: Optional[str] = None) -> Optional[QueryResult]:
        if not entities:
            return None

        primary = entities[0].lower().strip()

        # 1. Capital Lookup
        if intent == Intent.CAPITAL_LOOKUP:
            country_info = COUNTRIES_DATA.get(primary)
            if country_info:
                text = (
                    f"🏛️ **Capital of {country_info['name']}**\n\n"
                    f"The capital of **{country_info['name']}** is **{country_info['capital']}**.\n\n"
                    f"- **Continent**: {country_info['continent']} ({country_info['region']})\n"
                    f"- **Country Population**: {country_info['population']:,}\n"
                    f"- **Official Currency**: {country_info['currency']}\n\n"
                    f"{country_info['overview']}"
                )
                return QueryResult(
                    text=text,
                    interpreted_query=f"capital of {country_info['name']}",
                    domain=Domain.GEOGRAPHY,
                    intent=Intent.CAPITAL_LOOKUP,
                    entities=[(primary, country_info['name'])],
                    metadata={"country": country_info["name"], "capital": country_info["capital"]},
                    sources=["GeoMind World Factbook", "National Geographic Standards"]
                )

        # 2. Population Query
        if intent == Intent.POPULATION_QUERY:
            # Check country
            if primary in COUNTRIES_DATA:
                c = COUNTRIES_DATA[primary]
                text = (
                    f"👥 **Population of {c['name']}**\n\n"
                    f"The population of **{c['name']}** is approximately **{c['population']:,}**.\n\n"
                    f"- **Land Area**: {c['area_sq_km']:,} km²\n"
                    f"- **Density**: ~{c['population'] / c['area_sq_km']:.1f} people/km²\n"
                    f"- **Capital City**: {c['capital']}"
                )
                return QueryResult(
                    text=text,
                    interpreted_query=f"population of {c['name']}",
                    domain=Domain.GEOGRAPHY,
                    intent=Intent.POPULATION_QUERY,
                    entities=[(primary, c['name'])],
                    metadata={"entity": c['name'], "population": c['population']},
                    sources=["UN World Population Prospects"]
                )
            if primary in WORLD_CITIES:
                city = WORLD_CITIES[primary]
                text = (
                    f"👥 **Population of {city['name']}**\n\n"
                    f"The metropolitan population of **{city['name']}** ({city['country']}) is approximately **{city['population']:,}**.\n\n"
                    f"- **Country**: {city['country']}\n"
                    f"- **Coordinates**: {city['coords']}\n"
                    f"- **Role**: {'Capital City' if city['is_capital'] else 'Major City / Commercial Center'}"
                )
                return QueryResult(
                    text=text,
                    interpreted_query=f"population of {city['name']}",
                    domain=Domain.GEOGRAPHY,
                    intent=Intent.POPULATION_QUERY,
                    entities=[(primary, city['name'])],
                    metadata={"entity": city['name'], "population": city['population']},
                    sources=["Demographia World Urban Areas"]
                )

        # 3. Bordering Countries
        if intent == Intent.BORDERING_COUNTRIES:
            c = COUNTRIES_DATA.get(primary)
            if c:
                borders = c["borders"]
                if borders:
                    borders_str = ", ".join(f"**{b}**" for b in borders)
                    body = f"**{c['name']}** shares land borders with **{len(borders)}** countries:\n\n{borders_str}"
                else:
                    body = f"**{c['name']}** is an island nation / sovereign state with **no land borders**."

                text = (
                    f"🗺️ **Borders of {c['name']}**\n\n"
                    f"{body}\n\n"
                    f"- **Continent**: {c['continent']}\n"
                    f"- **Region**: {c['region']}"
                )
                return QueryResult(
                    text=text,
                    interpreted_query=f"bordering countries of {c['name']}",
                    domain=Domain.GEOGRAPHY,
                    intent=Intent.BORDERING_COUNTRIES,
                    entities=[(primary, c['name'])],
                    metadata={"country": c['name'], "borders": borders},
                    sources=["UN Cartographic Section"]
                )

        # 4. Currency
        if intent == Intent.CURRENCY_LOOKUP:
            c = COUNTRIES_DATA.get(primary)
            if c:
                text = (
                    f"💵 **Currency of {c['name']}**\n\n"
                    f"The official currency of **{c['name']}** is the **{c['currency']}**.\n\n"
                    f"- **Capital**: {c['capital']}\n"
                    f"- **Official Language(s)**: {', '.join(c['languages'])}"
                )
                return QueryResult(
                    text=text,
                    interpreted_query=f"currency of {c['name']}",
                    domain=Domain.GEOGRAPHY,
                    intent=Intent.CURRENCY_LOOKUP,
                    entities=[(primary, c['name'])],
                    metadata={"country": c['name'], "currency": c['currency']},
                    sources=["ISO 4217 Currency Standards"]
                )

        # 5. General Country / City Overview
        if primary in COUNTRIES_DATA:
            c = COUNTRIES_DATA[primary]
            borders_str = ", ".join(c["borders"]) if c["borders"] else "None (Island nation)"
            languages_str = ", ".join(c["languages"])
            features_str = ", ".join(c["major_features"])

            text = (
                f"🌍 **Country Profile: {c['name']}** ({c['official_name']})\n\n"
                f"{c['overview']}\n\n"
                f"### 📍 Geographic & Administrative Key Facts\n"
                f"- **Capital**: {c['capital']}\n"
                f"- **Continent / Region**: {c['continent']} ({c['region']})\n"
                f"- **Coordinates**: {c['coords']}\n"
                f"- **Land Area**: {c['area_sq_km']:,} km²\n"
                f"- **Population**: {c['population']:,}\n"
                f"- **Currency**: {c['currency']}\n"
                f"- **Official Language(s)**: {languages_str}\n"
                f"- **Bordering Nations**: {borders_str}\n"
                f"- **Prominent Landforms**: {features_str}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"profile of {c['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, c['name'])],
                metadata=c,
                sources=["GeoMind World Factbook"]
            )

        if primary in WORLD_CITIES:
            city = WORLD_CITIES[primary]
            text = (
                f"🏙️ **City Profile: {city['name']}**\n\n"
                f"{city['description']}\n\n"
                f"### 📍 Key Facts\n"
                f"- **Country**: {city['country']}\n"
                f"- **Status**: {'National Capital' if city['is_capital'] else 'Metropolitan City'}\n"
                f"- **Coordinates**: {city['coords']}\n"
                f"- **Estimated Population**: {city['population']:,}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"profile of {city['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.CITY_INFO,
                entities=[(primary, city['name'])],
                metadata=city,
                sources=["GeoMind Urban Geography Database"]
            )

        # 6. Mountains and Mountain Ranges
        if primary in MOUNTAINS_CACHE:
            m = MOUNTAINS_CACHE[primary]
            c_str = ", ".join(m.get("countries", []))
            first_ascent = m.get("first_ascent", "Ancient/Unrecorded")
            text = (
                f"🏔️ **Mountain Profile: {m['name']}**\n\n"
                f"{m.get('description', '')}\n\n"
                f"### 📍 Key Geographic Facts\n"
                f"- **Elevation**: {m.get('elevation_meters', 0):,} meters ({m.get('elevation_feet', 0):,} ft)\n"
                f"- **Mountain Range**: {m.get('range', 'N/A')}\n"
                f"- **Country / Location**: {c_str}\n"
                f"- **Coordinates**: {m.get('coords', [])}\n"
                f"- **First Historic Ascent**: {first_ascent}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {m['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, m['name'])],
                metadata=m,
                sources=["GeoMind Physical Geography", "Wikipedia Topography"]
            )

        # 7. Rivers
        if primary in RIVERS_CACHE:
            r = RIVERS_CACHE[primary]
            c_str = ", ".join(r.get("countries", []))
            text = (
                f"🌊 **River Profile: {r['name']}**\n\n"
                f"{r.get('description', '')}\n\n"
                f"### 📍 Hydrological Facts\n"
                f"- **Length**: {r.get('length_km', 0):,} km ({r.get('length_miles', 0):,} miles)\n"
                f"- **Basin Area**: {r.get('basin_area_sq_km', 0):,} km²\n"
                f"- **Average Discharge**: {r.get('discharge_m3_s', 0):,} m³/s\n"
                f"- **Source**: {r.get('source', 'N/A')}\n"
                f"- **Outflow / Mouth**: {r.get('outflow', 'N/A')}\n"
                f"- **Countries Traversed**: {c_str}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {r['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, r['name'])],
                metadata=r,
                sources=["GeoMind Hydrology", "Wikipedia World Rivers"]
            )

        # 8. Oceans and Seas
        if primary in OCEANS_CACHE:
            o = OCEANS_CACHE[primary]
            bordering = ", ".join(o.get("bordering_continents", []))
            text = (
                f"🌊 **Ocean & Sea Profile: {o['name']}**\n\n"
                f"{o.get('description', '')}\n\n"
                f"### 📍 Oceanic Dimensions\n"
                f"- **Surface Area**: {o.get('area_sq_km', 0):,} km²\n"
                f"- **Deepest Point**: {o.get('deepest_point', 'N/A')} ({o.get('deepest_depth_meters', 0):,} meters)\n"
                f"- **Average Depth**: {o.get('average_depth_meters', 0):,} meters\n"
                f"- **Volume**: ~{o.get('volume_cubic_km', 0):,} km³\n"
                f"- **Bordering Continents**: {bordering}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {o['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, o['name'])],
                metadata=o,
                sources=["GeoMind Oceanography", "Wikipedia Marine Sciences"]
            )

        # 9. Deserts
        if primary in DESERTS_CACHE:
            d = DESERTS_CACHE[primary]
            c_str = ", ".join(d.get("countries", []))
            text = (
                f"🏜️ **Desert Profile: {d['name']}**\n\n"
                f"{d.get('description', '')}\n\n"
                f"### 📍 Arid Landform Facts\n"
                f"- **Surface Area**: {d.get('area_sq_km', 0):,} km²\n"
                f"- **Desert Classification**: {d.get('type', 'Arid Desert')}\n"
                f"- **Countries / Territories**: {c_str}\n"
                f"- **Temperature Range**: {d.get('temperature_range', 'Variable')}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {d['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, d['name'])],
                metadata=d,
                sources=["GeoMind Physical Geography", "Wikipedia Deserts"]
            )

        # 10. Islands
        if primary in ISLANDS_CACHE:
            isl = ISLANDS_CACHE[primary]
            text = (
                f"🏝️ **Island Profile: {isl['name']}**\n\n"
                f"{isl.get('description', '')}\n\n"
                f"### 📍 Geographic Dimensions\n"
                f"- **Land Area**: {isl.get('area_sq_km', 0):,} km²\n"
                f"- **Sovereign Nation / Territory**: {isl.get('country_or_territory', 'N/A')}\n"
                f"- **Continent**: {isl.get('continent', 'N/A')}\n"
                f"- **Highest Elevation**: {isl.get('highest_point', 'N/A')} ({isl.get('elevation_m', 0):,} meters)\n"
                f"- **Population**: {isl.get('population', 0):,}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {isl['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, isl['name'])],
                metadata=isl,
                sources=["GeoMind Insular Geography", "Wikipedia Islands"]
            )

        # 11. Lakes
        if primary in LAKES_CACHE:
            lk = LAKES_CACHE[primary]
            c_str = ", ".join(lk.get("countries", []))
            text = (
                f"💧 **Lake Profile: {lk['name']}**\n\n"
                f"{lk.get('description', '')}\n\n"
                f"### 📍 Limnological Facts\n"
                f"- **Surface Area**: {lk.get('surface_area_sq_km', 0):,} km²\n"
                f"- **Maximum Depth**: {lk.get('max_depth_m', 0):,} meters\n"
                f"- **Water Volume**: {lk.get('volume_cubic_km', 0):,} km³\n"
                f"- **Bordering Nations**: {c_str}\n"
                f"- **Water Type**: {lk.get('type', 'Freshwater')}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {lk['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, lk['name'])],
                metadata=lk,
                sources=["GeoMind Limnology", "Wikipedia Lakes"]
            )

        # 12. World Wonders & Landmarks
        if primary in WONDERS_CACHE:
            w = WONDERS_CACHE[primary]
            text = (
                f"🏛️ **World Landmark: {w['name']}**\n\n"
                f"{w.get('description', '')}\n\n"
                f"### 📍 Architectural & Historical Facts\n"
                f"- **Category**: {w.get('category', 'Historic Monument')}\n"
                f"- **Location**: {w.get('location', '')}, {w.get('country', '')}\n"
                f"- **Coordinates**: {w.get('coords', [])}\n"
                f"- **Constructed**: {w.get('constructed', 'Ancient Era')}\n"
                f"- **Builder / Civilization**: {w.get('builder', 'Historical Civilization')}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {w['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, w['name'])],
                metadata=w,
                sources=["GeoMind Heritage Archive", "UNESCO World Heritage", "Wikipedia"]
            )

        # 13. Straits and Canals
        if primary in STRAITS_CACHE:
            st = STRAITS_CACHE[primary]
            c_str = ", ".join(st.get("bordering_countries", []))
            conn = " and ".join(st.get("connects", []))
            text = (
                f"🚢 **Maritime Passage: {st['name']}**\n\n"
                f"{st.get('description', '')}\n\n"
                f"### 📍 Maritime & Strategic Facts\n"
                f"- **Type**: {st.get('type', 'Maritime Strait')}\n"
                f"- **Connects**: {conn}\n"
                f"- **Bordering Nations**: {c_str}\n"
                f"- **Length**: {st.get('length_km', 'N/A')} km\n"
                f"- **Coordinates**: {st.get('coords', [])}\n"
                f"- **Strategic Significance**: {st.get('strategic_significance', '')}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"information about {st['name']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, st['name'])],
                metadata=st,
                sources=["GeoMind Maritime Geography", "Wikipedia Straits"]
            )

        # 14. Geographical Extremes
        if primary in EXTREMES_CACHE:
            ex = EXTREMES_CACHE[primary]
            text = (
                f"🌐 **Geographical Record: {ex['record']}**\n\n"
                f"**Record Holder**: **{ex['feature']}** ({ex.get('value', '')})\n\n"
                f"- **Location**: {ex.get('location', '')}\n"
                f"- **Key Fact**: {ex.get('description', '')}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"geographical record: {ex['record']}",
                domain=Domain.GEOGRAPHY,
                intent=Intent.COUNTRY_INFO,
                entities=[(primary, ex['feature'])],
                metadata=ex,
                sources=["GeoMind World Records", "Wikipedia Extremes"]
            )

        return None
