from flask import Blueprint, jsonify, request
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

analysis_bp = Blueprint('analysis', __name__)

# Configuração da API brapi.dev
BRAPI_BASE_URL = "https://brapi.dev/api"
BRAPI_TOKEN = os.getenv('BRAPI_TOKEN', '')

class SocietyAnalyzer:
    """Classe responsável por implementar a lógica do Método Society"""
    
    def __init__(self):
        self.criteria_weights = {
            'setor_perene': 1,
            'fluxo_caixa': 1,
            'lucros_consistentes': 1,
            'receita_crescente': 1,
            'payout_aceitavel': 1,
            'pouca_divida': 1,
            'bons_dividendos': 1,
            'bom_roe': 1,
            'bom_roic': 1
        }
    
    def analyze_asset(self, asset_data):
        """Analisa um ativo com base nos critérios do Método Society"""
        results = {}
        score = 0
        total_criteria = len(self.criteria_weights)
        
        # 1. Setor Perene
        results['setor_perene'] = self._check_setor_perene(asset_data)
        if results['setor_perene']['passed']:
            score += 1
        
        # 2. Fluxo de Caixa
        results['fluxo_caixa'] = self._check_fluxo_caixa(asset_data)
        if results['fluxo_caixa']['passed']:
            score += 1
        
        # 3. Lucros Consistentes
        results['lucros_consistentes'] = self._check_lucros_consistentes(asset_data)
        if results['lucros_consistentes']['passed']:
            score += 1
        
        # 4. Receita Crescente
        results['receita_crescente'] = self._check_receita_crescente(asset_data)
        if results['receita_crescente']['passed']:
            score += 1
        
        # 5. Payout Aceitável
        results['payout_aceitavel'] = self._check_payout_aceitavel(asset_data)
        if results['payout_aceitavel']['passed']:
            score += 1
        
        # 6. Pouca Dívida
        results['pouca_divida'] = self._check_pouca_divida(asset_data)
        if results['pouca_divida']['passed']:
            score += 1
        
        # 7. Bons Dividendos
        results['bons_dividendos'] = self._check_bons_dividendos(asset_data)
        if results['bons_dividendos']['passed']:
            score += 1
        
        # 8. Bom ROE
        results['bom_roe'] = self._check_bom_roe(asset_data)
        if results['bom_roe']['passed']:
            score += 1
        
        # 9. Bom ROIC
        results['bom_roic'] = self._check_bom_roic(asset_data)
        if results['bom_roic']['passed']:
            score += 1
        
        # Score final
        final_score = (score / total_criteria) * 100
        
        return {
            'symbol': asset_data.get('symbol', ''),
            'company_name': asset_data.get('longName', ''),
            'analysis_date': datetime.now().isoformat(),
            'score': round(final_score, 2),
            'criteria_results': results,
            'recommendation': self._get_recommendation(final_score)
        }
    
    def _check_setor_perene(self, asset_data):
        """Verifica se o ativo pertence a um setor perene"""
        setores_perenes = [
            'utilities', 'energy', 'healthcare', 'financial services',
            'banks', 'insurance', 'real estate', 'consumer staples'
        ]
        
        sector = asset_data.get('summaryProfile', {}).get('sector', '').lower()
        industry = asset_data.get('summaryProfile', {}).get('industry', '').lower()
        
        is_perene = any(setor in sector or setor in industry for setor in setores_perenes)
        
        return {
            'passed': is_perene,
            'value': sector or industry or 'N/A',
            'description': 'Setor considerado perene' if is_perene else 'Setor não perene'
        }
    
    def _check_fluxo_caixa(self, asset_data):
        """Verifica se o fluxo de caixa operacional é positivo"""
        cashflow_data = asset_data.get('cashflowHistory', [])
        
        if not cashflow_data:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de fluxo de caixa não disponíveis'
            }
        
        # Verifica os últimos 3 anos
        positive_years = 0
        total_years = min(3, len(cashflow_data))
        
        for year_data in cashflow_data[:total_years]:
            operating_cashflow = year_data.get('operatingCashflow', 0)
            if operating_cashflow and operating_cashflow > 0:
                positive_years += 1
        
        passed = positive_years >= 2  # Pelo menos 2 dos últimos 3 anos positivos
        
        return {
            'passed': passed,
            'value': f"{positive_years}/{total_years} anos positivos",
            'description': 'Fluxo de caixa operacional consistentemente positivo' if passed else 'Fluxo de caixa operacional inconsistente'
        }
    
    def _check_lucros_consistentes(self, asset_data):
        """Verifica se os lucros são consistentes"""
        income_data = asset_data.get('incomeStatementHistory', [])
        
        if not income_data:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de demonstração de resultados não disponíveis'
            }
        
        # Verifica os últimos 3 anos
        positive_years = 0
        total_years = min(3, len(income_data))
        
        for year_data in income_data[:total_years]:
            net_income = year_data.get('netIncome', 0)
            if net_income and net_income > 0:
                positive_years += 1
        
        passed = positive_years >= 2  # Pelo menos 2 dos últimos 3 anos com lucro
        
        return {
            'passed': passed,
            'value': f"{positive_years}/{total_years} anos com lucro",
            'description': 'Lucros consistentes' if passed else 'Lucros inconsistentes'
        }
    
    def _check_receita_crescente(self, asset_data):
        """Verifica se a receita está crescendo"""
        income_data = asset_data.get('incomeStatementHistory', [])
        
        if len(income_data) < 2:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados insuficientes para análise de crescimento de receita'
            }
        
        # Compara os últimos 2 anos
        current_revenue = income_data[0].get('totalRevenue', 0)
        previous_revenue = income_data[1].get('totalRevenue', 0)
        
        if not current_revenue or not previous_revenue:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de receita não disponíveis'
            }
        
        growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100
        passed = growth_rate > 0
        
        return {
            'passed': passed,
            'value': f"{growth_rate:.2f}%",
            'description': f'Crescimento de receita de {growth_rate:.2f}%' if passed else f'Queda de receita de {abs(growth_rate):.2f}%'
        }
    
    def _check_payout_aceitavel(self, asset_data):
        """Verifica se o payout está em um nível aceitável"""
        key_stats = asset_data.get('defaultKeyStatistics', {})
        payout_ratio = key_stats.get('payoutRatio')
        
        if payout_ratio is None:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de payout não disponíveis'
            }
        
        # Para ações: payout < 80% é considerado bom
        # Para FIIs: pode ser mais alto
        symbol = asset_data.get('symbol', '')
        is_fii = symbol.endswith('11')
        
        if is_fii:
            passed = payout_ratio <= 1.0  # 100% para FIIs
            threshold = "100%"
        else:
            passed = payout_ratio <= 0.8  # 80% para ações
            threshold = "80%"
        
        return {
            'passed': passed,
            'value': f"{payout_ratio * 100:.2f}%",
            'description': f'Payout de {payout_ratio * 100:.2f}% (limite: {threshold})'
        }
    
    def _check_pouca_divida(self, asset_data):
        """Verifica se a empresa tem pouca dívida"""
        financial_data = asset_data.get('financialData', {})
        total_debt = financial_data.get('totalDebt')
        ebitda = financial_data.get('ebitda')
        
        if not total_debt or not ebitda or ebitda <= 0:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de dívida ou EBITDA não disponíveis'
            }
        
        debt_to_ebitda = total_debt / ebitda
        passed = debt_to_ebitda < 3.0  # Dívida/EBITDA < 3x
        
        return {
            'passed': passed,
            'value': f"{debt_to_ebitda:.2f}x",
            'description': f'Dívida/EBITDA de {debt_to_ebitda:.2f}x (limite: 3.0x)'
        }
    
    def _check_bons_dividendos(self, asset_data):
        """Verifica se o dividend yield é atrativo"""
        key_stats = asset_data.get('defaultKeyStatistics', {})
        dividend_yield = key_stats.get('dividendYield')
        
        if dividend_yield is None:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de dividend yield não disponíveis'
            }
        
        # Dividend yield > 4% é considerado bom
        passed = dividend_yield > 0.04
        
        return {
            'passed': passed,
            'value': f"{dividend_yield * 100:.2f}%",
            'description': f'Dividend Yield de {dividend_yield * 100:.2f}% (mínimo: 4%)'
        }
    
    def _check_bom_roe(self, asset_data):
        """Verifica se o ROE é bom"""
        key_stats = asset_data.get('defaultKeyStatistics', {})
        roe = key_stats.get('returnOnEquity')
        
        if roe is None:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de ROE não disponíveis'
            }
        
        # ROE > 15% é considerado bom
        passed = roe > 0.15
        
        return {
            'passed': passed,
            'value': f"{roe * 100:.2f}%",
            'description': f'ROE de {roe * 100:.2f}% (mínimo: 15%)'
        }
    
    def _check_bom_roic(self, asset_data):
        """Verifica se o ROIC é bom"""
        key_stats = asset_data.get('defaultKeyStatistics', {})
        roic = key_stats.get('returnOnInvestedCapital')
        
        if roic is None:
            return {
                'passed': False,
                'value': 'N/A',
                'description': 'Dados de ROIC não disponíveis'
            }
        
        # ROIC > 12% é considerado bom
        passed = roic > 0.12
        
        return {
            'passed': passed,
            'value': f"{roic * 100:.2f}%",
            'description': f'ROIC de {roic * 100:.2f}% (mínimo: 12%)'
        }
    
    def _get_recommendation(self, score):
        """Retorna uma recomendação baseada no score"""
        if score >= 80:
            return "FORTE COMPRA - Excelente ativo segundo o Método Society"
        elif score >= 60:
            return "COMPRA - Bom ativo segundo o Método Society"
        elif score >= 40:
            return "NEUTRO - Ativo mediano segundo o Método Society"
        else:
            return "VENDA - Ativo não recomendado pelo Método Society"

