// result.js

// 每日名言列表
const quotes = [
  { text: "生活中不是缺少美，而是缺少发现美的眼睛。", author: "罗丹" },
  {
    text: "人生就像一场马拉松，重要的不是瞬间的速度，而是坚持的耐力。",
    author: "佚名",
  },
  {
    text: "成功不是将来才有的，而是从决定去做的那一刻起，持续累积而成。",
    author: "佚名",
  },
  {
    text: "当你的才华还撑不起你的野心时，你就应该静下心来学习。",
    author: "佚名",
  },
  {
    text: "没有人可以回到过去重新开始，但谁都可以从现在开始，书写一个全然不同的结局。",
    author: "佚名",
  },
  { text: "种一棵树最好的时间是十年前，其次是现在。", author: "佚名" },
  { text: "不要等待机会，而要创造机会。", author: "佚名" },
  { text: "做你害怕做的事情，然后你会发现，不过如此。", author: "佚名" },
  { text: "最困难的时候，也是离成功最近的时候。", author: "佚名" },
  { text: "每一个不曾起舞的日子，都是对生命的辜负。", author: "尼采" },
  { text: "生命不在于活得长短，而在于活得有多精彩。", author: "杨绛" },
  { text: "时光不负有心人，未来终会眷顾坚持的你。", author: "佚名" },
  { text: "把每一个平凡的日子，都过成诗意的模样。", author: "佚名" },
  { text: "愿你成为自己喜欢的样子，遇见想遇见的人。", author: "佚名" },
  { text: "心之所向，素履以往，生如逆旅，一苇以航。", author: "木心" },
];

// 获取随机名言
function getRandomQuote() {
  const randomIndex = Math.floor(Math.random() * quotes.length);
  return quotes[randomIndex];
}

// 更新每日名言
function updateDailyQuote() {
  const quote = getRandomQuote();
  document.getElementById("quoteText").textContent = quote.text;
  document.getElementById("quoteAuthor").textContent = `— ${quote.author}`;
}

