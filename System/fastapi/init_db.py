"""
数据库初始化脚本
运行此脚本创建数据库表结构
"""
from utils.database import init_db
from config.database import SessionLocal
from models.user import User
from utils.security import get_password_hash

if __name__ == "__main__":
    print("开始初始化数据库...")
    
    # 创建所有表
    init_db()
    
    # 创建默认管理员账户
    db = SessionLocal()
    try:
        # 检查是否已存在管理员
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                phone="13800000000",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("默认管理员账户创建成功！")
            print("用户名: admin")
            print("手机号: 13800000000")
            print("密码: admin123")
        else:
            print("管理员账户已存在")
    except Exception as e:
        print(f"创建管理员账户时出错: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("数据库初始化完成！")

