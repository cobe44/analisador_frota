import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import math
import io
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Gestão de Frota", layout="wide")
st.title("🚛 Gestão de Frota")

# --- 1. LOCAIS (POIs) ---

POIS_TATUI = {
    "Base Tatuí": [(-23.332105, -47.847368), (-23.331969, -47.84704)],
    "Garagem/Pernoite": [(-23.322100, -47.828800)], 
    "JBS Tatuí (Incubatório)": [(-23.379379, -47.784094), (-23.37939, -47.782949)], 
    "Sarapuí": [(-23.620132, -47.824889)],
    "Granja Bragança": [(-22.902751, -46.488519), (-22.904339, -46.488448)],
    "Conchal": [(-22.327445, -47.107089), (-22.327704, -47.106906)],
    "Conchal (Ponto 2)": [(-22.408612, -47.083524), (-22.408293, -47.083835)],
    "Santo Antonio da Posse": [(-22.654077, -46.909709), (-22.650286, -46.905149)],
    "Buri": [(-23.784699, -48.558509), (-23.783429, -48.555581)],
    "Pereiras": [(-23.052282, -47.961171), (-23.052906, -47.960992)],
    "Corumbataí": [(-22.275962, -47.625296), (-22.274258, -47.623837), (-22.27449, -47.621821)]
}