// 处理分析结果数据
function handleAnalysisData(data) {
  // 基本信息
  document.getElementById("basicInfo").innerHTML = `
        <p>八字: ${data.八字}</p>
        <p>日主: ${data.日主}</p>
    `;

  // 五行分析
  const wuxingElements = {
    木: ["wood", "#4CAF50"],
    火: ["fire", "#F44336"],
    土: ["earth", "#FFC107"],
    金: ["metal", "#9E9E9E"],
    水: ["water", "#2196F3"],
  };

  const wuxingHtml = Object.entries(data.五行强弱)
    .map(
      ([element, value]) => `
            <div class="wuxing-circle ${wuxingElements[element][0]}" 
                 data-value="${value.toFixed(1)}">
                ${element}
            </div>
        `
    )
    .join("");
  document.getElementById("wuxingAnalysis").innerHTML = wuxingHtml;

  // 五行喜忌
  document.getElementById("wuxingLikes").innerHTML = `
        <p>喜用神: ${data.五行喜忌.喜用神}</p>
        <p>忌神: ${data.五行喜忌.忌神}</p>
    `;

  // 今日干支
  if (data.今日天干) {
    document.getElementById("todayGanzhi").innerHTML = `
            <p>天干：${data.今日天干[0] || "未知"}</p>
            <p>地支：${data.今日天干[1] || "未知"}</p>
        `;
  }

  // 幸运数字
  const luckyNumbersHtml = data.幸运数字
    .map((num) => `<span class="number">${num}</span>`)
    .join("");
  document.getElementById("luckyNumbers").innerHTML = luckyNumbersHtml;

  // 今日幸运色
  document.getElementById("luckyColor").innerHTML = `
        <div class="lucky-color-display" style="background-color: ${data.幸运颜色.color}"></div>
        <p class="color-strategy">${data.幸运颜色.strategy}</p>
    `;

  // 幸运色
  const luckyColorDiv = document.getElementById("luckyColor");
  if (data.幸运色 && data.visualization) {
    luckyColorDiv.innerHTML = `
            <div class="color-display">
                <div class="color-swatch" style="background-color: ${
                  data.visualization.preview
                }"></div>
                <div class="color-info">
                    <p>今日幸运色: ${data.visualization.hex}</p>
                    <p>RGB值: ${data.visualization.rgb}</p>
                    <p>${data.visualization.description}</p>
                    <p class="strategy">${data.调解策略 || ""}</p>
                </div>
            </div>
        `;
  }

  // 水晶推荐
  const crystalHtml = data.喜用神_天干
    .map((crystal) => {
      const [name, description] = crystal.split(":");
      return `<div class="crystal-item">
                <strong>${name}</strong>${description ? `: ${description}` : ""}
            </div>`;
    })
    .join("");
  document.getElementById("crystalRecommendations").innerHTML = crystalHtml;

  // 五行缺失分析
  let deficiencyHtml = "";
  if (data.五行_水晶 && Array.isArray(data.五行_水晶.缺失五行)) {
    if (data.五行_水晶.缺失五行.length > 0) {
      // 显示缺失五行的详细信息
      const weakElementsHtml = data.五行_水晶.缺失五行.map(element => `
        <div class="weak-element">
          <p>五行: ${element.五行}</p>
          <p>比例: ${element.比例}</p>
          <p>分析: ${element.分析}</p>
        </div>
      `).join("");

      deficiencyHtml = `
        <div class="wuxing-deficiency">
          ${weakElementsHtml}
        </div>
        <div class="crystal-recommendations">
          ${Object.entries(data.五行_水晶.推荐补充水晶)
            .map(([element, crystals]) => `
              <div class="element-crystals">
                <h4>${element}相关水晶:</h4>
                ${Array.isArray(crystals) ? crystals
                  .map((crystal) => {
                    const [name, desc] = crystal.split(":");
                    return `<div class="crystal-item">
                      <strong>${name}</strong>${desc ? `: ${desc}` : ""}
                    </div>`;
                  })
                  .join("") : ''}
              </div>
            `)
            .join("")}
        </div>
      `;
    } else {
      deficiencyHtml = "<p>五行均衡，无明显缺失。</p>";
    }
  } else {
    deficiencyHtml = "<p>暂无五行分析数据。</p>";
  }
  document.getElementById("wuxingDeficiency").innerHTML = deficiencyHtml;

  // 每日推荐活动
  if (data.推荐活动 && !data.推荐活动.error) {
    document.getElementById("dailyActivities").innerHTML = `
            <div class="activities-section">
                <h4>基于${data.推荐活动.喜用神}五行的推荐活动：</h4>
                <ul class="activity-list">
                    ${data.推荐活动.推荐活动
                      .map(
                        (activity) =>
                          `<li class="activity-item">${activity}</li>`
                      )
                      .join("")}
                </ul>
                ${
                  data.推荐活动.五行缺失活动.length > 0
                    ? `
                    <h4>五行平衡补充活动：</h4>
                    <ul class="activity-list">
                        ${data.推荐活动.五行缺失活动
                          .map(
                            (activity) =>
                              `<li class="activity-item">${activity}</li>`
                          )
                          .join("")}
                    </ul>
                `
                    : ""
                }
            </div>
        `;
  }
}

// 页面加载完成后执行
document.addEventListener("DOMContentLoaded", function () {
  // 获取并显示分析结果
  const formData = JSON.parse(localStorage.getItem("baziFormData"));
  
  if (!formData) {
    console.error("未找到表单数据");
    return;
  }

  // 验证必要的字段
  const requiredFields = ['name', 'sex', 'type', 'year', 'month', 'day', 'hours', 'minute'];
  const missingFields = requiredFields.filter(field => !formData[field]);
  
  if (missingFields.length > 0) {
    console.error("缺少必要的字段:", missingFields);
    return;
  }

  // 显示加载状态
  document.querySelectorAll(".result-card div").forEach((div) => {
    div.textContent = "加载中...";
  });

  // 请求后台进行八字分析
  fetch("http://178.16.140.245:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: formData.name,
      sex: parseInt(formData.sex),
      birth_type: parseInt(formData.type),
      year: parseInt(formData.year),
      month: parseInt(formData.month),
      day: parseInt(formData.day),
      hours: parseInt(formData.hours),
      minute: parseInt(formData.minute)
    })
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.querySelectorAll(".result-card div").forEach((div) => {
          div.innerHTML = `<div class="error">错误: ${data.error}</div>`;
        });
      } else {
        handleAnalysisData(data);
      }
    })
    .catch((error) => {
      console.error("错误:", error);
      document.querySelectorAll(".result-card div").forEach((div) => {
        div.innerHTML = `<div class="error">请求失败: ${error.message}</div>`;
      });
    });
});
