# -*- coding: UTF-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import funds, market, holdings
from app.utils.cache import CacheService

# 创建FastAPI应用
app = FastAPI(
    title="基金助手API",
    description="基于FastAPI的基金数据查询和分析API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(funds.router, prefix="/api/funds", tags=["funds"])
app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(holdings.router, prefix="/api/holdings", tags=["holdings"])

# 初始化缓存服务
cache_service = CacheService()

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 加载缓存数据
    cache_service.load_cache()
    print("缓存数据加载完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    # 保存缓存数据
    cache_service.save_cache()
    print("缓存数据保存完成")

@app.get("/")
async def root():
    """根路径"""
    return {"message": "基金助手API服务运行中"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
