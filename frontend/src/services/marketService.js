// 导入配置
import { API_CONFIG } from '../constants/config.js';

// 后端API地址
const API_BASE_URL = `${API_CONFIG.BASE_URL}/market`;

/**
 * 加载全球指数数据
 * @returns {Promise<Array>} 全球指数数据
 */
export async function loadIndicesData() {
    try {
        const response = await fetch(`${API_BASE_URL}/indices`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载全球指数数据失败:', error);
        // 返回模拟数据作为 fallback
        return [
            { name: '上证指数', value: '4025.35', change: '+0.24%' },
            { name: '深证指数', value: '13938.09', change: '+0.62%' },
            { name: '创业板指', value: '3285.58', change: '+0.66%' },
            { name: '恒生指数', value: '26422.42', change: '-0.12%' },
            { name: '富时中国A50', value: '14640.49', change: '-0.08%' },
            { name: '日经指数', value: '54201.01', change: '+2.94%' },
            { name: '韩国首尔综合指数', value: '5195.56', change: '+4.97%' },
            { name: '纳斯达克', value: '25992.11', change: '+0.05%' },
            { name: '道琼斯', value: '49407.66', change: '+1.05%' },
            { name: '标普500', value: '6976.44', change: '+0.54%' }
        ];
    }
}

/**
 * 加载贵金属数据
 * @returns {Promise<Object>} 贵金属数据
 */
export async function loadGoldData() {
    try {
        const response = await fetch(`${API_BASE_URL}/gold`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载贵金属数据失败:', error);
        // 返回模拟数据作为 fallback
        return {
            current: '2023.50',
            change: '-6.53%',
            history: [
                { date: '2026-02-02', price: '2164.80' },
                { date: '2026-02-01', price: '2180.50' }
            ]
        };
    }
}

/**
 * 加载实时贵金属数据
 * @returns {Promise<Array>} 实时贵金属数据
 */
export async function loadRealTimeGoldData() {
    try {
        const response = await fetch(`${API_BASE_URL}/real-time-gold`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            cache: 'no-cache'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const text = await response.text();
        const data = JSON.parse(text);
        
        // 检查数据结构，如果是数组的数组，转换为对象数组
        if (Array.isArray(data) && data.length > 0 && Array.isArray(data[0])) {
            console.log('检测到数组的数组结构，开始转换');
            const convertedData = [];
            for (const item of data) {
                if (Array.isArray(item) && item.length >= 10) {
                    convertedData.push({
                        name: item[0] || "未知金属",
                        price: item[1] || "0",
                        change: item[2] || "0",
                        change_rate: item[3] || "0%",
                        open: item[4] || "0",
                        high: item[5] || "0",
                        low: item[6] || "0",
                        prev_close: item[7] || "0",
                        update_time: item[8] || new Date().toLocaleString(),
                        unit: item[9] || "元/克"
                    });
                }
            }
            console.log('转换后的数据:', convertedData);
            return convertedData;
        }
        
        return data;
    } catch (error) {
        console.error('加载实时贵金属数据失败:', error);
        // 返回模拟数据作为 fallback
        return [
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
    }
}

/**
 * 加载历史金价数据
 * @returns {Promise<Array>} 历史金价数据
 */
export async function loadGoldHistoryData() {
    try {
        // 这里可以调用后端API获取历史金价数据
        // 暂时返回模拟数据
        return [
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
        ];
    } catch (error) {
        console.error('加载历史金价数据失败:', error);
        // 返回模拟数据作为 fallback
        return [];
    }
}

/**
 * 加载行业板块数据
 * @returns {Promise<Array>} 行业板块数据
 */
export async function loadSectorsData() {
    try {
        const response = await fetch(`${API_BASE_URL}/sectors`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.sectors;
    } catch (error) {
        console.error('加载行业板块数据失败:', error);
        // 返回模拟数据作为 fallback
        return [
            { name: '船舶制造', change: '5.23%' },
            { name: '光伏设备', change: '4.9%' },
            { name: '航天航空', change: '3.26%' },
            { name: '通信设备', change: '2.80%' },
            { name: '小金属', change: '2.80%' },
            { name: '玻璃玻纤', change: '2.40%' },
            { name: '非金属材料', change: '2.40%' },
            { name: '光学光电子', change: '2.12%' },
            { name: '专用设备', change: '2.09%' },
            { name: '化学制品', change: '1.99%' }
        ];
    }
}

/**
 * 加载成交量趋势数据
 * @returns {Promise<Object>} 成交量趋势数据
 */
export async function loadVolumeTrendData() {
    try {
        // 这里可以调用后端API获取成交量趋势数据
        // 暂时返回模拟数据
        return {
            dates: ['02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07'],
            volumes: [3200, 2800, 3500, 2900, 3100, 3400, 3600]
        };
    } catch (error) {
        console.error('加载成交量趋势数据失败:', error);
        // 返回模拟数据作为 fallback
        return {
            dates: [],
            volumes: []
        };
    }
}

/**
 * 加载上证分时数据
 * @returns {Promise<Object>} 上证分时数据
 */
export async function loadShanghaiIndexData() {
    try {
        // 这里可以调用后端API获取上证分时数据
        // 暂时返回模拟数据
        return {
            times: ['09:30', '10:00', '10:30', '11:00', '11:30', '13:30', '14:00', '14:30', '15:00'],
            prices: [4000, 4005, 4010, 4008, 4012, 4015, 4020, 4018, 4012]
        };
    } catch (error) {
        console.error('加载上证分时数据失败:', error);
        // 返回模拟数据作为 fallback
        return {
            times: [],
            prices: []
        };
    }
}

/**
 * 加载新闻列表
 * @returns {Promise<Array>} 新闻列表
 */
export async function loadNewsList() {
    try {
        const response = await fetch(`${API_BASE_URL}/news`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载新闻列表失败:', error);
        // 返回模拟数据作为 fallback
        const now = new Date();
        return [
            {
                "time": (new Date(now.getTime() - 30 * 60000)).toLocaleTimeString(),
                "content": "游戏股集体跳水，世纪华通跌超9%"
            },
            {
                "time": (new Date(now.getTime() - 25 * 60000)).toLocaleTimeString(),
                "content": "寒武纪、沐曦等国产AI芯片股集体下跌"
            },
            {
                "time": (new Date(now.getTime() - 20 * 60000)).toLocaleTimeString(),
                "content": "奥瑞德、合肥AI与大数据研究院等新设创投合伙企业"
            },
            {
                "time": (new Date(now.getTime() - 15 * 60000)).toLocaleTimeString(),
                "content": "商业航天板块震荡上扬，巨力索具涨停创新高"
            },
            {
                "time": (new Date(now.getTime() - 10 * 60000)).toLocaleTimeString(),
                "content": "港股恒生指数涨幅扩大至1%"
            }
        ];
    }
}