# Instância global do analisador
analyzer = SocietyAnalyzer()

def get_demo_data(symbol):
    """Retorna dados de demonstração para quando não há token da API"""
    demo_data = {
        'PETR4': {
            'symbol': 'PETR4',
            'longName': 'Petróleo Brasileiro S.A. - Petrobras',
            'shortName': 'PETROBRAS PN',
            'currency': 'BRL',
            'regularMarketPrice': 38.50,
            'regularMarketChange': 0.30,
            'regularMarketChangePercent': 0.78,
            'marketCap': 503100000000,
            'logourl': 'https://icons.brapi.dev/logos/PETR4.png',
            'summaryProfile': {
                'sector': 'Energy',
                'industry': 'Oil & Gas Integrated'
            },
            'defaultKeyStatistics': {
                'dividendYield': 0.085,
                'returnOnEquity': 0.18,
                'returnOnInvestedCapital': 0.14,
                'payoutRatio': 0.65
            },
            'financialData': {
                'totalDebt': 45000000000,
                'ebitda': 25000000000
            },
            'incomeStatementHistory': [
                {'totalRevenue': 650000000000, 'netIncome': 45000000000},
                {'totalRevenue': 580000000000, 'netIncome': 35000000000}
            ],
            'cashflowHistory': [
                {'operatingCashflow': 55000000000},
                {'operatingCashflow': 48000000000}
            ]
        },
        'HGLG11': {
            'symbol': 'HGLG11',
            'longName': 'CSHG Logística FII',
            'shortName': 'HGLG11',
            'currency': 'BRL',
            'regularMarketPrice': 165.50,
            'regularMarketChange': -1.20,
            'regularMarketChangePercent': -0.72,
            'marketCap': 8500000000,
            'logourl': 'https://icons.brapi.dev/logos/HGLG11.png',
            'summaryProfile': {
                'sector': 'Real Estate',
                'industry': 'Real Estate Investment Trust'
            },
            'defaultKeyStatistics': {
                'dividendYield': 0.095,
                'returnOnEquity': 0.12,
                'returnOnInvestedCapital': 0.10,
                'payoutRatio': 0.95
            },
            'financialData': {
                'totalDebt': 1200000000,
                'ebitda': 800000000
            },
            'incomeStatementHistory': [
                {'totalRevenue': 950000000, 'netIncome': 720000000},
                {'totalRevenue': 880000000, 'netIncome': 650000000}
            ],
            'cashflowHistory': [
                {'operatingCashflow': 750000000},
                {'operatingCashflow': 680000000}
            ]
        }
    }
    
    return demo_data.get(symbol.upper(), {
        'symbol': symbol.upper(),
        'longName': f'Empresa {symbol.upper()}',
        'shortName': symbol.upper(),
        'currency': 'BRL',
        'regularMarketPrice': 100.00,
        'regularMarketChange': 0.00,
        'regularMarketChangePercent': 0.00,
        'marketCap': 1000000000,
        'logourl': '',
        'summaryProfile': {'sector': 'Unknown', 'industry': 'Unknown'},
        'defaultKeyStatistics': {},
        'financialData': {},
        'incomeStatementHistory': [],
        'cashflowHistory': []
    })

