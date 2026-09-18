# Dashboard de Controle de Tráfego Pago — PARTIU EMPREENDER / Imersão do Zero ao Lucro

> Repositório **já configurado** para o cliente PARTIU EMPREENDER (funil
> "Imersão do Zero ao Lucro", sigla de campanha `Imersão-SET26`).
> Os valores do cliente ficam em `build/config.py`; a engine
> (`build/build.py`, `build/template.html`, `ia-worker/worker.js`) continua
> genérica. Publicado em https://scale-ag.github.io/dash-partiu-imersao-set26/

## Visão geral

Dashboard de BI estática (HTML/CSS/JS + Chart.js via CDN) publicada no **GitHub
Pages**, que cruza o gerenciador **Meta Ads** com a lista de **Compradores**
(neste cliente, **duas planilhas Google Sheets separadas**) e se atualiza sozinha a cada ~30 min
(build na nuvem via GitHub Actions, disparado pelo cron-job.org). **Somente
leitura** das planilhas — o dashboard nunca escreve nelas.

Funil coberto: **lançamento pago / tráfego direto** (sem etapa de Leads/MQL) —
`Gasto → Impressões → Cliques → Page Views → Checkouts → Vendas → Faturamento`.
Produto principal: **Imersão do Zero ao Lucro** (edição de setembro/2026).

Como funciona, por dentro:

1. `build/build.py` lê 2 abas da planilha (Meta Ads + Compradores) via export CSV
   público e emite os registros brutos dentro do HTML final.
2. Toda a lógica (KPIs, filtros, gráficos, heatmap, imposto, tema) roda **no
   navegador** (`build/template.html` + `build/app.js`) — o Python não agrega nada,
   só emite as linhas cruas. Isso garante que KPIs, gráficos e tabelas nunca
   divergem entre si.
3. Um commit na `main` dispara o GitHub Actions, que builda e publica no Pages.
4. O `cron-job.org` chama o mesmo workflow a cada 30 min, então o dashboard fica
   sempre atualizado mesmo sem ninguém commitar nada (ver `SETUP-CRON.md`).
5. Uma aba opcional de **IA Insights** manda o funil para um Cloudflare Worker que
   chama a Claude e devolve uma análise (ver `SETUP-IA.md`) — **ainda não
   configurada** para este cliente (ver CLAUDE.md, checklist itens 7-10).

Nenhuma dessas peças exige servidor próprio ou banco de dados — tudo roda em
serviços gratuitos (GitHub Pages, GitHub Actions, cron-job.org) mais,
opcionalmente, o Cloudflare Workers (também com camada gratuita) para a IA.

## Requisitos

- Uma conta no **GitHub** (para hospedar o repositório e publicar no Pages).
- Duas **planilhas Google Sheets** — Meta Ads e Compradores — com o
  compartilhamento em **"Qualquer pessoa com o link pode visualizar"** (o build
  lê via export CSV público, somente leitura; a planilha nunca é editada).
- **Python 3.10+** só se você quiser testar o build localmente antes de publicar
  (o GitHub Actions já roda o Python sozinho, você não precisa instalar nada
  para só publicar).
- Uma conta gratuita em **[cron-job.org](https://cron-job.org)** (dispara o
  build a cada 30 min).
- *Opcional* — para a aba **IA Insights**: conta na **Cloudflare** (Workers) e
  uma chave de API da **Anthropic** (`sk-ant-...`).

Teste local do build (não é obrigatório — o Actions builda sozinho):
```bash
python build/build.py --meta-file meta.csv --sales-file sales.csv --out dist/index.html
```
`meta.csv`/`sales.csv` são exports locais das abas, usados só para não depender
da internet durante o desenvolvimento. Sem `--meta-file`/`--sales-file`, o build
busca as planilhas reais via `SPREADSHEET_ID`/`GID_*` de `build/config.py`.

## Como ativar o GitHub Pages

O workflow `.github/workflows/deploy.yml` tenta habilitar o Pages **sozinho** na
primeira execução (`actions/configure-pages` com `enablement: true`), mas o
`GITHUB_TOKEN` do Actions normalmente não tem permissão de **administração do
repositório** para *criar* o site do Pages (falha com `Resource not accessible
by integration`). Se isso acontecer:

1. No repositório, vá em **Settings → Pages**.
2. Em **Build and deployment → Source**, selecione **"GitHub Actions"**.
3. Re-execute o workflow (aba **Actions** → **"Build & Deploy Dashboard"** →
   **Run workflow**, branch `main`).
4. Depois do primeiro deploy bem-sucedido, a URL pública aparece em **Settings
   → Pages** e é sempre `https://scale-ag.github.io/dash-partiu-imersao-set26/`.
5. Configure o cron-job.org para dar continuidade aos builds automáticos a cada
   30 min — passo a passo completo em **`SETUP-CRON.md`**.

## Como configurar a planilha/API (Google Sheets)

1. **Meta Ads** (`SPREADSHEET_ID`, gid `0`): colunas `Day · Campaign Name ·
   Ad Set Name · Ad Name · Amount Spent · Impressions · Link Clicks ·
   Landing Page Views · Checkouts Initiated`.
