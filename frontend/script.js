// frontend/script.js - FULLY FIXED PRO VERSION

const API_BASE = "http://127.0.0.1:8000/api";

let chartTrend = null;
let chartCategory = null;

// =========================
// FETCH ALL LIVE DATA
// =========================
async function fetchLiveData() {
    try {
        const [metricsRes, latestRes, trendRes, categoriesRes, topSourcesRes] = await Promise.all([
            fetch(`${API_BASE}/metrics`),
            fetch(`${API_BASE}/latest`),
            fetch(`${API_BASE}/trend`),
            fetch(`${API_BASE}/categories`),
            fetch(`${API_BASE}/top-sources`)
        ]);

        const metrics = await metricsRes.json();
        const latestData = await latestRes.json();
        const trendData = await trendRes.json();
        const categoriesData = await categoriesRes.json();
        const topSourcesData = await topSourcesRes.json();

        // =========================
        // METRICS (SAFE)
        // =========================
        document.getElementById('total-items').textContent = metrics.total_items || 0;
        document.getElementById('new-today').textContent = metrics.new_today || 0;
        document.getElementById('sources-count').textContent = metrics.sources || 0;
        document.getElementById('last-updated').textContent = metrics.last_updated || "—";

        // =========================
        // CHARTS
        // =========================
        renderTrendChart(trendData || { labels: [], itemsCollected: [], newItems: [] });
        renderCategoryChart(categoriesData || []);

        // =========================
        // TABLE
        // =========================
        renderLatestTable(latestData || []);

        // =========================
        // TOP SOURCES
        // =========================
        renderTopSources(topSourcesData || []);

        console.log("✅ Dashboard fully updated");

    } catch (e) {
        console.error("❌ Backend not responding:", e);
    }
}

// =========================
// TOP SOURCES (FIXED)
// =========================
function renderTopSources(sources) {
    const container = document.getElementById('top-sources');

    if (!container) return;

    if (!sources || sources.length === 0) {
        container.innerHTML = `
            <p class="text-slate-400 text-center py-8">
                No data yet.<br>Click RUN NOW to start scraping
            </p>`;
        return;
    }

    // Icon mapping
    const icons = {
        "HackerNews": "🟠",
        "BBC": "📰",
        "CNN": "🌍",
        "CoinDesk": "💰",
        "Reuters": "📊",
        "ESPN": "🏀"
    };

    const maxCount = Math.max(...sources.map(s => s.count), 1);

    const html = sources.map((s, index) => `
        <div class="flex items-center gap-4">
            
            <div class="w-8 h-8 flex items-center justify-center text-lg bg-slate-100 rounded-2xl">
                ${icons[s.name] || "🌐"}
            </div>

            <div class="flex-1">
                <div class="flex justify-between text-sm mb-1">
                    <span class="font-medium">
                        ${index + 1}. ${s.name}
                    </span>
                    <span class="font-semibold">${s.count} items</span>
                </div>

                <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div class="bg-blue-600 h-2 rounded-full transition-all"
                         style="width: ${(s.count / maxCount) * 100}%">
                    </div>
                </div>
            </div>

        </div>
    `).join('');

    container.innerHTML = html;
}

// =========================
// TREND CHART
// =========================
function renderTrendChart(data) {
    const ctx = document.getElementById('trend-chart');
    if (!ctx) return;

    if (chartTrend) chartTrend.destroy();

    chartTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [
                {
                    label: 'Items Collected',
                    data: data.itemsCollected || [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59,130,246,0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'New Items',
                    data: data.newItems || [],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16,185,129,0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } }
        }
    });
}

// =========================
// CATEGORY CHART
// =========================
function renderCategoryChart(categories) {
    const ctx = document.getElementById('category-chart');
    if (!ctx) return;

    if (chartCategory) chartCategory.destroy();

    chartCategory = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categories.map(c => c.name),
            datasets: [{
                data: categories.map(c => c.count),
                backgroundColor: categories.map(c => c.color),
                borderWidth: 5,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            cutout: '75%',
            plugins: { legend: { display: false } }
        }
    });

    const legendHTML = categories.map(c => `
        <div class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full" style="background-color: ${c.color}"></div>
            <span class="text-sm">${c.name}</span>
            <span class="text-xs text-slate-400 ml-auto">${c.count}</span>
        </div>
    `).join('');

    document.getElementById('category-legend').innerHTML = legendHTML;
}

// =========================
// TABLE (SAFE)
// =========================
function renderLatestTable(data) {
    const tbody = document.getElementById('latest-table');

    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-6 text-slate-400">
                    No data yet. Click RUN NOW to scrape data.
                </td>
            </tr>`;
        return;
    }

    tbody.innerHTML = data.slice(0, 5).map(item => `
        <tr class="table-row">
            <td class="py-4 font-medium">
                <a href="${item.url}" target="_blank">${item.title}</a>
            </td>
            <td class="py-4 text-slate-500">${item.source}</td>
            <td class="py-4">
                <span class="px-3 py-1 text-xs rounded-3xl bg-blue-100 text-blue-700">
                    ${item.category}
                </span>
            </td>
            <td class="py-4 font-medium">${item.price || '-'}</td>
            <td class="py-4 text-slate-500">${item.date || 'Just now'}</td>
        </tr>
    `).join('');
}

// =========================
// RUN SCRAPER (FIXED UX)
// =========================
async function runScraperNow(event) {
    const btn = event.currentTarget;
    btn.innerHTML = "⟳ SCRAPING...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/run-scraper`, {
            method: 'POST'
        });

        const result = await res.json();
        console.log("Scraper result:", result);

        setTimeout(fetchLiveData, 2000);

    } catch (e) {
        console.error("❌ Error running scraper:", e);
    } finally {
        btn.innerHTML = "▶️ RUN NOW";
        btn.disabled = false;
    }
}

// =========================
// AUTO REFRESH
// =========================
function startAutoRefresh() {
    fetchLiveData();
    setInterval(fetchLiveData, 15000);
}

window.onload = startAutoRefresh;