POIS_PASSOS = {
    "JBS Passos": [(-20.731648, -46.572150), (-20.73273, -46.573021), (-20.731648, -46.57215)],
    'GRANJA MANOELA': [(-20.80083, -46.304)], 'SÍTIO MORRO CAVADO': [(-20.77593, -46.37077)], 
    'FAZENDA CONQUISTA': [(-20.8788, -46.46472), (-21.31993, -47.00195)], 'SITIO SOQUETE': [(-20.79604, -46.39279)], 
    'SÍTIO LEMBRANÇA': [(-20.73954, -46.39466)], 'SÍTIO MONJOLINHO/SÃO JOSÉ': [(-20.88404, -46.40669)], 
    'GRANJA GONÇALVES': [(-20.88317, -46.45322)], 'FAZENDA SANTA CÂNDIDA': [(-20.91467, -46.47136)], 
    'FAZENDA PRIMAVERA': [(-21.24983, -46.1174)], 'FAZENDA MARINHEIRO': [(-21.31151, -46.94579)], 
    'SÍTIO TERRA NOVA': [(-21.28862, -46.94458)], 'ESTANCIA L.H.D.': [(-21.35395, -46.92693)], 
    'SÍTIO MENDES': [(-21.28193, -46.95551)], 'SÍTIO UNIÃO': [(-21.28893, -46.94949)], 
    "SÍTIO NOSSA SENHORA APARECIDA / SÍTIO OLHOS D'ÁGUA": [(-21.32871, -46.95216)], 'SÍTIO PRIMAVERA': [(-21.3249, -46.95071)], 
    'SÍTIO MAMDEMBO': [(-21.30659, -46.94204)], 'SÍTIO BAGAÇO': [(-21.35028, -46.97615)], 
    'FAZENDA BRITOS': [(-21.03227, -46.57611)], 'FAZENDA CÓRREGO DO OURO': [(-20.96551, -46.48639)], 
    'SÍTIO NICANOR / GRANJA PALMEIRAS': [(-20.99147, -46.50997)], 'FAZENDA PALMITAL': [(-21.46432, -46.32569), (-20.67564, -46.96479)], 
    'FAZENDA SÃO JOSÉ': [(-21.46983, -46.3906)], 'FAZENDA ITÁLIA II': [(-21.45987, -46.37785)], 
    'FAZENDA GROTÃO': [(-20.60469, -46.15272)], 'FAZENDA SOCORRO': [(-20.58068, -46.0097)], 
    'SITIO VIRADA': [(-20.81071, -46.21339)], 'FAZENDA PINHEIROS': [(-20.82645, -46.21318), (-20.84661, -46.19884)], 
    'FAZENDA SÍTIO DA VARGEM': [(-20.89167, -46.22708)], 'FAZENDA VARGEM DOS PINHEIROS': [(-20.84741, -46.22896)], 
    'FAZENDA SÃO SEBASTIÃO': [(-20.84278, -46.25489)], 'FAZENDA NOSSA SENHORA APARECIDA': [(-20.58601, -46.96098)], 
    'SÍTIO NOSSA SENHORA DE FÁTIMA': [(-20.46836, -46.91574)], 'FAZENDA MAMONO': [(-20.70876, -46.8724)], 
    'FAZENDA SANTA FÉ': [(-20.525, -46.95302), (-20.7117, -46.40118)], 'SÍTIO NOSSA SENHORA APARECIDA': [(-20.7032, -46.88562), (-20.88953, -46.95689)], 
    'FAZENDA SÃO MIGUEL': [(-21.09856, -46.14926)], 'FAZENDA SANTA CRUZ': [(-20.31945, -45.92343), (-20.83078, -46.29656)], 
    'FAZENDA MORRO GRANDE RETIRO': [(-20.31887, -45.91422)], 'FAZENDA MANDEMBO': [(-20.25968, -45.89388)], 
    'FAZENDA PRATA': [(-20.92784, -46.71557)], 'SÍTIO BELA VISTA': [(-21.34004, -46.88405)], 
    'SÍTIO ACONCHEGO': [(-21.35154, -46.75137)], 'FAZENDA BOM JARDIM': [(-21.33864, -46.6975)], 
    'SÍTIO JATOBÁ': [(-21.04232, -46.97038)], 'SÍTIO SERRA OU LAVRADO': [(-21.11289, -46.99578)], 
    'FAZENDA SÃO FRANCISCO': [(-21.09737, -46.97666)], 'FAZENDA SÃO JOÃO': [(-21.1313, -47.00708)], 
    'SÍTIO BOA VISTA': [(-20.70022, -46.75862), (-21.01609, -46.81136), (-21.26493, -46.59088)], 
    'SÍTIO SANTANA': [(-20.77027, -46.79905)], 'SÍTIO CARAS ALTAS': [(-20.77073, -46.79765)], 
    'SÍTIO SÃO JOSÉ': [(-20.99052, -46.72036), (-21.13335, -47.0006)], 'SÍTIO ZUDUM': [(-21.09155, -46.72187)], 
    'FAZENDA PINHAL DOS AFONSOS': [(-21.07127, -46.76625)], 'SÍTIO BICUDOS E ESTEVES': [(-21.06493, -46.80943)], 
    'SÍTIO MATO DENTRO': [(-21.06569, -46.79925)], 'SÍTIO RETIRO III': [(-20.99697, -46.77525)], 
    'SITIO AREIAS': [(-21.22392, -46.58939), (-21.21937, -46.57365)], 'FAZENDA CACHOEIRA': [(-21.20224, -46.48198), (-20.72632, -46.56935), (-20.78167, -46.52858)], 
    'SÍTIO SANTO ALEIXO': [(-21.2263, -46.49266), (-21.22167, -46.49951)], 'GRANJA BEIRA RIO': [(-21.20539, -46.59408)], 
    'SÍTIO GRAMA': [(-21.24198, -46.43059)], 'GRANJA AREIAS': [(-21.22568, -46.56873)], 
    'SÍTIO COCOROBO': [(-21.23082, -46.6017)], 'SÍTIO LARANJEIRA': [(-21.23632, -46.57128)], 
    'SÍTIO CANAÃ': [(-21.2745, -46.5704)], 'SÍTIO GOMES': [(-21.27324, -46.55551)], 
    'SÍTIO AREIA / SÍTIO PICA PAU': [(-21.22738, -46.55465)], 'SITIO BARRA MANSA': [(-21.24822, -46.5772)], 
    'SITIO SÃO JOSÉ/ SÍTIO AREIAS': [(-21.22344, -46.58394)], 'SÍTIO SÃO SEBASTIÃO': [(-21.25428, -46.53161), (-21.24879, -46.9477)], 
    'SÍTIO LARANJEIRAS': [(-21.24077, -46.58357)], 'SÍTIO AREIAS / SÍTIO SANTO ANTÔNIO': [(-21.23051, -46.57313)], 
    'SÍTIO SÃO PAULO / AREIAS': [(-21.22122, -46.57232)], 'SÍTIO BARRA MANSA': [(-21.23328, -46.58785)], 
    'SÍTIO SANTO ANTÔNIO / GUINÉ': [(-21.21384, -46.5418)], 'FAZENDA ITUPAVA': [(-21.29568, -46.59137)], 
    'SITIO AREIAS DA GRANJA': [(-21.22326, -46.5504)], 'FAZENDA SÃO LUIZ': [(-21.19755, -46.91748)], 
    'SÍTIO RECANTO SANTA LUZIA': [(-21.27339, -46.99435)], 'SÍTIO IPANEMA I E II': [(-21.21165, -46.87866)], 
    'FAZENDA LIMEIRA': [(-21.21123, -46.92336)], 'SÍTIO NOVA ESPERANÇA': [(-21.16046, -46.93101)], 
    'SÍTIO ESTANCIA JD': [(-21.18897, -46.93512)], 'SÍTIO JABAQUARA': [(-21.24655, -46.95186)], 
    'FAZENDA BANANAL': [(-21.23549, -47.02412)], 'SÍTIO JABAQUARA OU MARAMBAIA': [(-21.25446, -46.95311)], 
    'FAZENDA BOA ESPERANÇA': [(-21.25804, -46.94876), (-20.41528, -45.89707)], 'SÍTIO MÃE RAINHA': [(-21.17429, -46.85492)], 
    'SÍTIO RANCHO DA MONTANHA': [(-21.26386, -46.93502)], 'SÍTIO MODELO': [(-21.22792, -47.00853)], 
    'SÍTIO RECANTO OU GUARITA': [(-21.27391, -46.91092)], 'SÍTIO CACHOEIRINHA': [(-21.19149, -46.92346)], 
    'ESTÂNCIA SÃO JOÃO': [(-21.13624, -47.01362)], 'SÍTIO LIMOEIRO': [(-21.30637, -46.9943)], 
    'SÍTIO BAÚ DO BARBOSA': [(-21.19045, -47.09453)], 'SÍTIO SANTOS REIS': [(-21.19463, -46.91881)], 
    'SÍTIO MARIA FERREIRA': [(-21.18668, -46.95443)], 'FAZENDA DONOLANDA': [(-21.21412, -47.03282)], 
    'FAZENDA SANTA RITA': [(-21.22025, -47.0029)], 'SÍTIO MUZAMBO': [(-21.26077, -46.51495)], 
    'SITIO BOM RETIRO': [(-21.26506, -46.51686)], 'FAZENDA OURO BRANCO': [(-20.7868, -46.53807)], 
    'FAZENDA RETIRO DAS AROEIRAS': [(-20.75536, -46.678805)], 'GRANJA PASSOS/SÃO FRANCISCO': [(-20.75183, -46.55284)], 
    'FAZENDA CONQUISTINHA': [(-20.87376, -46.47114)], 'FAZENDA TAQUARUSSU': [(-20.77192, -46.46862)], 
    'GRANJA PANTANAL / FAZENDA SÃO JOÃO DA BOA VISTA': [(-20.80236, -46.66234)], 'FAZENDA MACAUBA': [(-20.70871, -46.56916)], 
    'FAZENDA AREIAS': [(-20.82558, -46.6742)], 'FAZENDA LAGE': [(-20.53653, -46.76786), (-20.74047, -46.31834)], 
    'FAZENDA CÓRREGO DA PORTEIRA': [(-20.50109, -45.97182)], 'FAZENDA CAMPO ALEGRE': [(-20.39191, -45.98669)], 
    'FAZENDA BOM SUCESSO': [(-20.3512, -46.08971), (-20.37927, -46.154)], 'FAZENDA ÁGUA FRIA': [(-20.45832, -45.9337)], 
    'SITIO MORADA DO SOL': [(-20.5213, -46.0299)], 'FAZENDA ROCHEDOS': [(-20.33906, -45.88261)], 
    'FAZENDA ÁGUA LIMPA': [(-20.54589, -45.98633), (-20.82083, -46.75389)], 'SÍTIO MORADA DAS ÁGUAS': [(-20.8233, -46.75882)], 
    'SÍTIO SANTO EXPEDITO': [(-20.80808, -46.87205)], 'SÍTIO SÃO PEDRO': [(-20.81974, -46.84161), (-20.74355, -46.81884)], 
    'FAZENDA PALESTINA OLARIA': [(-20.82409, -46.90179)], 'SÍTIO DA MATA': [(-20.79687, -46.82)], 
    'FAZENDA FÁBRICA': [(-20.8526, -46.88051)], 'SITIO DOIS IRMAOS': [(-20.69895, -46.83767)], 
    'FAZENDA PONTAL': [(-20.7564, -46.9401)], 'SÍTIO JD': [(-20.79067, -46.83151)], 
    'SÍTIO DOIS IRMÃOS': [(-20.69592, -46.8417)], 'FAZENDA PONTAL DA PRATA': [(-20.75907, -46.90998)], 
    'SÍTIO RANCHO DA LUA': [(-20.57351, -46.5025)], 'FAZENDA NOSSA SENHORA DA PENHA': [(-20.84833, -46.273)], 
    'GRANJA CANCANZINHO': [(-20.82648, -46.29172)], 'FAZENDA SANTA BÁRBARA': [(-20.85436, -46.27271)], 
    'FAZENDA PONTA DA SERRA': [(-20.71381, -46.23641)], 'FAZENDA FLORADA DA SERRA': [(-20.96938, -46.8849)], 
    'FAZENDA MORRO VERMELHO': [(-21.02975, -46.91374)], 'FAZENDA SANTANA': [(-20.9347, -46.92694)], 
    'FAZENDA MUMBUCA': [(-20.89542, -47.12121)], 'FAZENDA BARRA DA LONTRA': [(-20.90041, -46.92076)], 
    'SÍTIO MAMONINHO': [(-20.88282, -47.04195)], 'SÍTIO DAS OLIVEIRAS / BARREIRINHO': [(-20.9402, -46.88693)], 
    'SÍTIO SANTO ANTÔNIO': [(-20.9112, -46.91808)], 'FAZENDA BARREIRO': [(-20.98822, -46.85752)], 
    'FAZENDA RECANTO FELIZ': [(-20.95863, -46.88674)], 'SITIO NOSSA SENHORA DO DESTERRO': [(-20.9958, -46.9571)], 
    'FAZENDA TABULEIRO': [(-21.04108, -46.92811)], 'SÍTIO RIBEIRÃO FUNDO': [(-20.90232, -47.16151)], 
    'SÍTIO RECANTO FELIZ': [(-20.95913, -46.88719)], 'SÍTIO TÁBOAS': [(-20.92652, -46.92271)], 
    'SÍTIO PARAÍSO': [(-21.02702, -46.90079), (-21.04212, -46.9322)], 'FAZENDA BELA VISTA': [(-20.92852, -46.94781)], 
    'FAZENDA NOVO HORIZONTE DOS PAIXÃO': [(-20.80349, -47.04923)], 'FAZENDA PORTOBELLO': [(-20.82962, -47.1253)]
}