2. **Compradores** (`SPREADSHEET_ID_SALES`, aba **"Imersao 0 ao Lucro 4"**,
   gid `1083963375`): colunas `Data · Nome · Email · Valor da Compra ·
   Forma de Pagto · Utm_source · utm_campaign · utm_medium · utm_content ·
   Utm_term · Origem de Checkout · DATA (UTC -3)`.
3. Compartilhamento de ambas: **Arquivo → Compartilhar → Acesso geral →
   "Qualquer pessoa com o link"** → papel **"Leitor"**. O build só lê
   (`export?format=csv`), nunca escreve.
4. Detalhes de atribuição (qual coluna UTM carrega o Ad Name, por que
   `MAIN_PRODUCT_PREFIX` está vazio, etc.) estão documentados em **`CLAUDE.md`**
   → seção "Fontes de dados" e "Pontos de atenção".

## Como configurar o Cloudflare Worker (aba IA Insights — pendente)

A aba IA Insights **ainda não está configurada** para este cliente — sem ela,
a aba simplesmente fica indisponível (o resto do dashboard funciona normalmente).
Passo a passo completo em **`SETUP-IA.md`**; resumo dos itens pendentes no
checklist de `CLAUDE.md` (itens 7-10): criar o Worker na Cloudflare, cadastrar
os 4 *Secrets* no GitHub, e colar a URL do Worker em `IA_WORKER_URL`
(`build/config.py`).

## Métricas do funil VSL

Gasto · Impressões · **CPM** · Cliques · **CPC** · **CTR** · Page Views · **CPV** ·
**CR** (Cliques/Page Views) · Checkouts · **CPIC** · **VisCHK** (Checkouts/Page Views) ·
Vendas · **CAC** (Gasto/Vendas) · **ConvCHK** (Vendas/Checkouts) · Faturamento ·
**ROAS** (Faturamento/Gasto) · **Ticket Médio** (Faturamento/Vendas).

- **Produto principal** (base de Vendas / CAC / ConvCHK / Ticket): a aba de
  Compradores deste cliente não tem coluna de produto (é uma lista já filtrada
  para um único produto), então `MAIN_PRODUCT_PREFIX = ""` em `build/config.py`
  — casa com 100% das linhas, que é o comportamento correto aqui.
- **Faturamento / ROAS**: consideram **todos os produtos** do funil (orderbumps e
  upsells inclusos), atribuídos ao tráfego rastreado.
- **Imposto Meta**: toggle ON aplica o fator configurado em `TAX_FACTOR`
  (`build/config.py`) — `TAX_FACTOR = 1.13806` (+13,806%).

## O que a dashboard mostra

- **Aba 1 — Visão Geral:** KPIs principais/secundários do funil VSL, gráfico combinado
  diário (Vendas + Gasto/Faturamento/ROAS), barras por campanha/anúncio/produto
  e tabela diária com heatmap.
- **Aba 2 — Meta Ads:** funil em etapas, combinado diário, faturamento por
  anúncio, tabela diária e 3 tabelas hierárquicas (Campanha → Conjunto → Anúncio) com
  **filtro cruzado**, além da lista de compradores.
- **Aba 3 — Relatórios:** cards de visão geral/tráfego, tabela diária, visão por
  campanha e Top/Piores anúncios (sem link do criativo — a planilha do Meta não
  tem a coluna `Creative Instagram Permalink`), com briefing interpretativo
  pré-gerado por IA (opcional — ver `build/GUIA-RELATORIOS.md`).
- **Aba 4 — IA Insights:** análise por IA (Claude) do funil e das estruturas ativas
  — **pendente de configuração** (ver acima). Ver `SETUP-IA.md`.

Recursos: filtro global de data + presets, toggle de imposto, tema claro/escuro,
tabelas com ordenação/redimensionamento/multi-seleção, cache-bust.

## Arquivos

- `build/template.html` — a **engine** (CSS + JS). Não editar por cliente.
- `build/build.py` — a **engine** de leitura das planilhas. Não editar por cliente.
- `build/config.py` — **config do cliente** (Spreadsheet ID, gids, imposto,
  produto principal, rótulos, metas, URL do Worker).
- `config.js` — metadados de publicação (usuário/repo do GitHub).
- `.github/workflows/deploy.yml` — build + deploy no Pages.
- `.github/workflows/deploy-worker.yml` — deploy automático do Worker da IA Insights.
- `.github/workflows/gerar-relatorios-metrics.yml` — números da aba Relatórios.
- `ia-worker/worker.js` — backend da aba IA Insights (engine, genérico).
- `ia-worker/wrangler.toml` — nome do Worker (`partiu-empreender-ia-insights`).
- `GUIA-REPLICACAO.md` — arquitetura, CSS/JS e solução dos problemas de publicação.
- `CLAUDE.md` — contexto do projeto + checklist de novo cliente.
- `SETUP-CRON.md` — configuração do cron-job.org.
- `SETUP-IA.md` — configuração da aba IA Insights (Cloudflare Worker).
- `LICENSE` — licença deste template.

## Privacidade

O e‑mail dos compradores é **mascarado** no build (a página é pública). Para exibir
contatos completos, use repositório/Pages **privado**.
