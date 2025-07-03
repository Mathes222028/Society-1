import { useState } from 'react'
import { Search, TrendingUp, Shield, DollarSign, BarChart3, Building2, Newspaper } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import './App.css'

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedAsset, setSelectedAsset] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!searchTerm.trim()) return
    
    setLoading(true)
    try {
      // Fazer requisição para o backend Flask na porta 5000
      const response = await fetch(`http://localhost:5000/api/analyze/${searchTerm.toUpperCase()}`)
      if (response.ok) {
        const data = await response.json()
        setAnalysisResult(data)
        setSelectedAsset(data.basic_data)
      } else {
        console.error('Erro ao buscar dados do ativo')
      }
    } catch (error) {
      console.error('Erro na requisição:', error)
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-blue-600'
    if (score >= 40) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBadgeVariant = (score) => {
    if (score >= 80) return 'default'
    if (score >= 60) return 'secondary'
    if (score >= 40) return 'outline'
    return 'destructive'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Society Analyzer</h1>
                <p className="text-sm text-gray-600">Análise Inteligente de Investimentos</p>
              </div>
            </div>
            <Badge variant="outline" className="text-blue-600 border-blue-600">
              Método Society
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Search className="h-5 w-5" />
              <span>Buscar Ativo</span>
            </CardTitle>
            <CardDescription>
              Digite o ticker de uma ação ou fundo imobiliário para análise (ex: PETR4, HGLG11)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              <Input
                placeholder="Digite o ticker do ativo..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1"
              />
              <Button onClick={handleSearch} disabled={loading}>
                {loading ? 'Analisando...' : 'Analisar'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        {analysisResult && (
          <div className="space-y-6">
            {/* Asset Overview */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-2xl">{selectedAsset?.symbol}</CardTitle>
                    <CardDescription className="text-lg">{selectedAsset?.longName}</CardDescription>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">
                      {selectedAsset?.currency} {selectedAsset?.regularMarketPrice?.toFixed(2)}
                    </div>
                    <div className={`text-sm ${selectedAsset?.regularMarketChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {selectedAsset?.regularMarketChange >= 0 ? '+' : ''}
                      {selectedAsset?.regularMarketChange?.toFixed(2)} 
                      ({selectedAsset?.regularMarketChangePercent?.toFixed(2)}%)
                    </div>
                  </div>
                </div>
              </CardHeader>
            </Card>

            {/* Society Score */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5" />
                  <span>Score Society</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center mb-6">
                  <div className={`text-6xl font-bold ${getScoreColor(analysisResult.score)}`}>
                    {analysisResult.score}%
                  </div>
                  <Badge variant={getScoreBadgeVariant(analysisResult.score)} className="mt-2">
                    {analysisResult.recommendation}
                  </Badge>
                </div>
                <Progress value={analysisResult.score} className="h-3" />
              </CardContent>
            </Card>

            {/* Detailed Analysis */}
            <Tabs defaultValue="criteria" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="criteria">Critérios</TabsTrigger>
                <TabsTrigger value="fundamentals">Fundamentos</TabsTrigger>
                <TabsTrigger value="news">Notícias</TabsTrigger>
              </TabsList>

              <TabsContent value="criteria" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {Object.entries(analysisResult.criteria_results).map(([key, result]) => (
                    <Card key={key}>
                      <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium">
                          {getCriteriaTitle(key)}
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center justify-between">
                          <Badge variant={result.passed ? 'default' : 'destructive'}>
                            {result.passed ? 'Aprovado' : 'Reprovado'}
                          </Badge>
                          {result.value && (
                            <span className="text-sm text-gray-600">{result.value}</span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500 mt-2">{result.description}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="fundamentals">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BarChart3 className="h-5 w-5" />
                      <span>Dados Fundamentalistas</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">
                          {selectedAsset?.marketCap ? formatMarketCap(selectedAsset.marketCap) : 'N/A'}
                        </div>
                        <div className="text-sm text-gray-600">Valor de Mercado</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600">
                          {analysisResult.criteria_results.bons_dividendos?.value || 'N/A'}
                        </div>
                        <div className="text-sm text-gray-600">Dividend Yield</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">
                          {analysisResult.criteria_results.bom_roe?.value || 'N/A'}
                        </div>
                        <div className="text-sm text-gray-600">ROE</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-orange-600">
                          {analysisResult.criteria_results.pouca_divida?.value || 'N/A'}
                        </div>
                        <div className="text-sm text-gray-600">Dívida/EBITDA</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="news">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Newspaper className="h-5 w-5" />
                      <span>Notícias</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-8 text-gray-500">
                      <Newspaper className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>Funcionalidade de notícias em desenvolvimento</p>
                      <p className="text-sm">Em breve, você terá acesso às últimas notícias sobre o ativo</p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        )}

        {/* Welcome Message */}
        {!analysisResult && (
          <div className="text-center py-12">
            <div className="max-w-md mx-auto">
              <div className="bg-blue-600 p-4 rounded-full w-20 h-20 mx-auto mb-6 flex items-center justify-center">
                <Building2 className="h-10 w-10 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Bem-vindo ao Society Analyzer
              </h2>
              <p className="text-gray-600 mb-6">
                Analise ações e fundos imobiliários usando o Método Society. 
                Digite um ticker acima para começar sua análise.
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-white p-4 rounded-lg shadow-sm">
                  <DollarSign className="h-6 w-6 text-green-600 mx-auto mb-2" />
                  <div className="font-medium">Análise Completa</div>
                  <div className="text-gray-600">9 critérios fundamentais</div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-sm">
                  <Shield className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                  <div className="font-medium">Score de Segurança</div>
                  <div className="text-gray-600">Baseado no Método Society</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

// Helper functions
function getCriteriaTitle(key) {
  const titles = {
    setor_perene: 'Setor Perene',
    fluxo_caixa: 'Fluxo de Caixa',
    lucros_consistentes: 'Lucros Consistentes',
    receita_crescente: 'Receita Crescente',
    payout_aceitavel: 'Payout Aceitável',
    pouca_divida: 'Pouca Dívida',
    bons_dividendos: 'Bons Dividendos',
    bom_roe: 'Bom ROE',
    bom_roic: 'Bom ROIC'
  }
  return titles[key] || key
}

function formatMarketCap(value) {
  if (value >= 1e12) return `R$ ${(value / 1e12).toFixed(1)}T`
  if (value >= 1e9) return `R$ ${(value / 1e9).toFixed(1)}B`
  if (value >= 1e6) return `R$ ${(value / 1e6).toFixed(1)}M`
  return `R$ ${value.toLocaleString()}`
}

export default App

