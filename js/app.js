// Dylan Content Generator - Client-Side Application
class DylanContentGenerator {
    constructor() {
        this.openaiKey = null;
        this.fredKey = null;
        this.marketData = {};
        this.newsData = [];
        this.contentTemplates = this.initializeTemplates();
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadMarketData();
        this.loadNews();
        this.updateStatus('Ready');
    }

    bindEvents() {
        // API Key inputs
        document.getElementById('openai-key').addEventListener('input', (e) => {
            this.openaiKey = e.target.value;
        });
        
        document.getElementById('fred-key').addEventListener('input', (e) => {
            this.fredKey = e.target.value;
        });

        // Generate button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.generateContent();
        });

        // Utility buttons
        document.getElementById('copy-btn').addEventListener('click', () => {
            this.copyToClipboard();
        });

        document.getElementById('download-btn').addEventListener('click', () => {
            this.downloadContent();
        });

        document.getElementById('refresh-data').addEventListener('click', () => {
            this.loadMarketData();
        });
    }

    initializeTemplates() {
        return {
            short: {
                multifamily: `🏢 MULTIFAMILY MARKET UPDATE

The multifamily sector continues to show resilience despite headwinds. Key insights:

• Rent growth moderating but still positive in most metros
• Construction starts declining, helping supply-demand balance
• Cap rates stabilizing as interest rate volatility decreases

{market_data}

What are you seeing in your markets? 

#CommercialRealEstate #Multifamily #CRE #RealEstate`,

                'interest-rates': `📈 INTEREST RATE IMPACT ON CRE

Fed policy continues to shape commercial real estate dynamics:

• Higher rates pressuring valuations across all sectors
• Debt markets showing signs of stabilization
• Buyers and sellers finding new pricing equilibrium

{market_data}

How are you adjusting your investment strategy?

#InterestRates #CRE #CommercialRealEstate #Investment`,

                'gateway-markets': `🌆 GATEWAY MARKET RENAISSANCE

Major metros showing renewed strength:

• Flight-to-quality driving institutional capital back to core markets
• Office fundamentals improving in select gateway cities
• Retail experiencing urban revival in prime locations

{market_data}

Which gateway market offers the best opportunity?

#GatewayMarkets #CRE #UrbanRealEstate #Investment`
            },
            long: {
                multifamily: `# The Multifamily Market: Navigating Current Dynamics

## Executive Summary

The multifamily sector remains a cornerstone of commercial real estate investment, demonstrating remarkable resilience in the face of economic headwinds. As we analyze current market conditions, several key trends emerge that will shape investment strategies moving forward.

## Current Market Conditions

{market_data}

### Supply and Demand Dynamics

The multifamily market is experiencing a recalibration of supply and demand fundamentals. Construction starts have declined significantly from peak levels, providing relief to markets that were experiencing oversupply concerns. This moderation in new supply, combined with continued household formation, is creating a more balanced market environment.

### Rent Growth Trends

While rent growth has decelerated from the unprecedented levels seen in 2021-2022, most markets continue to experience positive rent growth. This normalization reflects a healthier, more sustainable trajectory that benefits both operators and residents.

### Investment Activity

Transaction volume remains below historical averages as buyers and sellers work to establish new pricing benchmarks. However, we're seeing increased activity among institutional investors who view the current environment as an opportunity to acquire quality assets at more attractive yields.

## Regional Spotlight

Different regions are experiencing varying degrees of performance:

- **Sun Belt Markets**: Moderating after rapid growth
- **Midwest**: Showing steady, consistent performance
- **Gateway Cities**: Experiencing renewed investor interest

## Outlook

The multifamily sector's fundamental drivers remain intact. Demographics, urbanization trends, and lifestyle preferences continue to support long-term demand for quality rental housing.

## Investment Implications

For investors, the current environment presents opportunities to:
- Acquire assets at more attractive cap rates
- Focus on markets with strong employment growth
- Emphasize operational excellence and resident experience

---

*This analysis incorporates real-time market data and economic indicators to provide current insights into multifamily market dynamics.*`
            }
        };
    }

    async generateContent() {
        this.updateStatus('Generating content...');
        const generateBtn = document.getElementById('generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Generating...';

        try {
            const contentType = document.getElementById('content-type').value;
            const topic = document.getElementById('topic').value;

            let content;
            if (this.openaiKey) {
                content = await this.generateWithAI(contentType, topic);
            } else {
                content = this.generateFromTemplate(contentType, topic);
            }

            this.displayContent(content);
            this.updateStatus('Content generated successfully');
        } catch (error) {
            console.error('Error generating content:', error);
            this.updateStatus('Error generating content');
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-cog mr-2"></i>Generate Content';
        }
    }

    async generateWithAI(contentType, topic) {
        const marketContext = this.formatMarketDataForAI();
        const newsContext = this.formatNewsForAI();
        
        const prompt = this.buildAIPrompt(contentType, topic, marketContext, newsContext);
        
        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.openaiKey}`
                },
                body: JSON.stringify({
                    model: 'gpt-3.5-turbo',
                    messages: [
                        {
                            role: 'system',
                            content: 'You are Dylan Steman, a commercial real estate expert specializing in multifamily and institutional investment. Write engaging, data-driven content for CRE professionals.'
                        },
                        {
                            role: 'user',
                            content: prompt
                        }
                    ],
                    max_tokens: contentType === 'long' ? 1500 : 500,
                    temperature: 0.7
                })
            });

            if (!response.ok) {
                throw new Error(`OpenAI API error: ${response.status}`);
            }

            const data = await response.json();
            return data.choices[0].message.content;
        } catch (error) {
            console.error('AI generation failed, falling back to template:', error);
            return this.generateFromTemplate(contentType, topic);
        }
    }

    generateFromTemplate(contentType, topic) {
        const template = this.contentTemplates[contentType]?.[topic];
        if (!template) {
            return `Content template not found for ${contentType} - ${topic}`;
        }

        const marketDataText = this.formatMarketDataForTemplate();
        return template.replace('{market_data}', marketDataText);
    }

    buildAIPrompt(contentType, topic, marketContext, newsContext) {
        const basePrompt = contentType === 'short' 
            ? `Write a LinkedIn post about ${topic} in commercial real estate. Keep it under 300 words, engaging, and professional.`
            : `Write a detailed article about ${topic} in commercial real estate. Include market analysis, trends, and investment implications.`;

        return `${basePrompt}

Current Market Data:
${marketContext}

Recent Industry News:
${newsContext}

Style: Professional but engaging, data-driven, include relevant emojis for LinkedIn posts.`;
    }

    async loadMarketData() {
        this.updateStatus('Loading market data...');
        
        try {
            const data = {};
            
            // Load FRED data if API key available
            if (this.fredKey) {
                const fredData = await this.fetchFREDData();
                data.economic = fredData;
            }
            
            // Load public market data (no API key required)
            const publicData = await this.fetchPublicMarketData();
            data.public = publicData;
            
            this.marketData = data;
            this.displayMarketData();
            this.updateStatus('Market data loaded');
        } catch (error) {
            console.error('Error loading market data:', error);
            this.loadFallbackMarketData();
        }
    }

    async fetchFREDData() {
        const series = [
            'FEDFUNDS',    // Federal Funds Rate
            'GS10',        // 10-Year Treasury
            'MORTGAGE30US', // 30-Year Mortgage Rate
            'UNRATE'       // Unemployment Rate
        ];

        const data = {};
        
        for (const seriesId of series) {
            try {
                const response = await fetch(
                    `https://api.stlouisfed.org/fred/series/observations?series_id=${seriesId}&api_key=${this.fredKey}&file_type=json&limit=1&sort_order=desc`
                );
                
                if (response.ok) {
                    const result = await response.json();
                    if (result.observations && result.observations.length > 0) {
                        const latest = result.observations[0];
                        if (latest.value !== '.') {
                            data[seriesId] = {
                                value: parseFloat(latest.value),
                                date: latest.date
                            };
                        }
                    }
                }
                
                // Rate limiting
                await new Promise(resolve => setTimeout(resolve, 100));
            } catch (error) {
                console.error(`Error fetching ${seriesId}:`, error);
            }
        }
        
        return data;
    }

    async fetchPublicMarketData() {
        // Simulate public data sources (in real implementation, these would be actual APIs)
        return {
            timestamp: new Date().toISOString(),
            sources: ['Market Intelligence', 'Public Reports'],
            indicators: {
                'market_sentiment': 'Cautiously Optimistic',
                'transaction_volume': 'Below Average',
                'cap_rate_trend': 'Stabilizing'
            }
        };
    }

    loadFallbackMarketData() {
        this.marketData = {
            fallback: true,
            timestamp: new Date().toISOString(),
            economic: {
                'FEDFUNDS': { value: 5.25, date: '2024-08-01' },
                'GS10': { value: 4.15, date: '2024-08-01' },
                'MORTGAGE30US': { value: 6.85, date: '2024-08-01' },
                'UNRATE': { value: 3.8, date: '2024-08-01' }
            },
            public: {
                indicators: {
                    'market_sentiment': 'Mixed Signals',
                    'transaction_volume': 'Recovering',
                    'cap_rate_trend': 'Stabilizing'
                }
            }
        };
        
        this.displayMarketData();
        this.updateStatus('Using fallback market data');
    }

    async loadNews() {
        try {
            // In a real implementation, this would fetch from RSS feeds or news APIs
            // For now, using simulated data
            this.newsData = [
                {
                    title: 'Multifamily Investment Activity Shows Signs of Recovery',
                    source: 'Commercial Observer',
                    date: new Date().toISOString().split('T')[0],
                    summary: 'Transaction volume increasing as buyers and sellers find pricing equilibrium...'
                },
                {
                    title: 'Gateway Markets Attract Renewed Institutional Interest',
                    source: 'Bisnow',
                    date: new Date().toISOString().split('T')[0],
                    summary: 'Flight-to-quality driving capital back to core metropolitan areas...'
                },
                {
                    title: 'Construction Starts Decline Across Major Markets',
                    source: 'Globe St',
                    date: new Date().toISOString().split('T')[0],
                    summary: 'Supply moderation helping to balance market fundamentals...'
                }
            ];
            
            this.displayNews();
        } catch (error) {
            console.error('Error loading news:', error);
        }
    }

    displayMarketData() {
        const container = document.getElementById('market-data');
        const data = this.marketData;
        
        let html = '';
        
        if (data.economic) {
            html += '<div class="space-y-2">';
            
            if (data.economic.FEDFUNDS) {
                html += `<div class="flex justify-between">
                    <span class="text-sm text-gray-600">Fed Funds Rate:</span>
                    <span class="text-sm font-medium">${data.economic.FEDFUNDS.value}%</span>
                </div>`;
            }
            
            if (data.economic.GS10) {
                html += `<div class="flex justify-between">
                    <span class="text-sm text-gray-600">10-Year Treasury:</span>
                    <span class="text-sm font-medium">${data.economic.GS10.value}%</span>
                </div>`;
            }
            
            if (data.economic.MORTGAGE30US) {
                html += `<div class="flex justify-between">
                    <span class="text-sm text-gray-600">30-Year Mortgage:</span>
                    <span class="text-sm font-medium">${data.economic.MORTGAGE30US.value}%</span>
                </div>`;
            }
            
            if (data.economic.UNRATE) {
                html += `<div class="flex justify-between">
                    <span class="text-sm text-gray-600">Unemployment:</span>
                    <span class="text-sm font-medium">${data.economic.UNRATE.value}%</span>
                </div>`;
            }
            
            html += '</div>';
        }
        
        if (data.public?.indicators) {
            html += '<div class="mt-4 pt-4 border-t space-y-2">';
            
            Object.entries(data.public.indicators).forEach(([key, value]) => {
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                html += `<div class="flex justify-between">
                    <span class="text-sm text-gray-600">${label}:</span>
                    <span class="text-sm font-medium">${value}</span>
                </div>`;
            });
            
            html += '</div>';
        }
        
        if (data.fallback) {
            html += '<div class="mt-2 text-xs text-amber-600">Using sample data</div>';
        }
        
        container.innerHTML = html;
    }

    displayNews() {
        const container = document.getElementById('news-feed');
        
        const html = this.newsData.map(article => `
            <div class="border-l-4 border-blue-500 pl-4">
                <h3 class="font-medium text-gray-900">${article.title}</h3>
                <p class="text-sm text-gray-600 mt-1">${article.summary}</p>
                <div class="flex items-center mt-2 text-xs text-gray-500">
                    <span>${article.source}</span>
                    <span class="mx-2">•</span>
                    <span>${article.date}</span>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }

    displayContent(content) {
        const container = document.getElementById('content-output');
        container.innerHTML = `<pre class="whitespace-pre-wrap font-sans">${content}</pre>`;
        
        // Enable utility buttons
        document.getElementById('copy-btn').disabled = false;
        document.getElementById('download-btn').disabled = false;
    }

    formatMarketDataForTemplate() {
        const data = this.marketData;
        let text = '';
        
        if (data.economic) {
            text += 'Current Economic Indicators:\n';
            if (data.economic.FEDFUNDS) text += `• Fed Funds Rate: ${data.economic.FEDFUNDS.value}%\n`;
            if (data.economic.GS10) text += `• 10-Year Treasury: ${data.economic.GS10.value}%\n`;
            if (data.economic.MORTGAGE30US) text += `• 30-Year Mortgage: ${data.economic.MORTGAGE30US.value}%\n`;
        }
        
        return text || 'Market data loading...';
    }

    formatMarketDataForAI() {
        return this.formatMarketDataForTemplate();
    }

    formatNewsForAI() {
        return this.newsData.map(article => 
            `${article.title} - ${article.summary}`
        ).join('\n');
    }

    async copyToClipboard() {
        const content = document.getElementById('content-output').textContent;
        try {
            await navigator.clipboard.writeText(content);
            this.updateStatus('Content copied to clipboard');
        } catch (error) {
            console.error('Failed to copy:', error);
            this.updateStatus('Failed to copy content');
        }
    }

    downloadContent() {
        const content = document.getElementById('content-output').textContent;
        const contentType = document.getElementById('content-type').value;
        const topic = document.getElementById('topic').value;
        
        const filename = `dylan-content-${contentType}-${topic}-${Date.now()}.txt`;
        
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.updateStatus('Content downloaded');
    }

    updateStatus(message) {
        document.getElementById('status').textContent = message;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new DylanContentGenerator();
});
