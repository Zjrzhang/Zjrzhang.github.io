# 科研成果管理系统 - 后端API

## 项目简介

这是科研成果管理系统的后端服务，基于 FastAPI 框架开发。

## 技术栈

- **框架**: FastAPI 0.115.0
- **数据库**: MySQL
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)

## 项目结构

```
fastapi/
├── main.py              # 应用入口
├── init_db.py           # 数据库初始化脚本
├── requirements.txt     # 依赖管理
├── config/              # 配置文件
│   ├── database.py      # 数据库配置
│   └── settings.py      # 应用配置
├── models/              # 数据库模型
│   ├── user.py
│   ├── paper.py
│   ├── patent.py
│   ├── project.py
│   ├── personnel.py
│   └── relations.py
├── schemas/             # Pydantic模式
│   ├── user.py
│   ├── paper.py
│   ├── patent.py
│   ├── project.py
│   └── personnel.py
├── api/                 # API路由
│   ├── auth.py
│   └── __init__.py
├── services/            # 业务逻辑层
│   ├── auth_service.py
│   └── __init__.py
└── utils/               # 工具函数
    ├── security.py      # 密码加密、JWT
    └── database.py      # 数据库工具
```

## 环境要求

- Python 3.8+
- MySQL 5.7+ 或 8.0+

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并修改配置：

```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/research_management?charset=utf8mb4

# JWT配置
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
DEBUG=True
PROJECT_NAME=科研成果管理系统
```

### 3. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE research_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库表

运行初始化脚本：

```bash
python init_db.py
```

这将创建所有数据表，并创建一个默认管理员账户：
- 用户名: `admin`
- 密码: `admin123`

### 5. 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 `http://localhost:8000` 启动。

## API文档

启动服务后，可以访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 认证相关

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息（需要认证）

### 其他端点

将在后续阶段实现。

## 开发说明

### 数据库模型

所有数据库模型定义在 `models/` 目录下，使用 SQLAlchemy ORM。

### API路由

API路由定义在 `api/` 目录下，使用 FastAPI 的路由系统。

### 业务逻辑

业务逻辑封装在 `services/` 目录下，实现与数据库的交互。

### 数据验证

使用 Pydantic 进行数据验证，模式定义在 `schemas/` 目录下。

## 注意事项

1. 生产环境请修改 `SECRET_KEY`
2. 生产环境请设置 `DEBUG=False`
3. 定期备份数据库
4. 使用HTTPS保护API通信