POIS_IPIGUA = { "Incubatório Ipiguá": [(-20.652477, -49.387725)] }

# --- MAPEAMENTO DE CIDADES (PASSOS) ---
MAPA_CIDADES_PASSOS = {
    'GRANJA MANOELA': 'ALPINÓPOLIS', 'SÍTIO MORRO CAVADO': 'ALPINÓPOLIS', 'FAZENDA CONQUISTA': 'ALPINÓPOLIS',
    'SITIO SOQUETE': 'ALPINÓPOLIS', 'SÍTIO LEMBRANÇA': 'ALPINÓPOLIS', 'SÍTIO MONJOLINHO/SÃO JOSÉ': 'ALPINÓPOLIS',
    'GRANJA GONÇALVES': 'ALPINÓPOLIS', 'FAZENDA SANTA CÂNDIDA': 'ALPINÓPOLIS', 'FAZENDA PRIMAVERA': 'ALTINÓPOLIS',
    'FAZENDA MARINHEIRO': 'ARCEBURGO', 'SÍTIO TERRA NOVA': 'ARCEBURGO', 'ESTANCIA L.H.D.': 'ARCEBURGO',
    'SÍTIO MENDES': 'ARCEBURGO', 'SÍTIO UNIÃO': 'ARCEBURGO', "SÍTIO NOSSA SENHORA APARECIDA / SÍTIO OLHOS D'ÁGUA": 'ARCEBURGO',
    'SÍTIO PRIMAVERA': 'ARCEBURGO', 'SÍTIO MAMDEMBO': 'ARCEBURGO', 'SÍTIO BAGAÇO': 'ARCEBURGO',
    'FAZENDA BRITOS': 'AREZ', 'FAZENDA CÓRREGO DO OURO': 'BOM JESUS DA PENHA', 'SÍTIO NICANOR / GRANJA PALMEIRAS': 'BOM JESUS DA PENHA',
    'FAZENDA PALMITAL': 'BOM JESUS DA PENHA', 'FAZENDA SÃO JOSÉ': 'BOM JESUS DA PENHA', 'FAZENDA ITÁLIA II': 'BOM JESUS DA PENHA',
    'FAZENDA GROTÃO': 'CAPITÓLIO', 'FAZENDA SOCORRO': 'CAPITÓLIO', 'SITIO VIRADA': 'CARMO DO RIO CLARO',
    'FAZENDA PINHEIROS': 'CARMO DO RIO CLARO', 'FAZENDA SÍTIO DA VARGEM': 'CARMO DO RIO CLARO', 'FAZENDA VARGEM DOS PINHEIROS': 'CARMO DO RIO CLARO',
    'FAZENDA SÃO SEBASTIÃO': 'CARMO DO RIO CLARO', 'FAZENDA NOSSA SENHORA APARECIDA': 'CÁSSIA', 'SÍTIO NOSSA SENHORA DE FÁTIMA': 'CÁSSIA',
    'FAZENDA MAMONO': 'CÁSSIA', 'FAZENDA SANTA FÉ': 'CÁSSIA', 'SÍTIO NOSSA SENHORA APARECIDA': 'CÁSSIA',
    'FAZENDA SÃO MIGUEL': 'CONCEIÇÃO DA APARECIDA', 'FAZENDA SANTA CRUZ': 'DELFINÓPOLIS', 'FAZENDA MORRO GRANDE RETIRO': 'DELFINÓPOLIS',
    'FAZENDA MANDEMBO': 'DELFINÓPOLIS', 'FAZENDA PRATA': 'FORTALEZA DE MINAS', 'SÍTIO BELA VISTA': 'GUAXUPÉ',
    'SÍTIO ACONCHEGO': 'GUAXUPÉ', 'FAZENDA BOM JARDIM': 'GUAXUPÉ', 'SÍTIO JATOBÁ': 'ITAMOGI', 'SÍTIO SERRA OU LAVRADO': 'ITAMOGI',
    'FAZENDA SÃO FRANCISCO': 'ITAMOGI', 'FAZENDA SÃO JOÃO': 'ITAMOGI', 'SÍTIO BOA VISTA': 'ITAÚ DE MINAS', 'SÍTIO SANTANA': 'ITAÚ DE MINAS',
    'SÍTIO CARAS ALTAS': 'ITAÚ DE MINAS', 'SÍTIO SÃO JOSÉ': 'JACUÍ', 'SÍTIO ZUDUM': 'JACUÍ', 'FAZENDA PINHAL DOS AFONSOS': 'JACUÍ',
    'SÍTIO BICUDOS E ESTEVES': 'JACUÍ', 'SÍTIO MATO DENTRO': 'JACUÍ', 'SÍTIO RETIRO III': 'JACUÍ', 'SITIO AREIAS': 'JURUAIA',
    'FAZENDA CACHOEIRA': 'JURUAIA', 'SÍTIO SANTO ALEIXO': 'JURUAIA', 'GRANJA BEIRA RIO': 'JURUAIA', 'SÍTIO GRAMA': 'JURUAIA',
    'GRANJA AREIAS': 'JURUAIA', 'SÍTIO COCOROBO': 'JURUAIA', 'SÍTIO LARANJEIRA': 'JURUAIA', 'SÍTIO CANAÃ': 'JURUAIA',
    'SÍTIO GOMES': 'JURUAIA', 'SÍTIO AREIA / SÍTIO PICA PAU': 'JURUAIA', 'SITIO BARRA MANSA': 'JURUAIA', 'SITIO SÃO JOSÉ/ SÍTIO AREIAS': 'JURUAIA',
    'SÍTIO SÃO SEBASTIÃO': 'JURUAIA', 'SÍTIO LARANJEIRAS': 'JURUAIA', 'SÍTIO AREIAS / SÍTIO SANTO ANTÔNIO': 'JURUAIA',
    'SÍTIO SÃO PAULO / AREIAS': 'JURUAIA', 'SÍTIO BARRA MANSA': 'JURUAIA', 'SÍTIO SANTO ANTÔNIO / GUINÉ': 'JURUAIA',
    'FAZENDA ITUPAVA': 'JURUAIA', 'SITIO AREIAS DA GRANJA': 'JURUAIA', 'FAZENDA SÃO LUIZ': 'MONTE SANTO DE MINAS',
    'SÍTIO RECANTO SANTA LUZIA': 'MONTE SANTO DE MINAS', 'SÍTIO IPANEMA I E II': 'MONTE SANTO DE MINAS', 'FAZENDA LIMEIRA': 'MONTE SANTO DE MINAS',
    'SÍTIO NOVA ESPERANÇA': 'MONTE SANTO DE MINAS', 'SÍTIO ESTANCIA JD': 'MONTE SANTO DE MINAS', 'SÍTIO JABAQUARA': 'MONTE SANTO DE MINAS',
    'FAZENDA BANANAL': 'MONTE SANTO DE MINAS', 'SÍTIO JABAQUARA OU MARAMBAIA': 'MONTE SANTO DE MINAS', 'FAZENDA BOA ESPERANÇA': 'MONTE SANTO DE MINAS',
    'SÍTIO MÃE RAINHA': 'MONTE SANTO DE MINAS', 'SÍTIO RANCHO DA MONTANHA': 'MONTE SANTO DE MINAS', 'SÍTIO MODELO': 'MONTE SANTO DE MINAS',
    'SÍTIO RECANTO OU GUARITA': 'MONTE SANTO DE MINAS', 'SÍTIO CACHOEIRINHA': 'MONTE SANTO DE MINAS', 'ESTÂNCIA SÃO JOÃO': 'MONTE SANTO DE MINAS',
    'SÍTIO LIMOEIRO': 'MONTE SANTO DE MINAS', 'SÍTIO BAÚ DO BARBOSA': 'MONTE SANTO DE MINAS', 'SÍTIO SANTOS REIS': 'MONTE SANTO DE MINAS',
    'SÍTIO MARIA FERREIRA': 'MONTE SANTO DE MINAS', 'FAZENDA DONOLANDA': 'MONTE SANTO DE MINAS', 'FAZENDA SANTA RITA': 'MONTE SANTO DE MINAS',
    'SÍTIO MUZAMBO': 'MUZAMBINHO', 'SITIO BOM RETIRO': 'MUZAMBINHO', 'FAZENDA OURO BRANCO': 'PASSOS',
    'FAZENDA RETIRO DAS AROEIRAS': 'PASSOS', 'GRANJA PASSOS/SÃO FRANCISCO': 'PASSOS', 'FAZENDA CONQUISTINHA': 'PASSOS',
    'FAZENDA TAQUARUSSU': 'PASSOS', 'GRANJA PANTANAL / FAZENDA SÃO JOÃO DA BOA VISTA': 'PASSOS', 'FAZENDA MACAUBA': 'PASSOS',
    'FAZENDA AREIAS': 'PASSOS', 'FAZENDA LAGE': 'PIUMHI', 'FAZENDA CÓRREGO DA PORTEIRA': 'PIUMHI', 'FAZENDA CAMPO ALEGRE': 'PIUMHI',
    'FAZENDA BOM SUCESSO': 'PIUMHI', 'FAZENDA ÁGUA FRIA': 'PIUMHI', 'SITIO MORADA DO SOL': 'PIUMHI', 'FAZENDA ROCHEDOS': 'PIUMHI',
    'FAZENDA ÁGUA LIMPA': 'PRATÁPOLIS', 'SÍTIO MORADA DAS ÁGUAS': 'PRATÁPOLIS', 'SÍTIO SANTO EXPEDITO': 'PRATÁPOLIS',
    'SÍTIO SÃO PEDRO': 'PRATÁPOLIS', 'FAZENDA PALESTINA OLARIA': 'PRATÁPOLIS', 'SÍTIO DA MATA': 'PRATÁPOLIS',
    'FAZENDA FÁBRICA': 'PRATÁPOLIS', 'SITIO DOIS IRMAOS': 'PRATÁPOLIS', 'FAZENDA PONTAL': 'PRATÁPOLIS', 'SÍTIO JD': 'PRATÁPOLIS',
    'SÍTIO DOIS IRMÃOS': 'PRATÁPOLIS', 'FAZENDA PONTAL DA PRATA': 'PRATÁPOLIS', 'SÍTIO RANCHO DA LUA': 'PRATÁPOLIS',
    'FAZENDA NOSSA SENHORA DA PENHA': 'SÃO JOÃO BATISTA DO GLÓRIA', 'GRANJA CANCANZINHO': 'SÃO JOÃO BATISTA DO GLÓRIA',
    'FAZENDA SANTA BÁRBARA': 'SÃO JOÃO BATISTA DO GLÓRIA', 'FAZENDA PONTA DA SERRA': 'SÃO JOÃO BATISTA DO GLÓRIA',
    'FAZENDA FLORADA DA SERRA': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA MORRO VERMELHO': 'SÃO SEBASTIÃO DO PARAÍSO',
    'FAZENDA SANTANA': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA MUMBUCA': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA BARRA DA LONTRA': 'SÃO SEBASTIÃO DO PARAÍSO',
    'SÍTIO MAMONINHO': 'SÃO SEBASTIÃO DO PARAÍSO', 'SÍTIO DAS OLIVEIRAS / BARREIRINHO': 'SÃO SEBASTIÃO DO PARAÍSO',
    'SÍTIO SANTO ANTÔNIO': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA BARREIRO': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA RECANTO FELIZ': 'SÃO SEBASTIÃO DO PARAÍSO',
    'SITIO NOSSA SENHORA DO DESTERRO': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA TABULEIRO': 'SÃO SEBASTIÃO DO PARAÍSO',
    'SÍTIO RIBEIRÃO FUNDO': 'SÃO SEBASTIÃO DO PARAÍSO', 'SÍTIO RECANTO FELIZ': 'SÃO SEBASTIÃO DO PARAÍSO',
    'SÍTIO TÁBOAS': 'SÃO SEBASTIÃO DO PARAÍSO', 'SÍTIO PARAÍSO': 'SÃO SEBASTIÃO DO PARAÍSO', 'FAZENDA BELA VISTA': 'SÃO SEBASTIÃO DO PARAÍSO',
    'FAZENDA NOVO HORIZONTE DOS PAIXÃO': 'SÃO TOMÁS DE AQUINO', 'FAZENDA PORTOBELLO': 'SÃO TOMÁS DE AQUINO'
}

