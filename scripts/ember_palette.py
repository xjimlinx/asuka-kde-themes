"""Asuka Ember: image-inspired oxblood, vermilion, copper and teal."""
import re

COLORS = {
    '#211A1E': '#241519', '#151316': '#180E11', '#261B1F': '#301B20',
    '#302326': '#40262A', '#39292B': '#482D30', '#21181B': '#261619',
    '#2B1D21': '#311C21', '#302125': '#3A2327', '#1D191C': '#211619',
    '#251F22': '#2B1B20', '#1E191D': '#231419', '#291F23': '#301D22',
    '#B82E36': '#9E392B', '#942831': '#7B2B24', '#D9443F': '#C65036',
    '#F5EDE4': '#EEDFD3', '#FFF5E8': '#FFF0E2', '#B3A2A2': '#BDA49C',
    '#FF8267': '#F09A76', '#F4BD70': '#E6AC82', '#83BCE8': '#80BAC6',
    '#D6A0C8': '#CFA4B5', '#FF8A85': '#F38E7F', '#91C99A': '#ADC395',
    '#191417': '#1C1014', '#695057': '#7B4D49', '#493138': '#553032',
    '#EF7167': '#EB8066', '#FF9387': '#F4A38A', '#D99451': '#C87B50',
    '#FFDA94': '#F6CCA1', '#B2DEAC': '#CDD8AB', '#AED8FA': '#AAD2DA',
    '#ECC0DF': '#E6C1CC', '#80C7C5': '#7CC5C2', '#A3E1DB': '#ADE0D6',
    '#45373D': '#503036', '#DED0C8': '#DFCABE', '#AC979C': '#B59890',
    '#E6DED5': '#D5C3B7', '#B8ADA3': '#AA9386', '#77716E': '#76605B',
    '#897052': '#8F604A', '#7D4545': '#7E4134', '#F16A5E': '#EC795A',
    '#A62932': '#963727', '#403A3D': '#463135',
    '#361D26': '#3A1820', '#E65143': '#CC613D', '#67212D': '#551D23',
    '#100F13': '#130C10', '#A48679': '#B98F7B', '#862F36': '#843428',
}

def transform(text):
    """One-pass color substitution for SVG/QML/JSON and KConfig RGB triples."""
    def rgb(h):
        return ','.join(str(int(h[i:i+2],16)) for i in (1,3,5))
    text = re.sub(r'#[0-9a-fA-F]{6}', lambda m: COLORS.get(m[0].upper(), m[0]), text)
    triples = {rgb(a): rgb(b) for a,b in COLORS.items()}
    text = re.sub(r'(?<![\d,])\d{1,3},\d{1,3},\d{1,3}(?![\d,])', lambda m: triples.get(m[0],m[0]), text)
    text = re.sub(r'AsukaRounded|com\.omen\.asuka|Asuka', lambda m: {
        'AsukaRounded':'AsukaEmberRounded', 'com.omen.asuka':'com.omen.asukaember',
        'Asuka':'AsukaEmber'}[m[0]], text)
    return text.replace('明日香 · 二号机', '明日香 · 余烬').replace('ASUKA / UNIT 02','ASUKA / EMBER').replace('ASUKA / SCARLET EDITION','ASUKA / EMBER EDITION')
