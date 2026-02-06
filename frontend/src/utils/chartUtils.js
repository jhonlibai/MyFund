/**
 * 初始化图表
 * @returns {Object} 图表实例对象
 */
export function initCharts() {
    try {
        // 检查echarts是否存在
        if (typeof echarts === 'undefined') {
            console.error('echarts库未加载');
            return {};
        }
        
        // 初始化全球指数图表
        let indicesChart = null;
        const indicesElement = document.getElementById('indicesChart');
        if (indicesElement) {
            indicesChart = echarts.init(indicesElement);
        }
        
        // 初始化实时贵金属图表
        let realTimeGoldChart = null;
        const realTimeGoldElement = document.getElementById('realTimeGoldChart');
        if (realTimeGoldElement) {
            realTimeGoldChart = echarts.init(realTimeGoldElement);
        }
        
        // 初始化成交量趋势图表
        let volumeTrendChart = null;
        const volumeTrendElement = document.getElementById('volumeTrendChart');
        if (volumeTrendElement) {
            volumeTrendChart = echarts.init(volumeTrendElement);
        }
        
        // 初始化上证分时图表
        let shanghaiIndexChart = null;
        const shanghaiIndexElement = document.getElementById('shanghaiIndexChart');
        if (shanghaiIndexElement) {
            shanghaiIndexChart = echarts.init(shanghaiIndexElement);
        }
        
        // 初始化历史金价图表
        let goldHistoryChart = null;
        const goldHistoryElement = document.getElementById('goldHistoryChart');
        if (goldHistoryElement) {
            goldHistoryChart = echarts.init(goldHistoryElement);
        }
        
        console.log('图表初始化成功');
        
        return {
            indicesChart,
            realTimeGoldChart,
            volumeTrendChart,
            shanghaiIndexChart,
            goldHistoryChart
        };
    } catch (error) {
        console.error('图表初始化失败:', error);
        return {};
    }
}

/**
 * 更新全球指数图表
 * @param {Object} chart 图表实例
 * @param {Array} data 数据数组
 */
export function updateIndicesChart(chart, data) {
    try {
        if (!chart || typeof echarts === 'undefined') {
            console.warn('图表未初始化');
            return;
        }
        
        const option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['上证指数', '深证指数', '创业板指', '恒生指数']
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
            series: [
                {
                    name: '上证指数',
                    type: 'line',
                    data: [4000, 4005, 4010, 4008, 4012, 4015, 4012],
                    lineStyle: {
                        color: '#F56C6C'
                    }
                },
                {
                    name: '深证指数',
                    type: 'line',
                    data: [13900, 13910, 13920, 13915, 13925, 13930, 13925],
                    lineStyle: {
                        color: '#409EFF'
                    }
                },
                {
                    name: '创业板指',
                    type: 'line',
                    data: [3270, 3275, 3280, 3278, 3282, 3285, 3280],
                    lineStyle: {
                        color: '#67C23A'
                    }
                },
                {
                    name: '恒生指数',
                    type: 'line',
                    data: [26400, 26405, 26410, 26408, 26412, 26415, 26410],
                    lineStyle: {
                        color: '#E6A23C'
                    }
                }
            ]
        };
        
        chart.setOption(option);
        console.log('全球指数图表更新成功');
    } catch (error) {
        console.error('更新全球指数图表失败:', error);
    }
}

/**
 * 更新实时贵金属图表
 * @param {Object} chart 图表实例
 * @param {Array} data 数据数组
 */
export function updateRealTimeGoldChart(chart, data) {
    try {
        if (!chart || typeof echarts === 'undefined') {
            console.warn('图表未初始化');
            return;
        }
        
        if (!data || data.length === 0) {
            console.warn('数据为空');
            return;
        }
        
        const option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: data.map(item => item.name)
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
            series: data.map((item, index) => {
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
                    name: item.name,
                    type: 'line',
                    data: priceData,
                    lineStyle: {
                        color: colors[index % colors.length]
                    }
                };
            })
        };
        
        chart.setOption(option);
        console.log('实时贵金属图表更新成功');
    } catch (error) {
        console.error('更新实时贵金属图表失败:', error);
    }
}

/**
 * 更新成交量趋势图表
 * @param {Object} chart 图表实例
 * @param {Object} data 数据对象
 */
export function updateVolumeTrendChart(chart, data) {
    try {
        if (!chart || typeof echarts === 'undefined') {
            console.warn('图表未初始化');
            return;
        }
        
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
                    data: data?.dates || ['02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07'],
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
                    data: data?.volumes || [3200, 2800, 3500, 2900, 3100, 3400, 3600],
                    itemStyle: {
                        color: '#409EFF'
                    }
                }
            ]
        };
        
        chart.setOption(option);
        console.log('成交量趋势图表更新成功');
    } catch (error) {
        console.error('更新成交量趋势图表失败:', error);
    }
}

/**
 * 更新上证分时图表
 * @param {Object} chart 图表实例
 * @param {Object} data 数据对象
 */
export function updateShanghaiIndexChart(chart, data) {
    try {
        if (!chart || typeof echarts === 'undefined') {
            console.warn('图表未初始化');
            return;
        }
        
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
                data: data?.times || ['09:30', '10:00', '10:30', '11:00', '11:30', '13:30', '14:00', '14:30', '15:00']
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
                    data: data?.prices || [4000, 4005, 4010, 4008, 4012, 4015, 4020, 4018, 4012],
                    lineStyle: {
                        color: '#F56C6C'
                    },
                    areaStyle: {
                        color: 'rgba(245, 108, 108, 0.3)'
                    }
                }
            ]
        };
        
        chart.setOption(option);
        console.log('上证分时图表更新成功');
    } catch (error) {
        console.error('更新上证分时图表失败:', error);
    }
}

/**
 * 更新历史金价图表
 * @param {Object} chart 图表实例
 * @param {Array} data 数据数组
 */
export function updateGoldHistoryChart(chart, data) {
    try {
        if (!chart || typeof echarts === 'undefined') {
            console.warn('图表未初始化');
            return;
        }
        
        if (!data || data.length === 0) {
            console.warn('数据为空');
            return;
        }
        
        // 按日期升序排序
        const sortedData = [...data].sort((a, b) => {
            return new Date(a.date) - new Date(b.date);
        });
        
        const dates = sortedData.map(item => item.date);
        const chinaGoldFundPrices = sortedData.map(item => parseFloat(item.chinaGoldFundPrice));
        const chowTaiFookPrices = sortedData.map(item => parseFloat(item.chowTaiFookPrice));
        
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
        
        chart.setOption(option);
        console.log('历史金价图表更新成功');
    } catch (error) {
        console.error('更新历史金价图表失败:', error);
    }
}

/**
 * 调整图表大小
 * @param {Array} charts 图表实例数组
 */
export function resizeCharts(charts) {
    try {
        if (!Array.isArray(charts)) {
            console.error('charts参数必须是数组');
            return;
        }
        
        charts.forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
        
        console.log('图表大小调整成功');
    } catch (error) {
        console.error('调整图表大小失败:', error);
    }
}