# --- 2. SELETOR DE OPERAÇÃO ---
st.sidebar.header("Configuração da Operação")
operacao_selecionada = st.sidebar.selectbox("Selecione a Operação:", ["Tatuí (Ovos)", "Passos (Frango)", "Ipiguá (Pintos)"])

if operacao_selecionada == "Tatuí (Ovos)":
    POIS_ATIVOS = POIS_TATUI
    NOME_BASE = "Base Tatuí"
    RAIO_PADRAO_BASE = 3000
    RAIO_LOCAL_PADRAO = 600 
elif operacao_selecionada == "Passos (Frango)":
    POIS_ATIVOS = POIS_PASSOS
    NOME_BASE = "JBS Passos" 
    RAIO_PADRAO_BASE = 3000 
    RAIO_LOCAL_PADRAO = 120 
else: 
    POIS_ATIVOS = POIS_IPIGUA
    NOME_BASE = "Incubatório Ipiguá"
    RAIO_PADRAO_BASE = 2000
    RAIO_LOCAL_PADRAO = 1000

# --- INPUTS ---
col_placa, col_vazio = st.columns([1, 3])
placa_veiculo = col_placa.text_input("Placa do Veículo", placeholder="Ex: ABC-1234").upper()

st.sidebar.markdown("---")
raio_base = st.sidebar.slider("Raio da Base (m)", 500, 5000, RAIO_PADRAO_BASE)
raio_poi = st.sidebar.slider("Raio dos Locais (m)", 100, 3000, RAIO_LOCAL_PADRAO) 
min_idling_minutes = st.sidebar.number_input("Alerta Ociosidade (min)", value=10)