@analysis_bp.route('/analyze/<symbol>', methods=['GET'])
def analyze_asset(symbol):
    """Endpoint para analisar um ativo específico"""
    try:
        asset_data = None
        
        # Verifica se há token configurado
        if BRAPI_TOKEN and BRAPI_TOKEN != 'YOUR_TOKEN_HERE':
            # Busca dados da API brapi.dev
            modules = [
                'summaryProfile',
                'defaultKeyStatistics',
                'financialData',
                'incomeStatementHistory',
                'cashflowHistory'
            ]
            
            url = f"{BRAPI_BASE_URL}/quote/{symbol.upper()}"
            params = {
                'modules': ','.join(modules),
                'token': BRAPI_TOKEN
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results'):
                    asset_data = data['results'][0]
        
        # Se não conseguiu dados da API, usa dados de demonstração
        if not asset_data:
            asset_data = get_demo_data(symbol)
            demo_mode = True
        else:
            demo_mode = False
        
        # Realiza a análise
        analysis_result = analyzer.analyze_asset(asset_data)
        
        # Adiciona dados básicos do ativo
        analysis_result['basic_data'] = {
            'symbol': asset_data.get('symbol'),
            'longName': asset_data.get('longName'),
            'shortName': asset_data.get('shortName'),
            'currency': asset_data.get('currency'),
            'regularMarketPrice': asset_data.get('regularMarketPrice'),
            'regularMarketChange': asset_data.get('regularMarketChange'),
            'regularMarketChangePercent': asset_data.get('regularMarketChangePercent'),
            'marketCap': asset_data.get('marketCap'),
            'logourl': asset_data.get('logourl')
        }
        
        # Adiciona informação sobre modo de demonstração
        analysis_result['demo_mode'] = demo_mode
        if demo_mode:
            analysis_result['demo_message'] = 'Dados de demonstração - Configure seu token da brapi.dev para dados reais'
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({
            'error': f'Erro interno: {str(e)}'
        }), 500

@analysis_bp.route('/search/<query>', methods=['GET'])
def search_assets(query):
    """Endpoint para buscar ativos (implementação básica)"""
    try:
        # Lista de ativos populares para demonstração
        popular_assets = [
            {'symbol': 'PETR4', 'name': 'Petróleo Brasileiro S.A. - Petrobras'},
            {'symbol': 'VALE3', 'name': 'Vale S.A.'},
            {'symbol': 'ITUB4', 'name': 'Itaú Unibanco Holding S.A.'},
            {'symbol': 'BBDC4', 'name': 'Banco Bradesco S.A.'},
            {'symbol': 'ABEV3', 'name': 'Ambev S.A.'},
            {'symbol': 'WEGE3', 'name': 'WEG S.A.'},
            {'symbol': 'MGLU3', 'name': 'Magazine Luiza S.A.'},
            {'symbol': 'HGLG11', 'name': 'CSHG Logística FII'},
            {'symbol': 'KNRI11', 'name': 'Kinea Renda Imobiliária FII'},
            {'symbol': 'XPML11', 'name': 'XP Malls FII'},
            {'symbol': 'VISC11', 'name': 'Vinci Shopping Centers FII'},
            {'symbol': 'BCFF11', 'name': 'BTG Pactual Fundo de CRI FII'}
        ]
        
        # Filtra baseado na query
        filtered_assets = [
            asset for asset in popular_assets
            if query.upper() in asset['symbol'] or query.upper() in asset['name'].upper()
        ]
        
        return jsonify(filtered_assets[:10])  # Retorna no máximo 10 resultados
        
    except Exception as e:
        return jsonify({
            'error': f'Erro interno: {str(e)}'
        }), 500

@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    token_status = "configurado" if BRAPI_TOKEN and BRAPI_TOKEN != 'YOUR_TOKEN_HERE' else "não configurado"
    
    return jsonify({
        'status': 'ok',
        'message': 'Society Analyzer API está funcionando',
        'token_status': token_status,
        'demo_mode': token_status == "não configurado",
        'timestamp': datetime.now().isoformat()
    })

