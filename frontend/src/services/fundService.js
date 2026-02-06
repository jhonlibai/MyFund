// 导入配置
import { API_CONFIG } from '../constants/config.js';

// 后端API地址
const API_BASE_URL = `${API_CONFIG.BASE_URL}/funds`;

/**
 * 加载基金列表
 * @returns {Promise<Array>} 基金列表
 */
export async function loadFundsList() {
    try {
        const response = await fetch(`${API_BASE_URL}/list`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载基金列表失败:', error);
        // 返回模拟数据作为 fallback
        return [];
    }
}

/**
 * 加载盘后更新的基金列表
 * @returns {Promise<Array>} 盘后更新的基金列表
 */
export async function loadLastFundsList() {
    try {
        const response = await fetch(`${API_BASE_URL}/list/last`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载盘后更新的基金列表失败:', error);
        // 返回空数组作为 fallback
        return [];
    }
}

/**
 * 加载总持仓信息
 * @returns {Promise<Object>} 总持仓信息
 */
export async function loadTotalInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/total-info`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载总持仓信息失败:', error);
        // 返回模拟数据作为 fallback
        return {
            total_hold_amount: 0,
            total_profit_loss: 0,
            total_valuation: 0,
            total_profit_loss_rate: 0
        };
    }
}

/**
 * 添加基金
 * @param {string} fundCode 基金代码
 * @returns {Promise<Object>} 添加结果
 */
export async function addFund(fundCode) {
    try {
        const response = await fetch(`${API_BASE_URL}/add?fund_code=${fundCode}`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('添加基金失败:', error);
        throw error;
    }
}

/**
 * 删除基金
 * @param {string} fundCode 基金代码
 * @returns {Promise<Object>} 删除结果
 */
export async function deleteFund(fundCode) {
    try {
        const response = await fetch(`${API_BASE_URL}/delete?fund_code=${fundCode}`, {
            method: 'POST'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('删除基金失败:', error);
        throw error;
    }
}

/**
 * 设置持有金额
 * @param {string} fundCode 基金代码
 * @param {number} holdAmount 持有金额
 * @returns {Promise<Object>} 设置结果
 */
export async function setHoldAmount(fundCode, holdAmount) {
    try {
        const response = await fetch(`${API_BASE_URL}/set-hold-amount`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fund_code: fundCode, amount: holdAmount })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('设置持有金额失败:', error);
        throw error;
    }
}

/**
 * 查看基金详情
 * @param {string} fundCode 基金代码
 * @returns {Promise<Object>} 基金详情
 */
export async function viewFundDetail(fundCode) {
    try {
        const response = await fetch(`${API_BASE_URL}/${fundCode}/history`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('查看基金详情失败:', error);
        // 返回模拟数据作为 fallback
        return {
            fund_info: {
                fund_code: fundCode,
                fund_name: '基金名称',
                now_time: new Date().toLocaleString(),
                forecast_growth: '0.00%',
                day_of_growth: '0.00%',
                current_net_value: '1.0000'
            },
            history_data: []
        };
    }
}
