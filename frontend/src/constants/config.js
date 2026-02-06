// API 配置
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000/api',
  TIMEOUT: 10000
};

// 图表配置
export const CHART_CONFIG = {
  COLORS: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'],
  FONT_SIZE: {
    TITLE: 16,
    SUBTITLE: 14,
    AXIS: 12,
    LEGEND: 12
  }
};

// 基金相关配置
export const FUND_CONFIG = {
  DEFAULT_HOLD_AMOUNT: 0,
  REFRESH_INTERVAL: 60000, // 60秒
  MAX_FUNDS_PER_PAGE: 20
};

// 市场相关配置
export const MARKET_CONFIG = {
  INDICES: ['sh000001', 'sh000300', 'sz399001', 'sz399006'],
  GOLD_API: 'https://api.coingecko.com/api/v3/simple/price',
  NEWS_API: 'https://api.example.com/news'
};

// 时间格式
export const DATE_FORMAT = {
  YYYY_MM_DD: 'YYYY-MM-DD',
  YYYY_MM_DD_HH_MM: 'YYYY-MM-DD HH:mm',
  YYYY_MM_DD_HH_MM_SS: 'YYYY-MM-DD HH:mm:ss'
};

// 消息提示配置
export const MESSAGE_CONFIG = {
  SUCCESS_DURATION: 2000,
  ERROR_DURATION: 3000,
  WARNING_DURATION: 2500,
  INFO_DURATION: 2000
};

// 正则表达式
export const REGEX = {
  FUND_CODE: /^\d{6}$/,
  AMOUNT: /^\d+(\.\d{1,2})?$/
};

// 路由配置
export const ROUTES = {
  HOME: '/',
  FUND_LIST: '/funds',
  FUND_DETAIL: '/fund/detail',
  MARKET: '/market',
  ANALYSIS: '/analysis'
};
