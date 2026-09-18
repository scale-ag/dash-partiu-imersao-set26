// Metadados de publicação (GitHub/infra).
//
// Este arquivo NÃO é lido pelo dashboard em runtime (o app é um HTML estático
// gerado por build/build.py; os dados do funil e da senha da IA Insights são
// tratados separadamente — ver build/config.py e SETUP-IA.md). Ele serve como
// referência única para os valores que você repete manualmente nos lugares
// abaixo, para não perder o fio de qual valor vai onde.
window.CONFIG = {
  // Usuário ou organização dona do repositório no GitHub.
  GITHUB_USERNAME: "scale-ag",

  // Nome do repositório no GitHub.
  GITHUB_REPOSITORY: "dash-partiu-imersao-set26",

  // Nome do projeto/cliente, usado só como referência em documentação e no
  // nome do Worker sugerido em ia-worker/wrangler.toml.
  PROJECT_NAME: "Partiu Empreender — Imersão do Zero ao Lucro (SET26)",

  // Preenchido automaticamente a partir de GITHUB_USERNAME/GITHUB_REPOSITORY
  // acima — é a URL pública que o dashboard terá depois de ativar o Pages.
  get PAGES_URL() {
    return `https://${this.GITHUB_USERNAME}.github.io/${this.GITHUB_REPOSITORY}/`;
  },
};
