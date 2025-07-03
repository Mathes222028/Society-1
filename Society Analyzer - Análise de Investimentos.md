# Society Analyzer - Análise de Investimentos

Uma aplicação web completa para análise de ações e fundos imobiliários usando o **Método Society**, desenvolvida com React (frontend) e Flask (backend).

## 🎯 Sobre o Projeto

O Society Analyzer é uma ferramenta de análise de investimentos que avalia ativos financeiros com base em 9 critérios fundamentais do Método Society, fornecendo um score de 0 a 100% e uma recomendação de investimento.

### Critérios do Método Society

1. **Setor Perene** - Verifica se o ativo pertence a um setor considerado perene
2. **Fluxo de Caixa** - Analisa a consistência do fluxo de caixa operacional
3. **Lucros Consistentes** - Verifica a consistência dos lucros ao longo do tempo
4. **Receita Crescente** - Analisa o crescimento da receita
5. **Payout Aceitável** - Verifica se o payout está em níveis adequados
6. **Pouca Dívida** - Analisa o nível de endividamento (Dívida/EBITDA)
7. **Bons Dividendos** - Verifica se o dividend yield é atrativo
8. **Bom ROE** - Analisa o retorno sobre o patrimônio líquido
9. **Bom ROIC** - Analisa o retorno sobre o capital investido

## 🚀 Funcionalidades

- ✅ Análise completa de ações e FIIs
- ✅ Score de 0 a 100% baseado no Método Society
- ✅ Interface moderna e responsiva
- ✅ Dados em tempo real via API brapi.dev
- ✅ Modo demonstração com dados fictícios
- ✅ Análise detalhada por critérios
- ✅ Visualização de dados fundamentalistas

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React** - Biblioteca JavaScript para interfaces
- **Tailwind CSS** - Framework CSS utilitário
- **shadcn/ui** - Componentes de interface
- **Lucide Icons** - Ícones modernos
- **Vite** - Build tool e dev server

### Backend
- **Flask** - Framework web Python
- **Flask-CORS** - Suporte a CORS
- **Requests** - Cliente HTTP para APIs
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### API Externa
- **brapi.dev** - API de dados financeiros do mercado brasileiro

## 📦 Estrutura do Projeto

```
society-analyzer/
├── society_analyzer/          # Backend Flask
│   ├── src/
│   │   ├── routes/
│   │   │   └── analysis.py    # Rotas de análise
│   │   ├── models/            # Modelos de dados
│   │   └── main.py           # Aplicação principal
│   ├── .env                  # Variáveis de ambiente
│   ├── requirements.txt      # Dependências Python
│   └── venv/                 # Ambiente virtual
│
└── society-analyzer-frontend/ # Frontend React
    ├── src/
    │   ├── components/        # Componentes React
    │   ├── App.jsx           # Componente principal
    │   └── main.jsx          # Ponto de entrada
    ├── public/               # Arquivos estáticos
    └── package.json          # Dependências Node.js
```

## 🔧 Configuração e Instalação

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- Conta na brapi.dev (opcional, para dados reais)

### 1. Configuração do Backend

```bash
# Navegar para o diretório do backend
cd society_analyzer

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar token da API (opcional)
# Edite o arquivo .env e substitua YOUR_TOKEN_HERE pelo seu token da brapi.dev
```

### 2. Configuração do Frontend

```bash
# Navegar para o diretório do frontend
cd society-analyzer-frontend

# Instalar dependências
pnpm install
```

### 3. Obter Token da API brapi.dev (Opcional)

1. Acesse [brapi.dev](https://brapi.dev/)
2. Clique em "Obter Chave de API"
3. Crie sua conta gratuita
4. No Dashboard, copie seu token
5. Edite o arquivo `.env` no backend:
   ```
   BRAPI_TOKEN=seu_token_aqui
   ```

**Planos disponíveis:**
- **Gratuito**: 15.000 requisições/mês
- **Startup**: R$ 599,90/ano - dados mais completos
- **Pro**: R$ 999,90/ano - dados completos com histórico

## 🚀 Executando a Aplicação

### 1. Iniciar o Backend
```bash
cd society_analyzer
source venv/bin/activate
python src/main.py
```
O backend estará disponível em: `http://localhost:5000`

### 2. Iniciar o Frontend
```bash
cd society-analyzer-frontend
pnpm run dev --host
```
O frontend estará disponível em: `http://localhost:5173`

## 📊 Como Usar

1. **Acesse a aplicação** no navegador
2. **Digite um ticker** de ação (ex: PETR4) ou FII (ex: HGLG11)
3. **Clique em "Analisar"** para obter a análise completa
4. **Visualize o score** e a recomendação do Método Society
5. **Explore as abas**:
   - **Critérios**: Detalhes de cada critério avaliado
   - **Fundamentos**: Dados fundamentalistas do ativo
   - **Notícias**: Em desenvolvimento

## 🎨 Interface

A aplicação possui uma interface moderna e intuitiva com:

- **Design responsivo** - Funciona em desktop e mobile
- **Cores intuitivas** - Verde para aprovado, vermelho para reprovado
- **Score visual** - Barra de progresso e percentual destacado
- **Navegação por abas** - Organização clara das informações
- **Feedback visual** - Estados de loading e erro

## 🔍 Modo Demonstração

Quando não há token configurado, a aplicação funciona em modo demonstração com dados fictícios para:
- PETR4 (Petrobras)
- HGLG11 (CSHG Logística FII)
- Outros ativos com dados genéricos

## 🛡️ Segurança

- Variáveis de ambiente para tokens sensíveis
- CORS configurado adequadamente
- Validação de entrada nos endpoints
- Tratamento de erros robusto

## 📈 Próximas Funcionalidades

- [ ] Integração com notícias financeiras
- [ ] Criação de carteiras de investimento
- [ ] Comparação entre ativos
- [ ] Histórico de análises
- [ ] Alertas personalizados
- [ ] Exportação de relatórios

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Entre em contato através do email

---

**Desenvolvido com ❤️ para investidores que buscam análises fundamentalistas sólidas.**

