import requests
import math

URL = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-SNI-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt"
]
CD = 5
country_order = [
    "Russia", "Germany", "Netherlands", "Finland", "Sweden", "Norway", "Denmark",
    "Poland", "Czech", "Austria", "Switzerland", "France", "Spain", "Italy",
    "United Kingdom", "Canada", "USA", "Japan", "Singapore", "Australia",
    "Belgium", "Ireland", "Portugal", "Greece", "Hungary", "Romania", "Bulgaria",
    "Croatia", "Slovakia", "Slovenia", "Estonia", "Latvia", "Lithuania",
    "Iceland", "Luxembourg", "Malta", "Cyprus", "Turkey", "Israel", "UAE",
    "Saudi Arabia", "India", "Indonesia", "Malaysia", "Thailand", "Vietnam",
    "Philippines", "South Korea", "Brazil", "Argentina", "Chile", "Mexico",
    "South Africa", "Nigeria", "Kenya"
]

country_map = {
    "Russia": "🇷🇺 Россия", "Germany": "🇩🇪 Германия", "Netherlands": "🇳🇱 Нидерланды",
    "Finland": "🇫🇮 Финляндия", "Sweden": "🇸🇪 Швеция", "Norway": "🇳🇴 Норвегия",
    "Denmark": "🇩🇰 Дания", "Poland": "🇵🇱 Польша", "Czech": "🇨🇿 Чехия",
    "Austria": "🇦🇹 Австрия", "Switzerland": "🇨🇭 Швейцария", "France": "🇫🇷 Франция",
    "Spain": "🇪🇸 Испания", "Italy": "🇮🇹 Италия", "United Kingdom": "🇬🇧 Великобритания",
    "Canada": "🇨🇦 Канада", "USA": "🇺🇸 США", "Japan": "🇯🇵 Япония",
    "Singapore": "🇸🇬 Сингапур", "Australia": "🇦🇺 Австралия", "Belgium": "🇧🇪 Бельгия",
    "Ireland": "🇮🇪 Ирландия", "Portugal": "🇵🇹 Португалия", "Greece": "🇬🇷 Греция",
    "Hungary": "🇭🇺 Венгрия", "Romania": "🇷🇴 Румыния", "Bulgaria": "🇧🇬 Болгария",
    "Croatia": "🇭🇷 Хорватия", "Slovakia": "🇸🇰 Словакия", "Slovenia": "🇸🇮 Словения",
    "Estonia": "🇪🇪 Эстония", "Latvia": "🇱🇻 Латвия", "Lithuania": "🇱🇹 Литва",
    "Iceland": "🇮🇸 Исландия", "Luxembourg": "🇱🇺 Люксембург", "Malta": "🇲🇹 Мальта",
    "Cyprus": "🇨🇾 Кипр", "Turkey": "🇹🇷 Турция", "Israel": "🇮🇱 Израиль",
    "UAE": "🇦🇪 ОАЭ", "Saudi Arabia": "🇸🇦 Саудовская Аравия", "India": "🇮🇳 Индия",
    "Indonesia": "🇮🇩 Индонезия", "Malaysia": "🇲🇾 Малайзия", "Thailand": "🇹🇭 Таиланд",
    "Vietnam": "🇻🇳 Вьетнам", "Philippines": "🇵🇭 Филиппины", "South Korea": "🇰🇷 Южная Корея",
    "Brazil": "🇧🇷 Бразилия", "Argentina": "🇦🇷 Аргентина", "Chile": "🇨🇱 Чили",
    "Mexico": "🇲🇽 Мексика", "South Africa": "🇿🇦 ЮАР", "Nigeria": "🇳🇬 Нигерия",
    "Kenya": "🇰🇪 Кения"
}

def get_country(tag):
    for country in country_order:
        if country in tag:
            return country
    return "Other"

def transform_link(link, country_name):
    if '#' not in link:
        return link
    base = link.split('#')[0] + '#'
    ru_name = country_map.get(country_name, f"{country_name}")
    return f"{base}{ru_name} | viarvpn_free.t.me"

def main():
    all_lines = []
    for url in URL:
        resp = requests.get(url)
        for l in resp.text.splitlines():
            l = l.strip()
            if l and not l.startswith('#') and l.startswith('vless://'):
                all_lines.append(l)
    seen = set()
    unique_lines = []
    for line in all_lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    by_country = {c: [] for c in country_order}
    by_country["Other"] = []
    for line in unique_lines:
        found = False
        for c in country_order:
            if c in line:
                by_country[c].append(line)
                found = True
                break
        if not found:
            by_country["Other"].append(line)
    all_final_links = []
    for country in country_order:
        for link in by_country[country]:
            all_final_links.append(transform_link(link, country))
    for link in by_country["Other"]:
        all_final_links.append(transform_link(link, "Other"))
    total = len(all_final_links)
    chunk_size = math.ceil(total / CD)
    with open("all.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_final_links))
    for i in range(CD):
        start = i * chunk_size
        end = min(start + chunk_size, total)
        if start >= total:
            break
        with open(f"{i+1}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(all_final_links[start:end]))

if __name__ == "__main__":
    main()
