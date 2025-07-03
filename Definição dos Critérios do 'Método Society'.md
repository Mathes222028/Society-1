
# Definição dos Critérios do 'Método Society'

Com base nos requisitos do usuário e na análise da documentação da API `brapi.dev`, os seguintes critérios serão definidos para o 'Método Society':

## 1. Setor Perene

**Critério:** O ativo deve pertencer a um setor considerado perene (Ex: Energia, Saneamento, Bancos, Seguros, Saúde).

**Dados da API:** Este critério será avaliado com base na informação de 'setor' ou 'industry' disponível no módulo `summaryProfile` da API.

## 2. Bom Fluxo de Caixa

**Critério:** A empresa deve apresentar um fluxo de caixa operacional (FCO) consistentemente positivo.

**Dados da API:** O módulo `cashflowHistory` ou `cashflowHistoryQuarterly` pode fornecer o histórico do fluxo de caixa. Será necessário analisar a série histórica para verificar a consistência.

## 3. Lucros Consistentes

**Critério:** A empresa deve demonstrar lucros crescentes ou consistentes ao longo do tempo.

**Dados da API:** O módulo `incomeStatementHistory` ou `incomeStatementHistoryQuarterly` pode fornecer o histórico de lucro líquido (netIncome).

## 4. Receita Crescente

**Critério:** A empresa deve apresentar um crescimento de receita ao longo do tempo.

**Dados da API:** O módulo `financialData` ou `incomeStatementHistory` pode fornecer a receita total (totalRevenue).

## 5. Payout Aceitável

**Critério:** O payout (distribuição de lucros como dividendos) deve estar dentro de um limite aceitável.

**Dados da API:** O `defaultKeyStatistics` pode fornecer o payout ratio. Será necessário definir um limite máximo para este critério (ex: < 100% para ações, ou um valor específico para FIIs).

## 6. Pouca Dívida

**Critério:** A empresa deve ter um nível de endividamento saudável.

**Dados da API:** O `financialData` pode fornecer a dívida líquida (totalDebt) e o EBITDA. A relação Dívida Líquida/EBITDA (Net Debt/EBITDA) será um indicador chave. Será necessário definir um limite máximo para este critério (ex: < 3x).

## 7. Bons Dividendos

**Critério:** O ativo deve apresentar um bom Dividend Yield.

**Dados da API:** O `defaultKeyStatistics` pode fornecer o Dividend Yield. Será necessário definir um valor mínimo para este critério.

## 8. Boa Segurança (Score Society)

**Critério:** Este será um score composto, indicando a porcentagem de critérios do 'Método Society' que o ativo atende. Quanto mais critérios atendidos, maior a segurança.

**Dados da API:** Será calculado internamente pela aplicação com base nos resultados dos outros critérios.

## 9. Bom ROIC e ROE

**Critério:** A empresa deve apresentar bons retornos sobre o capital investido (ROIC) e sobre o patrimônio líquido (ROE).

**Dados da API:** O `defaultKeyStatistics` pode fornecer o ROE (returnOnEquity) e o ROIC (returnOnInvestedCapital). Será necessário definir valores mínimos para estes critérios.

## 10. Notícias Atualizadas

**Critério:** A aplicação deve fornecer notícias atualizadas sobre os fundos e ações.

**Dados da API:** A `brapi.dev` não parece ter um endpoint dedicado a notícias. Será necessário pesquisar outras fontes de API para notícias financeiras ou considerar a integração com feeds RSS de portais de notícias confiáveis, caso a API não seja viável.

## 11. CAGR (Compound Annual Growth Rate)

**Critério:** A empresa deve apresentar um bom crescimento composto anual da receita e/ou lucros.

**Dados da API:** O CAGR precisará ser calculado a partir dos dados históricos de receita (`incomeStatementHistory`) e lucro (`incomeStatementHistory`) fornecidos pela API.



# Estrutura da Aplicação

Para desenvolver a aplicação web completa, a seguinte estrutura será adotada:

## 1. Backend (API e Lógica de Negócio)

O backend será desenvolvido utilizando **Flask** (Python), que atuará como uma API para: 

*   **Integração com APIs Externas:** Será responsável por fazer as requisições à `brapi.dev` (e outras APIs, se necessário, para notícias) e processar os dados brutos.
*   **Lógica do Método Society:** Implementará os cálculos e a lógica de avaliação de cada critério do Método Society, gerando um score para cada ativo.
*   **Autenticação e Gerenciamento de Usuários:** (Futuro) Gerenciará o registro, login e perfis de usuários, bem como suas carteiras de investimento.
*   **Banco de Dados:** (Futuro) Armazenará dados de usuários, carteiras e, possivelmente, um cache de dados financeiros para otimizar o desempenho e reduzir o número de requisições às APIs externas.

## 2. Frontend (Interface do Usuário)

O frontend será desenvolvido utilizando **React** (JavaScript), proporcionando uma interface de usuário moderna, interativa e responsiva. As principais funcionalidades incluirão:

*   **Pesquisa de Ativos:** Um campo de busca para que o usuário possa encontrar ações e FIIs.
*   **Exibição de Dados:** Apresentação clara e organizada dos dados financeiros do ativo, incluindo cotações, indicadores e informações fundamentalistas.
*   **Análise do Método Society:** Visualização dos resultados da análise do Método Society para o ativo selecionado, indicando quais critérios foram atendidos e o score final.
*   **Notícias:** Exibição de notícias relevantes sobre o ativo.
*   **Gestão de Carteira:** (Futuro) Funcionalidades para o usuário adicionar ativos à sua carteira, acompanhar o desempenho e receber alertas.
*   **Visualizações Gráficas:** Gráficos interativos para acompanhar o histórico de preços, dividendos e outros indicadores.

## 3. Comunicação entre Frontend e Backend

A comunicação entre o frontend (React) e o backend (Flask) será feita através de requisições HTTP (RESTful API), utilizando JSON para a troca de dados.

## 4. Ambiente de Desenvolvimento e Implantação

*   **Desenvolvimento:** A aplicação será desenvolvida em um ambiente de sandbox Linux.
*   **Implantação:** O backend Flask poderá ser implantado usando `service_deploy_backend` e o frontend React usando `service_deploy_frontend` para acesso público, se o usuário desejar uma solução permanente.

