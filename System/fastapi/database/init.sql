-- 科研成果管理系统数据库初始化脚本
-- 数据库名称: research_management
-- 字符集: utf8mb4
-- 排序规则: utf8mb4_unicode_ci

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS research_management 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE research_management;

-- 注意：此脚本仅用于参考，实际表结构由SQLAlchemy ORM自动创建
-- 运行 init_db.py 脚本会自动创建所有表

-- 如果需要手动创建表，可以参考以下SQL（但建议使用ORM自动创建）

-- 用户表
-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,
--     role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
--     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--     INDEX idx_username (username),
--     INDEX idx_email (email)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 其他表结构由SQLAlchemy自动创建，包括：
-- - papers (论文表)
-- - patents (专利表)
-- - projects (项目表)
-- - personnel (人员表)
-- - paper_project_relations (论文-项目关联表)
-- - patent_project_relations (专利-项目关联表)
-- - author_paper_relations (作者-论文关联表)
-- - author_patent_relations (发明人-专利关联表)
-- - personnel_project_relations (人员-项目关联表)

