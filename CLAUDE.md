# CLAUDE.md — Dashboard de Controle de Tráfego Pago (PARTIU EMPREENDER)

> Este arquivo é lido automaticamente pelo Claude Code ao abrir o repositório.
> Repositório **configurado para o cliente PARTIU EMPREENDER** (funil
> "Imersão do Zero ao Lucro", sigla de campanha `Imersão-SET26`). A engine
> (`build/template.html`, `build/build.py`, `ia-worker/worker.js`) é genérica
> e não deve ser editada por cliente; os valores do cliente ficam em
> **`build/config.py`** (config do funil) e **`config.js`** (metadados de
> publicação no GitHub). Veja também `README.md` para a visão geral e o passo
> a passo completo de publicação.

---

## ✅ CHECKLIST DE NOVO CLIENTE — status

1. [x] **Config do cliente** — `build/config.py` preenchido (ver "Fontes de
   dados" abaixo para como cada valor foi obtido/confirmado).
2. [x] **Este arquivo (`CLAUDE.md`)** — preenchido.
3. [x] **`README.md`** — preenchido.
4. [x] **`config.js`** — preenchido (`GITHUB_USERNAME=scale-ag`,
   `GITHUB_REPOSITORY=dash-partiu-imersao-set26`).
5. [ ] **`SETUP-CRON.md`** — placeholders já substituídos pelos valores reais;
   falta **você gerar o token fine-grained** e cadastrar no cron-job.org (nunca
   commitar o token) — ver `SETUP-CRON.md`.
6. [x] **GitHub Pages** — workflow `.github/workflows/deploy.yml` na branch
   `main`; Pages tenta se autoconfigurar na 1ª execução (`configure-pages`
   com `enablement: true`). Se o token do Actions não tiver permissão de
   administração do repo, o passo falha e o Pages precisa ser ligado uma vez
   na mão em **Settings → Pages → Source: GitHub Actions** (ver `SETUP-CRON.md`
   Passo 1) — confira o status do primeiro build antes de assumir que já
   está publicado.
7. [ ] **Worker da IA Insights** — **NÃO configurado nesta rodada** (exige
   conta Cloudflare + chave Anthropic do cliente, fora do escopo pedido).
   `ia-worker/wrangler.toml` já tem o nome reservado
   (`partiu-empreender-ia-insights`); falta criar o Worker de fato. Passo a
   passo completo em `SETUP-IA.md`.
8. [ ] **4 Secrets do repositório no GitHub** (`CLOUDFLARE_API_TOKEN`,
   `CLOUDFLARE_ACCOUNT_ID`, `ANTHROPIC_API_KEY`, `INSIGHTS_PASSWORD`) —
   pendentes, junto com o item 7.
9. [ ] **Disparar o primeiro deploy do Worker** — pendente (depende do item 7).
10. [ ] **Embutir a URL do Worker no build** (`IA_WORKER_URL` em
    `build/config.py`) — pendente.
11. [ ] **Testar a aba IA Insights** — pendente.

O dashboard principal (abas Visão Geral, Meta Ads, Relatórios) funciona
normalmente sem os itens 7-11; só a aba **IA Insights** fica indisponível até
esses passos serem concluídos por quem tiver acesso à conta Cloudflare/Anthropic
do cliente.

---

## O que é

Dashboard de **Controle de Tráfego Pago** — app de BI estático (HTML/CSS/JS + Chart.js
via CDN) publicado no **GitHub Pages**, que cruza o gerenciador **Meta Ads** com a lista
de **Compradores** e se atualiza a cada ~30 min (build na nuvem via GitHub Actions,
disparado pelo cron-job.org). **Somente leitura** das planilhas.

- **URL pública:** `https://scale-ag.github.io/dash-partiu-imersao-set26/`
- **Cliente/projeto:** PARTIU EMPREENDER — "Imersão do Zero ao Lucro" (edição SET26)
- **Tipo de funil:** VSL / lançamento pago, tráfego direto (não há etapa de Leads/MQL,
  nenhuma coluna nos dados sugere uma) —
  `Gasto → Impressões → Cliques → Page Views → Checkouts → Vendas → Faturamento`

## Fontes de dados (Google Sheets)

Este cliente usa **duas planilhas separadas** (o template padrão assume uma só,
com dois gids). Por isso `build/config.py` tem `SPREADSHEET_ID_SALES` além de
`SPREADSHEET_ID`. Leitura via export CSV, **somente leitura**.

| Fonte | Planilha (`SPREADSHEET_ID*`) | gid | Aba |
|-------|------------------------------|-----|-----|
| **Meta Ads** | `1mXaJWC2Eecu7eSwQ8UkamO_sLCIuZCtI5u7tA0YRYFU` | `0` | 1ª aba (9 colunas) |
| **Compradores** | `1Qe1_LFcrd98hhOTa5rJAL78ZRUoHCZ-Pj4kIRgdiljI` | `1083963375` | **"Imersao 0 ao Lucro 4"** (12 colunas úteis) |

⚠️ O gid `1083963375` da aba de Compradores **não é o gid=0** dessa planilha —
foi obtido buscando a aba pelo nome exato ("Imersao 0 ao Lucro 4", como
informado) e depois confirmado batendo os 57 registros retornados contra o
gid numérico via `export?format=csv&gid=1083963375`. Se a planilha ganhar
outras abas no futuro, confira o gid antes de assumir que é a mesma.

**Colunas reais — Meta Ads** (já no formato padrão esperado pela engine, sem
precisar de alias novo):
`Day · Campaign Name · Ad Set Name · Ad Name · Amount Spent · Impressions ·
Link Clicks · Landing Page Views · Checkouts Initiated`

126 linhas (18/09/2026), 4 campanhas únicas, 8 anúncios únicos (`AD01` a `AD08`).

**Colunas reais — Compradores** (aba "Imersao 0 ao Lucro 4", 12 colunas úteis
+ ~15 colunas de cabeçalho vazio no fim da planilha, ignoradas pelo build):
`Data · Nome · Email · Valor da Compra · Forma de Pagto · Utm_source ·
utm_campaign · utm_medium · utm_content · Utm_term · Origem de Checkout ·
DATA (UTC -3)`

57 linhas (18/09/2026), R$ 3.592,99 somados em "Valor da Compra" (ticket
médio R$ 63,03; valores observados entre R$ 49 e R$ 69 — parecem ser lotes/
ofertas diferentes do ingresso, não um valor fixo).

### Pontos de atenção deste cliente (verificados na planilha em 18/09/2026)

1. **Sem coluna de Produto.** A aba de Compradores já vem filtrada para um
   único produto (a própria "Imersao 0 ao Lucro 4") — não existe coluna
   `PRODUTO`/`Produto` na planilha. Isso muda o comportamento padrão da
   engine em dois pontos:
   - **Funcional (corrigido em config):** `header_index()` (`build/build.py`)
     tem um *fallback posicional* para a chave `"prod"` que aponta pro índice
     `0` quando nenhuma coluna nomeada "produto"/"product" é encontrada — nesta
     planilha o índice `0` é a coluna `Data`, então sem ajuste toda venda
     entraria como "produto não-principal" (`main=0`) e a métrica **Vendas**
     (base de CAC/ConvCHK/Ticket) ficaria zerada, mesmo com Faturamento/ROAS
     corretos. Corrigido setando `MAIN_PRODUCT_PREFIX = ""` em
     `build/config.py`: como `str.startswith("")` é sempre `True`, toda linha
     passa a contar como produto principal — correto aqui, já que 100% da
     planilha É o produto principal.
   - **Cosmético (não corrigido, documentado):** a coluna "Produto" exibida na
     tabela de compradores (aba Meta Ads) vai mostrar o valor da coluna `Data`
     (efeito do mesmo fallback posicional) em vez de ficar em branco ou
     mostrar o nome do produto. Não afeta nenhum KPI/gráfico, só a coluna
     "Produto" dessa tabela específica. Se isso incomodar, a única forma de
     corrigir de verdade é a planilha ganhar uma coluna `Produto` (mesmo que
     com o mesmo valor em todas as linhas) — não editar `build/build.py` por
     cliente.
2. **Sem coluna de status de pagamento** → `COUNT_ALL_AS_PAID = True` (toda
   linha da aba "Imersao 0 ao Lucro 4" é uma compra confirmada).
3. **`AD_UTM_COLUMN = "utm_content"` — confirmado nos dados**, não assumido.
   Cruzando cada coluna UTM contra os 8 `Ad Name`/4 `Campaign Name` reais do
   Meta (55 vendas com UTM preenchida):

   | coluna UTM | preenchidas | match Campaign Name | match Ad Name |
   |---|---|---|---|
   | `Utm_source` | 56 | 0 | 0 |
   | `utm_campaign` | 55 | **55** | 0 |
   | `utm_medium` | 55 | 0 | 0 |
   | `utm_content` | 55 | 0 | **55** |
   | `Utm_term` | 55 | 0 | 0 |

   `utm_content` bate 100% com `Ad Name` → é o padrão do template, mas foi
   verificado nos dados reais deste cliente, não assumido por convenção.
   `Utm_term` carrega o **posicionamento** (`Instagram_Feed`, `Instagram_Reels`,
   `Instagram_Stories`, `Facebook_Stories`) — não usar para atribuição.
   `utm_medium` carrega o agrupamento de conjunto (ex.: `AUTO - ALL - 18a65 -
   BR - Mix Quente | AD1 ao AD4`), coerente com `Ad Set Name`, mas o match
   exato não foi conferido (não é necessário — a engine usa
   campanha+`AD_UTM_COLUMN` para atribuição, não `utm_medium`).
   Mapeamento: `utm_campaign → Campaign Name` · `utm_medium → Ad Set Name` ·
   `utm_content → Ad Name`.
4. **Sem coluna de permalink do criativo** na aba Meta Ads → o Top/Piores
   anúncios da aba Relatórios aparece **sem link** para o criativo. Para
   ativar, acrescente a coluna `Creative Instagram Permalink` na planilha do
   Meta.
5. **Sem coluna de MQL/Leads.** Nem a planilha de Meta Ads nem a de
   Compradores têm qualquer coluna relacionada a qualificação de lead — o
   funil é tráfego pago direto para a oferta, sem etapa de MQL nesta
   dashboard (igual ao padrão do template para funis VSL).

### Sigla do funil / convenção de campanha

Todas as 4 campanhas encontradas no Meta Ads compartilham o mesmo prefixo —
**sigla do funil = `Imersão-SET26`** (única sigla nos dados, não havia
ambiguidade a esclarecer):
- `Imersão-SET26 | E2-CAP | P2-QUENTE | CONV | ABO | V1 | 2026-09-03 | Teste de Criativos 2`
- `Imersão-SET26 | E2-CAP | P2-QUENTE | CONV | CBO | V1 | 2026-09-01 | Teste de Criativos`
- `Imersão-SET26 | E2-CAP | P2-QUENTE | CONV | CBO | V2 | 2026-09-09 | Teste de Paginas`
- `Imersão-SET26 | E2-CAP | P3-FRIO | CONV | CBO | V1 | 2026-09-04 | Advantage`

Anúncios no padrão `AD0X_V_ST_Captação_Imersão-SET26` (vídeo/Stories) e
`AD0X_E_Feed_Captação_Imersão-SET26` (estático/Feed), `X` de 01 a 08.

### Critério de MQL

Não há etapa de MQL/Leads nesta dashboard — nenhuma coluna nas planilhas reais
sugere qualificação de lead (ver "Pontos de atenção" #5). Funil é tráfego pago
direto para a oferta (VSL/lançamento), sem etapa intermediária.

URL de export CSV: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID}`

### Métricas do funil (`build.py` + `template.html`)
`Gasto → Impressões → Cliques → Page Views → Checkouts → Vendas → Faturamento`

Gasto · Impressões · CPM · Cliques · CPC · CTR · Page Views · CPV · CR (Cliques/PageViews) ·
Checkouts · CPIC · VisCHK (Checkouts/PageViews) · Vendas · CAC (Gasto/Vendas) ·
ConvCHK (Vendas/Checkouts) · Faturamento · ROAS (Faturamento/Gasto) · Ticket (Faturamento/Vendas).

### Produto principal / atribuição
- **Produto principal** = `MAIN_PRODUCT_PREFIX = ""` (definido em `build/config.py`) —
  vazio porque a planilha de Compradores já é uma lista de um único produto,
  sem coluna `Produto` (ver "Pontos de atenção" #1). Base de
  **Vendas / CAC / ConvCHK / Ticket**.
- **Faturamento / ROAS** = soma de **todos os produtos** do funil (orderbumps/upsells,
  se houver — não identificados nos dados atuais).
- Uma venda entra no funil se: é o produto principal **OU** a combinação **`UTM Campaign`
  + `UTM Content`** (campanha + anúncio) casa com uma linha real do Meta. Como
  `MAIN_PRODUCT_PREFIX` é vazio, TODAS as 57 linhas já entram por serem "produto
  principal"; o match campanha+anúncio com o Meta (campo `meta`, usado pela aba
  Meta Ads) ainda é o que decide se a venda aparece **atribuída ao tráfego pago**
  (a maioria das 57 — 55 tinham UTM preenchida e batem 100% com o Meta) ou como
  venda "sem match" (2 linhas sem UTM preenchida, tráfego orgânico/direto). Só
  conta status pago (aqui, sempre — ver `COUNT_ALL_AS_PAID`).

### Imposto Meta Ads
Toggle ON aplica o `TAX_FACTOR` (definido em `build/config.py`). Nenhum imposto
foi informado para este cliente — `TAX_FACTOR = 1.0` (sem efeito). Ajuste se o
gestor confirmar um imposto sobre o gasto do Meta.

## IA Insights

**Não configurada nesta rodada** — fora do escopo pedido (exige conta
Cloudflare + chave Anthropic do cliente, que o agente não tem acesso). Ver
checklist itens 7-11 acima e `SETUP-IA.md` para o passo a passo completo
quando alguém com essas credenciais for configurar.

## Arquitetura / arquivos

A dashboard é montada a partir de **arquivos separados** (visual x lógica), costurados
pelo `build.py` no `render()`:

```
build/build.py             # ENGINE: lê os 2 CSVs (read-only), emite meta[]/sales[] e COSTURA os arquivos abaixo
build/config.py            # CONFIG DO CLIENTE (este arquivo, já preenchido)
build/config.example.py    # modelo comentado de build/config.py
build/template.html        # esqueleto HTML (placeholders __STYLES__ / __APP_JS__ / __DATA_JSON__)
build/identidade-visual.css # cores (temas claro/escuro, paleta de gráficos, heatmap)
build/estilos.css          # layout/componentes (CSS não-cor)
build/app.js               # lógica + renderização (gráficos/heatmap leem as cores via CSS vars)
.github/workflows/deploy.yml         # roda build.py e publica no Pages
.github/workflows/deploy-worker.yml  # publica o Worker da IA Insights (Cloudflare)
.github/workflows/gerar-relatorios-metrics.yml # busca as planilhas e commita relatorios_metrics.json
ia-worker/worker.js    # backend da aba IA Insights (ENGINE — não editar por cliente)
ia-worker/wrangler.toml # nome do Worker: partiu-empreender-ia-insights
build/relatorios.json  # briefings do Gestor por período (aba Relatórios) — ainda não existe (gerado pela Routine)
build/relatorios_metrics.json # números por período (gerado pelo Actions) — ainda não existe
build/gerar_relatorios.py # calcula as métricas por período (rodado pelo Actions)
build/GUIA-RELATORIOS.md  # passo a passo da Routine que regenera os briefings
dist/index.html        # saída gerada (gitignored; o Actions reconstrói)
GUIA-REPLICACAO.md     # engine explicada + solução dos problemas de publicação
config.js               # metadados de publicação (GitHub) — já preenchido
SETUP-CRON.md          # valores do cron-job.org (já com owner/repo reais)
SETUP-IA.md            # passo a passo da aba IA Insights (pendente para este cliente)
```

### Aba Relatórios (relatórios automáticos do funil)
Funciona com os filtros de data da topbar e os dados já embutidos
(`meta[]`/`sales[]`) — tudo calculado no navegador. O **Briefing do Gestor**
(texto interpretativo por período, gerado por IA) depende de
`build/relatorios.json`, que **ainda não existe** para este cliente — a aba
mostra os cards/tabelas normalmente, só sem o briefing, até alguém configurar
a Routine diária descrita em `build/GUIA-RELATORIOS.md` (não vem pronta neste
template, precisa ser configurada por cliente).

O `build.py` **não agrega**: exporta as linhas cruas e toda a lógica (filtros, KPIs,
tabelas, gráficos, heatmap, imposto, tema) roda no navegador.

Teste local:
`python build/build.py --meta-file meta.csv --sales-file sales.csv --out dist/index.html`

## Publicação — problemas conhecidos e soluções

1. **Push com integração somente‑leitura:** se `git push`/MCP derem `403 Resource not
   accessible by integration`, faça push com o **PAT do usuário** direto ao github.com
   (`git push https://x-access-token:<TOKEN>@github.com/<owner>/<repo>.git main:main`).
   **Nunca** grave o token no `.git/config` (use a URL efêmera).
2. **cron-job.org só funciona na `main`:** `workflow_dispatch` só existe na branch padrão.
3. **Pages não liga sozinho por padrão:** o `GITHUB_TOKEN` do Actions costuma não
   ter permissão de administração do repo para *criar* o site do Pages — precisa
   ligar uma vez na mão em Settings → Pages (ver `SETUP-CRON.md` Passo 1).
4. **Proxy do sandbox:** o agente NÃO alcança `docs.google.com`, `*.github.io` nem a API
   REST de Actions/Pages e nem `api.cloudflare.com` — mas o runner do Actions alcança
   tudo. Os gids/colunas reais deste cliente (acima) foram descobertos rodando um
   workflow de diagnóstico temporário no Actions (removido depois de confirmado).
5. **Token exposto no chat:** revogar e gerar um novo (fine‑grained, só Actions: r/w no repo).
6. **Criação de repositório via API:** o GitHub App usado pelo agente **não tem**
   permissão de "Administration" na org `scale-ag` — não é possível criar
   repositórios novos via API com o token atual (`403 Resource not accessible
   by integration`). Este repositório foi criado manualmente pelo usuário.
7. **"A dash trava" / "não atualiza":** o build roda a cada 30 min e publica normalmente
   — confira em Actions antes de suspeitar do pipeline. A página **não recarrega
   sozinha**; ela mostra um aviso "Novos dados publicados · Atualizar agora" e
   compara `<meta name="build">` (com `cache:'no-store'`) para evitar cache
   desatualizado. Rodapé do menu lateral (`build ...`) mostra o build atual.
8. **Venda não aparece na aba Meta Ads (ou aparece na campanha errada):** confirme
   qual coluna UTM carrega o `Ad Name` real do Meta e ajuste `AD_UTM_COLUMN` —
   **não assuma pela convenção**, confira contando quantos valores de cada
   coluna UTM batem exatamente com o `Ad Name`/`Campaign Name` reais do Meta
   (processo documentado em "Pontos de atenção" #3 acima). O match usa
   campanha+anúncio juntos, nunca só o nome do anúncio (nomes como `AD01` podem
   se repetir entre campanhas).
