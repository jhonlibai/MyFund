// 导入模块
import { loadFundsList, addFund, deleteFund, setHoldAmount, viewFundDetail, loadTotalInfo as fetchTotalInfo, loadLastFundsList } from './services/fundService.js';
import { loadIndicesData, loadGoldData, loadVolumeTrendData, loadShanghaiIndexData, loadGoldHistoryData, loadNewsList, loadRealTimeGoldData } from './services/marketService.js';
import { initCharts, updateRealTimeGoldChart } from './utils/chartUtils.js';
import { API_CONFIG, MESSAGE_CONFIG } from './constants/config.js';

// 后端API地址
const API_BASE_URL = `${API_CONFIG.BASE_URL}/market`;

// 测试JavaScript执行
console.log('JavaScript执行正常');
console.log('Vue对象:', Vue);
console.log('API_BASE_URL:', API_BASE_URL);

// 初始化Vue应用
console.log('开始初始化Vue应用');
const app = Vue.createApp({
    data() {
        return {
            activeTab: 'news',
            fundsList: [],
            totalInfo: null,
            loading: false,
            isFirstLoadToday: true,
            fundForm: {
                fundCode: '',
                holdAmount: ''
            },
            sectorForm: {
                sectorName: ''
            },
            sectorFundsList: [],
            sectorLoading: false,
            selectedSector: null,
            newsList: [],
            // 定时器
            newsRefreshTimer: null,
            // 基金分页相关
            currentFundPage: 1,
            fundPageSize: 10,
            totalFunds: 0,
            // 实时贵金属数据
            realTimeGoldData: [],
            // 历史金价数据
            goldHistoryData: [
                { date: '2026-02-02', chinaGoldFundPrice: '1969.6', chowTaiFookPrice: '1495.0', chinaGoldFundChange: -44.4, chowTaiFookChange: -44.4 },
                { date: '2026-01-31', chinaGoldFundPrice: '1195.0', chowTaiFookPrice: '1489.0', chinaGoldFundChange: -63.0, chowTaiFookChange: -63.0 },
                { date: '2026-01-30', chinaGoldFundPrice: '1168.0', chowTaiFookPrice: '1625.0', chinaGoldFundChange: -76.7, chowTaiFookChange: -76.7 },
                { date: '2026-01-29', chinaGoldFundPrice: '1244.7', chowTaiFookPrice: '1695.0', chinaGoldFundChange: 69.7, chowTaiFookChange: 69.7 },
                { date: '2026-01-28', chinaGoldFundPrice: '1175.0', chowTaiFookPrice: '1786.0', chinaGoldFundChange: 36.0, chowTaiFookChange: 36.0 },
                { date: '2026-01-27', chinaGoldFundPrice: '1139.0', chowTaiFookPrice: '1619.0', chinaGoldFundChange: -1.0, chowTaiFookChange: -1.0 },
                { date: '2026-01-26', chinaGoldFundPrice: '1140.0', chowTaiFookPrice: '1578.0', chinaGoldFundChange: 16.0, chowTaiFookChange: 16.0 },
                { date: '2026-01-24', chinaGoldFundPrice: '1124.0', chowTaiFookPrice: '1578.0', chinaGoldFundChange: 'N/A', chowTaiFookChange: 'N/A' },
                { date: '2026-01-23', chinaGoldFundPrice: '1111.0', chowTaiFookPrice: '1553.0', chinaGoldFundChange: 38.0, chowTaiFookChange: 38.0 },
                { date: '2026-01-22', chinaGoldFundPrice: '1073.0', chowTaiFookPrice: '1542.0', chinaGoldFundChange: -18.7, chowTaiFookChange: -18.7 }
            ],
            // 行业板块数据
            sectorsList: [
                { name: '船舶制造', change: '5.23%', mainInflow: '13.46亿', mainInflowRatio: '3.72%', smallInflow: '-7.22亿', smallInflowRatio: '-7.43%' },
                { name: '光伏设备', change: '4.9%', mainInflow: '13.56亿', mainInflowRatio: '2.7%', smallInflow: '0.34亿', smallInflowRatio: '0.08%' },
                { name: '航天航空', change: '3.26%', mainInflow: '16.39亿', mainInflowRatio: '5.53%', smallInflow: '-6.52亿', smallInflowRatio: '-2.17%' },
                { name: '通信设备', change: '2.80%', mainInflow: '12.99亿', mainInflowRatio: '1.01%', smallInflow: '-11.86亿', smallInflowRatio: '-0.92%' },
                { name: '小金属', change: '2.80%', mainInflow: '-4.9亿', mainInflowRatio: '-1.28%', smallInflow: '11.18亿', smallInflowRatio: '2.93%' },
                { name: '玻璃玻纤', change: '2.40%', mainInflow: '-0.46亿', mainInflowRatio: '-0.58%', smallInflow: '1.6亿', smallInflowRatio: '2.00%' },
                { name: '非金属材料', change: '2.40%', mainInflow: '0.96亿', mainInflowRatio: '-0.05%', smallInflow: '1.55亿', smallInflowRatio: '1.35%' },
                { name: '光学光电子', change: '2.12%', mainInflow: '8.61亿', mainInflowRatio: '3.02%', smallInflow: '-8.70亿', smallInflowRatio: '-3.29%' },
                { name: '专用设备', change: '2.09%', mainInflow: '-0.49亿', mainInflowRatio: '-0.06%', smallInflow: '3.87亿', smallInflowRatio: '0.53%' },
                { name: '化学制品', change: '1.99%', mainInflow: '8.06亿', mainInflowRatio: '3.77%', smallInflow: '1.68亿', smallInflowRatio: '0.78%' },
                { name: '电子化学品', change: '1.98%', mainInflow: '-2.46亿', mainInflowRatio: '-3.37%', smallInflow: '3.18亿', smallInflowRatio: '4.28%' },
                { name: '电源', change: '1.92%', mainInflow: '0.33亿', mainInflowRatio: '0.13%', smallInflow: '2.46亿', smallInflowRatio: '1.00%' },
                { name: '通用设备', change: '1.91%', mainInflow: '10.26亿', mainInflowRatio: '2.76%', smallInflow: '-2.34亿', smallInflowRatio: '-0.63%' },
                // 添加更多行业板块数据
                { name: '半导体', change: '1.85%', mainInflow: '15.67亿', mainInflowRatio: '4.21%', smallInflow: '-3.45亿', smallInflowRatio: '-1.23%' },
                { name: '计算机', change: '1.72%', mainInflow: '8.92亿', mainInflowRatio: '2.15%', smallInflow: '2.34亿', smallInflowRatio: '0.87%' },
                { name: '医药生物', change: '1.65%', mainInflow: '6.78亿', mainInflowRatio: '1.89%', smallInflow: '1.23亿', smallInflowRatio: '0.45%' },
                { name: '新能源', change: '1.58%', mainInflow: '12.34亿', mainInflowRatio: '3.45%', smallInflow: '-2.11亿', smallInflowRatio: '-0.78%' },
                { name: '汽车', change: '1.45%', mainInflow: '9.87亿', mainInflowRatio: '2.76%', smallInflow: '1.89亿', smallInflowRatio: '0.92%' },
                { name: '银行', change: '1.32%', mainInflow: '5.67亿', mainInflowRatio: '1.56%', smallInflow: '0.98亿', smallInflowRatio: '0.34%' },
                { name: '保险', change: '1.25%', mainInflow: '4.32亿', mainInflowRatio: '1.23%', smallInflow: '0.76亿', smallInflowRatio: '0.28%' },
                { name: '房地产', change: '1.18%', mainInflow: '3.45亿', mainInflowRatio: '1.05%', smallInflow: '0.54亿', smallInflowRatio: '0.21%' },
                { name: '煤炭', change: '1.05%', mainInflow: '2.78亿', mainInflowRatio: '0.98%', smallInflow: '0.34亿', smallInflowRatio: '0.15%' },
                { name: '钢铁', change: '0.98%', mainInflow: '2.12亿', mainInflowRatio: '0.87%', smallInflow: '0.23亿', smallInflowRatio: '0.12%' },
                { name: '有色', change: '0.85%', mainInflow: '1.98亿', mainInflowRatio: '0.76%', smallInflow: '0.19亿', smallInflowRatio: '0.10%' }
            ],
            // 分页相关
            currentPage: 1,
            pageSize: 10,
            totalSectors: 0,
            indicesList: [
                { name: '上证指数', value: '4025.35', change: '+0.24%' },
                { name: '深证指数', value: '13938.09', change: '+0.62%' },
                { name: '创业板指', value: '3285.58', change: '+0.66%' },
                { name: '恒生指数', value: '26422.42', change: '-0.12%' },
                { name: '富时中国A50', value: '14640.49', change: '-0.08%' },
                { name: '日经指数', value: '54201.01', change: '+2.94%' },
                { name: '韩国首尔综合指数', value: '5195.56', change: '+4.97%' },
                { name: '纳斯达克', value: '25992.11', change: '+0.05%' },
                { name: '道琼斯', value: '49407.66', change: '+1.05%' },
                { name: '标普500', value: '6976.44', change: '+0.54%' },
                { name: '富时加拿大指数', value: '1298.34', change: '+0.53%' },
                { name: '富时巴西指数', value: '209999.49', change: '-2.54%' },
                { name: '富时巴基斯坦指数', value: '4608.27', change: '+0.68%' }
            ],
            indicesChart: null,
            goldChart: null,
            realTimeGoldChart: null,
            volumeTrendChart: null,
            shanghaiIndexChart: null,
            goldHistoryChart: null
        };
    },
    computed: {
        // 计算当前页显示的行业板块数据
        currentSectorsList() {
            if (!this.sectorsList) {
                return [];
            }
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.sectorsList.slice(start, end);
        },
        // 计算当前页显示的基金列表数据（按基金代码升序排序）
        currentFundsList() {
            if (!this.fundsList) {
                return [];
            }
            // 按基金代码升序排序
            const sortedFunds = [...this.fundsList].sort((a, b) => {
                return a.fund_code.localeCompare(b.fund_code);
            });
            // 计算总基金数
            this.totalFunds = sortedFunds.length;
            // 计算当前页数据
            const start = (this.currentFundPage - 1) * this.fundPageSize;
            const end = start + this.fundPageSize;
            return sortedFunds.slice(start, end);
        }
    },
    watch: {
        // 监听tab页切换事件，重新加载对应的数据
        activeTab(newTab) {
            console.log('切换到tab页:', newTab);
            switch(newTab) {
                case 'news':
                    this.fetchNewsList();
                    break;
                case 'funds':
                    this.loadFundsList();
                    this.loadTotalInfo();
                    break;
                case 'indices':
                    this.loadIndicesData();
                    break;
                case 'gold':
                    this.loadGoldData();
                    this.loadGoldHistoryData();
                    break;
                case 'realTimeGold':
                    this.loadRealTimeGoldData();
                    break;
                case 'goldHistory':
                    this.loadGoldHistoryData();
                    break;
                case 'sectors':
                    this.loadSectorsData();
                    break;
                case 'volume':
                    this.loadVolumeTrendData();
                    break;
                case 'shanghai':
                    this.loadShanghaiIndexData();
                    break;
                case 'sector-fund':
                    // 板块基金查询页不需要自动加载数据，需要用户点击板块标签
                    break;
            }
        }
    },
    mounted() {
        console.log('Vue应用开始挂载');
        // 直接设置全球指数数据
        this.indicesList = [
            { name: '上证指数', value: '4025.35', change: '+0.24%' },
            { name: '深证指数', value: '13938.09', change: '+0.62%' },
            { name: '创业板指', value: '3285.58', change: '+0.66%' },
            { name: '恒生指数', value: '26422.42', change: '-0.12%' },
            { name: '富时中国A50', value: '14640.49', change: '-0.08%' },
            { name: '日经指数', value: '54201.01', change: '+2.94%' },
            { name: '韩国首尔综合指数', value: '5195.56', change: '+4.97%' },
            { name: '纳斯达克', value: '25992.11', change: '+0.05%' },
            { name: '道琼斯', value: '49407.66', change: '+1.05%' },
            { name: '标普500', value: '6976.44', change: '+0.54%' },
            { name: '富时加拿大指数', value: '1298.34', change: '+0.53%' },
            { name: '富时巴西指数', value: '209999.49', change: '-2.54%' },
            { name: '富时巴基斯坦指数', value: '4608.27', change: '+0.68%' }
        ];
        console.log('全球指数数据已设置:', this.indicesList);
        
        // 加载新闻列表
        console.log('准备加载新闻列表');
        this.fetchNewsList();
        // 加载基金列表
        console.log('准备加载基金列表');
        this.loadFundsList();
        // 加载总持仓信息
        console.log('准备加载总持仓信息');
        this.loadTotalInfo();
        // 初始化图表
        console.log('准备初始化图表');
        this.initCharts();
        // 加载市场数据
        console.log('准备加载市场数据');
        this.loadMarketData();
        
        // 设置新闻自动刷新定时器，每30秒刷新一次
        console.log('准备设置新闻自动刷新定时器');
        this.startNewsRefreshTimer();
        console.log('Vue应用挂载完成');
    },
    beforeUnmount() {
        // 清理定时器
        this.clearNewsRefreshTimer();
    },
    methods: {
        // 加载基金列表
        async loadFundsList() {
            this.loading = true;
            try {
                // 检查是否是当天第一次加载且在交易时间段内
                const now = new Date();
                const hour = now.getHours();
                const isTradingHours = hour >= 9 && hour < 16;
                
                if (this.isFirstLoadToday && isTradingHours) {
                    console.log('交易时间段第一次加载，读取盘后更新的数据');
                    try {
                        // 先加载盘后更新的数据
                        const lastFunds = await loadLastFundsList();
                        this.fundsList = lastFunds;
                        console.log('盘后数据加载成功:', lastFunds);
                    } catch (error) {
                        console.error('加载盘后数据失败，使用实时数据:', error);
                        // 如果加载盘后数据失败，使用实时数据
                        const funds = await loadFundsList();
                        this.fundsList = funds;
                    } finally {
                        // 更新标志，当天后续不再使用盘后数据
                        this.isFirstLoadToday = false;
                    }
                } else {
                    console.log('非首次加载或非交易时间段，使用实时数据');
                    // 非首次加载或非交易时间段，使用实时数据
                    const funds = await loadFundsList();
                    this.fundsList = funds;
                }
            } catch (error) {
                console.error('加载基金列表失败:', error);
                this.$message.error('加载基金列表失败');
            } finally {
                this.loading = false;
            }
        },
        
        // 刷新基金列表
        async refreshFundList() {
            await this.loadFundsList();
            await this.loadTotalInfo();
            this.$message.success('基金列表已刷新');
        },
        
        // 加载总持仓信息
        async loadTotalInfo() {
            try {
                console.log('开始加载总持仓信息');
                const totalInfo = await fetchTotalInfo();
                console.log('获取到总持仓信息:', totalInfo);
                console.log('totalInfo类型:', typeof totalInfo);
                console.log('totalInfo是否为对象:', totalInfo && typeof totalInfo === 'object');
                this.totalInfo = totalInfo;
                console.log('更新后totalInfo:', this.totalInfo);
                this.$forceUpdate();
                console.log('强制更新后');
            } catch (error) {
                console.error('加载总持仓信息失败:', error);
                console.error('错误详情:', error.message);
                console.error('错误堆栈:', error.stack);
            }
        },
        
        // 添加基金
        async addFund() {
            if (!this.fundForm.fundCode) {
                this.$message.warning('请输入基金代码');
                return;
            }
            
            try {
                await addFund(this.fundForm.fundCode);
                this.$message.success('添加基金成功');
                // 重新加载基金列表
                this.loadFundsList();
            } catch (error) {
                console.error('添加基金失败:', error);
                this.$message.error('添加基金失败');
            }
        },
        
        // 删除基金
        async deleteFund(fundCode) {
            try {
                await deleteFund(fundCode);
                this.$message.success('删除基金成功');
                // 重新加载基金列表
                this.loadFundsList();
            } catch (error) {
                console.error('删除基金失败:', error);
                this.$message.error('删除基金失败');
            }
        },
        
        // 设置持有金额
        async setHoldAmount() {
            if (!this.fundForm.fundCode || !this.fundForm.holdAmount) {
                this.$message.warning('请输入基金代码和持有金额');
                return;
            }
            
            try {
                await setHoldAmount(this.fundForm.fundCode, parseFloat(this.fundForm.holdAmount));
                this.$message.success('设置持有金额成功');
                // 重新加载基金列表和总持仓信息
                this.loadFundsList();
                this.loadTotalInfo();
            } catch (error) {
                console.error('设置持有金额失败:', error);
                this.$message.error('设置持有金额失败');
            }
        },
        
        // 查看基金详情
        async viewFundDetail(fundCode) {
            try {
                console.log('开始获取基金历史净值数据:', fundCode);
                // 获取基金历史净值数据
                const fundData = await viewFundDetail(fundCode);
                console.log('获取数据成功:', fundData);
                
                const fundInfo = fundData.fund_info;
                const historyData = fundData.history_data;
                
                console.log('基金信息:', fundInfo);
                console.log('历史数据:', historyData);
                
                // 准备图表数据
                const dates = historyData.map(item => item.date).reverse();
                const unitNavs = historyData.map(item => parseFloat(item.unit_nav)).reverse();
                const growthRates = historyData.map(item => {
                    const rate = item.daily_growth.replace('%', '');
                    return parseFloat(rate);
                }).reverse();
                
                // 将数据转换为JSON字符串
                const chartDataJson = JSON.stringify({
                    dates: dates,
                    unitNavs: unitNavs,
                    growthRates: growthRates
                });
                
                // 创建新标签页的HTML内容
                const htmlContent = `
                    <!DOCTYPE html>
                    <html lang="zh-CN">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>基金历史净值 - ${fundInfo.fund_name || fundCode}</title>
                        <style>
                            * {
                                margin: 0;
                                padding: 0;
                                box-sizing: border-box;
                            }
                            body {
                                font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
                                background-color: #f5f7fa;
                                color: #303133;
                                padding: 20px;
                            }
                            .container {
                                max-width: 1000px;
                                margin: 0 auto;
                                background-color: white;
                                border-radius: 8px;
                                box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
                                padding: 20px;
                            }
                            h1 {
                                font-size: 24px;
                                font-weight: 600;
                                margin-bottom: 20px;
                                color: #409EFF;
                            }
                            .info-section {
                                margin-bottom: 30px;
                                padding-bottom: 20px;
                                border-bottom: 1px solid #f0f0f0;
                            }
                            .info-grid {
                                display: grid;
                                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                                gap: 15px;
                            }
                            .info-item {
                                padding: 10px;
                                background-color: #f9f9f9;
                                border-radius: 4px;
                            }
                            .info-label {
                                font-size: 12px;
                                color: #606266;
                                margin-bottom: 5px;
                            }
                            .info-value {
                                font-size: 16px;
                                font-weight: 500;
                                color: #303133;
                            }
                            .profit-positive {
                                color: #F56C6C;
                            }
                            .profit-negative {
                                color: #67C23A;
                            }
                            .chart-section {
                                margin-bottom: 30px;
                            }
                            .chart-title {
                                font-size: 16px;
                                font-weight: 500;
                                margin-bottom: 15px;
                                color: #409EFF;
                            }
                            .chart-container {
                                width: 100%;
                                height: 400px;
                                margin-bottom: 30px;
                            }
                            .table-section {
                                overflow-x: auto;
                            }
                            table {
                                width: 100%;
                                border-collapse: collapse;
                                margin-bottom: 20px;
                            }
                            th, td {
                                padding: 12px;
                                text-align: left;
                                border-bottom: 1px solid #f0f0f0;
                            }
                            th {
                                background-color: #f5f7fa;
                                font-weight: 600;
                                color: #606266;
                            }
                            tr:hover {
                                background-color: #f9f9f9;
                            }
                            .back-btn {
                                margin-top: 20px;
                                padding: 8px 16px;
                                background-color: #409EFF;
                                color: white;
                                border: none;
                                border-radius: 4px;
                                cursor: pointer;
                                font-size: 14px;
                            }
                            .back-btn:hover {
                                background-color: #66b1ff;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>基金历史净值 - ${fundInfo.fund_name || fundCode}</h1>
                            
                            <!-- 基金基本信息 -->
                            <div class="info-section">
                                <div class="info-grid">
                                    <div class="info-item">
                                        <div class="info-label">基金代码</div>
                                        <div class="info-value">${fundInfo.fund_code || fundCode}</div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">基金名称</div>
                                        <div class="info-value">${fundInfo.fund_name || 'N/A'}</div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">估值时间</div>
                                        <div class="info-value">${fundInfo.now_time || 'N/A'}</div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">估值涨跌幅</div>
                                        <div class="info-value ${fundInfo.forecast_growth && !fundInfo.forecast_growth.includes('-') ? 'profit-positive' : 'profit-negative'}">
                                            ${fundInfo.forecast_growth || 'N/A'}
                                        </div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">日涨幅</div>
                                        <div class="info-value ${fundInfo.day_of_growth && !fundInfo.day_of_growth.includes('-') ? 'profit-positive' : 'profit-negative'}">
                                            ${fundInfo.day_of_growth || 'N/A'}
                                        </div>
                                    </div>
                                    <div class="info-item">
                                        <div class="info-label">当前净值</div>
                                        <div class="info-value">${fundInfo.current_net_value || 'N/A'}</div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- 净值走势图表 -->
                            <div class="chart-section">
                                <div class="chart-title">净值走势图</div>
                                <div class="chart-container" id="navChart"></div>
                            </div>
                            
                            <!-- 涨跌幅图表 -->
                            <div class="chart-section">
                                <div class="chart-title">日涨跌幅走势图</div>
                                <div class="chart-container" id="growthChart"></div>
                            </div>
                            
                            <!-- 历史净值表格 -->
                            <div class="table-section">
                                <h2 style="font-size: 18px; margin-bottom: 15px; color: #409EFF;">历史净值数据</h2>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>日期</th>
                                            <th>单位净值</th>
                                            <th>累计净值</th>
                                            <th>日涨跌幅</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${historyData.map(item => `
                                            <tr>
                                                <td>${item.date}</td>
                                                <td>${item.unit_nav}</td>
                                                <td>${item.cumulative_nav}</td>
                                                <td class="${item.daily_growth && !item.daily_growth.includes('-') ? 'profit-positive' : 'profit-negative'}">
                                                    ${item.daily_growth}
                                                </td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                            
                            <button class="back-btn" onclick="window.close()">关闭</button>
                        </div>
                        
                        <!-- 内嵌 echarts 库 -->
                        <script>
                            // 简化版的图表实现，使用原生Canvas
                            function initSimpleCharts(dates, unitNavs, growthRates) {
                                console.log('初始化简化版图表');
                                
                                // 绘制净值走势图
                                const navCanvas = document.createElement('canvas');
                                navCanvas.width = 800;
                                navCanvas.height = 300;
                                navCanvas.style.border = '1px solid #e0e0e0';
                                navCanvas.style.backgroundColor = '#fafafa';
                                
                                const navChartContainer = document.getElementById('navChart');
                                if (navChartContainer) {
                                    navChartContainer.innerHTML = '';
                                    navChartContainer.appendChild(navCanvas);
                                    
                                    const navCtx = navCanvas.getContext('2d');
                                    const navChartData = { dates, values: unitNavs, title: '单位净值' };
                                    drawLineChart(navCtx, navChartData);
                                }
                                
                                // 绘制涨跌幅走势图
                                const growthCanvas = document.createElement('canvas');
                                growthCanvas.width = 800;
                                growthCanvas.height = 300;
                                growthCanvas.style.border = '1px solid #e0e0e0';
                                growthCanvas.style.backgroundColor = '#fafafa';
                                
                                const growthChartContainer = document.getElementById('growthChart');
                                if (growthChartContainer) {
                                    growthChartContainer.innerHTML = '';
                                    growthChartContainer.appendChild(growthCanvas);
                                    
                                    const growthCtx = growthCanvas.getContext('2d');
                                    const growthChartData = { dates, values: growthRates, title: '日涨跌幅(%)' };
                                    drawBarChart(growthCtx, growthChartData);
                                }
                            }
                            
                            function drawLineChart(ctx, chartData) {
                                const { dates, values, title } = chartData;
                                const width = ctx.canvas.width;
                                const height = ctx.canvas.height;
                                const padding = 40;
                                
                                // 清空画布
                                ctx.clearRect(0, 0, width, height);
                                
                                // 绘制标题
                                ctx.font = '14px Arial';
                                ctx.fillStyle = '#333';
                                ctx.textAlign = 'center';
                                ctx.fillText(title, width / 2, 20);
                                
                                // 计算数据范围
                                const minValue = Math.min(...values);
                                const maxValue = Math.max(...values);
                                const valueRange = maxValue - minValue;
                                
                                // 计算坐标转换
                                const xScale = (width - 2 * padding) / (dates.length - 1);
                                const yScale = (height - 2 * padding) / (valueRange || 1);
                                
                                // 绘制坐标轴
                                ctx.strokeStyle = '#ccc';
                                ctx.lineWidth = 1;
                                
                                // X轴
                                ctx.beginPath();
                                ctx.moveTo(padding, height - padding);
                                ctx.lineTo(width - padding, height - padding);
                                ctx.stroke();
                                
                                // Y轴
                                ctx.beginPath();
                                ctx.moveTo(padding, padding);
                                ctx.lineTo(padding, height - padding);
                                ctx.stroke();
                                
                                // 绘制数据点和连线
                                ctx.strokeStyle = '#409EFF';
                                ctx.fillStyle = '#409EFF';
                                ctx.lineWidth = 2;
                                
                                ctx.beginPath();
                                for (let i = 0; i < dates.length; i++) {
                                    const x = padding + i * xScale;
                                    const y = height - padding - (values[i] - minValue) * yScale;
                                    
                                    if (i === 0) {
                                        ctx.moveTo(x, y);
                                    } else {
                                        ctx.lineTo(x, y);
                                    }
                                    
                                    // 绘制数据点
                                    ctx.beginPath();
                                    ctx.arc(x, y, 3, 0, Math.PI * 2);
                                    ctx.fill();
                                    ctx.closePath();
                                }
                                ctx.stroke();
                                
                                // 绘制日期标签
                                ctx.font = '10px Arial';
                                ctx.fillStyle = '#666';
                                ctx.textAlign = 'center';
                                
                                const labelInterval = Math.max(1, Math.floor(dates.length / 10));
                                for (let i = 0; i < dates.length; i += labelInterval) {
                                    const x = padding + i * xScale;
                                    ctx.fillText(dates[i], x, height - padding + 15);
                                }
                            }
                            
                            function drawBarChart(ctx, chartData) {
                                const { dates, values, title } = chartData;
                                const width = ctx.canvas.width;
                                const height = ctx.canvas.height;
                                const padding = 40;
                                
                                // 清空画布
                                ctx.clearRect(0, 0, width, height);
                                
                                // 绘制标题
                                ctx.font = '14px Arial';
                                ctx.fillStyle = '#333';
                                ctx.textAlign = 'center';
                                ctx.fillText(title, width / 2, 20);
                                
                                // 计算数据范围
                                const maxAbsValue = Math.max(...values.map(v => Math.abs(v)));
                                
                                // 计算坐标转换
                                const barWidth = (width - 2 * padding) / dates.length * 0.6;
                                const yScale = (height - 2 * padding) / (2 * maxAbsValue || 1);
                                
                                // 绘制坐标轴
                                ctx.strokeStyle = '#ccc';
                                ctx.lineWidth = 1;
                                
                                // X轴
                                ctx.beginPath();
                                ctx.moveTo(padding, height - padding);
                                ctx.lineTo(width - padding, height - padding);
                                ctx.stroke();
                                
                                // Y轴
                                ctx.beginPath();
                                ctx.moveTo(padding, padding);
                                ctx.lineTo(padding, height - padding);
                                ctx.stroke();
                                
                                // 绘制零线
                                ctx.strokeStyle = '#999';
                                ctx.setLineDash([5, 5]);
                                ctx.beginPath();
                                ctx.moveTo(padding, height / 2);
                                ctx.lineTo(width - padding, height / 2);
                                ctx.stroke();
                                ctx.setLineDash([]);
                                
                                // 绘制柱状图
                                for (let i = 0; i < dates.length; i++) {
                                    const x = padding + i * (barWidth * 1.2) + barWidth * 0.1;
                                    const barHeight = Math.abs(values[i]) * yScale;
                                    const y = values[i] >= 0 ? height / 2 - barHeight : height / 2;
                                    
                                    // 设置颜色
                                    ctx.fillStyle = values[i] >= 0 ? '#F56C6C' : '#67C23A';
                                    
                                    // 绘制柱子
                                    ctx.fillRect(x, y, barWidth, barHeight);
                                }
                                
                                // 绘制日期标签
                                ctx.font = '10px Arial';
                                ctx.fillStyle = '#666';
                                ctx.textAlign = 'center';
                                
                                const labelInterval = Math.max(1, Math.floor(dates.length / 10));
                                for (let i = 0; i < dates.length; i += labelInterval) {
                                    const x = padding + i * (barWidth * 1.2) + barWidth * 0.5;
                                    ctx.fillText(dates[i], x, height - padding + 15);
                                }
                            }
                        </script>
                        
                        <script>
                            // 图表数据
                            var chartData = JSON.parse('${chartDataJson}');
                            var dates = chartData.dates;
                            var unitNavs = chartData.unitNavs;
                            var growthRates = chartData.growthRates;
                            
                            // 初始化图表函数
                            function initCharts() {
                                console.log('开始初始化图表');
                                console.log('日期数据:', dates);
                                console.log('净值数据:', unitNavs);
                                console.log('涨跌幅数据:', growthRates);
                                
                                // 检查DOM元素
                                console.log('navChart元素:', document.getElementById('navChart'));
                                console.log('growthChart元素:', document.getElementById('growthChart'));
                                
                                // 使用简化版Canvas图表
                                try {
                                    initSimpleCharts(dates, unitNavs, growthRates);
                                    console.log('图表初始化成功');
                                } catch (error) {
                                    console.error('图表初始化失败:', error);
                                }
                            }
                            
                            // 当DOM加载完成后初始化图表
                            if (document.readyState === 'loading') {
                                document.addEventListener('DOMContentLoaded', initCharts);
                            } else {
                                initCharts();
                            }
                        </script>
                    </body>
                    </html>
                `;
                
                // 创建Blob对象
                const blob = new Blob([htmlContent], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                
                // 打开新标签页
                window.open(url, '_blank');
            } catch (error) {
                console.error('获取基金历史净值失败:', error);
                this.$message.error('获取基金历史净值失败');
            }
        },
        
        // 初始化图表
        initCharts() {
            try {
                // 使用导入的工具函数初始化图表
                const charts = initCharts();
                // 保存图表实例到Vue组件的data中
                this.indicesChart = charts.indicesChart;
                this.realTimeGoldChart = charts.realTimeGoldChart;
                this.volumeTrendChart = charts.volumeTrendChart;
                this.shanghaiIndexChart = charts.shanghaiIndexChart;
                this.goldHistoryChart = charts.goldHistoryChart;
                console.log('图表初始化成功:', charts);
            } catch (error) {
                console.error('图表初始化失败:', error);
                // 即使图表初始化失败，也不影响其他功能
            }
        },
        
        // 加载市场数据
        async loadMarketData() {
            console.log('开始加载市场数据');
            // 加载全球指数数据
            console.log('准备加载全球指数数据');
            this.loadIndicesData();
            
            // 加载贵金属数据
            console.log('准备加载贵金属数据');
            this.loadGoldData();
            
            // 加载行业板块数据
            console.log('准备加载行业板块数据');
            this.loadSectorsData();
            
            // 实时贵金属数据将在用户点击标签页时加载
            console.log('实时贵金属数据将在用户点击标签页时加载');
            // 加载成交量趋势数据
            console.log('准备加载成交量趋势数据');
            this.loadVolumeTrendData();
            // 加载上证分时数据
            console.log('准备加载上证分时数据');
            this.loadShanghaiIndexData();
            // 加载历史金价图表数据
            console.log('准备加载历史金价图表数据');
            this.loadGoldHistoryData();
            console.log('市场数据加载完成');
        },
        
        // 加载全球指数数据
        async loadIndicesData() {
            try {
                const indices = await loadIndicesData();
                this.indicesList = indices;
                console.log('全球指数数据加载成功:', indices);
            } catch (error) {
                console.error('加载全球指数数据失败:', error);
            }
        },
        
        // 加载贵金属数据
        async loadGoldData() {
            try {
                const goldData = await loadGoldData();
                console.log('贵金属数据加载成功:', goldData);
            } catch (error) {
                console.error('加载贵金属数据失败:', error);
            }
        },
        
        // 加载行业板块数据
        async loadSectorsData() {
            try {
                // 调用后端API获取行业板块数据
                const response = await fetch(`${API_BASE_URL}/sectors`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log('获取到行业板块数据:', data);
                
                // 更新数据
                if (data.sectors) {
                    this.sectorsList = data.sectors;
                    this.totalSectors = data.sectors.length;
                }
            } catch (error) {
                console.error('加载行业板块数据失败:', error);
            }
        },
        
        // 处理基金分页大小变化
        handleFundSizeChange(size) {
            this.fundPageSize = size;
            this.currentFundPage = 1;
        },
        
        // 处理基金分页当前页变化
        handleFundCurrentChange(current) {
            this.currentFundPage = current;
        },
        
        // 加载历史金价图表数据
        async loadGoldHistoryData() {
            try {
                // 检查echarts是否存在
                if (typeof echarts === 'undefined') {
                    console.warn('echarts库未加载，跳过历史金价图表数据加载');
                    return;
                }
                
                // 确保DOM元素存在
                const goldHistoryElement = document.getElementById('goldHistoryChart');
                if (!goldHistoryElement) {
                    // 当元素不存在时，静默返回，不输出错误信息
                    return;
                }
                
                // 重新初始化图表
                this.goldHistoryChart = echarts.init(goldHistoryElement);
                
                // 从goldHistoryData数组中提取数据
                const dates = [];
                const chinaGoldFundPrices = [];
                const chowTaiFookPrices = [];
                
                // 按日期升序排序
                const sortedData = [...this.goldHistoryData].sort((a, b) => {
                    return new Date(a.date) - new Date(b.date);
                });
                
                for (const item of sortedData) {
                    dates.push(item.date);
                    chinaGoldFundPrices.push(parseFloat(item.chinaGoldFundPrice));
                    chowTaiFookPrices.push(parseFloat(item.chowTaiFookPrice));
                }
                
                // 设置图表选项
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        formatter: function(params) {
                            let result = params[0].name + '<br/>';
                            params.forEach(function(item) {
                                result += item.marker + item.seriesName + ': ' + item.value + '<br/>';
                            });
                            return result;
                        }
                    },
                    legend: {
                        data: ['中国黄金基金金价', '周大福金价'],
                        top: 10
                    },
                    grid: {
                        left: '2%',
                        right: '2%',
                        bottom: '15%',
                        top: '20%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: dates,
                        axisLabel: {
                            rotate: 45,
                            interval: 0,
                            fontSize: 10
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        axisLine: {
                            show: true
                        }
                    },
                    yAxis: {
                        type: 'value',
                        scale: true,
                        axisLabel: {
                            formatter: '{value}'
                        }
                    },
                    series: [
                        {
                            name: '中国黄金基金金价',
                            type: 'line',
                            data: chinaGoldFundPrices,
                            lineStyle: {
                                color: '#FFD700',
                                width: 2
                            },
                            itemStyle: {
                                color: '#FFD700',
                                borderWidth: 2,
                                borderColor: '#fff'
                            },
                            areaStyle: {
                                color: 'rgba(255, 215, 0, 0.3)'
                            }
                        },
                        {
                            name: '周大福金价',
                            type: 'line',
                            data: chowTaiFookPrices,
                            lineStyle: {
                                color: '#E91E63',
                                width: 2
                            },
                            itemStyle: {
                                color: '#E91E63',
                                borderWidth: 2,
                                borderColor: '#fff'
                            },
                            areaStyle: {
                                color: 'rgba(233, 30, 99, 0.3)'
                            }
                        }
                    ]
                };
                
                if (this.goldHistoryChart) {
                    this.goldHistoryChart.setOption(option);
                }
            } catch (error) {
                // 静默处理错误，不输出错误信息
                console.debug('加载历史金价图表数据失败:', error);
            }
        },
        
        // 加载新闻列表
        async fetchNewsList() {
            try {
                // 调用导入的loadNewsList函数获取新闻数据
                const news = await loadNewsList();
                this.newsList = news;
            } catch (error) {
                console.error('加载新闻列表失败:', error);
                this.newsList = [];
            }
        },
        
        // 启动新闻刷新定时器
        startNewsRefreshTimer() {
            // 清除之前的定时器
            this.clearNewsRefreshTimer();
            
            // 设置新的定时器，每30秒刷新一次新闻
            this.newsRefreshTimer = setInterval(() => {
                // 只有当当前激活的标签页是新闻页时才刷新
                if (this.activeTab === 'news') {
                    this.fetchNewsList();
                }
            }, 30000); // 30秒
        },
        
        // 清除新闻刷新定时器
        clearNewsRefreshTimer() {
            if (this.newsRefreshTimer) {
                clearInterval(this.newsRefreshTimer);
                this.newsRefreshTimer = null;
            }
        },
        
        // 加载实时贵金属数据
        async loadRealTimeGoldData() {
            console.log('开始加载实时贵金属数据');
            console.log('当前realTimeGoldData值:', this.realTimeGoldData);
            console.log('当前this对象:', this);
            
            try {
                // 检查echarts是否存在
                if (typeof echarts === 'undefined' || !this.realTimeGoldChart) {
                    console.warn('echarts库未加载或图表未初始化，只加载数据不初始化图表');
                }
                
                // 使用marketService.js中的loadRealTimeGoldData函数
                console.log('准备调用marketService中的loadRealTimeGoldData函数');
                const goldData = await loadRealTimeGoldData();
                console.log('获取到实时贵金属数据:', goldData);
                console.log('数据类型:', typeof goldData);
                console.log('数据长度:', Array.isArray(goldData) ? goldData.length : '不是数组');
                
                // 更新数据
                console.log('准备更新realTimeGoldData');
                this.realTimeGoldData = goldData || [];
                console.log('更新后的数据:', this.realTimeGoldData);
                console.log('更新后的数据长度:', Array.isArray(this.realTimeGoldData) ? this.realTimeGoldData.length : 0);
                
                // 强制Vue更新
                this.$forceUpdate();
                console.log('强制Vue更新后');
                
                // 准备图表数据
                if (this.realTimeGoldChart && Array.isArray(goldData) && goldData.length > 0) {
                    try {
                        const option = {
                            tooltip: {
                                trigger: 'axis'
                            },
                            legend: {
                                data: goldData.map(item => item.name || "未知金属")
                            },
                            grid: {
                                left: '3%',
                                right: '4%',
                                bottom: '3%',
                                containLabel: true
                            },
                            xAxis: {
                                type: 'category',
                                boundaryGap: false,
                                data: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00']
                            },
                            yAxis: {
                                type: 'value'
                            },
                            series: goldData.map((item, index) => {
                                // 生成模拟的时间序列数据
                                const basePrice = parseFloat(item.price) || 1000;
                                const priceData = [];
                                for (let i = 0; i < 7; i++) {
                                    // 生成围绕基准价格的随机波动
                                    const randomChange = (Math.random() - 0.5) * 20;
                                    priceData.push(basePrice + randomChange);
                                }
                                
                                // 为不同金属使用不同颜色
                                const colors = ['#FFD700', '#C0C0C0', '#E5E4E2'];
                                
                                return {
                                    name: item.name || "未知金属",
                                    type: 'line',
                                    data: priceData,
                                    lineStyle: {
                                        color: colors[index % colors.length]
                                    }
                                };
                            })
                        };
                        
                        this.realTimeGoldChart.setOption(option);
                        console.log('图表数据已更新');
                    } catch (chartError) {
                        console.error('更新图表数据失败:', chartError);
                    }
                }
            } catch (error) {
                console.error('加载实时贵金属数据失败:', error);
                console.error('错误详情:', error.message);
                console.error('错误堆栈:', error.stack);
                
                // 检查是否是网络错误
                if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                    console.error('网络错误：无法连接到后端API，请检查后端服务是否运行');
                }
                
                // 使用默认数据
                console.log('准备使用默认数据');
                this.realTimeGoldData = [
                    {
                        "name": "黄金9999",
                        "price": "1964.9",
                        "change": "34.0",
                        "change_rate": "1.76%",
                        "open": "1919.8",
                        "high": "1989.99",
                        "low": "1980.9",
                        "prev_close": "1930.9",
                        "update_time": new Date().toLocaleString(),
                        "unit": "元/克"
                    },
                    {
                        "name": "现货黄金",
                        "price": "4795.39",
                        "change": "180.84",
                        "change_rate": "3.91%",
                        "open": "4670.61",
                        "high": "4855.15",
                        "low": "4664.74",
                        "prev_close": "4633.35",
                        "update_time": new Date().toLocaleString(),
                        "unit": "美元/盎司"
                    },
                    {
                        "name": "现货白银",
                        "price": "81.27",
                        "change": "2.13",
                        "change_rate": "2.69%",
                        "open": "79.19",
                        "high": "85.65",
                        "low": "79.19",
                        "prev_close": "79.15",
                        "update_time": new Date().toLocaleString(),
                        "unit": "美元/盎司"
                    }
                ];
                console.log('使用默认数据:', this.realTimeGoldData);
                
                // 强制Vue更新
                this.$forceUpdate();
                console.log('强制Vue更新后');
            }
        },
        
        // 加载成交量趋势数据
        async loadVolumeTrendData() {
            try {
                // 检查echarts是否存在
                if (typeof echarts === 'undefined' || !this.volumeTrendChart) {
                    console.warn('echarts库未加载或图表未初始化，跳过成交量趋势数据加载');
                    return;
                }
                
                // 模拟成交量趋势数据
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            crossStyle: {
                                color: '#999'
                            }
                        }
                    },
                    legend: {
                        data: ['成交量']
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: ['02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07'],
                            axisPointer: {
                                type: 'shadow'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '成交量',
                            min: 0,
                            max: 5000,
                            interval: 1000,
                            axisLabel: {
                                formatter: '{value}亿'
                            }
                        }
                    ],
                    series: [
                        {
                            name: '成交量',
                            type: 'bar',
                            data: [3200, 2800, 3500, 2900, 3100, 3400, 3600],
                            itemStyle: {
                                color: '#409EFF'
                            }
                        }
                    ]
                };
                
                this.volumeTrendChart.setOption(option);
            } catch (error) {
                console.error('加载成交量趋势数据失败:', error);
            }
        },
        
        // 加载上证分时数据
        async loadShanghaiIndexData() {
            try {
                // 检查echarts是否存在
                if (typeof echarts === 'undefined' || !this.shanghaiIndexChart) {
                    console.warn('echarts库未加载或图表未初始化，跳过上证分时数据加载');
                    return;
                }
                
                // 模拟上证分时数据
                const option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['上证指数']
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: ['09:30', '10:00', '10:30', '11:00', '11:30', '13:30', '14:00', '14:30', '15:00']
                    },
                    yAxis: {
                        type: 'value',
                        min: 3990,
                        max: 4030
                    },
                    series: [
                        {
                            name: '上证指数',
                            type: 'line',
                            data: [4000, 4005, 4010, 4008, 4012, 4015, 4020, 4018, 4012],
                            lineStyle: {
                                color: '#F56C6C'
                            },
                            areaStyle: {
                                color: 'rgba(245, 108, 108, 0.3)'
                            }
                        }
                    ]
                };
                
                this.shanghaiIndexChart.setOption(option);
            } catch (error) {
                console.error('加载上证分时数据失败:', error);
            }
        },
        
        // 选择板块
        async selectSector(sectorName) {
            // 立即更新板块名称，让用户看到即时反馈
            this.selectedSector = sectorName;
            // 显示加载状态
            this.sectorLoading = true;
            // 清空现有数据，准备显示新数据
            this.sectorFundsList = [];
            
            try {
                console.log('选择板块:', sectorName);
                // 调用后端API获取板块基金数据
                const response = await fetch(`${API_BASE_URL}/sector?bk_id=${encodeURIComponent(sectorName)}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log('API返回数据:', data);
                
                // 转换数据格式
                this.sectorFundsList = data.results.map(item => {
                    // 确保item是数组且有足够的元素
                    if (!Array.isArray(item) || item.length < 11) {
                        return {
                            fund_code: 'N/A',
                            fund_name: 'N/A',
                            day_of_growth: 'N/A',
                            weekly_growth: 'N/A',
                            monthly_growth_rate: 'N/A',
                            quarterly_growth: 'N/A',
                            half_year_growth: 'N/A',
                            year_to_date_growth: 'N/A',
                            yearly_growth: 'N/A'
                        };
                    }
                    // 尝试提取日涨幅，处理可能的匹配失败和编码问题
                    let dayOfGrowth = 'N/A';
                    try {
                        // 处理编码问题，替换可能的乱码字符
                        const cleanedString = item[4].replace(/[ï¼]/g, '');
                        // 使用更宽松的正则表达式匹配涨跌幅
                        const match = cleanedString.match(/[-+]?\d+(?:\.\d+)?%/);
                        if (match && match[0]) {
                            dayOfGrowth = match[0];
                        }
                    } catch (e) {
                        console.error('解析日涨幅失败:', e);
                    }
                    return {
                        fund_code: item[0] || 'N/A',
                        fund_name: item[1] || 'N/A',
                        day_of_growth: dayOfGrowth,
                        weekly_growth: item[5] || 'N/A',
                        monthly_growth_rate: item[6] || 'N/A',
                        quarterly_growth: item[7] || 'N/A',
                        half_year_growth: item[8] || 'N/A',
                        year_to_date_growth: item[9] || 'N/A',
                        yearly_growth: item[10] || 'N/A'
                    };
                });
                console.log('转换后的数据:', this.sectorFundsList);
            } catch (error) {
                console.error('获取板块基金数据失败:', error);
                // 显示错误提示
                this.$message.error('获取板块基金数据失败，使用默认数据');
                // 根据板块名称使用不同的模拟数据
                this.sectorFundsList = this.getSectorFundsData(sectorName);
            } finally {
                // 数据加载完成，隐藏加载状态
                this.sectorLoading = false;
            }
        },
        
        // 根据板块名称获取模拟基金数据
        getSectorFundsData(sectorName) {
            // 猪肉板块基金
            if (sectorName === '猪肉') {
                return [
                    { 
                        fund_code: '001245', 
                        fund_name: '国泰大农业股票', 
                        day_of_growth: '+1.23%', 
                        weekly_growth: '+3.45%',
                        monthly_growth_rate: '8.92%',
                        quarterly_growth: '15.67%',
                        half_year_growth: '22.34%',
                        year_to_date_growth: '5.67%',
                        yearly_growth: '35.43%'
                    },
                    { 
                        fund_code: '000713', 
                        fund_name: '嘉实农业产业股票', 
                        day_of_growth: '+0.89%', 
                        weekly_growth: '+2.34%',
                        monthly_growth_rate: '7.65%',
                        quarterly_growth: '13.45%',
                        half_year_growth: '19.87%',
                        year_to_date_growth: '4.32%',
                        yearly_growth: '32.15%'
                    },
                    { 
                        fund_code: '161030', 
                        fund_name: '富国中证农业主题ETF联接', 
                        day_of_growth: '+0.67%', 
                        weekly_growth: '+1.89%',
                        monthly_growth_rate: '6.54%',
                        quarterly_growth: '11.23%',
                        half_year_growth: '17.65%',
                        year_to_date_growth: '3.45%',
                        yearly_growth: '28.92%'
                    },
                    { 
                        fund_code: '003634', 
                        fund_name: '鹏华中证畜牧养殖ETF联接', 
                        day_of_growth: '+1.45%', 
                        weekly_growth: '+3.89%',
                        monthly_growth_rate: '9.87%',
                        quarterly_growth: '16.78%',
                        half_year_growth: '24.56%',
                        year_to_date_growth: '6.78%',
                        yearly_growth: '38.76%'
                    },
                    { 
                        fund_code: '005267', 
                        fund_name: '南方中证农业主题ETF联接', 
                        day_of_growth: '+0.56%', 
                        weekly_growth: '+1.67%',
                        monthly_growth_rate: '5.43%',
                        quarterly_growth: '10.12%',
                        half_year_growth: '15.34%',
                        year_to_date_growth: '2.34%',
                        yearly_growth: '25.67%'
                    }
                ];
            }
            // 半导体板块基金
            else if (sectorName === '半导体' || sectorName === '芯片') {
                return [
                    { 
                        fund_code: '025209', 
                        fund_name: '永赢先锋半导体智选混合C', 
                        day_of_growth: '-7.37%', 
                        weekly_growth: '-5.23%',
                        monthly_growth_rate: '24.78%',
                        quarterly_growth: '32.15%',
                        half_year_growth: '45.67%',
                        year_to_date_growth: '15.23%',
                        yearly_growth: '67.89%'
                    },
                    { 
                        fund_code: '005678', 
                        fund_name: '华夏半导体芯片ETF联接', 
                        day_of_growth: '+1.23%', 
                        weekly_growth: '+3.45%',
                        monthly_growth_rate: '18.92%',
                        quarterly_growth: '29.45%',
                        half_year_growth: '42.34%',
                        year_to_date_growth: '15.67%',
                        yearly_growth: '62.34%'
                    },
                    { 
                        fund_code: '159813', 
                        fund_name: '鹏华国证半导体芯片ETF', 
                        day_of_growth: '-6.54%', 
                        weekly_growth: '-4.32%',
                        monthly_growth_rate: '21.34%',
                        quarterly_growth: '28.76%',
                        half_year_growth: '40.12%',
                        year_to_date_growth: '13.45%',
                        yearly_growth: '58.92%'
                    },
                    { 
                        fund_code: '008887', 
                        fund_name: '华夏国证半导体芯片ETF联接', 
                        day_of_growth: '-5.67%', 
                        weekly_growth: '-3.45%',
                        monthly_growth_rate: '19.87%',
                        quarterly_growth: '26.54%',
                        half_year_growth: '38.76%',
                        year_to_date_growth: '11.23%',
                        yearly_growth: '55.67%'
                    }
                ];
            }
            // 新能源板块基金
            else if (sectorName === '新能源') {
                return [
                    { 
                        fund_code: '001475', 
                        fund_name: '易方达国防军工混合', 
                        day_of_growth: '+2.34%', 
                        weekly_growth: '+5.67%',
                        monthly_growth_rate: '12.34%',
                        quarterly_growth: '18.76%',
                        half_year_growth: '25.43%',
                        year_to_date_growth: '8.92%',
                        yearly_growth: '42.34%'
                    },
                    { 
                        fund_code: '002190', 
                        fund_name: '农银汇理新能源主题', 
                        day_of_growth: '+1.89%', 
                        weekly_growth: '+4.32%',
                        monthly_growth_rate: '10.67%',
                        quarterly_growth: '16.54%',
                        half_year_growth: '22.34%',
                        year_to_date_growth: '7.65%',
                        yearly_growth: '38.76%'
                    },
                    { 
                        fund_code: '005939', 
                        fund_name: '工银瑞信新能源汽车', 
                        day_of_growth: '+1.56%', 
                        weekly_growth: '+3.89%',
                        monthly_growth_rate: '9.87%',
                        quarterly_growth: '15.34%',
                        half_year_growth: '20.76%',
                        year_to_date_growth: '6.54%',
                        yearly_growth: '35.43%'
                    }
                ];
            }
            // 默认基金数据
            else {
                return [
                    { 
                        fund_code: '022853', 
                        fund_name: '中航优选领航混合C', 
                        day_of_growth: '-3.33%', 
                        weekly_growth: '-1.23%',
                        monthly_growth_rate: '-0.02%',
                        quarterly_growth: '5.67%',
                        half_year_growth: '12.34%',
                        year_to_date_growth: '3.45%',
                        yearly_growth: '23.45%'
                    },
                    { 
                        fund_code: '001234', 
                        fund_name: '易方达科技创新混合', 
                        day_of_growth: '+2.34%', 
                        weekly_growth: '+5.67%',
                        monthly_growth_rate: '15.67%',
                        quarterly_growth: '25.34%',
                        half_year_growth: '38.76%',
                        year_to_date_growth: '12.34%',
                        yearly_growth: '56.78%'
                    },
                    { 
                        fund_code: '018490', 
                        fund_name: '万家中证工业有色金属主题ETF联接C', 
                        day_of_growth: '-7.50%', 
                        weekly_growth: '-3.12%',
                        monthly_growth_rate: '13.02%',
                        quarterly_growth: '21.45%',
                        half_year_growth: '33.78%',
                        year_to_date_growth: '8.92%',
                        yearly_growth: '45.36%'
                    }
                ];
            }
        },
        
        // 查询板块基金
        async searchSectorFunds() {
            if (!this.sectorForm.sectorName) {
                this.$message.warning('请输入板块名称');
                return;
            }
            
            this.selectedSector = this.sectorForm.sectorName;
            this.sectorLoading = true;
            try {
                // 模拟板块基金数据
                this.sectorFundsList = [
                    { 
                        fund_code: '025209', 
                        fund_name: '永赢先锋半导体智选混合C', 
                        day_of_growth: '-7.37%', 
                        weekly_growth: '-5.23%',
                        monthly_growth_rate: '24.78%',
                        quarterly_growth: '32.15%',
                        half_year_growth: '45.67%',
                        year_to_date_growth: '15.23%',
                        yearly_growth: '67.89%'
                    },
                    { 
                        fund_code: '018490', 
                        fund_name: '万家中证工业有色金属主题ETF联接C', 
                        day_of_growth: '-7.50%', 
                        weekly_growth: '-3.12%',
                        monthly_growth_rate: '13.02%',
                        quarterly_growth: '21.45%',
                        half_year_growth: '33.78%',
                        year_to_date_growth: '8.92%',
                        yearly_growth: '45.36%'
                    },
                    { 
                        fund_code: '022853', 
                        fund_name: '中航优选领航混合C', 
                        day_of_growth: '-3.33%', 
                        weekly_growth: '-1.23%',
                        monthly_growth_rate: '-0.02%',
                        quarterly_growth: '5.67%',
                        half_year_growth: '12.34%',
                        year_to_date_growth: '3.45%',
                        yearly_growth: '23.45%'
                    }
                ];
            } catch (error) {
                console.error('查询板块基金失败:', error);
                this.$message.error('查询板块基金失败');
            } finally {
                this.sectorLoading = false;
            }
        },
        
        // 加载全球指数数据
        async loadIndicesData() {
            console.log('开始加载全球指数数据');
            try {
                // 模拟全球指数数据，与老页面一致
                this.indicesList = [
                    { name: '上证指数', value: '4025.35', change: '+0.24%' },
                    { name: '深证指数', value: '13938.09', change: '+0.62%' },
                    { name: '创业板指', value: '3285.58', change: '+0.66%' },
                    { name: '恒生指数', value: '26422.42', change: '-0.12%' },
                    { name: '富时中国A50', value: '14640.49', change: '-0.08%' },
                    { name: '日经指数', value: '54201.01', change: '+2.94%' },
                    { name: '韩国首尔综合指数', value: '5195.56', change: '+4.97%' },
                    { name: '纳斯达克', value: '25992.11', change: '+0.05%' },
                    { name: '道琼斯', value: '49407.66', change: '+1.05%' },
                    { name: '标普500', value: '6976.44', change: '+0.54%' },
                    { name: '富时加拿大指数', value: '1298.34', change: '+0.53%' },
                    { name: '富时巴西指数', value: '209999.49', change: '-2.54%' },
                    { name: '富时巴基斯坦指数', value: '4608.27', change: '+0.68%' }
                ];
                console.log('全球指数数据加载完成:', this.indicesList);
            } catch (error) {
                console.error('加载全球指数数据失败:', error);
                this.indicesList = [];
            }
        },
        
        // 加载行业板块数据
        async loadSectorsData() {
            try {
                const response = await fetch(`${API_BASE_URL}/sectors`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const sectorsData = await response.json();
                
                // 准备图表数据
                const categories = [];
                const values = [];
                const colors = [];
                
                if (sectorsData.sectors) {
                    for (const sector of sectorsData.sectors) {
                        categories.push(sector.name);
                        const change = parseFloat(sector.change.replace('%', ''));
                        values.push(change);
                        colors.push(change >= 0 ? '#F56C6C' : '#67C23A');
                    }
                }
                
                // 设置图表选项
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                        formatter: function(params) {
                            return params[0].name + '<br/>涨跌幅: ' + params[0].value + '%';
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value}%'
                        }
                    },
                    yAxis: {
                        type: 'category',
                        data: categories
                    },
                    series: [
                        {
                            name: '涨跌幅',
                            type: 'bar',
                            data: values,
                            itemStyle: {
                                color: function(params) {
                                    return colors[params.dataIndex];
                                }
                            },
                            label: {
                                show: true,
                                position: 'right',
                                formatter: '{c}%'
                            }
                        }
                    ]
                };
                
                // 设置图表选项
                if (this.sectorsChart) {
                    this.sectorsChart.setOption(option);
                }
            } catch (error) {
                console.error('加载行业板块数据失败:', error);
            }
        },
        
        // 加载金价数据
        async loadGoldData() {
            try {
                const response = await fetch(`${API_BASE_URL}/gold`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const goldData = await response.json();
                
                // 准备图表数据
                const dates = [];
                const prices = [];
                
                if (goldData.history) {
                    for (const item of goldData.history) {
                        dates.push(item.date);
                        prices.push(parseFloat(item.price));
                    }
                }
                
                // 设置图表选项
                const option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['金价']
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: dates
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            name: '金价',
                            type: 'line',
                            stack: 'Total',
                            data: prices,
                            areaStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    {
                                        offset: 0,
                                        color: 'rgba(131, 191, 246, 0.5)'
                                    },
                                    {
                                        offset: 1,
                                        color: 'rgba(131, 191, 246, 0.1)'
                                    }
                                ])
                            },
                            lineStyle: {
                                color: '#188df0'
                            },
                            itemStyle: {
                                color: '#188df0'
                            }
                        }
                    ]
                };
                
                // 设置图表选项
                if (this.goldChart) {
                    this.goldChart.setOption(option);
                }
            } catch (error) {
                console.error('加载金价数据失败:', error);
            }
        },
        
       
        
        // 加载成交量趋势数据
        async loadVolumeTrendData() {
            try {
                // 模拟成交量趋势数据
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            crossStyle: {
                                color: '#999'
                            }
                        }
                    },
                    legend: {
                        data: ['成交量']
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: ['02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07'],
                            axisPointer: {
                                type: 'shadow'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '成交量',
                            min: 0,
                            max: 5000,
                            interval: 1000,
                            axisLabel: {
                                formatter: '{value}亿'
                            }
                        }
                    ],
                    series: [
                        {
                            name: '成交量',
                            type: 'bar',
                            data: [3200, 2800, 3500, 2900, 3100, 3400, 3600],
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    {
                                        offset: 0,
                                        color: '#83bff6'
                                    },
                                    {
                                        offset: 0.5,
                                        color: '#188df0'
                                    },
                                    {
                                        offset: 1,
                                        color: '#188df0'
                                    }
                                ])
                            }
                        }
                    ]
                };
                
                if (this.volumeTrendChart) {
                    this.volumeTrendChart.setOption(option);
                }
            } catch (error) {
                console.error('加载成交量趋势数据失败:', error);
            }
        },
        
        // 加载上证分时数据
        async loadShanghaiIndexData() {
            try {
                // 模拟上证分时数据
                const option = {
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['上证指数']
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: ['09:30', '10:00', '10:30', '11:00', '11:30', '13:30', '14:00', '14:30', '15:00']
                    },
                    yAxis: {
                        type: 'value',
                        min: 3990,
                        max: 4030
                    },
                    series: [
                        {
                            name: '上证指数',
                            type: 'line',
                            data: [4000, 4005, 4010, 4008, 4012, 4015, 4020, 4018, 4012],
                            lineStyle: {
                                color: '#F56C6C'
                            },
                            areaStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    {
                                        offset: 0,
                                        color: 'rgba(245, 108, 108, 0.5)'
                                    },
                                    {
                                        offset: 1,
                                        color: 'rgba(245, 108, 108, 0.1)'
                                    }
                                ])
                            }
                        }
                    ]
                };
                
                if (this.shanghaiIndexChart) {
                    this.shanghaiIndexChart.setOption(option);
                }
            } catch (error) {
                console.error('加载上证分时数据失败:', error);
            }
        },
        
        // 处理分页变化
        handleSizeChange(val) {
            this.pageSize = val;
            this.currentPage = 1;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        }
    }
});

// 使用Element Plus
app.use(ElementPlus);

// 挂载Vue应用
app.mount('#app');
