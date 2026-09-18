# -*- coding: utf-8 -*-
"""
Configuração do cliente — PARTIU EMPREENDER / Imersão do Zero ao Lucro (SET26).

Este é o ÚNICO arquivo que precisa ser editado para ajustar o funil deste
cliente. Depois de editar, teste localmente:

    python build/build.py --meta-file meta.csv --sales-file sales.csv --out dist/index.html

`build/config.example.py` é a cópia intacta do modelo, para consulta.
"""
from __future__ import annotations

# ==========================================================================
# 1) PLANILHAS DO CLIENTE (Google Sheets)
# ==========================================================================
# Este cliente usa DUAS planilhas separadas (o template padrão assume uma só,
# com dois gids). SPREADSHEET_ID_SALES cobre esse caso.
#
# Meta Ads:     https://docs.google.com/spreadsheets/d/1mXaJWC2Eecu7eSwQ8UkamO_sLCIuZCtI5u7tA0YRYFU/
# Compradores:  https://docs.google.com/spreadsheets/d/1Qe1_LFcrd98hhOTa5rJAL78ZRUoHCZ-Pj4kIRgdiljI/
#               (aba "Imersao 0 ao Lucro 4", gid=1083963375 — NÃO é a gid=0
#               dessa planilha; confirmado buscando a aba pelo nome e batendo
#               os 57 registros contra o gid numérico)
# Ambas lidas via export CSV público — SOMENTE LEITURA, o build nunca escreve.
SPREADSHEET_ID = "1mXaJWC2Eecu7eSwQ8UkamO_sLCIuZCtI5u7tA0YRYFU"
SPREADSHEET_ID_SALES = "1Qe1_LFcrd98hhOTa5rJAL78ZRUoHCZ-Pj4kIRgdiljI"
GID_META = "0"                # aba Meta Ads (9 colunas)
GID_SALES = "1083963375"      # aba "Imersao 0 ao Lucro 4" (12 colunas úteis)

# ==========================================================================
# 2) REGRAS DE NEGÓCIO
# ==========================================================================
# Fator de imposto sobre o gasto do Meta Ads (toggle "Imposto Meta" na topbar).
TAX_FACTOR = 1.13806   # +13,806%

# Produto principal do funil. O match é por PREFIXO sobre o nome NORMALIZADO
# (sem acento, minúsculas) da coluna PRODUTO — por isso o valor abaixo também
# precisa estar sem acento e em minúsculas.
#
# Esta planilha de Compradores (aba "Imersao 0 ao Lucro 4") NÃO TEM coluna de
# produto — é uma lista já filtrada para um único produto (a própria edição 4
# da Imersão). Prefixo vazio ("") casa com QUALQUER string via
# str.startswith(""), então is_main_product() sempre retorna True aqui, que é
# o comportamento certo (100% das linhas são o produto principal). Ver
# CLAUDE.md ("Pontos de atenção") para o efeito colateral cosmético disso.
MAIN_PRODUCT_PREFIX = ""

# Coluna UTM que carrega o Ad Name do Meta. CONFIRMADO nos dados (55 vendas
# com UTM, 8 Ad Name distintos no Meta): utm_content bate 55/55 com Ad Name;
# utm_campaign bate 55/55 com Campaign Name; Utm_term carrega o POSICIONAMENTO
# (Instagram_Feed/Stories/Reels, Facebook_Stories), não o anúncio.
#   utm_campaign -> Campaign Name  ·  utm_medium -> Ad Set Name  ·  utm_content -> Ad Name
AD_UTM_COLUMN = "utm_content"

# A aba de Compradores não tem coluna de status de pagamento — toda linha já
# é uma compra confirmada. Por isso True.
COUNT_ALL_AS_PAID = True

# ==========================================================================
# 3) RÓTULOS EXIBIDOS NA INTERFACE
# ==========================================================================
CLIENT_NAME = "PARTIU EMPREENDER"
CLIENT_SUB = "IMERSÃO DO ZERO AO LUCRO - SETEMBRO 2026"
TAX_LABEL = "Imposto Meta ×1,13806"
MAIN_PRODUCT = "Imersão do Zero ao Lucro"

# ==========================================================================
# 4) METAS (aba Relatórios) — código de cor de CAC/ROAS
# ==========================================================================
#   • ROAS: quanto MAIOR, melhor  -> desempenho = roas / ROAS_TARGET
#   • CAC : quanto MENOR, melhor  -> desempenho = CAC_TARGET / cac
# Faixas: <REPORT_BAND_LOW vermelho · até 0,99 amarelo · até REPORT_BAND_HIGH
# verde · acima disso azul-ciano.
#
# PROVISÓRIO — alinhar com o gestor. ROAS_TARGET = 1,00 (break-even) foi
# passado explicitamente; CAC_TARGET não foi informado, então foi calculado
# para ficar coerente com ROAS_TARGET = 1,00 (ROAS 1,00 <=> CAC = ticket
# médio): ticket médio real da aba Compradores em 18/09/2026 (57 compras,
# R$ 3.592,99 somados) = R$ 63,03.
CAC_TARGET = 63.03
ROAS_TARGET = 1.00
REPORT_BAND_LOW = 0.70
REPORT_BAND_HIGH = 1.30

# ==========================================================================
# 5) IA INSIGHTS (Cloudflare Worker) — ver SETUP-IA.md
# ==========================================================================
# Vazio = aba IA Insights indisponível. Preencher depois de publicar o Worker
# (passos 7-10 do checklist em CLAUDE.md) — fora do escopo desta configuração
# inicial (exige conta Cloudflare + chave Anthropic do cliente).
IA_WORKER_URL = ""