# --- FUNÇÕES ---

def format_seconds_to_hms(seconds):
    if pd.isna(seconds) or seconds == 0: return "00:00:00"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatorio')
    return output.getvalue()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def is_near_poi(lat, lon, poi_coords_list, threshold):
    for (p_lat, p_lon) in poi_coords_list:
        if haversine(lat, lon, p_lat, p_lon) <= threshold:
            return True
    return False

def get_current_poi_name(lat, lon, pois_dict, threshold):
    for name, coords_list in pois_dict.items():
        if is_near_poi(lat, lon, coords_list, threshold):
            return name
    return None

def normalize_columns(df):
    df.columns = [
        str(c).strip().upper()
        .replace('Ã', 'A').replace('Ç', 'C').replace('Ó', 'O').replace('Í', 'I').replace('É', 'E')
        for c in df.columns
    ]
    
    mapa = {
        'DATA': 'DATA/HORA', 'DATA/HORA POSICAO': 'DATA/HORA', 'DATAHORA': 'DATA/HORA', 'DHR': 'DATA/HORA',
        'LAT': 'LATITUDE', 'LON': 'LONGITUDE', 'VELOCIDADE': 'KM/H', 'VEL': 'KM/H',
        'IGNICAO': 'IGNIÇÃO', 'IGN': 'IGNIÇÃO', 'HODOMETRO': 'HODÔMETRO', 'HORIMETRO': 'HORÍMETRO',
        'KM': 'HODÔMETRO', 
        'ENDERECO': 'RUA', 'LOCALIZACAO': 'RUA', 'POSICAO': 'RUA', 'MUNICIPIO': 'CIDADE'
    }
    df.rename(columns=mapa, inplace=True)
    
    if 'DATA' in df.columns and 'HORA' in df.columns and 'DATA/HORA' not in df.columns:
        try: df['DATA/HORA'] = df['DATA'].astype(str) + ' ' + df['HORA'].astype(str)
        except: pass
    return df

