# 八字分析系统部署问答文档

## 部署过程中的常见问题和解决方案

### 1. 前端API请求问题

**Q: 为什么前端请求返回CORS错误？**
A: 这是由于CORS配置不正确导致。我们通过以下步骤解决：
1. 在 app.py 中添加了完整的CORS配置：
```python
CORS(app, 
     resources={r"/*": {
         "origins": [
             "http://127.0.0.1:5000",  # 本地开发
             "http://127.0.0.1:5500",  # Live Server
             "http://178.16.140.245",  # VPS IP
             "http://178.16.140.245:5000"  # Flask/Gunicorn 端口
         ],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"],
         "supports_credentials": True
     }})
```

2. 在前端请求中添加正确的配置：
```javascript
fetch("http://178.16.140.245:5000/analyze", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    mode: "cors",
    credentials: "include",
    body: JSON.stringify(formData)
})
```

### 2. API端口统一问题

**Q: 前端API请求使用的端口不一致怎么办？**
A: 发现script.js和result.js中使用的端口不一致：
- script.js使用: `http://178.16.140.245/`
- result.js使用: `http://178.16.140.245:5000/analyze`

解决方案：统一使用5000端口，因为：
1. Flask应用运行在5000端口
2. Gunicorn配置使用5000端口
3. 保持前后端端口一致，便于维护

### 3. 数据显示问题

**Q: 为什么某些数据不能正确显示在页面上？**
A: 这是由于前端数据处理逻辑和后端返回的数据结构不匹配导致。修改包括：
1. 统一后端返回的数据结构
2. 在前端添加数据存在性检查
3. 为所有可能的空值添加默认显示
4. 修复数据访问路径

### 4. 服务器部署问题

**Q: 如何在VPS上正确部署和更新代码？**
A: 部署流程如下：
1. 本地代码更新：
```bash
git add .
git commit -m "更新说明"
git push origin main
```

2. 连接VPS：
```bash
ssh root@178.16.140.245
```

3. 服务器更新：
```bash
cd /var/www/zuizhongban
git pull
sudo systemctl restart zuizhongban
```

### 5. wsgi.py配置问题

**Q: wsgi.py的配置是否需要修改？**
A: 是的，需要修改以支持外部访问：
```python
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

### 6. 服务持久化问题

**Q: 关闭本地开发环境后，网站还能访问吗？**
A: 可以，因为：
1. 网站运行在VPS服务器上，不依赖本地环境
2. Gunicorn通过systemd配置为系统服务，会持续运行
3. 只有需要更新代码时才需要连接VPS

## 重要提醒

### 本地开发
1. 修改代码前先在本地测试
2. 确保所有API请求使用正确的端口
3. 添加适当的错误处理和日志记录

### 服务器部署
1. 总是使用git管理代码更新
2. 更新后要重启Gunicorn服务
3. 定期检查服务状态和日志

### 调试技巧
1. 使用浏览器开发者工具检查网络请求
2. 查看服务器日志：`sudo journalctl -u zuizhongban`
3. 检查Gunicorn状态：`sudo systemctl status zuizhongban`

## 常用命令参考

### 本地开发
```bash
# 启动开发服务器
python app.py

# 代码提交
git add .
git commit -m "更新说明"
git push origin main
```

### 服务器操作
```bash
# 连接VPS
ssh root@178.16.140.245

# 更新代码
cd /var/www/zuizhongban
git pull

# 服务管理
sudo systemctl restart zuizhongban  # 重启服务
sudo systemctl status zuizhongban   # 查看状态
sudo journalctl -u zuizhongban      # 查看日志
```
