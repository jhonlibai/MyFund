# 基金助手项目

一个基于FastAPI和Vue 3的基金管理工具，支持实时基金数据查询、总持仓信息计算、贵金属数据展示等功能。

## 项目结构

```
fund-master/
├── backend/            # 后端代码
│   ├── app/            # FastAPI应用
│   │   ├── api/        # API路由
│   │   ├── services/   # 业务逻辑
│   │   └── utils/      # 工具类
│   └── run.py          # 运行脚本
├── frontend/           # 前端代码
│   ├── src/            # 源代码
│   │   ├── services/   # 服务层
│   │   ├── utils/      # 工具类
│   │   └── constants/  # 常量定义
│   └── index.html      # 主页面
├── requirements.txt    # Python依赖
└── README.md           # 项目说明
```

## 运行环境

- Python 3.8+
- 现代浏览器（支持Vue 3）

## 安装依赖

1. **安装Python依赖**

```bash
# 进入项目根目录
cd fund-master

# 安装依赖
pip install -r requirements.txt
```

## 运行项目

### 1. 启动后端服务

```bash
# 进入backend目录
cd backend

# 运行FastAPI服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将运行在 `http://localhost:8000`

### 2. 启动前端服务

```bash
# 进入frontend目录
cd frontend

# 使用Python内置HTTP服务器
python -m http.server 3000
```

前端服务将运行在 `http://localhost:3000`

### 3. 访问项目

在浏览器中打开 `http://localhost:3000` 即可访问基金助手应用。

## 主要功能

1. **基金管理**
   - 添加基金
   - 设置持有金额
   - 删除基金
   - 查看基金详情

2. **数据展示**
   - 总持仓信息
   - 基金列表
   - 实时估值
   - 历史净值

3. **市场数据**
   - 实时贵金属数据
   - 全球指数
   - 行业板块
   - 7*24快讯

4. **图表分析**
   - 基金净值走势
   - 涨跌幅分析
   - 贵金属价格趋势

## API文档

后端服务启动后，可以访问以下地址查看API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 注意事项

1. **数据更新频率**
   - 基金估值数据每10秒自动更新
   - 市场数据每30秒自动更新

2. **交易时间**
   - 交易时段（9:00-15:00）：显示实时估值
   - 非交易时段：显示盘后数据

3. **外部API依赖**
   - 基金数据：天天基金网API
   - 贵金属数据：外部市场API
   - 市场快讯：百度财经API

4. **缓存机制**
   - 基金数据会缓存到本地文件
   - 收盘后自动保存盘后数据

## 故障排除

1. **后端服务启动失败**
   - 检查端口8000是否被占用
   - 确保所有依赖已安装

2. **前端页面无数据**
   - 检查后端服务是否正常运行
   - 检查浏览器控制台是否有错误信息

3. **API调用失败**
   - 检查网络连接
   - 检查外部API是否可访问

## 技术栈

- **后端**：FastAPI, Python 3.11+
- **前端**：Vue 3, ECharts
- **数据存储**：本地文件缓存
- **API**：RESTful API
- **CORS**：支持跨域请求

## 许可证

MIT License