def load_data_universal(uploaded_file):
    try:
        header_idx = 0
        file_ext = uploaded_file.name.lower()
        
        if file_ext.endswith(('.xlsx', '.xls')):
            try:
                df_temp = pd.read_excel(uploaded_file, header=None, nrows=50)
                for i, row in df_temp.iterrows():
                    line = " ".join([str(x).upper() for x in row.values])
                    if ("LAT" in line and "LON" in line) or ("LAT" in line and "DATA" in line): 
                        header_idx = i; break
                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file, skiprows=header_idx)
            except: return None
        else:
            uploaded_file.seek(0)
            try:
                content = uploaded_file.read(10000).decode('latin1', errors='ignore')
                uploaded_file.seek(0)
                lines = content.split('\n')
                for i, line in enumerate(lines[:50]):
                    l_up = line.upper()
                    if ("LAT" in l_up and "DATA" in l_up) or ("LAT" in l_up and "VEL" in l_up):
                        header_idx = i
                        break
                
                df = pd.read_csv(uploaded_file, sep=';', decimal=',', encoding='latin1', skiprows=header_idx, on_bad_lines='skip')
                if len(df.columns) < 4:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep=',', decimal='.', encoding='utf-8', skiprows=header_idx, on_bad_lines='skip')
            except: return None

        df = normalize_columns(df)
        df['DATA/HORA'] = pd.to_datetime(df['DATA/HORA'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['DATA/HORA']).sort_values('DATA/HORA').reset_index(drop=True)
        
        def clean_float(val):
            if isinstance(val, str): return float(val.replace(',', '.'))
            return float(val)

        for col in ['LATITUDE', 'LONGITUDE', 'KM/H', 'HODÔMETRO']:
            if col in df.columns:
                if df[col].dtype == object: df[col] = df[col].apply(clean_float)
                else: df[col] = pd.to_numeric(df[col], errors='coerce')
        
        if 'CIDADE' in df.columns:
            df['CIDADE'] = df['CIDADE'].astype(str).str.encode('ascii', 'ignore').str.decode('utf-8').str.title()

        return df
    except Exception as e:
        st.error(f"Erro leitura: {e}"); return None

def process_routes(df, raio_base, raio_points, placa, pois_dict, base_name, nome_op):
    viagens = []
    em_viagem = False
    viagem_atual = {}
    
    coords_base = pois_dict.get(base_name, [])
    if not coords_base: coords_base = [(df.iloc[0]['LATITUDE'], df.iloc[0]['LONGITUDE'])]

    ultimo_hodo_base = 0
    ultima_data_base = df.iloc[0]['DATA/HORA']
    
    lat_ini, lon_ini = df.iloc[0]['LATITUDE'], df.iloc[0]['LONGITUDE']
    if is_near_poi(lat_ini, lon_ini, coords_base, raio_base):
        ultimo_hodo_base = df.iloc[0]['HODÔMETRO'] if 'HODÔMETRO' in df.columns else 0
    else:
        em_viagem = True
        hodo = df.iloc[0]['HODÔMETRO'] if 'HODÔMETRO' in df.columns else 0
        viagem_atual = {
            'id': df.iloc[0]['DATA/HORA'].strftime('%Y%m%d%H%M'),
            'placa': placa, 'inicio': df.iloc[0]['DATA/HORA'],
            'hodo_inicial': hodo,
            'rota_seq': ["Início Externo"], 'last_poi': "Início Externo",
            'coords': [], 'dados': []
        }

    for idx, row in df.iterrows():
        lat, lon = row['LATITUDE'], row['LONGITUDE']
        if pd.isna(lat) or lat == 0: continue

        perto_base = is_near_poi(lat, lon, coords_base, raio_base)
        
        if perto_base:
            val_hodo = row['HODÔMETRO'] if 'HODÔMETRO' in df.columns else 0
            if val_hodo > 0: ultimo_hodo_base = val_hodo
            ultima_data_base = row['DATA/HORA']

        if not em_viagem and not perto_base:
            em_viagem = True
            start_hodo = ultimo_hodo_base if ultimo_hodo_base > 0 else (row['HODÔMETRO'] if 'HODÔMETRO' in df.columns else 0)
            viagem_atual = {
                'id': row['DATA/HORA'].strftime('%Y%m%d%H%M'),
                'placa': placa, 'inicio': ultima_data_base,
                'hodo_inicial': start_hodo,
                'rota_seq': [base_name], 'last_poi': base_name,
                'coords': [], 'dados': []
            }
        
        if em_viagem:
            viagem_atual['coords'].append([lat, lon])
            viagem_atual['dados'].append(row)
            
            poi = get_current_poi_name(lat, lon, pois_dict, raio_points)
            
            # Lógica para Ipiguá (sem POIs fixos, apenas Cidades)
            if not poi and "Ipiguá" in base_name:
                if row['KM/H'] == 0 and 'CIDADE' in df.columns and pd.notna(row['CIDADE']):
                    c_raw = str(row['CIDADE']).strip().title()
                    if "IPIGUA" not in c_raw.upper(): poi = c_raw

            if poi and poi != base_name and poi != viagem_atual['last_poi']:
                viagem_atual['rota_seq'].append(poi)
                viagem_atual['last_poi'] = poi

            if perto_base and len(viagem_atual['rota_seq']) > 0:
                delta_min = (row['DATA/HORA'] - viagem_atual['inicio']).total_seconds()/60
                if delta_min > 15 or "Início Externo" in viagem_atual['rota_seq']:
                    
                    viagem_atual['fim'] = row['DATA/HORA']
                    viagem_atual['rota_seq'].append(base_name)
                    
                    hodo_final = row['HODÔMETRO'] if 'HODÔMETRO' in df.columns else 0
                    dist = abs(hodo_final - viagem_atual['hodo_inicial'])
                    duracao_segundos = (viagem_atual['fim'] - viagem_atual['inicio']).total_seconds()
                    duracao_fmt = format_seconds_to_hms(duracao_segundos)
                    duracao_hours = duracao_segundos / 3600
                    
                    df_v = pd.DataFrame(viagem_atual['dados'])
                    
                    vel_media_mov = 0
                    if not df_v.empty and 'KM/H' in df_v.columns:
                        velocidades_validas = df_v[df_v['KM/H'] > 50]['KM/H']
                        if not velocidades_validas.empty:
                            vel_media_mov = velocidades_validas.mean()
                    
                    tempo_idle, local_crit, tempo_local = 0, "-", 0
                    if not df_v.empty and 'IGNIÇÃO' in df_v.columns:
                        ign = df_v['IGNIÇÃO'].astype(str).str.upper()
                        mask = ign.isin(['SIM','ON','LIGADO','1','TRUE']) & (df_v['KM/H'] == 0)
                        df_idle = df_v[mask].copy()
                        if len(df_v)>1:
                            delta_t = df_v['DATA/HORA'].diff().mean().total_seconds()/60
                            if delta_t <=0 or math.isnan(delta_t): delta_t=0.5
                            tempo_idle = len(df_idle)*delta_t
                            if not df_idle.empty:
                                df_idle['POI'] = df_idle.apply(lambda r: get_current_poi_name(r['LATITUDE'], r['LONGITUDE'], pois_dict, raio_points), axis=1)
                                if "Ipiguá" in base_name and 'CIDADE' in df_idle.columns:
                                    df_idle['POI'] = df_idle['POI'].fillna(df_idle['CIDADE'])
                                
                                df_idle['L'] = df_idle['POI'].fillna("Via")
                                ct = df_idle['L'].value_counts()
                                if not ct.empty: local_crit, tempo_local = ct.idxmax(), ct.max()*delta_t

                    # CIDADE PRINCIPAL & ROTA LIMPA (PASSOS)
                    cidade_destino_principal = "-"
                    
                    # Limpa a lista de rota para remover cidades se for operação Passos
                    rota_limpa = []
                    for ponto in viagem_atual['rota_seq']:
                        if nome_op == "Passos (Frango)":
                            # Só adiciona se for a Base ou estiver na lista de POIs conhecidos (Granjas)
                            if ponto == base_name or ponto in POIS_PASSOS:
                                rota_limpa.append(ponto)
                        else:
                            rota_limpa.append(ponto)
                    
                    rota_display = " > ".join(rota_limpa)

                    # Busca Cidade Principal (Baseada no mapa)
                    if 'CIDADE' in df_v.columns:
                        # Prioridade: Cidade do Local Crítico (Ociosidade)
                        if local_crit in MAPA_CIDADES_PASSOS:
                            cidade_destino_principal = MAPA_CIDADES_PASSOS[local_crit]
                        
                        # Fallback: Cidade onde ficou mais tempo parado no geral
                        if cidade_destino_principal == "-":
                            stops = df_v[df_v['KM/H'] == 0].copy()
                            if not stops.empty:
                                stops['C_NORM'] = stops['CIDADE'].astype(str).str.strip().str.upper()
                                ex = ["-", "NAN"] + base_name.upper().split()
                                cts = stops['C_NORM'].value_counts()
                                for c, _ in cts.items():
                                    if not any(x in c for x in ex):
                                        cidade_destino_principal = stops[stops['C_NORM']==c]['CIDADE'].iloc[0].title()
                                        break
                    
                    # Se for Passos e tiver só Base > Base, tenta inserir a fazenda se detectada
                    if nome_op == "Passos (Frango)":
                        # Se a rota ficou "JBS > JBS", mas tem um local critico (fazenda), insere ele
                        if len(rota_limpa) == 2 and local_crit in POIS_PASSOS:
                             rota_display = f"{base_name} > {local_crit} > {base_name}"
                             if cidade_destino_principal == "-":
                                 cidade_destino_principal = MAPA_CIDADES_PASSOS.get(local_crit, "-")

                    viagens.append({
                        'Operação': nome_op,
                        'Placa': placa, 
                        'ID Viagem': viagem_atual['id'],
                        'Data Início': viagem_atual['inicio'],
                        'Data Fim': viagem_atual['fim'],
                        'Tempo Total': duracao_fmt,
                        'Duração Horas': duracao_hours,
                        'Cidade Principal': cidade_destino_principal, 
                        'Rota': rota_display,
                        'Distância (km)': round(dist, 2),
                        'Vel. Média >50km/h': round(vel_media_mov, 1),
                        'Tempo Ocioso TOTAL (min)': round(tempo_idle, 1),
                        'Local Mais Ocioso': local_crit,
                        'Tempo Ocioso NO LOCAL (min)': round(tempo_local, 1),
                        'Coords': viagem_atual['coords']
                    })
                    em_viagem = False
    
    if em_viagem:
        dur = (df.iloc[-1]['DATA/HORA'] - viagem_atual['inicio']).total_seconds()
        viagens.append({
            'Operação': nome_op,
            'Placa': placa, 'ID Viagem': viagem_atual['id'],
            'Data Início': viagem_atual['inicio'], 'Data Fim': df.iloc[-1]['DATA/HORA'],
            'Tempo Total': format_seconds_to_hms(dur),
            'Duração Horas': dur/3600,
            'Cidade Principal': "-",
            'Rota': " > ".join(viagem_atual['rota_seq']),
            'Distância (km)': 0, 'Vel. Média >50km/h': 0,
            'Tempo Ocioso TOTAL (min)': 0, 'Local Mais Ocioso': "-", 'Tempo Ocioso NO LOCAL (min)': 0,
            'Coords': viagem_atual['coords']
        })
    return pd.DataFrame(viagens)

# --- INTERFACE ---

uploaded_file = st.file_uploader("Arraste relatórios (Qualquer formato)", type=['xlsx', 'xls', 'csv'])

if uploaded_file:
    if not placa_veiculo:
        st.warning("⚠️ Digite a PLACA.")
    else:
        raw_df = load_data_universal(uploaded_file)
        if raw_df is not None:
            df_final = process_routes(raw_df, raio_base, raio_poi, placa_veiculo, POIS_ATIVOS, NOME_BASE, operacao_selecionada)
            
            if df_final.empty:
                st.error(f"Nenhuma viagem detectada saindo de {NOME_BASE}.")
            else:
                st.success(f"Operação {operacao_selecionada}: {len(df_final)} viagens identificadas.")
                
                cols_display = ['Operação', 'Placa', 'ID Viagem', 'Data Início', 'Data Fim', 'Cidade Principal', 'Rota', 'Tempo Total', 'Distância (km)', 'Vel. Média >50km/h', 'Tempo Ocioso TOTAL (min)', 'Local Mais Ocioso', 'Tempo Ocioso NO LOCAL (min)']
                df_show = df_final.copy()
                df_show['Data Início'] = df_show['Data Início'].dt.strftime('%d/%m/%Y %H:%M:%S')
                df_show['Data Fim'] = df_show['Data Fim'].dt.strftime('%d/%m/%Y %H:%M:%S')

                tab1, tab2 = st.tabs(["Relatório", "Dashboard"])
                
                with tab1:
                    st.dataframe(df_show[cols_display].style.map(lambda x: 'background-color: #ffcccc' if x > min_idling_minutes else '', subset=['Tempo Ocioso TOTAL (min)', 'Tempo Ocioso NO LOCAL (min)']), width="stretch")
                    st.download_button("Baixar Excel", data=to_excel(df_show[cols_display]), file_name=f"Resumo_{placa_veiculo}.xlsx")
                    
                    st.markdown("---")
                    trip = st.selectbox("Ver no Mapa:", df_final['ID Viagem'].tolist(), format_func=lambda x: f"{x} | {df_final[df_final['ID Viagem']==x].iloc[0]['Rota']}")
                    if trip:
                        r = df_final[df_final['ID Viagem']==trip].iloc[0]
                        m = folium.Map(location=r['Coords'][len(r['Coords'])//2], zoom_start=9)
                        folium.PolyLine(r['Coords'], color="blue", weight=5).add_to(m)
                        for n, l in POIS_ATIVOS.items():
                            for lat, lon in l: folium.CircleMarker([lat, lon], radius=5, color="orange", popup=n, fill=True).add_to(m)
                        st_folium(m, width=1200, height=500)

                with tab2:
                    c1, c2 = st.columns(2)
                    with c1:
                        fig = px.bar(df_final, x='ID Viagem', y='Tempo Ocioso TOTAL (min)', title="Ociosidade", custom_data=['Rota', 'Local Mais Ocioso', 'Tempo Ocioso NO LOCAL (min)'])
                        fig.update_traces(hovertemplate="Rota: %{customdata[0]}<br>Total: %{y}<br>Local: %{customdata[1]} (%{customdata[2]} min)")
                        st.plotly_chart(fig, use_container_width=True)
                    with c2:
                        # GRÁFICO TEMPO MÉDIO
                        # Agrupa por Rota (limpa) ou Cidade Principal se disponível
                        df_final['Agrupador'] = df_final.apply(lambda x: x['Rota'] if x['Cidade Principal'] == "-" else x['Cidade Principal'], axis=1)
                        df_g = df_final.groupby('Agrupador')['Duração Horas'].mean().reset_index()
                        fig = px.bar(df_g, y='Agrupador', x='Duração Horas', orientation='h', title="Tempo Médio (h)", text_auto='.1f')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    c3, c4 = st.columns(2)
                    with c3:
                        fig = px.bar(df_final, x='ID Viagem', y='Distância (km)', title="KM Rodado", custom_data=['Rota'])
                        fig.update_traces(hovertemplate="Rota: %{customdata[0]}<br>KM: %{y}")
                        st.plotly_chart(fig, use_container_width=True)
                    with c4:
                        fig = px.scatter(df_final, x='Distância (km)', y='Duração Horas', size='Tempo Ocioso TOTAL (min)', title="Eficiência", custom_data=['Rota'])
                        fig.update_traces(hovertemplate="Rota: %{customdata[0]}")
                        st.plotly_chart(fig, use_container_width=True)
