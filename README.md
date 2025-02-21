八字分析系统
这是一个基于八字理论的个人命理分析系统，结合现代科技和传统命理学，为用户提供个性化的分析和建议。

功能特点
🎯 八字分析：根据用户的出生年月日时进行八字分析
🌈 五行分析：计算五行能量平衡，提供个性化建议
💎 水晶推荐：基于八字分析结果推荐合适的水晶
🎨 每日幸运色：根据八字和当日干支生成个性化幸运色
🔢 幸运数字：基于五行属性计算个人幸运数字
📅 日常活动建议：根据五行特点推荐适合的日常活动
💫 每日励志语录：提供积极向上的每日励志语录
技术栈
后端
Python 3.x
Flask：Web框架
Flask-CORS：处理跨域请求
Requests：处理HTTP请求
前端
HTML5
CSS3
JavaScript（原生）
系统架构
zhubao/
├── app.py              # Flask后端应用
├── index.html          # 首页（数据输入）
├── result.html         # 结果页面
├── script.js           # 首页JavaScript逻辑
├── result.js           # 结果页JavaScript逻辑
└── styles.css          # 样式表
核心功能模块
八字计算模块

支持农历/公历转换
天干地支计算
五行能量平衡分析
五行分析模块

计算五行强弱
确定喜用神与忌神
生成五行调衡建议
个性化推荐模块

水晶推荐系统
幸运色生成器
幸运数字计算
日常活动建议
用户界面模块

响应式设计
用户友好的表单输入
直观的结果展示
每日励志语录展示
安装和运行
环境要求

Python 3.x
Flask
Flask-CORS
Requests
安装依赖

pip install flask flask-cors requests
运行应用

python app.py
应用将在 http://127.0.0.1:5000 启动

使用说明
打开首页，点击"填写个人信息"按钮
在弹出的表单中填写：
姓名
性别
出生类型（农历/公历）
出生年月日时分
点击"开始分析"按钮
系统将展示详细的分析结果，包括：
八字信息
五行分析
个性化建议
今日幸运色
幸运数字
水晶推荐
日常活动建议
数据安全
所有数据仅用于计算，不会被存储
分析结果仅供参考
用户信息严格保密
注意事项
建议使用现代浏览器（Chrome、Firefox、Safari等）访问
确保输入的出生信息准确
分析结果仅供参考，不作为决策依据
贡献指南
欢迎提交问题和建议！如果您想为项目做出贡献，请：

Fork 本仓库
创建您的特性分支 (git checkout -b feature/AmazingFeature)
提交您的更改 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
打开一个 Pull Request
许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件